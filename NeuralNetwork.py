import random
import math

class Node:
  def __init__(self, num, connections, activation, value, biasWeight):
    self.num = num
    self.connections = connections
    self.activation = activation
    self.value = value
    self.biasWeight = biasWeight
    self.connected = []

class Connection:
  def __init__(self, weight, edge):
    self.weight = weight
    self.edge = edge

def cost(net, goal):
  return (goal-net)**2

def costDerive(net, goal):
  return 2 * (goal-net)

def linear(z):
  return(z)

def linearDerive(z):
  return(1)

def sig(z):
  
  return (1/(1+math.exp(-z)))

def sigDerive(z):
  return sig(z)*(1-sig(z))

def relu(z):
  if z < 0:
    z = 0
  return z

def reluDerive(z):
  if z < 0:
    z = 0
  else:
    z = 1
  return z

def connectedFinder():
  for i in range(len(Nodes)):
    
    for o in range(len(Nodes[i].connections)):
      Nodes[i].connections[o].otherEdge = i
      Nodes[Nodes[i].connections[o].edge].connected.append(Nodes[i].connections[o])
      
def weightNumMaker():
  counter = 0
  for i in range(len(Nodes)):
    Nodes[i].biasWeightNum = counter
    counter += 1
    for o in range(len(Nodes[i].connections)):
      Nodes[i].connections[o].weightNum = counter
      counter += 1
  return counter
  
def funcFinder(string, value):
  if string == "linear":
    return linear(value)
  if string == "sig":
    return sig(value)
  if string == "relu":
    return relu(value)

def funcDeriveFinder(string, value):
  if string == "linear":
    return linearDerive(value)
  if string == "sig":
    return sigDerive(value)
  if string == "relu":
    return reluDerive(value)

def runAvailableNodes(Nodes,sums,OtherEdgesSum,Completed):
  for i in range(len(Nodes)):
    if NumOtherEdges[i] == OtherEdgesSum[i] and (Completed[i] != True):
      Completed[i] = True
      for o in range(len(Nodes[i].connections)):
        sums[Nodes[i].connections[o].edge] += (Nodes[i].value * Nodes[i].connections[o].weight)
        OtherEdgesSum[Nodes[i].connections[o].edge] += 1

def activateActivationFuncs(sums, OtherEdgesSum):
  for i in range(len(Nodes)):
    try: InputNodes[i]
    except:
      if OtherEdgesSum[i] == NumOtherEdges[i]:
        Nodes[i].value = funcFinder(Nodes[i].activation,(sums[i] + (B * Nodes[i].biasWeight)))
        Nodes[i].sum = (sums[i] + (B * Nodes[i].biasWeight))
  
def feedForward(inputs):
  sums = {}
  OtherEdgesSum = {}
  Completed = {}
  
  for i in range(len(Nodes)):
    sums[i] = 0
    OtherEdgesSum[i] = 0
    Completed[i] = False
  
  for i in range(len(InputNodes)):
    InputNodes[i].value = inputs[i]
    sums[i] = inputs[i]
    InputNodes[i].sum = inputs[i]

  for i in range(len(InputNodes)):
    runAvailableNodes(InputNodes, sums, OtherEdgesSum, Completed)
    activateActivationFuncs(sums, OtherEdgesSum)

  for i in range(len(Nodes)-1):
    runAvailableNodes(Nodes, sums, OtherEdgesSum, Completed)
    activateActivationFuncs(sums,OtherEdgesSum)
  netOutput = []
  for i in range(len(OutputNodes)):
    netOutput.append(OutputNodes[i].value)
  netOutputs.append(netOutput)

def recursionOrSomething(currentNode,prevDerives,counter):
  weightGradient[counter][currentNode.biasWeightNum] += prevDerives * funcDeriveFinder(currentNode.activation, currentNode.sum) * B
  for i in range(len(currentNode.connected)):
    weightGradient[counter][currentNode.connected[i].weightNum] += prevDerives * funcDeriveFinder(currentNode.activation, currentNode.sum) * Nodes[currentNode.connected[i].otherEdge].value
    newNode = Nodes[currentNode.connected[i].otherEdge]
    newDerives = prevDerives * funcDeriveFinder(currentNode.activation,currentNode.sum) * currentNode.connected[i].weight
    recursionOrSomething(newNode, newDerives, counter)


def backpropagation(outputs, netOutputs, counter):
  for i in range(len(OutputNodes)):
    weightGradient[counter][OutputNodes[i].biasWeightNum] += costDerive(netOutputs[i], outputs[i]) * funcDeriveFinder(OutputNodes[i].activation, OutputNodes[i].sum) * B
    for o in range(len(OutputNodes[i].connected)):
      weightGradient[counter][OutputNodes[i].connected[o].weightNum] += costDerive(netOutputs[i], outputs[i]) * funcDeriveFinder(OutputNodes[i].activation, OutputNodes[i].sum) * Nodes[OutputNodes[i].connected[o].otherEdge].value
      currentNode = Nodes[OutputNodes[i].connected[o].otherEdge]
      prevDerives = costDerive(netOutputs[i], outputs[i]) * funcDeriveFinder(OutputNodes[i].activation, OutputNodes[i].sum) * OutputNodes[i].connected[o].weight
      recursionOrSomething(currentNode, prevDerives, counter)
  
def weightGradientAverager():
  for i in range(len(inputs)):
    for o in range(len(weightGradient[i])):
      weightSum[o] = 0
      weightAverage[o] = 0
  for i in range(len(inputs)):
    for o in range(len(weightGradient[i])):
      weightSum[o] += weightGradient[i][o]
  for i in range(len(weightAverage)):
    weightAverage[i] = weightSum[i]/len(inputs)
      
def weightChanger():
  for i in range(len(Nodes)):
    Nodes[i].biasWeight += weightAverage[Nodes[i].biasWeightNum]
    for o in range(len(Nodes[i].connections)):
      Nodes[i].connections[o].weight += weightAverage[Nodes[i].connections[o].weightNum]
    
#variables --------------------------
B = 1

Input0 = Node(0, [Connection(random.random(), 4), 
                  Connection(random.random(), 5), 
                  Connection(random.random(), 6)],
              "linear", 0, 0)
Input1 = Node(1, [Connection(random.random(), 4), 
                  Connection(random.random(), 5), 
                  Connection(random.random(), 6)],
              "linear", 0, 0)
Input2 = Node(2, [Connection(random.random(), 4), 
                  Connection(random.random(), 5), 
                  Connection(random.random(), 6)],
              
              "linear", 0, 0)
Input3 = Node(3, [Connection(random.random(), 4), 
                  Connection(random.random(), 5), 
                  Connection(random.random(), 6)],
              "linear", 0, 0)

Node2 = Node(4, [Connection(random.random(),7)], "sig", 0, random.random())
Node3 = Node(5, [Connection(random.random(),7)], "relu", 0, random.random())
Node4 = Node(6, [Connection(random.random(),7)], "relu", 0, random.random())

Output5 = Node(7, [], "sig", 0, random.random())

NumOtherEdges = {}

Nodes = [Input0,Input1,Input2,Input3,Node2,Node3,Node4,Output5]
InputNodes = [Input0, Input1,Input2,Input3]
OutputNodes = [Output5]

for i in range(len(Nodes)):
    NumOtherEdges[i] = 0
for i in range(len(Nodes)):
  for o in range(len(Nodes[i].connections)):
    NumOtherEdges[Nodes[i].connections[o].edge] += 1





inputs = [[1,0,-1,2],[0,1,1,1],[2,-1,-1,2],[0,-1,2,-1]]
outputs = [[0.5],[0.123],[0.8],[1]]



connectedFinder()
totalWeights = weightNumMaker()
weightSum = {}
weightAverage = {}


weightGradient = {}
for i in range(len(inputs)):
  weightGradient[i] = []
  for o in range(totalWeights):
    weightGradient[i].append(0)
# -------------------------------------------
for i in range(9999):
  print()
  print("Epoch " + str(i))
  print()
  netOutputs = []
  for o in range(len(inputs)):
    print(inputs[o])
    feedForward(inputs[o])
    print(netOutputs[o])
    backpropagation(outputs[o], netOutputs[o], o)
  weightGradientAverager()
  weightChanger()
  weightGradient = {}
  for i in range(len(inputs)):
    weightGradient[i] = []
    for o in range(totalWeights):
      weightGradient[i].append(0)
    