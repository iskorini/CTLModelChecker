from pyparsing import Literal,CaselessLiteral,Word,Combine,Group,Optional,\
    ZeroOrMore,Forward,nums,alphas
class CTLParser:

    global bnf

    exprStack = []

    def pushFirst(self, strg, loc, toks ):
        self.exprStack.append( toks[0] )

    def pushUNot(self,  strg, loc, toks ):
        if toks and toks[0]=='!':
            self.exprStack.append( '!' )
    def pushUAlways(self, strg, loc, toks ):
        if toks and toks[0]=="[]":
            self.exprStack.append( '[]' )
    def pushNext(self, strg, loc, toks):
        if toks and toks[0]=="NEXT":
            self.exprStack.append('NEXT')

    bnf = None
    def CTL(self):
        global bnf
        if not bnf:
            atomicVal = Word("abcdefghijklmnopqrstuvwxyz") | "TRUE"
            lpar  = Literal( "(" ).suppress()
            rpar  = Literal( ")" ).suppress()
            notOp = Literal( "!")
            andOp = Literal( "&" )
            untilOp = Literal( "UNTIL" )
            expr = Forward()
            atom0 = (Optional("[]") + (atomicVal | lpar + atomicVal  + rpar ).setParseAction( self.pushFirst ) | Optional("[]") + ( lpar + expr + rpar )).setParseAction(self.pushUAlways)
            atom1 = (Optional("!")  + (atomicVal | lpar + atomicVal  + rpar ).setParseAction( self.pushFirst ) | Optional("!")  + ( lpar + expr + rpar )).setParseAction(self.pushUNot)
            atom2 = (Optional("NEXT") + (atomicVal | lpar + atomicVal  + rpar ).setParseAction( self.pushFirst)  | Optional("NEXT") + ( lpar + expr + rpar )).setParseAction(self.pushNext)
            factor = Forward()
            factor = (atom1|atom0|atom2) + ZeroOrMore( ( andOp + (atom1|atom0|atom2) | untilOp +(atom1|atom0|atom2)  ).setParseAction( self.pushFirst ) )
            expr << factor
            bnf = expr
        return bnf

    def evaluateStack(self):
        op =  self.exprStack.pop()
        if op == "[]":
            op1 = "[]"+self.evaluateStack()
            print op1
            return op1
        if op == "!":
            op1 = "!"+self.evaluateStack()
            print op1
            return op1
        if op == "&":
            op1 = self.evaluateStack()
            op2 = self.evaluateStack()
            print op2 + " "+op+" "+ op1
            return op2+op1
        if op == "UNTIL":
            op1 = self.evaluateStack()
            op2 = self.evaluateStack()
            print op2 + " "+op+" "+ op1
            return op2+op1
        if op in "NEXT":
            return "NEXT"+self.evaluateStack()
        if op == "TRUE":
            return "TRUE"
        if op == "TRUE":
            return "TRUE"
        if op in "abcdefghijklmnopqrstuvwxyz":
            return op
        else:
            return op+":"+self.evaluateStack()

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
        val = parser.evaluateStack()




    #test("((a & b) # c) & (>< (d & e))")
    test("NEXT(TRUE) & (b UNTIL [](!c))")
    # test("!(a UNTIL b) & k")
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
