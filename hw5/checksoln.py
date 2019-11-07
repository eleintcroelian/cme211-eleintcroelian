import copy,sys
import numpy as np

if len(sys.argv)==3:
    maze_file=copy.copy(sys.argv[1])
    solution_file=copy.copy(sys.argv[2])
else:
    print('Usage: $python checksoln.py maze1.txt solution1.txt\n')
    sys.exit(0)
    # If the number of inputs are not correct, prints the usage directions 
    # and exits. Else, it assigns the file contents into variables.
maze=np.loadtxt(maze_file,int)
solution=np.loadtxt(solution_file,int)
# Assign file contents to variables
maze_row=maze[0][0]
maze_col=maze[0][1]
#From first line, we get the size of maze
maze_nh=np.delete(maze,0,0)
#Deleting first row and assigning to a new variable
current_row=0
current_col=-1
#initializing temporary variables
for i in maze_nh[maze_nh[:,0]==[0]]:
    #Looping over top row of maze
    #print(i[1])
    next_row=i[0]
    next_col=i[1]
    if next_col-current_col != 1:
        #If the difference between consecutive walls are more than 1, it
        #refers to the entrance
        entrance_col=current_col+1
        break
    else:
        current_row=copy.copy(next_row)
        current_col=copy.copy(next_col)
#Repeating same process for finding exit
current_row=0
current_col=-1
for i in maze_nh[maze_nh[:,0]==[maze_row-1]]:
    #loop over bottom of maze to find exit
    next_row=i[0]
    next_col=i[1]
    if next_col-current_col != 1:
        exit_col=current_col+1
        break
    else:
        current_row=copy.copy(next_row)
        current_col=copy.copy(next_col)
if not np.array_equal(solution[0],[0,entrance_col]):
    #Check if solution starts from the entrance
    print('Solution is not starting from entrance.\n')
    sys.exit(0)
    
if not np.array_equal(solution[-1],[maze_row-1,exit_col]):
    #Check if solution ends at the exit
    print('Solution does not finish at exit.\n')
    sys.exit(0)

maze_set = set(tuple(i) for i in maze)
sol_set = set(tuple(i) for i in solution)
# maze_set and sol_set are created to do a faster comparison to detect
# whether solution contains a wall grid or not.

if len(maze_set & sol_set) != 0 :
    #check if solution contains wall grids
    print('Solution should not contain wall grids.\n')
    sys.exit(0)     

for j in solution:
    # Looping over solution grids to check if it is out of bounds of maze
    if j[j<0].size != 0 or j[1]>(maze_col-1) or j[0]>(maze_row-1):
        print('Solution out of maze bounds.\n')
        sys.exit(0)
  
print('Solution succesful!\n')
