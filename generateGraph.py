#! /usr/bin/env python3
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

components = {}
visited = []
curCnt = 0
nodeMap = {}
labels = []

maxDepth = 100
depth = 0

def addStation(id):
    global curCnt
    nodeMap[id] = curCnt
    labels.append(id)
    components[id] = {}
    curCnt = curCnt + 1
    
    
def addSwitch(id, prevId, nextId, nextId2):
    #Validate the input
    if id is None or prevId is None or nextId is None or nextId2 is None:
        raise TypeError("All arguments must be not None")

    if id not in components.keys():
        components[id] = {}
    if prevId not in components.keys():
        components[prevId] = {}
    if nextId not in components.keys():
        components[nextId] = {}
    if nextId2 not in components.keys():
        components[nextId2] = {}

    components[id][nextId] = 1
    components[id][nextId2] = 1
    components[id][prevId] = -1

    # Only if it isn't filled already
    if id not in components[prevId].keys():
        components[prevId][id] = 1
    if id not in components[nextId].keys():
        components[nextId][id] = -1
    if id not in components[nextId2].keys():
        components[nextId2][id] = -1

    global curCnt
    nodeMap[id] = curCnt
    labels.append(id)
    curCnt = curCnt + 1

def genAdj(startId):
    global visited
    visited = [0 for i in range(curCnt)]

    adj = []
    for i in range(curCnt):
        adj.append([0 for i in range(curCnt)])

    return examineNeighbor(startId, adj)

# Recursive function, the default value searches all possible paths
def examineNeighbor(rootId, adj, sign = 0):
    # Check on global depth
    """
    global depth
    global maxDepth
    if depth > maxDepth:
        return adj
    depth = depth + 1
    """

    # Expose the list of visited nodes, and update
    global visited
    visited[nodeMap[rootId]] = 1
    print("Visiting %s with sign %d" % (rootId, sign))
    
    #print("Looking from %s for sign %d" % (rootId, sign) )

    # Look for the neighbors of opposite sign that haven't been visited
    for neighbor in components[rootId].keys():
        # If we found a valid neighbor travel there and look for its neighbors
        if sign != components[rootId][neighbor] and visited[nodeMap[neighbor]] == 0:
            adj[nodeMap[rootId]][nodeMap[neighbor]] = 1
            adj = examineNeighbor(neighbor, adj, components[neighbor][rootId])

    # Return the adj matrix
    return adj
    
def genLabelDict(labels):
    retDict = {}
    for i in range(len(labels)):
        retDict[i] = labels[i]
    return retDict

def showGraph(adjMatrix, myLabels):
    rows, cols = np.where(np.asarray(adjMatrix) == 1)
    edges = zip(rows.tolist(), cols.tolist())
    gr = nx.DiGraph()
    gr.add_edges_from(edges)
    nx.draw(gr, node_size=500, labels=genLabelDict(myLabels), with_labels=True)
    plt.show()

def showGraph(adjMatrix):
    rows, cols = np.where(np.asarray(adjMatrix) == 1)
    edges = zip(rows.tolist(), cols.tolist())
    gr = nx.DiGraph()
    gr.add_edges_from(edges)
    nx.draw(gr, node_size=500)
    plt.show()

addStation("A")
addStation("B")
addStation("C")
addStation("D")

addSwitch("S1", "A", "S2", "S3")
addSwitch("S2", "B", "S1", "S4")
addSwitch("S3", "S5", "S1", "S4")
addSwitch("S4", "S5", "S2", "S3")
addSwitch("S5", "S6", "S4", "S3")
addSwitch("S6", "S5", "D", "C")

print(components.keys())
print(components)
adj = genAdj("C")

for row in adj:
    for val in row:
        print(val, end=",")
    print()
print(genLabelDict(labels))
showGraph(adj)
