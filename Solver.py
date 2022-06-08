import copy
from queue import PriorityQueue
from tkinter.messagebox import RETRY

#global variables:
n = ""
initialState = []
initialStateASCII = []
type = ""
#Create a list of visited nodes 
visited = []
#Create a list of details for expanded nodes
report = []
# ID is assigned to each created node, duplicate nodes are not created 
id = 0
# solution path for the head node
solutionNode = -1
global file1

global goalState 

#set up goal state template for different sizes of n
def goalStateFunc():
    if n == '2':
        res = [['2','1'],['3',' ']]
        return res
    if n == '3':
        res = [['1','2','3'],['4',' ','6'],['7','5','8']]
        return res
    if n == '4':
        res = [['1','2','3','4'],['5','6','7','8'],['9','A','B','C'],['D','E',' ','F']]
        return res
    if n == '5':
        res = [['1','2',' ','4','5'],['6','7','3','9','A'],['B','C','8','D','E'],['F','G','H','I','J'],['K','L','M','N','O']]
        return res
    if n == '6':
        res = [['1','2','3','4','5','6'],['7','8','9','A','B','C'],['D','E','F','G','H','I'],['J','K','L','M','N','O'],['P','Q','R','S','T','U'],['V','W','X','Y','Z',' ']]
        return res


#varibles for output in .txt. file
depth = 0
numCreated = 0
numExpended = 0
maxFringe = 0

#reset globals 
def resetGlobal():
    n = ""
    initialState = []
    initialStateASCII = []
    type = ""
    visited = []
    report = []
    solution = -1
    depth = 0
    maxFringe = 0
    numCreated = 0
    numExpended = 0

#Prints output to .txt file
def printToFile(id):
    global numCreated, numExpended, maxFringe
    
    file1.write('\n')
    file1.write('n: ' + str(n) + ', ')
    file1.write('initial: ' + listToString(initialState) + ', ' )
    file1.write('goal: ' + listToString(goalState) + ', ')
    file1.write('searchmethod: ' + type + ', ')
    
    if (id == -1):
        dep = -1
        numCreated = -1
        numExpended = -1
        maxFringe = -1
    else: 
        dep = depth
        numExpended = len(visited)
    
    file1.write('\n')
    file1.write('depth: ' + str(dep) + ', ')
    file1.write('numCreated: ' + str(numCreated) + ', ')
    file1.write('numExpended: ' + str(numExpended) + ', ')
    file1.write('maxFringe: ' + str(maxFringe) + ', ')
    file1.write('\n')
    
    file1.write('[' + str(dep) + '], ')
    file1.write('[' + str(numCreated) + '], ')
    file1.write('[' + str(numExpended) + '], ')
    file1.write('[' + str(maxFringe) + '], ')
    file1.write('\n')
    
#parse User Input
def inputParse(userInput):
    global n, initialState, type, goalState
    open = False
    
    
    for element in userInput:
        if (element == " " and open == False):
            continue
        if ((element == '“' or element == '"') and open == False): 
            open = True
            continue
        if ((element == '”' or element == '"') and open == True): 
            open = False
            continue
        if(open == False and element.isdigit()):
            n = n + element
            continue
        if (open == True ):
            if(element == ' '): 
                initialState.append(' ')
                initialStateASCII.append(200)
            else: 
                initialState.append(element)
                initialStateASCII.append(ord(element))
        if (open == False and element.isalpha()):
            if(element != " "): type = type + element
    goalState = goalStateFunc()
    print('n: ' + str(n))
    print('Initial state: ' +str(initialState))
    print('Search: ' + str(type))
    print("Solvable?: " + str(ifSolvable(initialState))) 
    print("-----")
                   
#checks if puzzle is solvable
def ifSolvable(initialState):
    blankPosition = 0
    inversion = 0
    temp = copy.deepcopy(initialStateASCII)
    y = len(initialState)
    for x in range(0, y):
        #record blank square position 
        if (initialState[x] == ' '): 
            blankPosition = x
            temp.pop(0)
            continue
            
        if (ord(initialState[x]) > min(temp)):
            inversion = inversion + 1
        temp.pop(0)
    if(int(n)%2 == 0): # even n
        total = int((blankPosition/int(n)) + inversion)
        if (total % 2 != 0): return True
        else: return False 
    else: #odd n
        if(inversion % 2 == 0) : return True
        else: return False 

#Create a struct to save information about expanded nodes
class State:
    def __init__(self, identity, position, state, previous):
        self.identity = identity
        self.position = position
        self.state = state
        self.previous = previous

# To get blank space position for moving up, right, down, left
def blankPosition(a): #not used so far
    res =[]
    for i in range (0, len(a)):
        for y in range (0, len(a[i])):
            if a[i][y] == ' ': 
                res.append(i)
                res.append(y)
                return res

#Convert an input string to a Graph
def convertToGraph (charList):
    graph = []
    element = []
    global id
    levelCalc = int(len(charList)/int(n))
    i = 0
    r = State(id,0,0,-1)
    id+=1 
    for x in range (0, int(n)):
        for y in range (0,levelCalc):
            if(charList[i] == ' '): r.position = ([x,y])
            element.append(charList[i])
            i+=1
        graph.append(element.copy())
        element.clear()
    r.state = copy.deepcopy(graph)
    graph.clear();
    return r

#Compare if a current state equals to the goal state
def checkGoalState (graphA, graphB): #works
    for i in range(0, len(graphA)):
        for x in range(0,len(graphA[i])):
            if (graphA[i][x] != graphB[i][x]):  
                return False
    # print ("!!!!!!!!! GOAL !!!!!!!!!!!!!!")        
    return True

# Moves blank space up
def switchUp(graph, position, previous): # format => [[1,2][3,0]] , [1,2]
    res = copy.deepcopy(graph)
    global id
    if((position[0] - 1) >= 0):
        temp = res[position[0]-1][position[1]]
        res[position[0]-1][position[1]] = ' '
        res[position[0]][position[1]] = temp
    else: return 0
    r = State(id, [position[0]-1,position[1]], res, previous)
    if(checkIfSetExists(r.state)):
        return 0
    else: 
        id+=1
        return r

# Moves blank space right
def switchRight(graph, position, previous):
    res1 = copy.deepcopy(graph)
    global id
    if((position[1] + 1) < len(graph[0])):
        temp = res1[position[0]][position[1]+1]
        res1[position[0]][position[1]+1] = ' '
        res1[position[0]][position[1]] = temp
    else: return 0
    r = State(id, [position[0],position[1]+1], res1, previous)
    if(checkIfSetExists(r.state)):
        return 0
    else: 
        id+=1
        return r
    
# Moves blank space down  
def switchDown(graph, position, previous):
    res2 = copy.deepcopy(graph)
    global id
    if((position[0] + 1) < int(n)):
        temp = res2[position[0]+1][position[1]]
        res2[position[0]+1][position[1]] = ' '
        res2[position[0]][position[1]] = temp
    else: return 0
    r = State(id,[position[0]+1, position[1]], res2, previous)
    if(checkIfSetExists(r.state)):
        return 0
    else: 
        id+=1
        return r
    
# Moves blank space left
def switchLeft(graph, position,previous):
    res3 = copy.deepcopy(graph)
    global id
    if((position[1] - 1) >= 0):
        temp = res3[position[0]][position[1]-1]
        res3[position[0]][position[1]-1] = ' '
        res3[position[0]][position[1]] = temp 
    else: return 0
    r = State (id, [position[0], position[1]-1], res3, previous)
    if(checkIfSetExists(r.state)):
        return 0
    else: 
        id+=1
        return r
     
def resetGlobal():
    n = ""
    initialState = []
    initialStateASCII = []
    type = ""
    visited = []
    queue = []
    stack = []
    report = []
    
def listToString(list):
    res =''
    for x in range (0, len(list)):
        res = res + str(list[x]) + " "
    return res

# Supports BFS function
def bfsSupport (queue):
    global maxFringe, numCreated, solution, goalState
    
    while(queue):
        maxFringe = max(maxFringe, len(queue))
        t = queue[0]
        visited.append(t)
        # print ("current:")
        # print (t)
        # printGraph(report[t].state)
        if(checkGoalState(report[t].state, goalState)):
            # print("visited:")
            # print(visited)
            solution = t
            printPath(solution)
            printToFile(t)            
            return visited
        else:
            #Go up, add to Q, add to Report, check if goal
            up = switchUp(report[t].state, report[t].position,t)
            
            if(up != 0):
                queue.append(up.identity)
                report.append(up)
                # print (up.identity)
                # printGraph(up.state)
                numCreated += 1
                            
            #switchright, add to Q, add to report, check if goal
            right = switchRight(report[t].state, report[t].position,t)
            
            if (right != 0):
                queue.append(right.identity)
                report.append(right)
                # print (right.identity)
                # printGraph(right.state)
                numCreated += 1
                
            #switchdown, add to Q, add to report, check if goal
            down = switchDown(report[t].state, report[t].position, t)
            
            if(down != 0):
                queue.append(down.identity)
                report.append(down)
                # print (down.identity)
                # printGraph(down.state)
                numCreated += 1
                    
            #switchleft, add to Q, add to report, check if goal
            left = switchLeft(report[t].state, report[t].position, t)
            
            if (left != 0):
                queue.append(left.identity)
                report.append(left)
                # print (left.identity)
                # printGraph(left.state)
                numCreated += 1

            queue.pop(0)
            # print("end")
            
def bfs ():
    global id
    global numCreated, numExpended
    #Create a queue of expanded nodes
    queue = []
    if (ifSolvable(initialState)):
        if (len(initialState) == 0): 
            print ('The list is empty')
        else:
            p1 = convertToGraph(initialState)
            queue.append(p1.identity)
            report.append(p1)
            numCreated += 1
            bfsSupport(queue)
            
            
    else: 
        print ("The puzzle is not solvable")
        printToFile(-1)

    resetGlobal() 

#--------------------------------------------------------------------------
def printGraph (graphA): # used for debugging
    global n
    res =''
    for x in range (0, len(graphA)):
        res += (str(graphA[x][0])) 
        for w in range(1, len(graphA[x])):
            res += str(" - " + graphA[x][w])
        res += '\n'
    print (res)         
    print ("-------------")        

# Print solution in Console
def printPath(solution): #id
    global depth
    print ('')
    print ('Path: ')
    cur = solution
    res = []
    while cur != -1:
        res.append(cur)
        cur = report[cur].previous
    
    depth = len(res)
    for i in range (0, len(res)):
        temp = res[-1]
        res.pop()
        print(str(i) + ': ' + str(report[temp].state))
        
# Checks if identical record exists
def checkIfSetExists(graphA):
    for i in range(0, len(report)):
        global numCreated
        match = True
        for x in range (0, len(report[i].state)):
            for y in range (0, len(report[i].state[x] )):
                if(graphA[x][y] != report[i].state[x][y]):
                    match = False
        if match: 
            # print ("!!!!!!!!!!!!!!!!! DUPLICATE !!!!!!!!!!!!!!!!!!")
            break
    return match

#Supports DFS function
def dfsSupport(stack):
    global maxFringe, numCreated, solution, goalState
    
    while(stack):
        maxFringe = max(maxFringe, len(stack))
        s = stack[-1]
        visited.append(s)
        # print ("current:")
        # print (s)
        # printGraph(report[s].state)
        if(checkGoalState(report[s].state, goalState)):
            # print("visited:")
            # print(visited)
            solution = s
            printPath(solution)
            printToFile(s)
            return (visited)
        else:
            up = switchUp(report[s].state, report[s].position, s)
            
            if(up != 0):
                stack.append(up.identity)
                report.append(up)
                # print (up.identity)
                # printGraph(up.state)
                stack.pop(0)
                numCreated += 1
                continue
            right = switchRight(report[s].state, report[s].position, s)
            if (right != 0):
                stack.append(right.identity)
                report.append(right)
                # print (right.identity)
                # printGraph(right.state)
                stack.pop(0)
                numCreated += 1
                continue
            down = switchDown(report[s].state, report[s].position, s)
            if(down != 0):
                stack.append(down.identity)
                report.append(down)
                # print (down.identity)
                # printGraph(down.state)
                stack.pop(0)
                numCreated += 1
                continue
                    
            left = switchLeft(report[s].state, report[s].position, s)
            if (left != 0):
                stack.append(left.identity)
                report.append(left)
                # print (left.identity)
                # printGraph(left.state)
                stack.pop(0)
                numCreated += 1
                continue
            # print ("end")
        
def dfs ():
    global numCreated, numExpended
    stack = []
    
    if (ifSolvable(initialState)):
        if (len(initialState) == 0): 
            print ('the list is empty')
        else:
            p1 = convertToGraph(initialState)
            stack.append(p1.identity)
            report.append(p1)
            numCreated += 1
            dfsSupport(stack)
            
    else: 
        print ("The puzzle is not solvable")
        printToFile(-1)
    
    resetGlobal() 
#--------------------------------------------------------------------------
#calculates heuristics
def heuristicCalc(graphA, goalState):
    res = 0
    for i in range (0, len(graphA)):
        for j in range (0, len(graphA[i])):
            for x in range (0, len(goalState)):
                for y in range (0, len(goalState[x])):
                    if(graphA[i][j] != " "):
                        if (graphA[i][j] == goalState[x][y]):
                            res = res + abs(i - x) + abs(j - y)
    return res

# Supports GBFS frunction
def gbfsSupport (pq):
    global maxFringe, numCreated, solution, goalState
    
    while(pq):
        temp = pq.get()
        u = temp[1]
        visited.append(u)
       
        # print ("current:")
        # print (u)
        # printGraph(report[u].state)
        
        if(checkGoalState(report[u].state, goalState)):
            # print("visited:")
            # print(visited)
            solution = u
            printPath(solution)
            printToFile(u)
            return visited
        else:
            #Go up, add to Q, add to Report, check if goal
            up = switchUp(report[u].state, report[u].position, u)
            
            if(up != 0):
                temp = heuristicCalc(up.state, goalState)
                pq.put([temp, up.identity])
                report.append(up)
                # print (str(up.identity) + " h: " + str(temp))
                # printGraph(up.state)
                numCreated += 1
                
                # file1.write("\n")
                # file1.write(listToString(up.state))
                # file1.write(" " + str(heuristicCalc(up.state, goalState)))
                            
            #switchright, add to Q, add to report, check if goal
            right = switchRight(report[u].state, report[u].position, u)
            if (right != 0):
                temp = heuristicCalc(right.state, goalState)
                pq.put([temp, right.identity])
                report.append(right)
                # print (str(right.identity) + " h: " + str(temp))
                # printGraph(right.state)
                numCreated += 1
                
                # file1.write("\n")
                # file1.write(listToString(right.state))
                # file1.write(" " + str(heuristicCalc(right.state, goalState)))
               
            #switchdown, add to Q, add to report, check if goal
            down = switchDown(report[u].state, report[u].position, u)
            if(down != 0):
                temp = heuristicCalc(down.state, goalState)
                pq.put([temp, down.identity])
                report.append(down)
                # print (str(down.identity) + " h: " + str(temp))
                # printGraph(down.state)
                numCreated += 1
                
                # file1.write("\n")
                # file1.write(listToString(down.state))
                # file1.write(" " + str(heuristicCalc(down.state, goalState)))
                    
            #switchleft, add to Q, add to report, check if goal
            left = switchLeft(report[u].state, report[u].position, u)
            if (left != 0):
                temp = heuristicCalc(left.state, goalState)
                pq.put([temp, left.identity])
                report.append(left)
                # print (str(left.identity) + " h: " + str(temp))
                # printGraph(left.state)
                numCreated += 1
                
                # file1.write("\n")
                # file1.write(listToString(left.state))
                # file1.write(" " + str(heuristicCalc(left.state, goalState)))
            
            maxFringe = max(maxFringe, pq.qsize())
            
            # print("end")  
             
   
def gbfs():
    global numCreated, numExpended, solution
    pq = PriorityQueue()  
    q = []
    if (ifSolvable(initialState)):
        if (len(initialState) == 0): 
            print ('the list is empty')
        else:
            p1 = convertToGraph(initialState)
            pq.put([heuristicCalc(p1.state, goalState), p1.identity])
            report.append(p1)
            numCreated += 1
            gbfsSupport(pq)
            
            
    else: 
        print ("The puzzle is not solvable")
        printToFile(-1)
    resetGlobal() 
    
#--------------------------------------------------------------------------
# Sipports AStar function
def aStarSupport (pqA):
    global maxFringe, numCreated, solution, goalState
    
    while(pqA):
        temp = pqA.get()
        #maxFringe = max(maxFringe, pqA.queue.qsize())
        w = temp[2]
        visited.append(w)
       
        # print ("current:")
        # print (w)
        # printGraph(report[w].state)
        if(checkGoalState(report[w].state, goalState)):
            # print("visited:")
            # print(visited)
            solution = w
            printPath(solution)
            printToFile(w)            
            return visited
        else:
            #Go up, add to Q, add to Report, check if goal
            up = switchUp(report[w].state, report[w].position, w)
            if(up != 0):
                h = heuristicCalc(up.state, goalState) + temp[1] + 1
                pqA.put([h ,temp[1]+1, up.identity ])
                report.append(up)
                # print (str(up.identity) + ' h: ' + str(h))
                # printGraph(up.state)
                numCreated += 1
                
                # file1.write("\n")
                # file1.write(listToString(up.state))
                # file1.write(" " + str(heuristicCalc(up.state, goalState)))
                            
            #switchright, add to Q, add to report, check if goal
            right = switchRight(report[w].state, report[w].position, w)
            if (right != 0):
                h = heuristicCalc(right.state, goalState) + temp[1] + 1
                pqA.put([h, temp[1]+1, right.identity ])
                report.append(right)
                # print (str(right.identity) + ' h: ' + str(h))
                # printGraph(right.state)
                numCreated += 1
                
                # file1.write("\n")
                # file1.write(listToString(right.state))
                # file1.write(" " + str(heuristicCalc(right.state, goalState)))
               
                        
            #switchdown, add to Q, add to report, check if goal
            down = switchDown(report[w].state, report[w].position, w)
            if(down != 0):
                h = heuristicCalc(down.state, goalState) + temp[1] + 1
                pqA.put([h, temp[1]+1, down.identity ])
                report.append(down)
                # print (str(down.identity) + ' h: ' + str(h))
                # printGraph(down.state)
                numCreated += 1
                
                # file1.write("\n")
                # file1.write(listToString(down.state))
                # file1.write(" " + str(heuristicCalc(down.state, goalState)))
                    
            #switchleft, add to Q, add to report, check if goal
            left = switchLeft(report[w].state, report[w].position, w)
            if (left != 0):
                h = heuristicCalc(left.state, goalState) + temp[1] + 1
                pqA.put([h, temp[1]+1, left.identity])
                report.append(left)
                # print (str(left.identity) + ' h: ' + str(h))
                # printGraph(left.state)
                numCreated += 1
                
                # file1.write("\n")
                # file1.write(listToString(left.state))
                # file1.write(" " + str(heuristicCalc(left.state, goalState)))
             
            maxFringe = max(maxFringe, pqA.qsize())
            # print("end")

def astar():
    
    global numCreated, numExpended, pqA, solution
    pqA = PriorityQueue()
    if (ifSolvable(initialState)):
        if (len(initialState) == 0): 
            print ('the list is empty')
        else:
            p1 = convertToGraph(initialState)
            pqA.put([heuristicCalc(p1.state, goalState), 0, p1.identity])
            report.append(p1)
            numCreated += 1
            aStarSupport(pqA)
            
    else: 
        print ("The puzzle is not solvable")
        printToFile(-1)
        
    pqA.queue.clear()
    resetGlobal() 
#--------------------------------------------------------------------------

