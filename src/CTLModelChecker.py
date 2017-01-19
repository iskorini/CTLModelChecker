import networkx as nx
from CTLParser import CTLParser

class CTLModelChecker:

    __ts = ""
    __formula = ""
    __satisfactionSet = []
    def __init__(self, tsPath, formula):
        self.__ts = nx.read_gexf(tsPath,node_type=None, relabel=False, version='1.1draft')
        parser = CTLParser()
        parser.CTL().parseString(formula)
        self.__formula = parser.exprStack




    def checkFormula(self):
        op =  self.__formula.pop()
        if op == '!':
            element = self.__formula.pop()

        elif op == '&':

    def checkNot(self, element):





    def checkFormula(self):
        nodes = nx.get_node_attributes(self.__ts, 'label')
        print self.__formula
        #print nodes
        for element in self.__formula:
            if element not in ["><", "[]", "#", "!"]:
                for node in nodes:
                    if element in nodes[node]:
                        self.__satisfactionSet.append(node)
                        print self.__satisfactionSet
            elif element in "&":
                for node in nodes:




