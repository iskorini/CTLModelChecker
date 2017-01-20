import matplotlib.pyplot as plt
from CTLModelChecker import CTLModelChecker
from ENFConverter import ENFConverter
if __name__ == "__main__":
    path = '../inputfiles/hello-world.gexf'
    #graph = nx.read_gexf('/Users/federicoschipani/Desktop/UNI - Magistrale/MFVS - Metodi Formali Per la Verifica di Sistemi/Progetto/CTLModelChecker/inputfiles/hello-world.gexf',  node_type=None, relabel=False, version='1.1draft')
    #pos=nx.spring_layout(graph)
    #nx.draw_networkx_labels(graph, pos,font_size=16)
    #plt.axis('off')
    #list = nx.get_node_attributes(graph, 'label')
    #for a in list:
    #    print list[a]
    #nx.draw(graph)
    #plt.show()
    #nx.write_gexf("output.gexf")
    converter = ENFConverter()
    converter.convert("a FU (b & c)")
    modelChecker = CTLModelChecker(path, 'TRUE & b')
    print "Start check"
    print "Elementi soddisfatti "
    print modelChecker.iterativeCheckFormula()
