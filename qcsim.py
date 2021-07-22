import os
import numpy as np
import random

num_qubits = 0
term = 1/2**0.5

#Unitary for Identity
I = np.array([[1,0],[0,1]])

#Unitary for Hadamard
H = np.array([[term, term], [term,-term]])

#Unitary for T gate
T = np.array([[1,0],[0,term+ term*1.0j]], dtype=complex)

#Unitary for Pauli-X gate
X = np.array([[0,1],[1,0]])

#Unitary for Pauli-Y gate
Y = np.array([[0,-1j],[1j,0]], dtype=complex)

#Unitary for Pauli-Z gate
Z = np.array([[1,0],[0,-1]])

#Unitary for CX
#target is next qubit(control+1_)
CX_next = np.array([[1, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0]])

#target is previous qubit(control-1)
CX_prev = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]])

#map that maps gate names(strings) to corresponding unitaries(matrices)
gates = {
    'X': X,
    'Y': Y,
    'Z': Z,
    'H': H,
    'T': T
}


#function to initialize all states when Q[] is encountered
def initialiseStates(n):
    initialState = [0 for i in range(2**n)]
    initialState[0] = 1
    state = np.array(initialState, dtype=complex)
    return state


#Function to apply any single qubit gate passed as argument
def apply_single_qubit_gate(psi, num_qubits, n, gate):

    if n >= num_qubits or n < 0:
        raise Exception()

    U = [1]
    for i in range(num_qubits):
        if i == n:
            U = np.kron(gate, U)
        else:
            U = np.kron(I, U)
    
    psi = np.dot(U, psi)
    #print(U)
    return psi


#Function to apply CX gate
def apply_CX(psi, num_qubits, control, target):
    
    if target >= num_qubits or control >= num_qubits or target < 0 or control < 0 or abs(target - control > 1):
        raise Exception()
    
    U = [1]

    first_occurs = control
    CX = CX_next
    if target < control:
        first_occurs = target
        CX = CX_prev

    for i in range(0, num_qubits-1):
        if i == first_occurs:
            U = np.kron(CX, U)
        else:
            U = np.kron(I, U)
    
    psi = np.dot(U, psi)
    #print(U)
    return psi


#Function to measure a qubit
def measure_qubit(psi, n):
    
    if n >= num_qubits or n < 0:
        raise Exception()
        
    probability_of_1 = 0
    for i in range(1,len(psi)):
        if i%(2**n) == 0:
            probability_of_1 = probability_of_1 + abs(psi[i])**2

    #print("Probability of observing qubit {0} in state 1 is {1}".format(n, round(probability_of_1,3)))

    random_number = random.random()
    if random_number < probability_of_1:
        return 1
    return 0


#Helper functions

def display_state(psi, num_qubits):
    for i in range(len(psi)):
        if psi[i] == 0:
            continue
        state = '{0:b}'.format(int(i))
        state = state.zfill(num_qubits)
        print("({0} + {1}i) |{2}>".format(round(psi[i].real,3),round(psi[i].imag,3), state))
    print()

def check_valid(line):
    if len(line) != line.find(']')+1:
        return False
    return True

def error_occurred(line_number):
    print("Invalid syntax in line", line_number)
    quit()


#Driver code

filename = input("Enter the code file's name: ")
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, filename)
try:
    fhand = open(filename)
except:
    print("Can't open file!")
    quit()

line_number = 1
for line in fhand:
    line = line.rstrip()
    line = line.translate(line.maketrans('', '', ' \t\r'))
    valid = True

    #####

    # TODO: Try testing with Grover's search on 3 qubits
    # Handle CX for any target, control
    # Add Rx, Ry, Rz, SWAP gates
    
    #####

    if line[0] == 'Q':
        try:
            n = int(line[line.find('[')+1])
            psi = initialiseStates(n)
            num_qubits = n
            if not check_valid(line):
                raise Exception()
        except:
            error_occurred(line_number)
    

    elif line[0] in gates:
        try:
            n = int(line[line.find('[')+1])
            psi = apply_single_qubit_gate(psi, num_qubits, n, gates[line[0]])
            if not check_valid(line):
                raise Exception()
        except:
            error_occurred(line_number)


    elif line[0] == 'D':
        if len(line) != 1:
            error_occurred(line_number)
        print()
        print("The state of the qubits is : ")
        display_state(psi, num_qubits)
    

    elif line[0:2] == 'CX':
        try:
            control = int(line[line.find('[')+1])
            target = int(line[line.find(',')+1])
            psi = apply_CX(psi, num_qubits, control, target)
            if not check_valid(line):
                raise Exception()
        except:
            error_occurred(line_number)


    elif line[0:2] == 'MZ':
        try:
            n = int(line[line.find('[')+1])
            measurement_outcome = measure_qubit(psi, n)
            print("The qubit {0} collapsed to {1}".format(n, measurement_outcome))
            print()
            if not check_valid(line):
                raise Exception()
        except:
            error_occurred(line_number)

    else:
        error_occurred(line_number)
    
    line_number = line_number+1

    