import networkx as nx
from pyparsing import alphas
from CTLParser import CTLParser

class CTLModelChecker:

    __ts = ""
    __formula = ""
    __satisfactionSet = []
    __nodes = []
    def __init__(self, tsPath, formula):
        self.__ts = nx.read_gexf(tsPath,node_type=None, relabel=False, version='1.1draft')
        self.__nodes = nx.get_node_attributes(self.__ts, 'label')
        print self.__nodes
        parser = CTLParser()
        parser.CTL().parseString(formula)
        self.__formula = parser.exprStack
        print formula

    def checkFormula(self):
        op =  self.__formula.pop()
        listTemp = []
        if op == '!':
            elements = self.checkFormula()
            for e in elements:
                if e not in self.__nodes[e]:
                    self.__satisfactionSet.append(e)
                    listTemp.append(e)
            return listTemp
        elif op == '&':
            elements0 = self.checkFormula()
            elements1 = self.checkFormula()
            for e in elements0:
                if e in elements1:
                    self.__satisfactionSet.append(e)
                    listTemp.append(e)
            return listTemp
        elif op[0].isalpha():
            for node in self.__nodes:
                if op in self.__nodes[node]:
                    self.__satisfactionSet.append(node)
                    listTemp.append(node)
            # print "singoletto " + op
            # print listTemp
            return listTemp
