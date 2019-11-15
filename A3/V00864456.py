import numpy as np
import math
import sys

# Returns the distance of 2 sequences
def getDistance(i,j):
    distance = 0
    for c in range(len(i)):
        if(i[c]!=j[c]):
            distance+=1
    return distance

# Finds the clusters with the least distance between them
def findClosest():
    closest = []
    minimum = math.inf
    for i in range(len(clusterNames)):
        for j in range(i+1, len(clusterNames)):
            # Will keep track of more than 2 clusters if multiple equal minimum distances are found.
            if(minimum >= clusters[i][j]):
                if(minimum == clusters[i][j]):
                    closest.append((i,j))
                else:
                    closest = [(i,j)]
                    minimum = clusters[i][j]
    return closest

# Updates the value in the clusters and keeps track of changes such as matrix row names, nodes, and descendants
def updateClusters(clusters, i,j):
    for x in range(len(clusterNames)):
        if(x != i and x != j):
            dkx = (clusters[i][x] * clusterNames[i][1]) + (clusters[j][x] * clusterNames[j][1])
            dkx /= (clusterNames[i][1]) + (clusterNames[j][1])
            # cluster i is overwritten with new cluster k instead of deleting both i and j
            dkx = round(dkx,1)
            clusters[i][x] = dkx
            clusters[x][i] = dkx
    childs[getClusterName(i,j)] = (clusterNames[i][0], clusterNames[j][0])
    descendants = [] + clusterNames[i][2] + clusterNames[j][2]
    clusterNames[i] = (getClusterName(i,j), clusterNames[i][1] + clusterNames[j][1], descendants)
    # j is removed from the clusters
    clusterNames.pop(j)
    return np.delete( np.delete(clusters, j, 0), j, 1)
    
# Gets the new cluster name based on the two merged clusters
def getClusterName(i,j):
    return clusterNames[i][0] + clusterNames[j][0][1:]

# Recursively creates the tree working its way back to the root
def getTree(root):
    output=""
    if root in childs and root in heights:
        
        output += "(" + childs[root][0] + ":"
        if childs[root][0] in childs:
            output += str( round(heights[root] - heights[childs[root][0]], 1) ) + "(" + getTree(childs[root][0]) + ")"
        else:
            output += str(heights[root])
        output += ")"

        output += "(" + childs[root][1] + ":"
        if childs[root][1] in childs:
            output += str( round(heights[root] - heights[childs[root][1]], 1) ) + "(" + getTree(childs[root][1]) + ")"
        else:
            output += str(heights[root])
        output += ")"
    return output

# Assigns the height of the node
def setHeight(i,j):
    # heights[getClusterName(i,j)] = round(clusters[i][j]/2, 1)
    totalDistance=0
    for x in clusterNames[i][2]:
        for y in clusterNames[j][2]:
            totalDistance += matrix[x][y]
    heights[getClusterName(i,j)] = round(totalDistance/ ( 2 * (len(clusterNames[i][2])*len(clusterNames[j][2]))), 1)


# Keeps track of the sequences
sequences = []
# Keeps track of the cluster names and the sequences within the cluster
clusterNames = []
multipleTrees="NO"

# Read sequences from input and store them
with open(sys.argv[1]) as f:
    seq = f.readline().strip()
    while(len(seq)>0 and seq[0]==">"):
        sequences.append((seq[1:], f.readline().strip()))
        clusterNames.append((seq[1:], 1, [len(clusterNames)] ))
        seq = f.readline().strip()

# print(sequences)

# pairwise distance matrix
matrix = np.zeros([len(sequences), len(sequences)])

# Calculates the pairwise distance of all pairs
for i in range(len(sequences)):
    for j in range(i+1,len(sequences)):
        matrix[i,j] = getDistance(sequences[i][1], sequences[j][1])
        matrix[j,i] = matrix[i,j]

# Output for 3.o1
f1 = open("3.o1", "w+")
header = "-\t"
for i in range(len(sequences)):
    header += (sequences[i][0])
    if i < (len(sequences)-1):
        header+=" "
header+="\n"
f1.write(header)

# Iterates over all rows of the matrix and writes it to the output file
for i in range(len(sequences)):
    row=sequences[i][0]
    for j in range(len(sequences)):
        row += " " + str(int(matrix[i,j]))
    row += "\n"
    f1.write(row)
f1.close()
    
# print(matrix)

clusters = np.copy(matrix)
tree = ""
heights={}
childs={}

while(len(clusterNames)>1):
    closestList = findClosest()
    if(len(closestList)>1):
        multipleTrees="YES"
    # print("closestList: " + str(closestList))
    setHeight(closestList[0][0], closestList[0][1])
    # print("heights: " + str(heights))

    clusters = updateClusters(clusters, closestList[0][0], closestList[0][1])
    # print("clusters:\n"+ str(clusters))
    # print("childs: " + str(childs))
    # print("cluster names: " + str(clusterNames))

f2 = open("3.o2", "w+")
f2.write(clusterNames[0][0] + getTree(clusterNames[0][0]))
f2.close()

f3 = open("3.o3", "w+")
f3.write(multipleTrees)
f3.close()