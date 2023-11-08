import numpy as np
from qiskit import QuantumCircuit
from qiskit import transpile 
from qiskit.providers.aer import AerSimulator

# In this state array, the +1 player is represented by a qubit |1>
# and the -1 player is represented by a qubit |0>. The boundaries
# are represented as |0>+|1> or |0>-|1>
def plusminus(state):
    if(state==0):
        return "00"
    if(state==1):
        return "+1"
    if(state==-1):
        return "-1"
    return ""

def print_states():
    print("{} ----- {} ----- {}".format(plusminus(states[0,0,0]), plusminus(states[0,0,1]), plusminus(states[0,0,2])))
    print("|  {} -- {} -- {} |".format(plusminus(states[1,0,0]), plusminus(states[1,0,1]), plusminus(states[1,0,2])))
    print("|  |  {} {} {} |  |".format(plusminus(states[2,0,0]), plusminus(states[2,0,1]), plusminus(states[2,0,2])))
    print("{} {} {}    {} {} {}".format(plusminus(states[0,1,0]), plusminus(states[1,1,0]), plusminus(states[2,1,0]), plusminus(states[2,1,2]), plusminus(states[1,1,2]), plusminus(states[0,1,2])))
    print("|  |  {} {} {} |  |".format(plusminus(states[2,2,0]), plusminus(states[2,2,1]), plusminus(states[2,2,2])))
    print("|  {} -- {} -- {} |".format(plusminus(states[1,2,0]), plusminus(states[1,2,1]), plusminus(states[1,2,2])))
    print("{} ----- {} ----- {}".format(plusminus(states[0,2,0]), plusminus(states[0,2,1]), plusminus(states[0,2,2])))

def set_state(tup,value):
    states[tup[0],tup[1],tup[2]] = value

def get_state(tup):
    return states[tup[0],tup[1],tup[2]]

def get_input():
    while True:
        try:
            x = int(input("Enter the ring level (0-2): "))
            y = int(input("Enter the row (0-2): "))
            z = int(input("Enter the column (0-2):"))

            if 0 <= x <= 2 and 0 <= y <= 2 and 0 <= z <= 2:
                return x, y, z
            else:
                print("Coordinates must be between 0 and 2. Please try again.")
        except ValueError:
            print("Invalid input. Please enter integers between 0 and 2.")

def entangle(tups):
    #Use a set to keep track of qubits that are duplicate
    locations = []
    qubit = 0
    circ = QuantumCircuit(4)
    #Apply bit flips to 's to differentiate from zeros, add h for even qubits, and cnot for odd qubits
    for i in range(4):
        if(tups[i] not in locations):
            locations.append(tups[i])
            if(get_state(tups[i])==1):#Apply bit flip to +1
                circ.x(qubit)
            if(get_state(tups[i])==0):#Apply H to 0 as boundary
               circ.h(qubit)
            if(i%2==0):#Even qubits
                circ.h(qubit)
            else:#Odd qubits
                circ.cx(qubit-1,qubit)
            qubit = qubit + 1
        else:#Apply duplicate tup to existing qubit in location
            for j in range(qubit):
                if(tups[i]==locations[j]):
                    if(i%2==0):
                        circ.h(j)
                    else:
                        circ.cx(qubit,j)
    meas = QuantumCircuit(qubit, qubit)
    meas.barrier(range(qubit))
    # map the quantum measurement to the classical bits
    meas.measure(range(qubit), range(qubit))

    # The Qiskit circuit object supports composition.
    # Here the meas has to be first and front=True (putting it before) 
    # as compose must put a smaller circuit into a larger one.
    qc = meas.compose(circ, range(qubit), front=True)
    # Adding the transpiler to reduce the circuit to QASM instructions
    # supported by the backend

    # Use AerSimulator

    backend = AerSimulator()

    # First we have to transpile the quantum circuit 
    # to the low-level QASM instructions used by the 
    # backend
    qc_compiled = transpile(qc, backend)

    # Execute the circuit on the qasm simulator.
    # We've set the number of repeats of the circuit
    # to be 1024, which is the default.
    job_sim = backend.run(qc_compiled, shots=1024)

    # Grab the results from the job.
    result_sim = job_sim.result()
    counts = result_sim.get_counts(qc_compiled)
    print(counts)
    result = max(counts, key=lambda key: counts[key])
    for i in range(qubit):
        if(result[i]=="1"):
            set_state(locations[i],1)
        else:
            set_state(locations[i],-1)
    
def check_win():
    #Break algorithm into rings and check 4 sides, and in separate loop check 4 cross rings
    for i in range(3):
        triples = [0,0,0,0]
        for j in range(2):
            triples[j*2] = get_state((i,2*j,0))+get_state((i,2*j,1))+get_state((i,2*j,2))
            triples[j*2+1] = get_state((i,0,2*j))+get_state((i,1,2*j))+get_state((i,2,2*j))
        if(3 in triples):
            print("Player +1 wins")
        if(-3 in triples):
            print("Player -1 wins")
    #Cross ring check
    triples = [0,0,0,0]
    for j in range(2):
        triples[j*2] = get_state((0,1,2*j))+get_state((1,1,2*j))+get_state((2,1,2*j))
        triples[j*2+1] = get_state((0,2*j,1))+get_state((1,2*j,1))+get_state((2,2*j,1))
    if(3 in triples):
        print("Player +1 wins")
    if(-3 in triples):
        print("Player -1 wins")


def piece_input():
    player = 1
    for turn in range(18):#Change to 18
        print_states()
        print("Player ",player, "'s turn")
        tup = get_input()
        set_state(tup,player)
        player = -player
        check_win()

def gate_input():
    player = 1
    tups = []
    #Let a rule be each turn you get to choose two qubits to entangle
    for turn in range(9):#Change to 9
        print_states()
        print("Player ",player, "'s turn")
        print("Input two qubits to entangle")
        tups.append(get_input())
        tups.append(get_input())
        player = -player
        print("Player ",player, "'s turn")
        print("Input two qubits to entangle")
        tups.append(get_input())
        tups.append(get_input())
        player = -player
        entangle(tups)
        check_win()

#Start of the program
states = np.zeros((3, 3, 3))
piece_input()
gate_input()

#Initialize game board as example
#set_state((0,0,0),1)
#set_state((0,0,1),-1)
#set_state((0,0,2),1)
#set_state((1,0,1),-1)
#set_state((2,0,1),-1)

print_states()
print("Game over")