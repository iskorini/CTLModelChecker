from pyparsing import Literal, CaselessLiteral, Word, Combine, Group, Optional, ZeroOrMore, Forward, nums, alphas


class ENFConverter:

    global bnf

    exprStack = []

    def pushFirst(self, strg, loc, toks):
        self.exprStack.append(toks[0])

    def pushUNot(self, strg, loc, toks):
        if toks and toks[0] == '!':
            self.exprStack.append('!')

    def pushUAlways(self, strg, loc, toks):
        if toks and toks[0] == '[]':
            self.exprStack.append('[]')

    def pushNext(self, strg, loc, toks):
        if toks and toks[0] == 'NEXT':
            self.exprStack.append('NEXT')

    def pushForAllEventualy(self, strg, loc, toks):
        if toks and toks[0] == 'FE':
            self.exprStack.append('FE')

    def pushExistsEventualy(self, strg, loc, toks):
        if toks and toks[0] == 'EE':
            self.exprStack.append('EE')

    def pushForAllAlways(self, strg, loc, toks):
        if toks and toks[0] == 'FA':
            self.exprStack.append('FA')

    def pushForAllNext(self, strg, loc, toks):
        if toks and toks[0] == 'FN':
            self.exprStack.append('FN')

    bnf = None

    def ENF(self):
        global bnf
        if not bnf:
            atomicVal = Word('abcdefghijklmnopqrstuvwxyz') | 'TRUE'
            lpar = Literal('(').suppress()
            rpar = Literal(')').suppress()
            notOp = Literal('!')
            andOp = Literal('&')
            untilOp = Literal('UNTIL')
            forAllEventualy = Literal('FE')
            existsEventualy = Literal('EE')
            forAllAlways = Literal('FA')
            forAllNext = Literal('FN')
            forAllUntil = Literal('FU')
            expr = Forward()
            atom0 = (Optional('[]') + (atomicVal | lpar + atomicVal + rpar).setParseAction(self.pushFirst) | Optional('[]') + (lpar + expr + rpar)).setParseAction(self.pushUAlways)
            atom1 = (Optional('!') + (atomicVal | lpar + atomicVal + rpar).setParseAction(self.pushFirst) | Optional('!') + (lpar + expr + rpar)).setParseAction(self.pushUNot)
            atom2 = (Optional('NEXT') + (atomicVal | lpar + atomicVal + rpar).setParseAction(self.pushFirst) | Optional('NEXT') + (lpar + expr + rpar)).setParseAction(self.pushNext)
            atom3 = (Optional('FE') + (atomicVal | lpar + atomicVal + rpar).setParseAction(self.pushFirst) | Optional('FE') + (lpar + expr + rpar)).setParseAction(self.pushForAllEventualy)
            atom4 = (Optional('EE') + (atomicVal | lpar + atomicVal + rpar).setParseAction(self.pushFirst) | Optional('EE') + (lpar + expr + rpar)).setParseAction(self.pushExistsEventualy)
            atom5 = (Optional('FA') + (atomicVal | lpar + atomicVal + rpar).setParseAction(self.pushFirst) | Optional('FA') + (lpar + expr + rpar)).setParseAction(self.pushForAllAlways)
            atom6 = (Optional('FN') + (atomicVal | lpar + atomicVal + rpar).setParseAction(self.pushFirst) | Optional('FN') + (lpar + expr + rpar)).setParseAction(self.pushForAllNext)

            atoms = atom0 | atom1 | atom2 | atom3 | atom4 | atom5 | atom6
            factor = Forward()
            factor = (atoms) + ZeroOrMore((andOp + (atoms) | untilOp + (atoms) | forAllUntil + (atoms)).setParseAction(self.pushFirst))
            expr << factor
            bnf = expr
        return bnf

    def evaluateStack(self):
        op = self.exprStack.pop()
        if op == '[]':
            op1 = '[](' + self.evaluateStack() + ')'
            # print op1
            return op1
        if op == '!':
            op1 = '!(' + self.evaluateStack() + ')'
            # print op1
            return op1
        if op == '&':
            op1 = self.evaluateStack()
            op2 = self.evaluateStack()
            # print op2 + ' '+op+' '+ op1
            return op2 + ' ' + op + ' ' + op1
        if op == 'UNTIL':
            op1 = self.evaluateStack()
            op2 = self.evaluateStack()
            # print op2 + ' '+op+' '+ op1
            return op2 + ' ' + op + ' ' + op1
        if op == 'FN':
            op1 = '!(NEXT(!(' + self.evaluateStack() + ')))'
            # print op1
            return op1
        if op == 'FE':
            op1 = '!([](!(' + self.evaluateStack() + ')))'
            # print op1
            return op1
        if op == 'FU':
            op1 = self.evaluateStack()  # phi
            op2 = self.evaluateStack()  # psi
            op3 = '!(!(' + op2 + ')UNTIL(!(' + op1 + ')&!(' + op2 + '))) & !([](!(' + op2 + ')))'
            # print op3
            return op3
        if op == 'FA':
            op1 = '!(TRUE UNTIL !(' + self.evaluateStack() + '))'
            # print op1
            return op1
        if op == 'EE':
            op1 = 'TRUE UNTIL (' + self.evaluateStack() + ')'
            # print op1
            return op1
        if op == 'TRUE':
            return 'TRUE'
        if op in 'abcdefghijklmnopqrstuvwxyz':
            return op
        else:
            return op + ' ' + self.evaluateStack()

    def getStack(self):
        return self.exprStack

    def convert(self, s):
        self.ENF().parseString(s)
        return self.evaluateStack()


if __name__ == '__main__':

    def test(s):
        parser = ENF()
        results = parser.ENF().parseString(s)
        print '### stringa di test ###'
        print s
        print '### stack  generato ###'
        print parser.exprStack
        val = parser.evaluateStack()

    test('(NEXT a) FU b')
    test('FA (a & b)')
    test('EE (a & b)')
    # test('FN(a & b) & FE(c UNTIL d)')
    # test('((a & b) # c) & (>< (d & e))')
    # test('FE(TRUE) & (b FU NEXT(!c))')
