from pyparsing import Literal,CaselessLiteral,Word,Combine,Group,Optional,\
    ZeroOrMore,Forward,nums,alphas
import networkx as nx
import math
import operator



class CTLParser:

    global bnf

    exprStack = []

    def pushFirst(self, strg, loc, toks ):
        self.exprStack.append( toks[0] )

    def pushUNot(self,  strg, loc, toks ):
        if toks and toks[0]=='!':
            self.exprStack.append( '!' )
    def pushUAlways(self, strg, loc, toks ):
        print toks
        if toks and toks[0]=="[]":
            self.exprStack.append( '[]' )
    def pushNext(self, strg, loc, toks):
        if toks and toks[0]=="><":
            self.exprStack.append('><')

    bnf = None
    def CTL(self):
        global bnf
        if not bnf:
            atomicVal = Word(alphas)
            lpar  = Literal( "(" ).suppress()
            rpar  = Literal( ")" ).suppress()
            notOp = Literal( "!")
            andOp = Literal( "&" )
            untilOp = Literal( "#" )
            expr = Forward()
            atom0 = (Optional("[]") + (atomicVal | lpar + atomicVal  + rpar ).setParseAction( self.pushFirst ) | Optional("[]") + ( lpar + expr + rpar )).setParseAction(self.pushUAlways)
            atom1 = (Optional("!") + (atomicVal | lpar + atomicVal  + rpar ).setParseAction( self.pushFirst ) | Optional("!") + ( lpar + expr + rpar )).setParseAction(self.pushUNot)
            atom2 = (Optional("><") + (atomicVal | lpar + atomicVal + rpar).setParseAction(self.pushFirst) | Optional("><") + (lpar + expr + rpar)).setParseAction(self.pushNext)
            factor = Forward()
            factor = (atom1|atom0|atom2) + ZeroOrMore( ( andOp + (atom1|atom0|atom2) | untilOp +(atom1|atom0|atom2)  ).setParseAction( self.pushFirst ) )
            expr << factor
            bnf = expr
        return bnf

    def evaluateStack(self):
        op =  self.exprStack.pop()
        if op == '[]':
            return "@"+self.evaluateStack()
        if op == '!':
            op1 = "!"+self.evaluateStack()
            print op1
            return op1
        if op in "&#":
            op1 = self.evaluateStack()
            op2 = self.evaluateStack()
            print op2 + " "+op+" "+ op1
            return op2+op1
        if op in "><":
            return "><"+self.evaluateStack()
        elif op[0].isalpha():
            return op[0]
        else:
            return float( op )

    def getStack(self):
        return self.exprStack





if __name__ == "__main__":

    def test( s ):
        parser = CTLParser()
        results = parser.CTL().parseString( s )
        print "### stringa di test ###"
        print s
        print "### stack  generato ###"
        print parser.exprStack
        #val = parser.evaluateStack()




    #test("((a & b) # c) & (>< (d & e))")
    #test("><(a) & (b # [](!c))")
    test("!(a & b) & k")
    #test("a")
    #test( "a & b")
    #print ""
    #test( "((a & b) # c) & ([] (d & e))")
    #print ""
    #test( "(a & b) # (c # (d # e))")
    #print ""
    #test ("!a")
    #print ""
    #test ("[](a)")
    #print ""

    #test ( "[] (a & !b)")
    #print ""
    #test ( "!(a & b)")
