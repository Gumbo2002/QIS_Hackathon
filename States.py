
class ThreeDArray:
    def __init__(self):
        self.array = [[[0] * 3 for _ in range(3)] for _ in range(3)]

    def set_element(self, x, y, z, value):
        if 0 <= x < 3 and 0 <= y < 3 and 0 <= z < 3:
            self.array[x][y][z] = value
        else:
            print("Invalid coordinates")

    def get_element(self, x, y, z):
        if 0 <= x < 3 and 0 <= y < 3 and 0 <= z < 3:
            return self.array[x][y][z]
        else:
            print("Invalid coordinates")
            return None

class GateQueue:
    def __init__(self):
        self.queue = []

    def add_gate(self, gate_function):
        self.queue.append(gate_function)

    def execute_gates(self):
        for gate in self.queue:
            gate()

def Hadamard():
    #Placeholder for circuit builder
    print("Hadamard")

def CNOT():
    #Placeholder for circuit builder
    print("Cnot")

def NOT():
    #Placeholder for circuit builder
    print("Not")


queue = GateQueue()
states = ThreeDArray()
states.set_element(0,0,1,"|1>")
queue.add_gate(Hadamard)
queue.execute_gates()
