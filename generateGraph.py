#! /usr/bin/env python3

components = {}

currId = 0
nodeMap = {}

def addStation(id, prevId, nextId):

    #if prevId in null skip it
    if prevId is not None:
        if id not in components.keys():
            components[id] = {}
        components[id][prevId] = -1

    #if nextId is null skip it
    if nextId is not None:
        if id not in components.keys():
            components[id] = {}
        components[id][nextId] = 1

    global currId
    nodeMap[id] = currId
    currId = currId + 1
    
    
def addSwitch(id, prevId, nextId, nextId2):
    #Validate the input
    if id is None or prevId is None or nextId is None or nextId2 is None:
        raise TypeError("All arguments must be not None")

    if id not in components.keys():
        components[id] = {}
    if prevId not in components.keys():
        components[prevId] = {}

    components[id][nextId] = 1
    components[id][nextId2] = 1
    components[id][prevId] = -1
    components[prevId][id] = 1

    global currId
    nodeMap[id] = currId
    currId = currId + 1

    
addStation("A", None, None)
addStation("B", None, None)
addStation("C", None, None)
print(components)
addSwitch("S1", "A", "S2","S3")
addSwitch("S2", "C", "S1","S3")
addSwitch("S3", "B", "S1","S2")

print(components)


# Generate one of the adjacancy matrices
# Get a place to start

print(nodeMap)    

# Create blank adj map
adj = []
adjBack = []
for i in range(currId):
    adj.append([0 for i in range(currId)])
    adjBack.append([0 for i in range(currId)])

# Look at each node in the list
for id in nodeMap.keys():
    
    #Get all of its neighbors fill in matrix
    for neighbor in components[id].keys():
        if components[id][neighbor] == 1 :
            adj[nodeMap[id]][nodeMap[neighbor]] = 1
        else:
            adjBack[nodeMap[id]][nodeMap[neighbor]] = 1



# Print the matrx
for row in adj:
    for val in row:
        print(val, end=",")
    print()

print()
for row in adjBack:
    for val in row:
        print(val, end=",")
    print()
