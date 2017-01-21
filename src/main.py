import matplotlib.pyplot as plt
from CTLModelChecker import CTLModelChecker
from ENFConverter import ENFConverter
import networkx as nx
if __name__ == "__main__":
    path = '../inputfiles/hello-world.gexf'
    graph = nx.read_gexf(path)
    pos=nx.circular_layout(graph,scale=2)
    # print graph.nodes()
    nx.draw_networkx_nodes(graph,pos,
                       node_color='#42f4dc',
                       node_size=600,
                       alpha=0.8)
    nx.draw_networkx_edges(graph,pos,width=2.0,arrows=True,alpha=0.5)
    nx.draw_networkx_labels(graph,pos,font_size=16)
    #nx.write_gexf("output.gexf")
    converter = ENFConverter()
    convertedFormula = converter.convert("EE (!(!(a & c & !b) & !(!a & !c & b)))")
    modelChecker = CTLModelChecker(path, convertedFormula)
    print "Start check"
    print "Elementi soddisfatti "
    result = modelChecker.iterativeCheckFormula()
    # print result
    nx.draw_networkx_nodes(graph,pos,
                       result[1],
                       node_color='#42f46e',
                       node_size=600,
                       alpha=0.8)
    plt.figure(1)
    plt.axis('off')
    plt.savefig("ts.png")
