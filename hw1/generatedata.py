import sys, random, copy, string # _____________________
#                                  _____________________ Modules to be used.

if len(sys.argv) != 6: # _______________________________ Checking if we get all the input we need.
	print("Usage:")
	print(" $ python3  generatedata.py <ref_length> <nreads> <read_len> <ref_file> <reads_file>")
	sys.exit(0)

ref_length=int(copy.copy(sys.argv[1])) # _______________ Assigning the input to variables.

nreads=int(copy.copy(sys.argv[2]))

read_len=int(copy.copy(sys.argv[3]))

ref_file=copy.copy(sys.argv[4])

reads_file=copy.copy(sys.argv[5])

align1=0 # _____________________________________________ Initializing the counters.
align2=0
align0=0

if ref_file[-4:]!='.txt' or reads_file[-4:]!='.txt': # _ Checking if the files given as input are text files.

	print('Please specify a .txt file (Inputs [4] and [5])')
	sys.exit(0)

letters = ["A","G","T","C"]

currentref="" # ________________________________________ Initializing the reference.

with open(ref_file,"w") as ref_fl:
	for i in range(int(0.75*ref_length)): # ________ Generating the first 75% of the reference randomly.
		currentref=currentref+random.choice(letters)
	other25percent=ref_length-int(0.75*ref_length) # _____________ Calculating the length of the remaining reference part.
	ref=currentref+currentref[-other25percent:] # ________________ Appending the references last 25% to itself.
	ref_fl.write(ref+"\n") # _____________________________________ Writing it into a file.

with open(reads_file,"w") as reads_fl:
	for i in range(nreads): # ________________ Read generation loop.
		category=random.random() # __ Creating a random integer to decide whether the read will align 0,1 or 2 times.
		if category <= 0.75: # ______ Reads that align 1 time make 75% of all reads.
			starting_position=int(random.random()/2.*ref_length)
			 # __ Choosing a random position from the first half of the reference (Here,
			 # __ it doesn't matter whether some part of the read extends to the other half
			 # __ of the reference, since it can't align twice if it is not all in 50-75%).
			current_read=copy.copy(ref[starting_position:starting_position+read_len])
			align1 += 1 # ___________ Counter for reads that align once.
		elif category >= 0.90: # ________ Reads that align 2 times make 1.0-0.90 = 0.1 = 10% of all reads.
			starting_position=int((1.-random.random()/4.)*ref_length)
			if (ref_length-starting_position)<=read_len:
				starting_position=ref_length-read_len
			 # __ We force the starting position from read_len away from ref_length so that
			 # __ reads are not shorter than the input read length value.
			current_read=copy.copy(ref[starting_position:starting_position+read_len])
			align2 += 1 # __________________ Counter for reads that align twice.
		else: # ________________________________ Reads that align 0 times make up 15% of all reads.
			read_trial=""
			for i in range(read_len): # ____ Create a trial read for initial check.
				read_trial=read_trial+random.choice(letters)
			while ref.find(read_trial)!=-1:
				 # _____ While loop will be carried out only if the trial read is not aligned.
				read_trial=""
				for i in range(read_len):
				 # _____ Generate the next trial and check condition until it doesn't align.
					read_trial=read_trial+random.choice(letters)
			current_read=copy.copy(read_trial)
			align0 += 1
		reads_fl.write(current_read+"\n")

print("reference length: {}\nnumberreads: {}\nread length: {}".format(ref_length,nreads,read_len))
print("aligns 0: {}\naligns 1: {}\naligns 2: {}\n".format(align0/nreads,align1/nreads,align2/nreads))
# __ Prints the results
