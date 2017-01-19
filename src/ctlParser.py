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

        atomicVal = Word(alphas)

        lpar  = Literal( "(" ).suppress()
        rpar  = Literal( ")" ).suppress()

        notOp = Literal( "!")
        andOp = Literal( "&" )
        untilOp = Literal( "#" )

        expr = Forward()
        atom0 = (Optional("@") + (atomicVal | lpar + atomicVal  + rpar ).setParseAction( pushFirst ) | Optional("@") + ( lpar + expr + rpar )).setParseAction(pushUAlways)
        atom1 = (Optional("!") + (atomicVal | lpar + atomicVal  + rpar ).setParseAction( pushFirst ) | Optional("!") + ( lpar + expr + rpar )).setParseAction(pushUNot)

        factor = Forward()
        factor = (atom1|atom0) + ZeroOrMore( ( andOp + (atom1|atom0) | untilOp +(atom1|atom0)  ).setParseAction( pushFirst ) )

        expr << factor

        bnf = expr
    return bnf

def evaluateStack( s ):
    op = s.pop()
    if op == 'unary @':
        return "@"+evaluateStack( s )
    if op == 'unary !':
        op1 = "!"+evaluateStack( s )
        print op1
        return op1
    if op in "&#":
        op1 = evaluateStack( s )
        op2 = evaluateStack( s )
        print op2 + " "+op+" "+ op1
        return op2+op1
    elif op[0].isalpha():
        return op[0]
    else:
        return float( op )

if __name__ == "__main__":

    def test( s ):
        global exprStack
        exprStack = []
        results = BNF().parseString( s )
        print "### stringa di test ###"
        print s
        print "### stack  generato ###"
        print exprStack
        val = evaluateStack( exprStack[:] )

    test("a")
    test( "a & b")
    print ""
    test( "(a & b) # (c & (d & e))")
    print ""
    test( "(a & b) # (c # (d # e))")
    print ""
    test ("!a")
    print ""
    test ("@(a)")
    print ""

    test ( "@a & !b")
    print ""
    test ( "!(a & b)")
