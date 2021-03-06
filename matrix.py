'''
@author: Josh Payne

Description: For generating graphs, converting adjacency/Laplacian matrices into PauliSums
'''

import random
import math
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from pyquil.paulis import PauliSum, sX, sZ, sI
from pyquil import unitary_tools
from networkx.drawing.nx_agraph import graphviz_layout
import copy

c_1 = lambda n: 0.5*(sI(n)+sZ(n))
c_2 = lambda n: 0.5*(sX(n)+(sZ(n)*sX(n)))
c_3 = lambda n: 0.5*(sX(n)-(sZ(n)*sX(n)))
c_4 = lambda n: 0.5*(sI(n)-sZ(n))

def pauliBuilder(matrix) -> PauliSum:
    n = math.ceil(math.log2(matrix.shape[0]))-1
    if matrix.shape == (2,2):
        if str(matrix)==str(np.matrix('0 0; 0 0')): return sI(n) - sI(n)
        if str(matrix)==str(np.matrix('1 0; 0 1')): return sI(n)
        if str(matrix)==str(np.matrix('0 1; 1 0')): return sX(n)
        if str(matrix)==str(np.matrix('1 1; 1 1')): return sX(n)+sI(n)

        if str(matrix)==str(np.matrix('1 0; 0 0')): return c_1(n)
        if str(matrix)==str(np.matrix('0 1; 0 0')): return c_2(n)
        if str(matrix)==str(np.matrix('0 0; 1 0')): return c_3(n)
        if str(matrix)==str(np.matrix('0 0; 0 1')): return c_4(n)

        if str(matrix)==str(np.matrix('1 1; 0 0')): return c_1(n) + c_2(n)
        if str(matrix)==str(np.matrix('0 1; 0 1')): return c_2(n) + c_4(n)
        if str(matrix)==str(np.matrix('1 0; 1 0')): return c_1(n) + c_3(n)
        if str(matrix)==str(np.matrix('0 0; 1 1')): return c_3(n) + c_4(n)

        if str(matrix)==str(np.matrix('1 1; 1 0')): return c_1(n) + sX(n)
        if str(matrix)==str(np.matrix('1 1; 0 1')): return sI(n) + c_2(n)
        if str(matrix)==str(np.matrix('1 0; 1 1')): return sI(n) + c_3(n)
        if str(matrix)==str(np.matrix('0 1; 1 1')): return sX(n) + c_4(n)
    else:
        dim = matrix.shape[0]
        
        Adjacency_A, Adjacency_B, Adjacency_C, Adjacency_D = matrix[:int(dim/2), :int(dim/2)], \
                                                             matrix[:int(dim/2), int(dim/2):], \
                                                             matrix[int(dim/2):, :int(dim/2)], \
                                                             matrix[int(dim/2):, int(dim/2):]
        Pauli_A = c_1(n)*pauliBuilder(Adjacency_A)
        Pauli_B = c_2(n)*pauliBuilder(Adjacency_B)
        Pauli_C = c_3(n)*pauliBuilder(Adjacency_C)
        Pauli_D = c_4(n)*pauliBuilder(Adjacency_D)
        return Pauli_A + Pauli_B + Pauli_C + Pauli_D

def undirectedAdjacencyConstruct(size,show,density):
    nearest_power = math.ceil(math.log2(size))
    test_adjacency = np.zeros((2**nearest_power,2**nearest_power)).astype(int)
    
    for i in range(size):
        for j in range(i,size):
            if i!=j:
                if random.uniform(0, 1) < density:
                    test_adjacency[i][j] = 1
                    test_adjacency[j][i] = 1
    if (show):
        G = nx.from_numpy_matrix(test_adjacency)
        nx.draw(G, cmap = plt.get_cmap('jet'))
        plt.show()
    print(test_adjacency)
    return test_adjacency

def directedAdjacencyConstruct(size,show,density):
    nearest_power = math.ceil(math.log2(size))
    test_adjacency = np.zeros((2**nearest_power,2**nearest_power)).astype(int)
    for i in range(size):
        for j in range(size):
            if i!=j:
                if random.uniform(0, 1) < density:
                    test_adjacency[i][j] = 1
    if (show):
        G = nx.from_numpy_matrix(test_adjacency,create_using=nx.DiGraph())
        nx.draw(G, cmap = plt.get_cmap('jet'), arrows=True)
        plt.show()
    print(test_adjacency)
    return test_adjacency

def undirectedLaplacianConstruct(size,show,density):
    nearest_power = math.ceil(math.log2(size))
    test_laplacian = np.zeros((2**nearest_power,2**nearest_power)).astype(int)
    
    for i in range(size):
        for j in range(i,size):
            if i!=j:
                if random.uniform(0, 1) < density:
                    test_laplacian[i][j] = 1
                    test_laplacian[j][i] = 1
    if (show):
        G = nx.from_numpy_matrix(test_laplacian)
        nx.draw(G, cmap = plt.get_cmap('jet'))
        plt.show()
    test_laplacian*= -1
    for i in range(size):
        test_laplacian[i][i] = -1*sum(test_laplacian[i])
    print(test_laplacian)
    return test_laplacian

def directedOutDegreeLaplacianConstruct(size,show,density):
    nearest_power = math.ceil(math.log2(size))
    test_laplacian = np.zeros((2**nearest_power,2**nearest_power)).astype(int)
    
    for i in range(size):
        for j in range(size):
            if i!=j:
                if random.uniform(0, 1) < density:
                    test_laplacian[i][j] = 1
    if (show):
        G = nx.from_numpy_matrix(test_laplacian,create_using=nx.DiGraph())
        nx.draw(G, cmap = plt.get_cmap('jet'), arrows=True)
        plt.show()
    test_laplacian*= -1
    for i in range(size):
        test_laplacian[i][i] = -1*sum(test_laplacian[i])
    print(test_laplacian)
    return test_laplacian

def directedInDegreeLaplacianConstruct(size,show,density):
    nearest_power = math.ceil(math.log2(size))
    test_laplacian = np.zeros((2**nearest_power,2**nearest_power)).astype(int)
    
    for i in range(size):
        for j in range(size):
            if i!=j:
                if random.uniform(0, 1) < density:
                    test_laplacian[i][j] = 1
    if (show):
        G = nx.from_numpy_matrix(test_laplacian,create_using=nx.DiGraph())
        nx.draw(G, cmap = plt.get_cmap('jet'), arrows=True)
        plt.show()
    test_laplacian*= -1
    for i in range(size):
        test_laplacian[i][i] = -1*sum([test_laplacian[j][i] for j in range(size)])
    print(test_laplacian)
    return test_laplacian

def laplacianPauliBuilder(laplacian_matrix) -> PauliSum:
    adjacency_representation = copy.copy(laplacian_matrix)
    for i in range(adjacency_representation.shape[0]):
        adjacency_representation[i][i] = 0
    adjacency_representation *= -1
    laplacian_pauli = -1*pauliBuilder(adjacency_representation)
    for i in range(laplacian_matrix.shape[0]):
        deg_matrix = np.zeros(laplacian_matrix.shape).astype(int)
        deg_matrix[i][i] = 1
        deg_pauli = int(laplacian_matrix[i][i])*pauliBuilder(deg_matrix)
        laplacian_pauli+=deg_pauli
    return laplacian_pauli

### Test/debug down here ###


# test_adjacency = np.matrix('0 0 0 1; \
#                             0 0 1 1; \
#                             0 1 0 0; \
#                             1 1 0 0')

# print(laplacianPauliBuilder(directedInDegreeLaplacianConstruct(8,True,0.5)),range(3))