from array import array
import xml.etree.ElementTree as ET
# transizioni da uno stato all altro
stateTransition = {'T': 'H', 'H': 'W', 'W': 'E', 'E': 'T'}


def next(state, fork):
    # lista di tuple che contiene elementi (STATOSUCC, NUMFORK)
    successors = []
    for i in range(1, 2**numeroFilosofi):
        # le stringhe in python sono immutabili e tocca usare gli array
        tempState = array('c', state)
        tempFork = fork
        # uso i numeri binari per generare i possibili stati successivi
        binaryI = bin(i)[2:].zfill(numeroFilosofi)
        for j in range(0, len(state)):
            # se nella posizione j del binario c e 1
            # allora si fa una transizione
            if binaryI[j] == '1':
                tempState[j] = stateTransition[state[j]]
                # le fork diminuiscono se qualcuno passa da H a W e da W a E
                if 'W' in tempState[j]:
                    tempFork = tempFork - 1
                elif 'E' in tempState[j]:
                    tempFork = tempFork - 1
                elif 'T' in tempState[j]:  # da E a T si rilasciano le fork
                    tempFork = tempFork + 2
        # usando il numero di fork si evita di
        # inserire tuple del tipo ('EEE',-3)
        if tempFork >= 0 and checkEating(tempState):
            successors.append((tempState.tostring(), tempFork))
    return successors


def checkEating(state):
    # non possono esserci due filosofi vicini che mangiano
    if 'EE' in state.tostring():
        return False
    # caso ultimo e primo filosofo che condividono le fork
    if state[0] == 'E' and state[-1] == 'E':
        return False
    return True


if __name__ == '__main__':
    numeroFilosofi = 3
    statoIniziale = 'T' * numeroFilosofi
    states = {}  # dizionario degli stati
    states[statoIniziale] = []  # primo elemento
    stack = []
    stack.append((statoIniziale, numeroFilosofi))
    while len(stack) > 0:
        s = stack.pop(0)
        successors = next(s[0], s[1])
        for nextState in successors:
            # aggiunge al elemento del dizionario gli stati di Post(elemento)
            states[s[0]].append(nextState[0])
            if nextState[0] not in states.keys():  # se lo stato e' nuovo
                # si aggiunge al dizionario e si associa ad una lista di
                # adiacenza vuota
                states[nextState[0]] = []
                # si aggiunge allo stack per trovare i successori
                stack.append(nextState)
        print s[0], 'forchette disp ', s[1], ':', states[s[0]]

    # print 'TT ',next('TT' , 2)
    # print 'HH ',next('HH' , 2)
    # print 'WW ',next('WW' , 0), ' caso Deadlock'
    # print 'WH ',next('WH' , 1)
    # print 'EH ',next('EH' , 0)
