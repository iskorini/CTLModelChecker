from array import array
from xml.etree.ElementTree import Element, SubElement, Comment, tostring, ElementTree
from xml.dom import minidom
# transizioni da uno stato all altro
stateTransition = {'t': 'h', 'h': 'w', 'w': 'e', 'e': 't'}
states = {}


def prettify(elem):
    rough_string = tostring(elem)
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


def generateXML(philnumber):
    numeroFilosofi = philnumber
    statoIniziale = ""
    for i in range(numeroFilosofi):
        statoIniziale += "t" + str(i)
    # states = {}  # dizionario degli stati
    states[statoIniziale] = []  # primo elemento
    stack = []
    stack.append((statoIniziale, numeroFilosofi))
    while len(stack) > 0:
        s = stack.pop(0)
        successors = next(s[0], s[1], philnumber)
        for nextState in successors:
            # aggiunge al elemento del dizionario gli stati di Post(elemento)
            states[s[0]].append(nextState[0])
            if nextState[0] not in states.keys():  # se lo stato e' nuovo
                # si aggiunge al dizionario e si associa ad una lista di
                # adiacenza vuota
                states[nextState[0]] = []
                # si aggiunge allo stack per trovare i successori
                stack.append(nextState)
        # print s[0], "forchette disp ", s[1], ":", states[s[0]]
    top = Element('gexf', attrib={'xmlns': "http://www.gexf.net/1.2draft", 'xmlns:viz': "http://www.gexf.net/1.2draft/viz", 'xmlns:xsi': "http://www.w3.org/2001/XMLSchema-instance", 'xsi:schemaLocation': "http://www.gexf.net/1.2draft http://www.gexf.net/1.2draft/gexf.xsd", 'version': "1.2"})
    graphNode = SubElement(top, 'graph', attrib={'mode': "static", 'defaultedgetype': "directed"})
    nodesNode = SubElement(graphNode, 'nodes')
    edgesNode = SubElement(graphNode, 'edges')
    i = 0
    singlenode = SubElement(nodesNode, 'node', attrib={'id': 'S' + statoIniziale, 'label': statoIniziale})
    for nextValue in states[statoIniziale]:
        transition = SubElement(edgesNode, 'edge', attrib={'id': str(i), 'source': 'S' + statoIniziale, 'target': nextValue})
        i += 1
    states.pop(statoIniziale)
    for nodes in states:
        singlenode = SubElement(nodesNode, 'node', attrib={'id': nodes, 'label': nodes})
        if states[nodes] == []:
            transition = SubElement(edgesNode, 'edge', attrib={'id': str(i), 'source': nodes, 'target': nodes})
        for nextValue in states[nodes]:
            if nextValue == statoIniziale:
                transition = SubElement(edgesNode, 'edge', attrib={'id': str(i), 'source': nodes, 'target': 'S' + nextValue})
            else:
                transition = SubElement(edgesNode, 'edge', attrib={'id': str(i), 'source': nodes, 'target': nextValue})
            i += 1
    output_file = open('../inputfiles/filosofi.gexf', 'w')
    prettifiedfile = prettify(top)
    output_file.write(prettifiedfile[15 + 8:])
    output_file.close()


def next(state, fork, numeroFilosofi):
    # lista di tuple che contiene elementi (STATOSUCC, NUMFORK)
    successors = []
    for i in range(1, 2**numeroFilosofi):
        # le stringhe in python sono immutabili e tocca usare gli array
        tempState = array('c', state)
        tempFork = fork
        # uso i numeri binari per generare i possibili stati successivi
        binaryI = bin(i)[2:].zfill(numeroFilosofi)
        for j in range(0, (len(state) / 2)):
            # se nella posizione j del binario c e 1
            # allora si fa una transizione
            if binaryI[j] == '1':
                tempState[j * 2] = stateTransition[state[j * 2]]
                # le fork diminuiscono se qualcuno passa da H a W e da W a E
                if 'w' in tempState[j * 2]:
                    tempFork = tempFork - 1
                elif 'e' in tempState[j * 2]:
                    tempFork = tempFork - 1
                elif 't' in tempState[j * 2]:  # da E a T si rilasciano le fork
                    tempFork = tempFork + 2
        # usando il numero di fork si evita di
        # inserire tuple del tipo ('EEE',-3)
        if tempFork >= 0 and checkEating(tempState):
            successors.append((tempState.tostring(), tempFork))
    return successors


def generateState(state, posizione):
    listaStati = []
    for s in states.keys():
        if state in s[posizione]:
            listaStati.append(s)
    return listaStati


def checkEating(state):
    # non possono esserci due filosofi vicini che mangiano
    if 'ee' in state.tostring():
        return False
    # caso ultimo e primo filosofo che condividono le fork
    if state[0] == 'e' and state[-1] == 'e':
        return False
    return True


if __name__ == "__main__":
    # print next("t1t2",2,2)
    generateXML(5)
    # print generateState("e", 0)
    # print "TT ",next("TT" , 2)
    # print "HH ",next("HH" , 2)
    # print "WW ",next("WW" , 0), " caso Deadlock"
    # print "WH ",next("WH" , 1)
    # print "EH ",next("EH" , 0)
