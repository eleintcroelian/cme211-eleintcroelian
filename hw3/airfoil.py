import copy,math,os

class Airfoil:
    '''
    Airfoil class for processing pressure distribution data of
    2D cross sections of wing designs. For a given input directory,
    xy.dat and alpha<angle>.dat files are expected.
    '''
    def __init__(self,inputdir):
        '''
        Initiation method for the Airfoil class. Gets input directory as input.
        Runs importfiles, calc_chordlength and calc_delcx_delcy methods upon
        calling the class.
        '''

        self.inputdir=inputdir
        #store input direction
        self.importfiles()
        self.calc_chordlength()
        self.calc_delcx_delcy()

    def importfiles(self):
        '''
        File names inside the directory are stored in a data structure in
        the class. These names are then checked and the file whose name starts
        with 'xy' is stored as the geometry data. All the files whose names
        start with 'alpha' are stored as pressure coefficient data according
        to the digits following in the file name.
        '''

        self.filenames=[]
        self.alphasets={}
        self.nodes={}
        self.panel={}
        #initialize dictionaries

        for root, dirs, files in os.walk(self.inputdir, topdown=False):
            for name in files:
                self.filenames.append(os.path.join(name))
                #store all files in the inout directory
        try:
            os.chdir(self.inputdir)

        except FileNotFoundError:
            raise RuntimeError("File not found, possibly missing trailing\
                               delimiter.")
        xyflag=False
        alphaflag=False
        #Flags are True if there exists xy and alpha files.
        for name in self.filenames:
            if name.startswith('alpha'):
                alphaflag=True

                #select files that start with 'alpha'
                try:
                    if name[5:name.find('.dat')]=='':
                        raise RuntimeError("Data file format expected is\
                                           .dat")
                    datakey=float(name[5:name.find('.dat')])
                except ValueError:
                    raise RuntimeError("Expected digits after 'alpha'\
                                       (i.e. alpha-3.0.dat).")
                #get alpha value

                with open(name,'r') as alphafile:
                    next(alphafile)
                    #skip header
                    for line in alphafile:
                    #store alpha as keys and corresponding dataset to
                    #dictionary
                        try:
                            numeric_line=float(line.split()[0])
                        except Exception:
                            raise RuntimeError('Alpha '+
                                               'data contains non numeric '+
                                               'values or an extra '+
                                               'empty line.')
                        if datakey in self.alphasets:
                            self.alphasets[datakey].append(numeric_line)
                        else:
                            self.alphasets[datakey]=[numeric_line]

            elif name.startswith('xy'):
                #store xy file to another dictionary
                xyflag=True

                nodenumber=1
                #node number index initiation

                with open(name,'r') as xyfile:
                    next(xyfile)
                    #skip header

                    for line in xyfile:
                        try:
                            numeric_line1=float(line.split()[0])
                            numeric_line2=float(line.split()[1])
                        except Exception:
                            raise RuntimeError('XY '+ 
                                               'data contains non numeric '+
                                               'values or an extra '+
                                               'empty line.')
                        self.nodes[nodenumber]=(numeric_line1,
                                  numeric_line2)
                        nodenumber+=1
                        #assign each line in xy file as a node, give an index
                        #and store coordinates as a tuple

                for panelnumber in range(len(self.nodes)-1):
                    self.panel[panelnumber+1]=(panelnumber+1,panelnumber+2)
                    #assign every incrementing couple of nodes as a panel

                with open(name,'r') as xyfile:
                    self.title=xyfile.readline()
                    #get the dataset title
            else:
                continue

        if not xyflag:
            raise RuntimeError("Could not find xy file (need xy.dat).")
        if not alphaflag:
            raise RuntimeError("Could not find alpha files (need\
                                    alpha<value>.dat).")

    def calc_chordlength(self):
        '''
        Distance between all nodes are compared and the maximum is chosen
        to be the chord length. Horizontal convex airfoil design is assumed.
        '''
        #initiate node numbers for nodes in leading and trailing edge
        dist=0

        for node1 in self.nodes.keys():
            #looping over nodes
            x1=self.nodes[node1][0]
            y1=self.nodes[node1][1]
            #storing x and y coords of each node
            for node2 in self.nodes.keys():
                #looping over nodes again
                x2=self.nodes[node2][0]
                y2=self.nodes[node2][1]
                temp_dist=math.sqrt(pow((x1-x2),2)+
                                    pow((y1-y2),2))
                #calculating the distance between node1 and node2
                if temp_dist>dist:
                    dist=copy.copy(temp_dist)
                #update chord length if new distance is bigger
        self.chord_length=copy.copy(dist)

    def calc_delcx_delcy(self):
        '''
        By multiplying the pressure coefficient by the panel length and non-
        dimensionalizing with the chord length the dimensionless force
        for each panel is calculated. This force is then decomposed to cartesian
        coordinates and then each of these components are summed for all the
        panels. Then for each attack angle, the lift coefficient is calculated.
        '''
        self.panel_delx={}
        self.panel_dely={}
        self.panel_length={}
        #initialize delta x, delta y

        for panelnumber in self.panel.keys():
            #iterating over panels

            node1=copy.copy(self.panel[panelnumber][0])
            node2=copy.copy(self.panel[panelnumber][1])
            #get nodes of the current panel

            self.panel_delx[panelnumber]=self.nodes[node2][0]\
                                            -self.nodes[node1][0]

            self.panel_dely[panelnumber]=self.nodes[node2][1]\
                                            -self.nodes[node1][1]
            #calculate x and y coordinate difference (delta x, delta y) for
            #each panel
            self.panel_length[panelnumber]=math.sqrt(
                                        pow(self.panel_delx[panelnumber],2)
                                        +pow(self.panel_dely[panelnumber],2))
            #using delta x and delta y, calculate panel length
        self.cl={}
        self.stagpoint={}
        #initialize dictionaries for cl and stagnation points

        for alpha in self.alphasets.keys():
            del_c_y=[]
            del_c_x=[]
            #iterating over different alpha sets

            for panel in self.panel.keys():
                #iterating over panels
                pressure_coeff=self.alphasets[alpha][panel-1]
                #get the pressure coefficient of the current alpha set for
                #the panel

                force=pressure_coeff*self.panel_length[panel]\
                                            /self.chord_length
                #calculate the force ortogonal to each panel
                del_c_y.append(force*(self.panel_delx[panel])/\
                               self.panel_length[panel])
                del_c_x.append(force*(-self.panel_dely[panel])/\
                               self.panel_length[panel])
                #calculate delc_x and delc_y for each panel
            c_x=sum(del_c_x)
            c_y=sum(del_c_y)
            #sum all delc_x and delc_y

            self.cl[alpha]=round(c_y*math.cos(alpha/180*math.pi)-\
                   c_x*math.sin(alpha/180*math.pi),4)
            #calculate cl for each alpha

            currentcoeffs=copy.copy(self.alphasets[alpha])
            #copy the current alpha set later to manupulate

            currentcoeffs=[abs(x-1) for x in currentcoeffs]
            #subtract 1 from each pressure coefficient, take its absolute

            index_min = min(range(len(currentcoeffs)),
                            key=currentcoeffs.__getitem__)
            #get index of minimum of the manipulated data set gives the
            #value which is the closest to 1.0

            stagnodes=copy.copy(self.panel[index_min+1])
            #using this index to find corresponding the panel number and
            #assign its nodes to a temporary variable

            x_avg=(self.nodes[stagnodes[0]][0]+\
                         self.nodes[stagnodes[1]][0])/2
            y_avg=(self.nodes[stagnodes[0]][1]+\
                         self.nodes[stagnodes[1]][1])/2
            #Get the average of x and y coordinates of the panels nodes

            self.stagpoint[alpha]=[(x_avg,y_avg),
                          self.alphasets[alpha][index_min]]
            #assign the averages as a tuple and the pressure coefficient
            #to a dictionary

    def __repr__(self):
        '''
        Upon calling print() for the Airfoil object, for each
        alpha value, lift coefficient and stagnation points
        with the corresponding pressure coefficients are displayed
        in a tabular form.
        '''
        l1='Test Case: {}\n'.format(self.title)
        l2=' alpha        cl               stagnation pt\n'
        l3=' ______     ________    _________________________\n'
        l4=''
        #first three lines are not dataset dependent

        for alpha in sorted(self.alphasets.keys()):
            #for each alpha set, add a line that contains the corresponding 
            #cl value and the stagnation point coordinates and the pressure
            #coefficient closest to 1.0

            l4=l4+"{:7.4f}     {:7.4f}     ({:7.4f},{:7.4f}) {:7.4f}\n"\
            .format(alpha,self.cl[alpha],self.stagpoint[alpha][0][0],\
                    self.stagpoint[alpha][0][1],self.stagpoint[alpha][1])

        return l1+l2+l3+l4
