import cvc5
import sys
from cvc5 import Kind
from z3 import *
from lia_star_solver import *


x1 = Int("x1")
x2 = Int("x2")

z1 = x1 == x2
z2 = x1 == x2

z3 = And(z1, z2)

interpolation_on = True
unfold = 5

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


def cvc5_to_z3(term, symbols):
    """
    Convert a cvc5 Term into a z3 term.
    symbols: dict mapping cvc5 terms to z3 constants
    """
    
    # const cases
    if term.isBooleanValue():
        return BoolVal(term.getBooleanValue())

    if term.isIntegerValue():
        value = term.getIntegerValue()        
        return IntVal(value)


    k = term.getKind()
    cvc5_children = list(term)    
    if k == Kind.CONSTANT or k == Kind.VARIABLE:
        return symbols[str(term)]

    # Recursive cases
    if k == Kind.STAR_CONTAINS:                
        lambda_term = list(cvc5_children[0])
        body = cvc5_to_z3(lambda_term[1], symbols)
        return body

    if term.getNumChildren() == 0:        
        raise Exception(f"Unhandled cvc5 term: {k} ({term})")
    
    z3_children = [cvc5_to_z3(child, symbols) for child in term]
    
    if k == Kind.EQUAL:                
        equality = z3_children[0] == z3_children[1]        
        return equality

    if k == Kind.NOT:                
        return Not(z3_children[0])

    if k == Kind.AND:                
        ret = And(*z3_children)        
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
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <filename.smt2>")
        sys.exit(1)
    filename = sys.argv[1]

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
        # invoke the command on the solver and the symbol manager, print the result        
        if cmd.getCommandName() != "check-sat":
            cmd.invoke(slv, sm)

    print("Finished parsing commands")
    # declare z3 constants
    symbols = {}
    for term in sm.getDeclaredTerms():
        symbols[str(term)] = Int(str(term))    
    # create a z3 solver
    z3_solver = Solver()
    phi_assertions = []
    star_predicate = None

    for assertion in slv.getAssertions():
        k = assertion.getKind()        
        assert k == Kind.AND        
        for conjunct in assertion:            
            z3_term = cvc5_to_z3(conjunct, symbols)            
            if conjunct.getKind() == Kind.STAR_CONTAINS:
                star_predicate = z3_term
            else:
                phi_assertions.append(z3_term)

    star_variables = [v for v in symbols.values()]
    result = sls_solver(phi_assertions, star_predicate, star_variables)
