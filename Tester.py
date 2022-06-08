import sys
import Solver

# Test cases: userInputs Goal State Test cases:
# userInput = "2 “12 3” BFS" #1
# userInput = "2 “132 ” AStar" #2
# userInput = "2 “ 132” AStar" #3
# userInput = "2 “32 1” DFS" #4 provided by professor/tested
# userInput = "3 “12345678 ” BFS" #5 /tested
# userInput = "3 “47315862 ” GBFS" #6 provided by professor
# userInput = "4 “123456789AB DEFC” BFS" #7 provided by professor/tested
# userInput = "3 “1234 5678” AStar" #8
# userInput = "5 “123456789ABC DEFGHIJKLMNO” AStar" #9/tested
# userInput = "6 “123456789ABCDEFGHIJKLMN PQRSTOVWXYZU” GBFS" #10/tested
# userInput = "2 “123 ” BFS" #11
# userInput = "3 “12345678 ” AStar" #12

# goalState = [[' ','1'],['3','2']] #1
# goalState = [['3',' '],['1','2']] #2
# goalState = [['1','2'],['3',' ']] #3
# goalState = [['2','1'],['3',' ']]  #4 #
# goalState =[['1','2','3'],['4',' ','6'],['7','5','8']] #5
# goalState = [[' ','1','2'],['3','4','5'],['6','7','8']] #6 #
# goalState = [['1','2','3','4'],['5','6','7','8'],['9','A','B','C'],['D','E',' ','F']] #7 #
# goalState =[['1','2','3'],['4','5','8'],['6','7',' ']] #8
# goalState =[['1','2','3','4','5'],['6','7','8','9','A'],[' ','B','C','D','E'],['F','G','H','I','J'],['K','L','M','N','O']] #9
# goalState = [['1','2','3','4','5','6'],['7','8','9','A','B','C'],['D','E','F','G','H','I'],['J','K','L','M','N','O'],['P','Q','R','S','T','U'],['V','W','X','Y','Z',' ']] #10
# goalState =  [['1','2'],['3',' ']] #11
# goalState =[['1','2','3'],[' ','4','5'],['7','8','6']] #12


if __name__=="__main__":
    
    print('')
    userInput = input("Current State Input: ")
    
    Solver.inputParse(userInput)
    
    
    Solver.file1 = open("Readme.txt","a")
    
    if (Solver.type == 'BFS'):
        Solver.bfs()
    if (Solver.type == 'DFS'):
        Solver.dfs()
    if (Solver.type == 'GBFS'):
        Solver.gbfs()
    if (Solver.type == 'AStar'):    
        Solver.astar()

    Solver.file1.close()  
    
