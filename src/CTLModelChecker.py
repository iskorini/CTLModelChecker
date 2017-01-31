import networkx as nx
import sys
from pyparsing import alphas
from CTLParser import CTLParser
from ENFConverter import ENFConverter


class CTLModelChecker:

    __ts = ''
    __formula = ''
    __satisfactionSet = []
    __nodes = []

    def __init__(self, tsPath, formula):
        ts = nx.read_gexf(tsPath, node_type=None, relabel=False, version='1.1draft')
        self.__ts = ts
        self.__nodes = nx.get_node_attributes(self.__ts, 'label')
        self.__formula = CTLParser().getParsedFormula(formula)

    def iterativeCheckFormula(self):
        satisfactionSet = []
        for i in self.__formula:
            if i == '!':
                el0 = satisfactionSet.pop()
                satisfactionSet.append(self.__checkNot(el0))
            elif i == '&':
                el0 = satisfactionSet.pop()
                el1 = satisfactionSet.pop()
                satisfactionSet.append(self.__checkAnd(el0, el1))
            elif i == 'UNTIL':
                el0 = satisfactionSet.pop()
                el1 = satisfactionSet.pop()
                satisfactionSet.append(self.__checkUntil(el0, el1))
            elif i == 'NEXT':
                el0 = satisfactionSet.pop()
                satisfactionSet.append(self.__checkNext(el0))
            elif i == '[]':
                el0 = satisfactionSet.pop()
                satisfactionSet.append(self.__checkAlways(el0))
            elif i == 'TRUE':
                satisfactionSet.append(self.__checkTrue())
            elif i[0].isalpha():
                satisfactionSet.append(self.__checkSingle(i))

        return (self.__checkInitialStates(satisfactionSet), satisfactionSet[0])

    def __checkInitialStates(self, satSet):
        initialStates = filter(lambda x: 'S' in x, self.__nodes)
        if satSet[0] is None:
            return False
        for state in initialStates:
            if state not in satSet[0]:
                return False
        return True

    def __checkAlways(self, el0):
        E = list(set(self.__nodes) - set(el0))
        T = el0
        count = dict()
        for el in el0:  # cambiare con map
            count[el] = len(self.__ts.successors(el))
        while len(E) > 0:
            s1 = E.pop()
            s1Preset = self.__ts.predecessors(s1)
            for s1pre in s1Preset:
                if s1pre in T:
                    count[s1pre] = count[s1pre] - 1
                    if count[s1pre] == 0:
                        E.append(s1pre)
                        T.remove(s1pre)
        return T

    def __checkNext(self, el0):
        tempList = []
        for node in self.__nodes:
            successors = self.__ts.successors(node)
            if len(set(successors).intersection(set(el0))) > 0:
                tempList.append(node)
        return tempList

    def __checkUntil(self, el0, el1):
        E = el0
        T = E[:]
        while len(E) > 0:
            s1 = E.pop()
            s1Preset = self.__ts.predecessors(s1)
            for s in s1Preset:
                if s in list(set(el1) - set(T)):
                    E.append(s)
                    T.append(s)
        return T

    def __checkTrue(self):
        return list(self.__nodes.keys())

    def __checkSingle(self, i):
        tempList = []
        for node in self.__nodes:
            if i in self.__nodes[node]:
                tempList.append(node)
        return tempList

    def __checkAnd(self, el0, el1):
        return list(set(el0).intersection(el1))

    def __checkNot(self, el0):
        if el0 is not None:
            return list(set(self.__nodes) - set(el0))
        return []

    def getTs(self):
        return self.__nodes

    def getFormulaStack(self):
        return self.__formula


if __name__ == '__main__':
    args = sys.argv
    convertedFormula = ENFConverter().convert(args[1])
    modelChecker = CTLModelChecker(args[2], convertedFormula)
    print modelChecker.iterativeCheckFormula()
