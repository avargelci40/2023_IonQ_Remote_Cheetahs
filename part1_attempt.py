# Team Name: Cheetahs
# Task Number: Part 1
# Point Person: Shwetlana Jha

import qiskit
import numpy as np
import os
import json
import pathlib

from qiskit.tools.visualization import plot_bloch_multivector
from qiskit.tools.visualization import plot_histogram
from qiskit import *


files=os.listdir("mock_data")
dataset=list()
for file in files:
    if pathlib.Path(file).suffix == ".json":
        with open('mock_data/'+file, "r") as infile:
            loaded = json.load(infile)
            dataset.append(loaded)

# Test images
dataset.append({'image': [[1, 0], [1, 1], [1, 1]]})
dataset.append({'image': [[1, 0], [0, 1]]})
                
def encode_qiskit(image, length):
    q = qiskit.QuantumRegister(length) # Qbits = Num of Sublists
    c = qiskit.ClassicalRegister(length) #Cbits = Qbits
    circuit = qiskit.QuantumCircuit(q, c)
    
    # Four possibilities: [0, 0], [0, 1], [1, 0], or [1, 1], |0>, |+>, |->, |1>
    for i in range(length):
        if image[i] == [0, 0]:
            pass
        elif image[i] == [1, 0]:
            circuit.h(i)
        elif image[i] == [0, 1]:
            circuit.x(i)
            circuit.h(i)
        elif image[i] == [1, 1]:
            circuit.x(i)
        
    return circuit

test_image = dataset[3]['image']

print(test_image)
#print(encode_qiskit(test_image, len(test_image)))


def circuit_to_statevector(circuit):
    simulator = Aer.get_backend('statevector_simulator')
    result = execute(circuit, backend = simulator).result()
    statevector = result.get_statevector()
    
    return statevector

    
statevector_test = circuit_to_statevector(encode_qiskit(test_image, len(test_image)))
print(statevector_test)

def statevector_to_hist(statevector):
    histogram = dict()
    for i in range(len(statevector)):
        population = abs(statevector[i]) ** 2
        histogram[bin(i)] = population
            
    return histogram

print(statevector_test)
hist = statevector_to_hist(statevector_test)
print(hist)
    
def decode(statevector):
    image = []
    
    for i in range(len(statevector)):
        if statevector[0] == 1:
            image = [[0, 0], [0, 0]]
        if statevector[-1] == 1:
            image = [[1, 1], [1, 1]]
            
    return image
            

# Step 1 is loading data into a list or whatever
# - Unique json files

# Step 2 is being able to convert a unique string of 0's and 1's into a unique qcircuit
# - Will produce a unique histogram

# Step 3 is being able to decrypt, so going backwards, histogram --> image

# 0, 0, 1, 0 ==> |10>

# 0, 0, 0, 0, 0, 1, 0, 0 ==>
