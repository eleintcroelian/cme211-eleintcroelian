import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import copy,math,warnings
from scipy.sparse import csr_matrix
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import spsolve


class Truss:
    def __init__(self,joints_file,beams_file,plot_file):
        self.joints_file=copy.copy(joints_file)
        self.beams_file=copy.copy(beams_file) 
        self.ImportFiles()
        if plot_file != 0:
            self.plot_file=plot_file
            self.PlotGeometry()

        self.Analysis()
        
        
    def ImportFiles(self):
        self.joint=np.loadtxt(self.joints_file)
        self.beam=np.loadtxt(self.beams_file)
        self.node_number=np.size(self.joint,0)
        self.element_number=np.size(self.beam,0)
        self.fixed_nodes=self.joint[self.joint[:,-1]==1.][:,0]
        
    def PlotGeometry(self):
        fig = plt.figure()
        for beamnumber in range(self.element_number):
            x_coord1=self.joint[int(self.beam[beamnumber][1])-1][1]            
            y_coord1=self.joint[int(self.beam[beamnumber][1])-1][2]
            x_coord2=self.joint[int(self.beam[beamnumber][2])-1][1]            
            y_coord2=self.joint[int(self.beam[beamnumber][2])-1][2]
            plt.plot([x_coord1,x_coord2],[y_coord1,y_coord2],color='b')
        fig.savefig(self.plot_file)
    
    def Analysis(self):
        try:
            warnings.filterwarnings('error',message='Matrix is exactly singular')
            warnings.filterwarnings('ignore',message="Changing the sparsity structure")            
            #self.T=np.zeros((2*self.node_number,2*self.node_number))
            self.T=csr_matrix((2*self.node_number,2*self.node_number))
            #self.F=np.zeros((2*self.node_number,1))
            self.F=csr_matrix((2*self.node_number,1))
            for joint in self.joint[:,0]:
                #print('in joint: {}'.format(joint))
                x_joint=self.joint[int(joint-1),1]
                y_joint=self.joint[int(joint-1),2]
                for beam in self.beam[:,0]:
                    if joint in self.beam[int(beam-1),1:2]:
                        otherjoint=self.beam[int(beam-1)][2]
                    elif joint in self.beam[int(beam-1),2:3]:
                        otherjoint=self.beam[int(beam-1)][1]
                    else:
                        continue
                    otherjoint_x=self.joint[int(otherjoint-1),1]
                    otherjoint_y=self.joint[int(otherjoint-1),2]
                    delx=x_joint-otherjoint_x
                    dely=y_joint-otherjoint_y
                    hip=math.sqrt(delx**2+dely**2)
                    self.T[int(joint*2-2),int(beam-1)]=delx/hip
                    self.T[int(joint*2-1),int(beam-1)]=dely/hip
                if joint in self.fixed_nodes:
                    index_fixed=(np.where(self.fixed_nodes==joint)[0][0]+1)*2+\
                                            self.element_number
                    #print(index_fixed)
                    self.T[int(joint*2-2),int(index_fixed-2)]=1
                    self.T[int(joint*2-1),int(index_fixed-1)]=1
            for i in range(self.node_number):
                self.F[2*i]=-self.joint[i,3]
                self.F[2*i+1]=-self.joint[i,4]
                #Catch warnings as exceptions
                self.solution=spsolve(self.T, self.F)
        except IndexError:
            raise RuntimeError("Truss geometry not suitable for static equilbrium analysis")
        except Exception:
            raise RuntimeError("Cannot solve the linear system, unstable truss?")

        
    def __repr__(self):
        line='Beam   Force\n'
        line += '_____________\n'
        
        for i in range(self.element_number):
            line+='{:2.0f}   {:7.3f}\n'.format(i+1,self.solution[i])
        return line
                    
                    
                    
                    

        
        
    
    
            
            
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        

