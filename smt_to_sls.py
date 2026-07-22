import argparse
import cvc5
import sys
from cvc5 import Kind
from z3 import *
from lia_star_solver import *


interpolation_on = True
unfold = 0

def sls_solver(phi_assertions, star_predicate, star_variables):
    A_assertions = phi_assertions
    B_assertions = [star_predicate]
    set_vars = star_variables

    # Record statistics
    statistics.problem_size = len(A_assertions) + len(B_assertions)
    if instrument:
        print(statistics.problem_size, flush=True)

    # Functionalize the given assertions so they can be called with arbitrary args
    A = toMacro(A_assertions)
    B = toMacro(B_assertions)
    A.args = set_vars + [a for a in A.args if a not in set_vars]
    B.args = set_vars + [b for b in B.args if b not in set_vars]

    # A(0) may be immediately satisfiable
    sls = semilinear.SLS(B, set_vars, len(B.args))
    X = findSolution(A, sls)
    if X:
        returnSolution(list(zip(A.args, X)), sls)

    # SLS construction loop
    i = interpolant.Interpolant(A, B)
    incomplete = sls.augment()
    while incomplete:

        # If there's a solution using this SLS, return it
        X = findSolution(A, sls)
        if X:
            returnSolution(list(zip(A.args, X)), sls)

        # Compute any new interpolants for this iteration
        start = time.time()
        if interpolation_on:
            i.update(sls)
            i.addForwardInterpolant(unfold)
            i.addBackwardInterpolant(unfold)

            # Extract all inductive clauses
            i.filterToInductive()
            inductive_clauses = i.getInductive()
            printV("\nInductive clauses: {}\n".format(inductive_clauses))

            # Check satisfiability against inductive interpolant
            if checkUnsatWithInterpolant(inductive_clauses, A):
                end = time.time()
                statistics.interpolation_time += end - start
                returnSolution(unsat, sls)
        end = time.time()
        statistics.interpolation_time += end - start

        # At every iteration, shorten the SLS / its vectors
        sls.reduce()

        # Add another vector to the SLS
        incomplete = sls.augment()
        printV("SLS: {}".format(sls.getSLS()))

    # If the SLS is equivalent to B and a solution was not found, the problem is unsat
    returnSolution(unsat, sls)


# ---------------------------------------------------------------------------
# cvc5 -> z3 translation.
#
# A star atom  (int.star-contains (lambda (v1..vd) BODY) p1 .. pd)  means:
# the point (p1..pd) is a sum of finitely many vectors, each satisfying BODY.
# sls_solver decides  phi /\ set_vars in {v | B(v)}*  where set_vars act both
# as the membership point and as B's coordinate variables. So each star atom
# gets FRESH coordinates q_i; its lambda body is translated over q_i; and the
# atom is replaced in phi by the linking equalities  p_i = q_i  (sound for
# positive occurrences: if the atom holds pick q_i := p_i, and conversely
# q_i's membership transfers to p_i through the equalities).
#
# Several stars combine into a single star via the padded-union construction:
#   (q_1..q_n) in C*  with  C(v) = OR_i (B_i(v_i) /\ AND_{k!=i} v_k = 0)
# which is equivalent to  AND_i q_i in B_i*  (each summand lives in exactly
# one block, so the blocks' sums are independent).
#
# Summand vectors are nonnegative (tuple-multiplicity semantics), so C also
# conjoins v >= 0 for every coordinate.
#
# Out of scope, rejected with an error (exit code != 0) instead of being
# mistranslated: star atoms under negative polarity, under an ite condition
# or a Boolean (dis)equality, and stars nested inside another star's body.
# ---------------------------------------------------------------------------

class StarCollector:
    def __init__(self):
        self.atoms = []  # {'qs': [z3 Int], 'body': z3 expr}
        self.cache = {}  # str(star term) -> replacement z3 expr


def has_star(term, memo):
    if term in memo:
        return memo[term]
    result = term.getKind() == Kind.STAR_CONTAINS or any(
        has_star(child, memo) for child in term)
    memo[term] = result
    return result


def cvc5_to_z3(term, symbols, stars, memo, polarity=True):
    """
    Convert a cvc5 Term into a z3 term.
    symbols: dict mapping variable names to z3 constants
    stars: StarCollector receiving one entry per distinct star atom
    polarity: True iff the term occurs under an even number of negations
    """

    # const cases
    if term.isBooleanValue():
        return BoolVal(term.getBooleanValue())

    if term.isIntegerValue():
        return IntVal(term.getIntegerValue())

    k = term.getKind()
    cvc5_children = list(term)
    if k == Kind.CONSTANT or k == Kind.VARIABLE:
        return symbols[str(term)]

    if k == Kind.APPLY_UF:
        # uninterpreted function application: child 0 is the function symbol
        fn = symbols[str(cvc5_children[0])]
        args = [cvc5_to_z3(c, symbols, stars, memo, polarity)
                for c in cvc5_children[1:]]
        return fn(*args)

    if k == Kind.STAR_CONTAINS:
        if not polarity:
            raise Exception("unsupported: star atom under negative polarity")
        key = str(term)
        if key in stars.cache:
            return stars.cache[key]
        lambda_term = list(cvc5_children[0])
        binders = [str(v) for v in list(lambda_term[0])]
        body_term = lambda_term[1]
        points = cvc5_children[1:]
        if len(points) != len(binders):
            raise Exception("unsupported: star arity mismatch")
        if has_star(body_term, memo):
            raise Exception("unsupported: star nested inside a star body")
        index = len(stars.atoms)
        qs = [Int("slsq{}_{}".format(index, j)) for j in range(len(binders))]
        inner = dict(symbols)
        inner.update(dict(zip(binders, qs)))
        body = cvc5_to_z3(body_term, inner, stars, memo, True)
        stars.atoms.append({'qs': qs, 'body': body})
        points_z3 = [cvc5_to_z3(p, symbols, stars, memo, polarity)
                     for p in points]
        replacement = And([p == q for (p, q) in zip(points_z3, qs)])
        stars.cache[key] = replacement
        return replacement

    if k == Kind.NOT:
        return Not(cvc5_to_z3(cvc5_children[0], symbols, stars, memo,
                              not polarity))

    if k == Kind.IMPLIES:
        return Implies(
            cvc5_to_z3(cvc5_children[0], symbols, stars, memo, not polarity),
            cvc5_to_z3(cvc5_children[1], symbols, stars, memo, polarity))

    if k == Kind.ITE:
        if has_star(cvc5_children[0], memo):
            raise Exception("unsupported: star atom inside an ite condition")
        z3_children = [cvc5_to_z3(c, symbols, stars, memo, polarity)
                       for c in cvc5_children]
        return If(z3_children[0], z3_children[1], z3_children[2])

    if k in (Kind.EQUAL, Kind.DISTINCT):
        if any(has_star(c, memo) for c in cvc5_children):
            raise Exception("unsupported: star atom under (dis)equality")

    if term.getNumChildren() == 0:
        raise Exception("Unhandled cvc5 term: {} ({})".format(k, term))

    z3_children = [cvc5_to_z3(child, symbols, stars, memo, polarity)
                   for child in term]

    if k == Kind.EQUAL:
        return z3_children[0] == z3_children[1]

    if k == Kind.DISTINCT:
        return Distinct(*z3_children)

    if k == Kind.AND:
        return And(*z3_children)

    if k == Kind.OR:
        return Or(*z3_children)

    if k == Kind.ADD:
        return Sum(z3_children)

    if k == Kind.SUB:
        return z3_children[0] - z3_children[1]

    if k == Kind.MULT:
        return z3_children[0] * z3_children[1]

    if k == Kind.LT:
        return z3_children[0] < z3_children[1]

    if k == Kind.LEQ:
        return z3_children[0] <= z3_children[1]

    if k == Kind.GT:
        return z3_children[0] > z3_children[1]

    if k == Kind.GEQ:
        return z3_children[0] >= z3_children[1]

    raise Exception("Unsupported cvc5 operator: {} ({})".format(k, term))


if __name__ == "__main__":
    p = argparse.ArgumentParser(
        description='Solves an smt2 file with int.star-contains atoms by '
                    'translating it to a LIA* problem')
    p.add_argument('file', metavar='FILEPATH', type=str,
                   help='path to the smt2 benchmark file')
    p.add_argument('--no-interp', action='store_true',
                   help='turn off interpolation')
    p.add_argument('--unfold', metavar='N', type=int, default=0,
                   help='number of unfoldings to use when interpolating '
                        '(default: 0)')
    args = p.parse_args()
    filename = args.file
    interpolation_on = not args.no_interp
    unfold = args.unfold

    tm = cvc5.TermManager()
    slv = cvc5.Solver(tm)

    # set that we should print success after each successful command
    slv.setOption("dag-thresh", "0")

    # construct an input parser associated the solver above
    parser = cvc5.InputParser(slv)

    parser.setFileInput(
        cvc5.InputLanguage.SMT_LIB_2_6,
        filename,
    )

    # get the symbol manager of the parser, used when invoking commands below
    sm = parser.getSymbolManager()

    # parse commands until finished
    while True:
        cmd = parser.nextCommand()
        if cmd.isNull():
            break
        # invoke the command on the solver and the symbol manager
        if cmd.getCommandName() != "check-sat":
            cmd.invoke(slv, sm)

    print("Finished parsing commands")
    # declare z3 constants; declare-fun symbols with arity > 0 become z3
    # uninterpreted Int functions (they may only occur outside star bodies)
    symbols = {}
    for term in sm.getDeclaredTerms():
        sort = term.getSort()
        if sort.isFunction():
            arity = sort.getFunctionArity()
            symbols[str(term)] = Function(
                str(term), *([IntSort()] * arity + [IntSort()]))
        else:
            symbols[str(term)] = Int(str(term))

    # translate all assertions, collecting star atoms along the way
    stars = StarCollector()
    memo = {}
    phi_assertions = [cvc5_to_z3(assertion, symbols, stars, memo)
                      for assertion in slv.getAssertions()]

    # star-free formulas need no SLS machinery
    if not stars.atoms:
        solver = Solver()
        solver.add(phi_assertions)
        print(solver.check())
        sys.exit(0)

    # padded-union of all star atoms + nonnegative summand coordinates
    all_q = [q for atom in stars.atoms for q in atom['qs']]
    if len(stars.atoms) == 1:
        combined = stars.atoms[0]['body']
    else:
        disjuncts = []
        for i, atom in enumerate(stars.atoms):
            zeros = [q == 0 for j, other in enumerate(stars.atoms) if j != i
                     for q in other['qs']]
            disjuncts.append(And([atom['body']] + zeros))
        combined = Or(disjuncts)
    combined = And([combined] + [q >= 0 for q in all_q])

    result = sls_solver(phi_assertions, combined, all_q)
