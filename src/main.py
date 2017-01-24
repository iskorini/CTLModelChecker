import matplotlib.pyplot as plt
from CTLModelChecker import CTLModelChecker
from ENFConverter import ENFConverter
import networkx as nx
if __name__ == "__main__":
    path = '../inputfiles/ts6_11.gexf'
    graph = nx.read_gexf(path)
    pos=nx.spring_layout(graph,scale=2)
    nx.draw_networkx_nodes(graph,pos,node_color='#42f4dc',node_size=600,alpha=0.8)
    nx.draw_networkx_edges(graph,pos,width=2.0,arrows=True,alpha=0.5)
    nx.draw_networkx_labels(graph,pos,font_size=12)
    converter = ENFConverter()
    # formula = "EE (!(!(a & c & !b) & !(!a & !c & b)))"
    formula = " FE b"
    print "Formula: ",formula
    convertedFormula = converter.convert(formula)
    print "Formula in ENF: ", convertedFormula
    modelChecker = CTLModelChecker(path, convertedFormula)
    print "Transition system: ",modelChecker.getTs()
    print "Formula stack: ", modelChecker.getFormulaStack()
    print "Start check"
    print "Risultato , Elementi soddisfatti "
    result = modelChecker.iterativeCheckFormula()
    print result
    nx.draw_networkx_nodes(graph,pos,result[1],node_color='#42f46e',node_size=600,alpha=0.8)
    plt.figure(1)
    plt.axis('off')
    plt.savefig("ts.png")
