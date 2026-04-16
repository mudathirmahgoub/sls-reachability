
import cvc5
from cvc5 import Kind
from z3 import *


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
        return IntVal(term.getIntegerValue())

    k = term.getKind()
    # print(f"Translating kind: {k}")
    if k == Kind.CONSTANT or k == Kind.VARIABLE:
        return symbols[str(term)]
    
    # Recursive cases    
    if k == Kind.STAR_CONTAINS:
        print(str(Kind.STAR_CONTAINS))        
        lambda_term = term[0]
        body = cvc5_to_z3(lambda_term[1], symbols)
        children = list(term)
        outer_vector = [cvc5_to_z3(child, symbols) for child in children[1:]]
        return body
    
    children = [cvc5_to_z3(child, symbols) for child in term]    

    if k == Kind.EQUAL:
        return children[0] == children[1]

    if k == Kind.NOT:
        return Not(children[0])

    if k == Kind.AND:
        return And(*children)

    if k == Kind.OR:
        return Or(*children)    

    if k == Kind.IMPLIES:
        return Implies(children[0], children[1])

    if k == Kind.ITE:
        return If(children[0], children[1], children[2])

    if k == Kind.ADD:
        return children[0] + children[1]

    if k == Kind.SUB:
        return children[0] - children[1]

    if k == Kind.MULT:
        return children[0] * children[1]

    if k == Kind.LT:
        return children[0] < children[1]

    if k == Kind.LEQ:
        return children[0] <= children[1]

    if k == Kind.GT:
        return children[0] > children[1]

    if k == Kind.GEQ:
        return children[0] >= children[1]

    raise Exception(f"Unsupported cvc5 operator: {k} ({term})")



if __name__ == "__main__":
    tm = cvc5.TermManager()
    slv = cvc5.Solver(tm)

    # set that we should print success after each successful command    
    slv.setOption("dag-thresh", "0")

    # construct an input parser associated the solver above
    parser = cvc5.InputParser(slv)   

    parser.setFileInput(cvc5.InputLanguage.SMT_LIB_2_6, "/home/mudathir/all/SQLSolver/cvc5/calcite/query013-call-0.smt2")

    # get the symbol manager of the parser, used when invoking commands below
    sm = parser.getSymbolManager()

    # parse commands until finished
    while True:
        cmd = parser.nextCommand()
        if cmd.isNull():
            break
        print(f"Executing command {cmd}:")
        # invoke the command on the solver and the symbol manager, print the result
        print(f"command: {cmd.getCommandName()}")
        print(f"command.toString(): {cmd.toString()}")
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
    for assertion in slv.getAssertions():
        print(assertion)
        z3_term = cvc5_to_z3(assertion, symbols)

