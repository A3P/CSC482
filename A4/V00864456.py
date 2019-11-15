import numpy as np
import math
import sys

seq=""
high={"H": 0.5, "L": 0.5, "A": 0.2, "C": 0.3, "G": 0.3, "T": 0.2}
low={"H": 0.4, "L": 0.6, "A": 0.3, "C": 0.2, "G": 0.2, "T": 0.3}
highLog={"H": math.log(0.5, 2), "L": math.log(0.5, 2), "A": math.log(0.2, 2), "C": math.log(0.3, 2), "G": math.log(0.3, 2), "T": math.log(0.2, 2)}
lowLog={"H": math.log(0.4, 2), "L": math.log(0.6, 2), "A": math.log(0.3, 2), "C": math.log(0.2, 2), "G": math.log(0.2, 2), "T": math.log(0.3, 2)}
pStart = 0.5
pStartLog= math.log(pStart, 2)

# Read sequences from input and store them
with open(sys.argv[1]) as f:
    f.readline()
    seq = f.readline().strip()


matrix = np.zeros([2, len(seq)])
parent = np.zeros([2, len(seq)], dtype=int)


# Calculates the value in the matrix using the HMM and the input sequence
if(len(seq) > 0):
    matrix[0,0] = pStart*high[seq[0]]
    matrix[1,0] = pStart*low[seq[0]]

for i in range(1, len(seq)):
    matrix[0,i] = matrix[0,i-1]*high["H"]*high[seq[i]] + matrix[1,i-1]*low["H"]*high[seq[i]]
    matrix[1,i] = matrix[1,i-1]*low["L"]*low[seq[i]] + matrix[0,i-1]*high["L"]*low[seq[i]] 


matrixLog = np.zeros([2, len(seq)])
# Calculates the value in the matrix using the HMM and the input sequence using the log base 2.
if(len(seq) > 0):
    matrixLog[0,0] = round(pStartLog + highLog[seq[0]], 2)
    matrixLog[1,0] = round(pStartLog + lowLog[seq[0]], 2)

for i in range(1, len(seq)):
    matrixLog[0,i] = round(highLog[seq[i]] + max(matrixLog[0,i-1] + highLog["H"], matrixLog[1,i-1] + lowLog["H"]), 2)
    if((matrixLog[0,i-1] + highLog["H"]) == matrixLog[1,i-1] + lowLog["H"]):
        parent[0,i] = 2
    elif((matrixLog[0,i-1] + highLog["H"]) > matrixLog[1,i-1] + lowLog["H"]):
        parent[0,i] = 0
    else:
        parent[0,i] = 1

    matrixLog[1,i] = round(lowLog[seq[i]] + max(matrixLog[0,i-1] + highLog["L"], matrixLog[1,i-1] + lowLog["L"]), 2)
    if((matrixLog[0,i-1] + highLog["L"]) == (matrixLog[1,i-1] + lowLog["L"])):
        parent[1,i] = 2
    elif((matrixLog[0,i-1] + highLog["L"]) > (matrixLog[1,i-1] + lowLog["L"])):
        parent[1,i] = 0
    else:
        parent[1,i] = 1

# Output for 3.o1
f1 = open("4.o1", "w+")
f1.write('{:.2e}'.format(matrix[0,-1] + matrix[1,-1]))
f1.close()

f2 = open("4.o2", "w+")

# Iterates over all rows of the matrix and writes it to the output file
header="- 0"
zeroes = "0 1"
rowH= "H 0"
rowL= "L 0"
for i in range(len(seq)):
    header += " " + seq[i]
    zeroes+= " 0"
    rowH+= " " + str(round(matrixLog[0,i],2))
    rowL+= " " + str(round(matrixLog[1,i],2))
    
f2.write(header+"\n")
f2.write(zeroes+"\n")
f2.write(rowH+"\n")
f2.write(rowL+"\n")
f2.close()

# Becomes yes if multiple paths are found during the backtrack.
multiplePaths="NO"

# Outputs the path by backtracking from the highest value in the last indices of the matrix
f3 = open("4.o3", "w+")
path=""
row=1
if(matrixLog[0,-1] == matrixLog[1,-1]):
    row=0
    multiplePaths="YES"
elif(matrixLog[0,-1] > matrixLog[1,-1]):
    row=0
column=len(seq)-1
while(column >= 0):
    if(row==0):
        path+="H"
    else:
        path+="L"
    row = parent[row,column]
    if(row==2):
        multiplePaths="YES"
        row = 0
    column -= 1

f3.write(''.join(reversed(path))+"\n")
f3.close()

# Outputs the probabilty of the most probable path by using the higher value of the last index in the H and L rows.
f4 = open("4.o4", "w+")
if(matrixLog[0,-1] > matrixLog[1,-1]):
    f4.write('{:.2e}'.format(pow(2,matrixLog[0,-1])))
else:
    f4.write('{:.2e}'.format(pow(2,matrixLog[1,-1])))
f4.write("\n")
f4.close()

# States if there are multiple paths.
f5 = open("4.o5", "w+")
f5.write(multiplePaths+"\n")
f5.close()

# Calculates the Posterior Probability
f6 = open("4.o6", "w+")
f6.write('{:.2e}'.format(matrix[0,3] / (matrix[0,3] + matrix[1,3])) + "\n" )
f6.write( "\n" + '{:.2e}'.format(matrix[1,3] / (matrix[0,3] + matrix[1,3])) + "\n" )
f6.close()

