import copy,sys

import truss


if len(sys.argv) >4 or len(sys.argv)<3:
    # Checking if the input arguments are as desired.
    print('Usage: $python3 [joints file] [beams file] [optional plot output file]\n')
    sys.exit(0)
joints_file=copy.copy(sys.argv[1])
beams_file=copy.copy(sys.argv[2])

if len(sys.argv)==4: # If the thresh value is available from user, assign it
    print_file=sys.argv[3]
else:
    print_file=0

a=truss.Truss(joints_file,beams_file,print_file)
print(a)

