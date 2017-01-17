import networkx as nx
import matplotlib.pyplot as plt


graph = nx.read_gexf('/Users/federicoschipani/Desktop/UNI - Magistrale/MFVS - Metodi Formali Per la Verifica di Sistemi/Progetto/CTLModelChecker/inputfiles/hello-world.gexf',  node_type=None, relabel=False, version='1.1draft')
pos=nx.spring_layout(graph)
nx.draw_networkx_labels(graph, pos,font_size=16)
plt.axis('off')
print nx.get_node_attributes(graph, 'label')
nx.draw(graph)
plt.show()
#nx.write_gexf("output.gexf")

