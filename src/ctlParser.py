# fourFn.py
#
# Demonstration of the pyparsing module, implementing a simple 4-function expression parser,
# with support for scientific notation, and symbols for e and pi.
# Extended to add exponentiation and simple built-in functions.
# Extended test cases, simplified pushFirst method.
#
# Copyright 2003-2006 by Paul McGuire
#
from pyparsing import Literal,CaselessLiteral,Word,Combine,Group,Optional,\
    ZeroOrMore,Forward,nums,alphas
import math
import operator

exprStack = []

def pushFirst( strg, loc, toks ):
    exprStack.append( toks[0] )
    # print toks[0]
def pushUMinus( strg, loc, toks ):
    if toks and toks[0]=='-':
        exprStack.append( 'unary -' )

def pushUNot( strg, loc, toks ):
    if toks and toks[0]=='!':
        exprStack.append( 'unary !' )
        #~ exprStack.append( '-1' )
        #~ exprStack.append( '*' )
def pushUAlways( strg, loc, toks ):
    if toks and toks[0]=='@':
        exprStack.append( 'unary @' )

bnf = None
def BNF():
    """
    expop   :: '^'
    multop  :: '*' | '/'
    addop   :: '+' | '-'
    integer :: ['+' | '-'] '0'..'9'+
    atom    :: PI | E | real | fn '(' expr ')' | '(' expr ')'
    factor  :: atom [ expop factor ]*
    term    :: factor [ multop factor ]*
    expr    :: term [ addop term ]*
    """
    global bnf
    if not bnf:
        point = Literal( "." )

        atomicVal = Word(alphas)
        fnumber = Combine( Word( "+-"+nums, nums ))

        plus  = Literal( "+" )
        minus = Literal( "-" )
        mult  = Literal( "*" )
        div   = Literal( "/" )
        lpar  = Literal( "(" ).suppress()
        rpar  = Literal( ")" ).suppress()
        addop  = plus | minus
        multop = mult | div
        expop = Literal( "^" )
        notOp = Literal( "!")
        andOp = Literal( "&" )
        untilOp = CaselessLiteral( "U" )
        pi    = CaselessLiteral( "PI" )

        expr = Forward()
        atom0 = (Optional("@") + (atomicVal | atomicVal + lpar + expr + rpar ).setParseAction( pushFirst ) | ( lpar + expr.suppress() + rpar )).setParseAction(pushUAlways)
        atom1 = (Optional("!") + (atomicVal | atomicVal + lpar + expr + rpar ).setParseAction( pushFirst ) | ( lpar + expr.suppress() + rpar )).setParseAction(pushUNot)

        factor0 = Forward()
        factor0 = atom0 + ZeroOrMore( ( notOp + andOp + untilOp + factor0 ).setParseAction( pushFirst ) )
        factor1 = Forward()
        factor1 = atom1 + ZeroOrMore( ( notOp + andOp + untilOp + factor1 ).setParseAction( pushFirst ) )

        term0 = factor1 + ZeroOrMore( ( andOp   + factor1  ).setParseAction( pushFirst ) )
        term1 = term0 + ZeroOrMore( ( untilOp + factor1 ).setParseAction( pushFirst ) )
        expr << term1

        bnf = expr
    return bnf

# map operator symbols to corresponding arithmetic operations
epsilon = 1e-12
opn = { "+" : operator.add,
        "-" : operator.sub,
        "*" : operator.mul,
        "/" : operator.truediv,
        "^" : operator.pow }
fn  = { "sin" : math.sin,
        "cos" : math.cos,
        "tan" : math.tan,
        "abs" : abs,
        "trunc" : lambda a: int(a),
        "round" : round,
        "sgn" : lambda a: abs(a)>epsilon and cmp(a,0) or 0}
def evaluateStack( s ):
    op = s.pop()
    if op == 'unary @':
        return "@"+evaluateStack( s )
    if op == 'unary !':
        op1 = "!"+evaluateStack( s )
        print op1
        return op1
    if op in "+-*/^":
        op2 = evaluateStack( s )
        op1 = evaluateStack( s )
        return opn[op]( op1, op2 )
    if op in "&U":
        op1 = evaluateStack( s )
        op2 = evaluateStack( s )
        print op1 + " "+op+" "+ op2
        return op1+op2
    elif op == "PI":
        return math.pi # 3.1415926535
    elif op in fn:
        return fn[op]( evaluateStack( s ) )
    elif op[0].isalpha():
        return op[0]
    else:
        return float( op )

if __name__ == "__main__":

    def test( s ):
        global exprStack
        exprStack = []
        results = BNF().parseString( s )
        print s
        print exprStack
        val = evaluateStack( exprStack[:] )
        # if val == expVal:
        #     print s, "=", val, results, "=>", exprStack
        # else:
        #     print s+"!!!", val, "!=", expVal, results, "=>", exprStack

    test( "a & b")
    test( "(a & b) U (c & (d & e))")
    test ("!a")
    test ("@a")

    test ( "@a & !b")
    test ( "!(a & b)")
