import os
import csv
import sys
import re
import importlib
import networkx as nx

# settings
#curDir = 'E:/GitHub/bioinformatics-algorithms-1/week9'
curDir = 'D:/Copy/Coursera/Bioinformatics Algorithms (part-I)/MyPrograms/week9'
inputFile = './data/3.LongestRepeat-2.txt'
inputFile = 'C:/Users/Ashis/Downloads/dataset_295_8.txt'
outputFile = './results/3.LongestRepeat.txt'

# set current directory
os.chdir(curDir)

## read input
with open(inputFile) as f:
    inputs = f.readlines()

genome = inputs[0].strip() + '$'
#print(genome)
#print(patterns)

## build trie graph
g = nx.DiGraph()
g.add_node(1)     # add root with id 1

# two required function
neighborsWithLabelPrefix = lambda node, prefix: [e[1] for e in g.edges_iter(node, data=True) if genome[e[2]['labelIdx'][0]] == prefix]
getNewNode = lambda : len(g.nodes())+1

def longestCommonPrefix(str1, str2):
    n = min([len(str1), len(str2)])
    i = 0
    while i < n and str1[i]==str2[i]:
        i += 1

    prefix = str1[0:i]
    return prefix

#print(longestCommonPrefix('abc','ab'))

genomeLen = len(genome)
for idx in range(genomeLen):
    if idx % 100 == 0:
        print(idx)
    #p = genome[idx:]

    # traverse as long as pattern matches
    curNode = 1
    i = idx
    while(i < genomeLen):
        # find the edge with the first prefix character
        nextNode = neighborsWithLabelPrefix(curNode, genome[i])

        # if there is no edge with the first prefix character,
        # it must be a new edge with the rest of the string.
        if len(nextNode) == 0:
            newNode = getNewNode()
            g.add_edge(curNode, newNode, {'labelIdx':[i,genomeLen]})
            break

        # get the edge label
        nextNode = nextNode[0]
        edgeLabelIndices = g.edge[curNode][nextNode]['labelIdx']
        edgeLabel = genome[edgeLabelIndices[0]:edgeLabelIndices[1]]
        edgeLabelLen = len(edgeLabel) 

        # if the rest of the string starts with edgeLabel,
        # move to the next node
        if genome[i:i+edgeLabelLen] == edgeLabel:
            curNode = nextNode
            i += edgeLabelLen
        else:
            # edgeLabel matches partially
            prefix = longestCommonPrefix(genome[i:i+edgeLabelLen], edgeLabel)
            prefixLen = len(prefix)

            # create two new node, one intermediate, another for unmatched string
            intermediateNode = getNewNode()
            unmatchedNode = intermediateNode + 1

            # remove existing edge from curNode to nextNode
            g.remove_edge(curNode, nextNode)
            
            # add edge from curNode to intermediateNode
            g.add_edge(curNode, intermediateNode, {'labelIdx':(edgeLabelIndices[0],edgeLabelIndices[0]+prefixLen)})

            # add edge from intermediateNode to nextNode
            g.add_edge(intermediateNode, nextNode, {'labelIdx':(edgeLabelIndices[0]+prefixLen, edgeLabelIndices[1])})

            # add edge from intermediateNode to unmatchedNode
            g.add_edge(intermediateNode, unmatchedNode, {'labelIdx':(i+prefixLen, genomeLen)})
            
            break


## find the longest repeat
# traverse the tree in bfs manner and update string length at nodes
edges = nx.dfs_edges(g)
lengthAttr = 'length'
g.node[1][lengthAttr] = 0
for e in edges:
    if genome[g.edge[e[0]][e[1]]['labelIdx'][1]-1] == '$':
        g.node[e[1]][lengthAttr] = 0
    else:
        g.node[e[1]][lengthAttr] = g.node[e[0]][lengthAttr] + g.edge[e[0]][e[1]]['labelIdx'][1] - g.edge[e[0]][e[1]]['labelIdx'][0]

# find the max length node
lengths = [(n, g.node[n][lengthAttr]) for n in g.nodes()]
longestNode = max(lengths, key=lambda x:x[1])
print(longestNode)

# the path from the root to the longestNode is the longest repeat
path = nx.shortest_path(g, 1, longestNode[0])
edgeLabels = [genome[g.edge[path[i-1]][path[i]]['labelIdx'][0]:g.edge[path[i-1]][path[i]]['labelIdx'][1]] for i in range(1,len(path))]
longestRepeat = "".join(edgeLabels)
print(longestRepeat)

## output
with open(outputFile, "w") as f:
    f.writelines(longestRepeat)

print('done.')
