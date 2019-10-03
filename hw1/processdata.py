import sys, random, copy, string #__ Importing the modules to be used.

if len(sys.argv) != 4:		 #__ Checking if the input arguments are as desired.
	print('Usage:\n $ python3 processdata.py <ref_file> <reads_file> <align_file>\n')
	sys.exit(0)

ref_file=copy.copy(sys.argv[1])
reads_file=copy.copy(sys.argv[2])
align_file=copy.copy(sys.argv[3])

if ref_file[-4:]!='.txt' or reads_file[-4:]!='.txt' or align_file[=4:]!='.txt':
				 # _ Checking if the files given as input are text files.
        print('Please specify a .txt file (Inputs [4] and [5])')
        sys.exit(0)


with open(ref_file,'r') as ref_f:
	ref=ref_f.read()	 # _ Reading the reference from input file.
ref=ref[:-1]

align0=0			 # _ Initializing the counters for the number of alignments.
align1=0
align2=0

with open(align_file,'w') as align_f:
	with open(reads_file,'r') as reads_f:
		for i,line in enumerate(reads_f): # _ Reads every line in the reads file.
			counter=0		  # _ Counter for the # of alignments of a read
			current_read=line[:-1]
			current_place=ref.find(current_read) # __ Attempt to find read in the reference
			align_f.write(current_read)
			if current_place == -1:	       # __ If the attempt failed, mark it in alignment file
				align_f.write(" -1\n") # __ and continue to next read
				align0 += 1
				continue
			while current_place != -1:     # __ If it did not fail, mark where it aligned and keep
				counter += 1	       # __ searching for it, increasing the start point by the length
						       # __ of the read. (Recursive repetition of a read is ignored.)
				align_f.write(" "+str(current_place))
				next_search=current_place+len(line)
				current_place=ref.find(current_read,next_search,len(ref))

			align_f.write("\n")

			if counter == 1:		    # __ Update the counters for the alignment
				align1 += 1		    # __ Alignments more than 2 are ignored since
			elif counter == 2:		    # __ the scope of homework doesn't cover it.
				align2 += 1

print("\naligns 0: {}\naligns 1: {}\naligns 2: {}\n".format(align0/(i+1),align1/(i+1),align2/(i+1)))
