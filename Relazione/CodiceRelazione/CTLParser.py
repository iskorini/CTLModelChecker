from pyparsing import Literal, CaselessLiteral, Word, Combine, Group, Optional, ZeroOrMore, Forward, nums, alphas, srange


class CTLParser:

    global bnf

    exprStack = []

    def pushAtom(self, toks):
        self.exprStack.append(toks[0])

    def pushUNot(self, toks):
        if toks and toks[0] == '!':
            self.exprStack.append('!')

    def pushUAlways(self, toks):
        if toks and toks[0] == '[]':
            self.exprStack.append('[]')

    def pushNext(self, toks):
        if toks and toks[0] == 'NEXT':
            self.exprStack.append('NEXT')

    def pushBinary(self, toks):
        if toks and toks[0] == 'UNTIL':
            self.exprStack.append('UNTIL')
        if toks and toks[0] == '&':
            self.exprStack.append('&')

    def CTL(self):
        bnf = None
        if not bnf:
            atomicVal = Word(srange("[a-z0-9]"), max=10) | 'TRUE'
            lpar = Literal('(').suppress()
            rpar = Literal(')').suppress()
            expr = Forward()
            atom0 = (Optional('[]') + (atomicVal | lpar + atomicVal + rpar).setParseAction(self.pushAtom) | Optional('[]') + (lpar + expr + rpar)).setParseAction(self.pushUAlways)
            atom1 = (Optional('!') + (atomicVal | lpar + atomicVal + rpar).setParseAction(self.pushAtom) | Optional('!') + (lpar + expr + rpar)).setParseAction(self.pushUNot)
            atom2 = (Optional('NEXT') + (atomicVal | lpar + atomicVal + rpar).setParseAction(self.pushAtom) | Optional('NEXT') + (lpar + expr + rpar)).setParseAction(self.pushNext)

            atoms = atom0 | atom1 | atom2

            andOp = Literal('&')
            untilOp = Literal('UNTIL')

            factor = Forward()
            factor = (atoms) + ZeroOrMore((andOp + (atoms) | untilOp + (atoms)).setParseAction(self.pushBinary))
            expr << factor
            bnf = expr
        return bnf

    def getParsedFormula(self, formula):
        results = self.CTL().parseString(formula)
        return self.exprStack

    ''' Debug '''
    def evaluateStack(self):
        op = self.exprStack.pop()
        if op == '[]':
            op1 = '[]' + self.evaluateStack()
            print op1
            return op1
        if op == '!':
            op1 = '!' + self.evaluateStack()
            print op1
            return op1
        if op == '&':
            op1 = self.evaluateStack()
            op2 = self.evaluateStack()
            print op2 + ' ' + op + ' ' + op1
            return op2 + op1
        if op == 'UNTIL':
            op1 = self.evaluateStack()
            op2 = self.evaluateStack()
            print op2 + ' ' + op + ' ' + op1
            return op2 + op1
        if op == 'TRUE':
            return 'TRUE'
        if op == 'TRUE':
            return 'TRUE'
        else:
            return op


if __name__ == '__main__':

    def test(s):
        parser = CTLParser()
        results = parser.getParsedFormula(s)
        print '### stringa di test ###'
        print s
        print '### stack  generato ###'
        print results

    # test('((a & b) # c) & (>< (d & e))')
    test('a & b & (c & d) & e')
    # test('!(a UNTIL b) & k')
    # test('a')
    # test( 'a & b')
    # print ''
    # test( '((a & b) # c) & ([] (d & e))')
    # print ''
    # test( '(a & b) # (c # (d # e))')
    # print ''
    # test ('!a')
    # print ''
    # test ('[](a)')
    # print ''

    # test ( '[] (a & !b)')
    # print ''
    # test ( '!(a & b)')
