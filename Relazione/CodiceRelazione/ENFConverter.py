from pyparsing import Literal, CaselessLiteral, Word, Combine, Group, Optional, ZeroOrMore, Forward, nums, alphas, srange


class ENFConverter:

    global bnf

    exprStack = []

    def pushAtom(self, toks):
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

    def pushBinary(self, toks):
        if toks and toks[0] == 'UNTIL':
            self.exprStack.append('UNTIL')
        if toks and toks[0] == '&':
            self.exprStack.append('&')
        if toks and toks[0] == 'FU':
            self.exprStack.append('FU')

    bnf = None

    def ENF(self):
        bnf = None
        if not bnf:
            atomicVal = Word(srange("[a-z0-9]"), max=10) | 'TRUE'
            lpar = Literal('(').suppress()
            rpar = Literal(')').suppress()
            expr = Forward()
            atom0 = (Optional('[]') + (atomicVal | lpar + atomicVal + rpar).setParseAction(self.pushAtom) | Optional('[]') + (lpar + expr + rpar)).setParseAction(self.pushUAlways)
            atom1 = (Optional('!') + (atomicVal | lpar + atomicVal + rpar).setParseAction(self.pushAtom) | Optional('!') + (lpar + expr + rpar)).setParseAction(self.pushUNot)
            atom2 = (Optional('NEXT') + (atomicVal | lpar + atomicVal + rpar).setParseAction(self.pushAtom) | Optional('NEXT') + (lpar + expr + rpar)).setParseAction(self.pushNext)
            atom3 = (Optional('EE') + (atomicVal | lpar + atomicVal + rpar).setParseAction(self.pushAtom) | Optional('EE') + (lpar + expr + rpar)).setParseAction(self.pushExistsEventualy)
            atom4 = (Optional('FE') + (atomicVal | lpar + atomicVal + rpar).setParseAction(self.pushAtom) | Optional('FE') + (lpar + expr + rpar)).setParseAction(self.pushForAllEventualy)
            atom5 = (Optional('FA') + (atomicVal | lpar + atomicVal + rpar).setParseAction(self.pushAtom) | Optional('FA') + (lpar + expr + rpar)).setParseAction(self.pushForAllAlways)
            atom6 = (Optional('FN') + (atomicVal | lpar + atomicVal + rpar).setParseAction(self.pushAtom) | Optional('FN') + (lpar + expr + rpar)).setParseAction(self.pushForAllNext)

            atoms = atom0 | atom1 | atom2 | atom3 | atom4 | atom5 | atom6

            andOp = Literal('&')
            untilOp = Literal('UNTIL')
            forAllUntil = Literal('FU')
            factor = Forward()
            factor = (atoms) + ZeroOrMore((andOp + (atoms) | untilOp + (atoms) | forAllUntil + (atoms)).setParseAction(self.pushBinary))
            expr << factor
            bnf = expr
        return bnf

    def evaluateStack(self):
        op = self.exprStack.pop()
        if op == '[]':
            op1 = '[](' + self.evaluateStack() + ')'
            return op1
        if op == '!':
            op1 = '!(' + self.evaluateStack() + ')'
            return op1
        if op == 'NEXT':
            op1 = 'NEXT(' + self.evaluateStack() + ')'
            return op1
        if op == '&':
            op1 = self.evaluateStack()
            op2 = self.evaluateStack()
            return op2 + ' ' + op + ' ' + op1
        if op == 'UNTIL':
            op1 = self.evaluateStack()
            op2 = self.evaluateStack()
            return '(' + op2 + ' ' + op + ' ' + op1 + ')'
        if op == 'FN':
            op1 = '!(NEXT(!(' + self.evaluateStack() + ')))'
            return op1
        if op == 'FE':
            op1 = '!([](!(' + self.evaluateStack() + ')))'
            return op1
        if op == 'FU':
            op1 = self.evaluateStack()  # phi
            op2 = self.evaluateStack()  # psi
            op3 = '!(!(' + op2 + ')UNTIL(!(' + op1 + ')&!(' + op2 + '))) & !([](!(' + op2 + ')))'
            return op3
        if op == 'FA':
            op1 = '!(TRUE UNTIL !(' + self.evaluateStack() + '))'
            return op1
        if op == 'EE':
            op1 = 'TRUE UNTIL (' + self.evaluateStack() + ')'
            return op1
        if op == 'TRUE':
            return 'TRUE'
        else:
            return op

    def getStack(self):
        return self.exprStack

    def convert(self, s):
        self.ENF().parseString(s)
        return self.evaluateStack()


if __name__ == '__main__':

    def test(s):
        parser = ENFConverter()
        results = parser.convert(s)
        print '### stringa di test ###'
        print s
        print '### stack  generato ###'
        print results
    test('[] FE (a)')
    # test('(NEXT a) FU b')
    # test('FA (a & b)')
    # test('EE (a & b)')
    # test('FN(a & b) & FE(c UNTIL d)')
    # test('((a & b) # c) & (>< (d & e))')
    # test('FE(TRUE) & (b FU NEXT(!c))')
