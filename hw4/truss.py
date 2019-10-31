import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import copy,math,warnings
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import spsolve

class Truss:
    '''Truss class for loading and analyzing a 2D truss using
    the method of joints. The initialization
    method of the class takes the names for joints
    and beams files as arguments.
    '''
    def __init__(self,joints_file,beams_file):
        '''Stores the input file names as local variables and initiates the
        ImportFiles() method.
        '''
        self.joints_file=copy.copy(joints_file)
        self.beams_file=copy.copy(beams_file) 
        self.ImportFiles()
        
    def ImportFiles(self):
        '''Saves the data in joints and beams file in seperate variables.
        Finds total beam and node numbers, and fixed joints.
        '''
        self.joint=np.loadtxt(self.joints_file)
        self.beam=np.loadtxt(self.beams_file)
        self.node_number=np.size(self.joint,0)
        self.element_number=np.size(self.beam,0)
        self.fixed_nodes=self.joint[self.joint[:,-1]==1.][:,0]
        
    def PlotGeometry(self,plot_file):
        '''Plots the truss geometry and saves it to the current directory
        with the name as given input plot_file.
        '''
        fig = plt.figure()
        for beamnumber in range(self.element_number):
            x_coord1=self.joint[int(self.beam[beamnumber][1])-1][1]
            y_coord1=self.joint[int(self.beam[beamnumber][1])-1][2]
            x_coord2=self.joint[int(self.beam[beamnumber][2])-1][1]
            y_coord2=self.joint[int(self.beam[beamnumber][2])-1][2]
            # Assigns x and y coordinates of each beam
            plt.plot([x_coord1,x_coord2],[y_coord1,y_coord2],color='b')
            # Plots each beam using the coordinates
        fig.savefig(plot_file)
        # Saves the figure in the current directory
    
    def Analysis(self):
        ''' Executes the static analysis of the truss system with method of
        joints, using two sparse matrix T(nxn) and  vector F(nx1) where n 
        is the number of unknown forces in each node in 2D plane. 
        (n=2* # of joints)
        '''
        warnings.filterwarnings('error',message='Matrix is exactly singular')
        warnings.filterwarnings('ignore',message="Changing the sparsity")
        # Sets the singularity warning of spsolve() as an error and
        # cost warning of csrmatrix is ignored.
        try:
            self.T=csr_matrix((2*self.node_number,2*self.node_number))
            self.F=csr_matrix((2*self.node_number,1))
            # Initiates T and F
            for joint in self.joint[:,0]:
                x_joint=self.joint[int(joint-1),1]
                y_joint=self.joint[int(joint-1),2]
                # For each joint, coordinates are stored
                for beam in self.beam[:,0]:
                    if joint in self.beam[int(beam-1),1:2]:
                        otherjoint=self.beam[int(beam-1)][2]
                    elif joint in self.beam[int(beam-1),2:3]:
                        otherjoint=self.beam[int(beam-1)][1]
                    else:
                        continue
                    # Each beam is iterated for each joint and checked if
                    # it is connected to the current joint or not, if it is 
                    # connected, the other joint number of the beam is stored.
                    otherjoint_x=self.joint[int(otherjoint-1),1]
                    otherjoint_y=self.joint[int(otherjoint-1),2]
                    delx=x_joint-otherjoint_x
                    dely=y_joint-otherjoint_y
                    hip=math.sqrt(delx**2+dely**2)
                    # coordinates of the other joints is stored and distances
                    # between the current joint are calculated, and beam
                    # length (hip) is found.
                    self.T[int(joint*2-2),int(beam-1)]=delx/hip
                    self.T[int(joint*2-1),int(beam-1)]=dely/hip
                    # cos() and sin() of the angle between beam and the joint
                    # are calculated and stored in T matrix, which are the
                    # coefficients of beam forces in summation of forces in
                    # x and y.                    
                if joint in self.fixed_nodes:
                    index_fixed=(np.where(self.fixed_nodes==joint)[0][0]+1)*2\
                    +self.element_number
                    self.T[int(joint*2-2),int(index_fixed-2)]=1
                    self.T[int(joint*2-1),int(index_fixed-1)]=1
                    # Current joint is checked whether it is a fixed one or
                    # not, if it is fixed, the coefficient for reaction force
                    # which is 1, is stored in T matrix.
            for i in range(self.node_number):
                self.F[2*i]=-self.joint[i,3]
                self.F[2*i+1]=-self.joint[i,4]
                # External forces are stored into F vector. - sign comes since
                # the original equation is TM+F=0 and we are solving TM=-F
            self.solution=spsolve(self.T, self.F)
            # TM=-F is solved with scipy.sparse.linalg.spsolve(), where T
            # consisting of coefficients of unknown forces, M, being the
            # unknowns which are sorted as [F1,F2,...,Fn,R1,R2,...Rn] where
            # F1,F2... are the beam forces and R1,R2... are the reactions.
            
        except IndexError:
            raise RuntimeError("Truss geometry not suitable for static\
                               equilbrium analysis")
            # Detects if the number of equations are equal to the number of 
            # unknowns, if not, system is overdetermined, and raises an error.
        except Warning:
            raise RuntimeError("Cannot solve the linear system, unstable\
                              truss?")
            # Detects if singularity warning was raised by spsolve(), if yes,
            # which leads to an unstable system, raises a run time error.
    def __repr__(self):
        '''Overloads print() for the class. Initiating print(<truss>) prints
        the resulting force in each beam in two columns. First column is the
        beam number and second is the resulting force in that beam.
        '''
        line='Beam   Force\n'
        line += '_____________\n'
        for i in range(self.element_number):
            line+='{:2.0f}   {:7.3f}\n'.format(i+1,self.solution[i])
        return line
