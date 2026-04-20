import cvc5
from cvc5 import Kind
from z3 import *
from lia_star_solver import *
import pdb



x1 = Int("x1")
x2 = Int("x2")

z1 = x1 == x2
z2 = x1 == x2

z3 = And(z1, z2)

def sls_solver(phi_assertions, star_predicate, star_variables):
    pdb.set_trace()
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


def cvc5_to_z3(term, symbols):
    """
    Convert a cvc5 Term into a z3 term.
    symbols: dict mapping cvc5 terms to z3 constants
    """
    print(f"translating term: {term}")

    # const cases
    if term.isBooleanValue():
        return BoolVal(term.getBooleanValue())

    if term.isIntegerValue():
        value = term.getIntegerValue()
        print(value)
        return IntVal(value)


    k = term.getKind()
    cvc5_children = list(term)
    # print(f"Translating kind: {k}")
    if k == Kind.CONSTANT or k == Kind.VARIABLE:
        return symbols[str(term)]

    # Recursive cases
    if k == Kind.STAR_CONTAINS:
        print(str(Kind.STAR_CONTAINS))
        
        lambda_term = list(cvc5_children[0])
        body = cvc5_to_z3(lambda_term[1], symbols)
        print(f"body: {lambda_term[1]}")
        outer_vector_smt = cvc5_children[1:]        
        print(f"outer_vector_smt: {outer_vector_smt}")
        outer_vector = [cvc5_to_z3(child, symbols) for child in outer_vector_smt]
        print(f"outer_vector: {outer_vector}")
        pdb.set_trace()
        return body

    if term.getNumChildren() == 0:        
        raise Exception(f"Unhandled cvc5 term: {k} ({term})")

    print(f"cvc5_children: {cvc5_children}")
    z3_children = [cvc5_to_z3(child, symbols) for child in term]
    print(f"after recursion term: {term}")
    print(f"after recursion children: {len(z3_children)}")
    # print(f"after recursion child[0]: {str(children[0])}")
    # print(f"after recursion children: {children}")    
    print(f"k: {k}")

    if k == Kind.EQUAL:        
        print(z3_children[0].sort())
        print(z3_children[1].sort())
        equality = z3_children[0] == z3_children[1]        
        return equality

    if k == Kind.NOT:        
        print(z3_children[0].sort())
        return Not(z3_children[0])

    if k == Kind.AND:        
        print("before Kind.AND")
        print(len(z3_children))
        print(z3_children[0].sort())
        print(z3_children[1].sort())
        ret = And(*z3_children)
        print("after Kind.AND")
        return ret

    if k == Kind.OR:
        return Or(*z3_children)

    if k == Kind.IMPLIES:
        return Implies(z3_children[0], z3_children[1])

    if k == Kind.ITE:        
        return If(z3_children[0], z3_children[1], z3_children[2])

    if k == Kind.ADD:
        return z3_children[0] + z3_children[1]

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

    raise Exception(f"Unsupported cvc5 operator: {k} ({term})")


if __name__ == "__main__":
    tm = cvc5.TermManager()
    slv = cvc5.Solver(tm)

    # set that we should print success after each successful command
    slv.setOption("dag-thresh", "0")

    # construct an input parser associated the solver above
    parser = cvc5.InputParser(slv)

    parser.setFileInput(
        cvc5.InputLanguage.SMT_LIB_2_6,
        "/home/mudathir/all/SQLSolver/cvc5/calcite/query013-call-0.smt2",
    )

    # get the symbol manager of the parser, used when invoking commands below
    sm = parser.getSymbolManager()

    # parse commands until finished
    while True:
        cmd = parser.nextCommand()
        if cmd.isNull():
            break
        print(f"{cmd}:")
        # invoke the command on the solver and the symbol manager, print the result        
        if cmd.getCommandName != "check-sat":
            cmd.invoke(slv, sm)

    print("Finished parsing commands")
    # declare z3 constants
    symbols = {}
    for term in sm.getDeclaredTerms():
        symbols[str(term)] = Int(str(term))
    print(symbols)
    # create a z3 solver
    z3_solver = Solver()
    phi_assertions = []
    star_predicate = None

    for assertion in slv.getAssertions():
        k = assertion.getKind()
        print(f'assertion: {assertion}')
        assert k == Kind.AND        
        for conjunct in assertion:
            print(f"translating conjunct: {conjunct}")
            z3_term = cvc5_to_z3(conjunct, symbols)            
            if conjunct.getKind() == Kind.STAR_CONTAINS:
                star_predicate = z3_term
            else:
                phi_assertions.append(z3_term)

    star_variables = [v for v in symbols.values()]
    result = sls_solver(phi_assertions, star_predicate, star_variables)
