from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, transpile
from qiskit.tools.visualization import circuit_drawer
from qiskit.quantum_info import state_fidelity
from qiskit import BasicAer

backend = BasicAer.get_backend('unitary_simulator')
position = [
            [0,0,0],
            [0,0,0],
            [0,0,0],
         [0,0,0,0,0,0], #layout of board
            [0,0,0],
            [0,0,0],
            [0,0,0]]

#gates = n x (no. of gates per round) matrix
# or
#gates = n x (no. of gates allowed on board at a time) 
    #old on left, new on right
    #cnot, bit flip, hadamard

def QuantumCreate(n, gates):
    q_b = QuantumRegister(n, name='qb')
    c_b = ClassicalRegister(n)
    circuit = QuantumCircuit(q_b, c_b)
    circuit.draw(output='mpl')
    control = -1
    target = -1
    N = 0
    
    for n in gates:
        for m in n:
            if m==1: #Bit Flip
                circuit.x(q_b[N])
                circuit.barrier(q_b)
            elif m==2: #Hadamard
                circuit.h(q_b[N])
                circuit.barrier(q_b)
            elif m==3: #CNOT control qbit
                control = N
            elif m==4: #CNOT target qbit
                target = N
            
            if (control != -1) & (target != -1):
                circuit.cx(q_b[control], q_b[target])
                circuit.barrier(q_b)
        N += 1
        
    circuit.measure(q_b, c_b)
    return circuit.draw(output='mpl')
#    print(control, target)
    
    
testGate = [
            [1,0,0],
            [0,0,0],
            [0,2,0],
            [0,0,0],
            [0,0,3],
            [0,0,4]]
QuantumCreate(6, testGate)
