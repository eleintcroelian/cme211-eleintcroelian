import copy,sys
import truss

if len(sys.argv)==4:
    # Checks the number of input arguments, stores file name inputs into 
    # variables, creates a truss class with beams and joints files.
    joints_file=copy.copy(sys.argv[1])
    beams_file=copy.copy(sys.argv[2])
    plot_file=sys.argv[3]
    a=truss.Truss(joints_file,beams_file)
    a.PlotGeometry(plot_file)
    # Plots the geometry and saves as the plot_file name to the current
    # directory.
elif len(sys.argv)==3:
    joints_file=copy.copy(sys.argv[1])
    beams_file=copy.copy(sys.argv[2])
    a=truss.Truss(joints_file,beams_file)
    # Does not plot the file if plot_file is not given as input.
else:
    print('Usage: $python3 [joints file] [beams file]\
    [optional plot output file]\n')
    sys.exit(0)
    # If the number of inputs are not correct, prints the usage directions 
    # and exits.
a.Analysis()
print(a)
# Runs the analysis of the system and prints results.
