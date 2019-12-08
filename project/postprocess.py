import copy,sys,math 
import numpy as np
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt

if len(sys.argv) !=3:
    # Checking if the input arguments are as desired.
    print('Usage: $python3 postprocess.py <input_file> <solution_file>')
    sys.exit(0)
#Store arguments into variables
input_file=copy.copy(sys.argv[1])
solution_file=copy.copy(sys.argv[2])
#Read solution file and store it to sol
try:
    sol=np.loadtxt(solution_file)
    #Read input file and store required variables as float type
    with open(input_file,'r') as f:
        line = f.readline()
        length=float(line.split()[0])
        width=float(line.split()[1])
        h=float(line.split()[2])
        line = f.readline()
        Tc=float(line.split()[0])
        Th=float(line.split()[1])
    #Number of nodes in x and y direction
    n_x=int(length/h+1)
    n_y=int(width/h+1)
    #Same M Matrix from C++ code is formed which contains node numbers as a grid
    M=np.zeros((n_y,n_x),int)
    count=1
    for i in range(1,n_y-1):
        for j in range(0,n_x-1):
            M[i,j]=count
            count=count+1
    
    for i in range(1,n_y-1):
        M[i,n_x-1]=count
        count=count+1
    
    for j in range(0,n_x):
        M[n_y-1,j]=count
        count=count+1
    
    for j in range (0,n_x):
        M[0,j]=count
        count=count+1
    # number of unknown nodes to be solved
    n_unk=(n_x-1)*(n_y-2)
    if n_unk != sol.size:
        raise RuntimeError("Input file does not correspond to the output "+
                       "file format.")
    # Boundary nodes are stored in BC array
    BC=np.zeros((n_y*n_x,1))
    
    for i in range((n_y-2)*n_x,(n_y-1)*n_x):
        BC[i]=copy.copy(Th)
        
    k=0
    for i in range((n_y-1)*n_x,(n_y)*n_x):
        BC[i]=-Tc*(math.exp(-10*pow((k-length/2),2))-2)
        k=k+h
    # sol_grid is the grid form of solution including boundary conditions
    sol_grid=np.zeros((n_y,n_x))
    for i in range(0,n_y):
        for j in range(0,n_x):
            sol_grid[i,j]=BC[M[i,j]-1]
    
    for i in range(1,n_y-1):
        for j in range(0,n_x-1):
            sol_grid[i,j]=sol[(M[i,j]-1)]
    
    for i in range(0,n_y-1):
       sol_grid[i,n_x-1]=sol_grid[i,0]
    # Mean temp is the average temparature in the grid
    meantemp=sol_grid.sum()/sol_grid.size
    # Display input file and Mean temperature
    print("Input file processed: " + input_file)
    print("Mean Temperature:{:7.3f}".format(meantemp))
    # Create xi yi which are x and y axes
    xi = np.arange(0, n_x)
    xi=np.multiply(xi,length/(n_x-1))
    yi = np.arange(0, n_y)
    yi=np.multiply(yi,width/(n_y-1))
    # Mesh grid of xi and yi
    X, Y = np.meshgrid(xi, yi)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    # Pseudocolor plot
    plt.pcolor(X, Y, sol_grid,cmap='jet')
    plt.colorbar()
    ax.set_aspect('equal')
    # Isothermal line of mean temperature
    plt.contour(X, Y, sol_grid,[meantemp],colors='k')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.show()

except OSError:
    raise RuntimeError("Input or output file not found.")
    
except IndexError:
    raise RuntimeError("Input file does not correspond to the output "+
                       "file format.")






