from array import array
import xml.etree.ElementTree as ET

stateTransition = {'T': 'H', 'H': 'W','W': 'E','E': 'T'} # transizioni da uno stato all altro

def next (state, fork):
    successors = [] # lista di tuple che contiene elementi (STATOSUCC, NUMFORK)
    for i in range(1,2**numeroFilosofi):
        tempState = array('c', state) # le stringhe in python sono immutabili e tocca usare gli array
        tempFork = fork
        binaryI = bin(i)[2:].zfill(numeroFilosofi) # uso i numeri binari per generare i possibili stati successivi
        for j in range(0,len(state)):
            if binaryI[j] == '1': # se nella posizione j del binario c e 1 allora si fa una transizione
                tempState[j] = stateTransition[state[j]]
                if   'W' in tempState[j]: # le fork diminuiscono se qualcuno passa da H a W e da W a E
                    tempFork = tempFork - 1
                elif 'E' in tempState[j]:
                    tempFork = tempFork - 1
                elif 'T' in tempState[j]: # da E a T si rilasciano le fork
                    tempFork = tempFork + 2
        if tempFork >= 0 and checkEating(tempState): # usando il numero di fork si evita di inserire tuple del tipo ('EEE',-3)
            successors.append((tempState.tostring(),tempFork))
    return successors

def checkEating(state):
    # non possono esserci due filosofi vicini che mangiano
    if 'EE' in state.tostring():
        return False
    if state[0] == 'E' and state[-1] == 'E': # caso ultimo e primo filosofo che condividono le fork
        return False
    return True

if __name__ == "__main__":
    numeroFilosofi = 3
    statoIniziale = "T" * numeroFilosofi
    states = {} # dizionario degli stati
    states[statoIniziale] = [] # primo elemento
    stack = []
    stack.append((statoIniziale,numeroFilosofi))
    while len(stack) > 0:
        s = stack.pop(0)
        successors = next(s[0], s[1])
        for nextState in successors:
            states[s[0]].append(nextState[0]) # aggiunge al elemento del dizionario gli stati di Post(elemento)
            if states.has_key(nextState[0]) == 0: # se lo stato e' nuovo
                states[nextState[0]] = [] # si aggiunge al dizionario e si associa ad una lista di adiacenza vuota
                stack.append(nextState) # si aggiunge allo stack per trovare i successori
        print s[0],"forchette disp ",s[1],":" , states[s[0]]

    # print "TT ",next("TT" , 2)
    # print "HH ",next("HH" , 2)
    # print "WW ",next("WW" , 0), " caso Deadlock"
    # print "WH ",next("WH" , 1)
    # print "EH ",next("EH" , 0)
