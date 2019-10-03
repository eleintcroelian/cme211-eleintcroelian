import sys, random, copy, string

if len(sys.argv) != 6:
	print("Usage:")
	print(" $ python3  generatedata.py <ref_length> <nreads> <read_len> <ref_file> <reads_file>")
	sys.exit(0)

ref_length=int(copy.copy(sys.argv[1]))

nreads=int(copy.copy(sys.argv[2]))

read_len=int(copy.copy(sys.argv[3]))

ref_file=copy.copy(sys.argv[4])

reads_file=copy.copy(sys.argv[5])

align1=0
align2=0
align0=0

if ref_file[-4:]!='.txt' or reads_file[-4:]!='.txt':

	print('Please specify a .txt file (Inputs [4] and [5])')
	sys.exit(0)

letters = ["A","G","T","C"]

currentref=""

# Reference

with open(ref_file,"w") as ref_fl:
	for i in range(int(0.75*ref_length)):
		currentref=currentref+random.choice(letters)
	other25percent=ref_length-int(0.75*ref_length)
	ref=currentref+currentref[-other25percent:]
	ref_fl.write(ref+"\n")
# Reads

with open(reads_file,"w") as reads_fl:
	for i in range(nreads):
		category=random.random()
		if category <= 0.75: #Reads that align 1 time
			starting_position=int(random.random()/2.*ref_length)
			current_read=copy.copy(ref[starting_position:starting_position+read_len])
			align1 += 1
		elif category >= 0.90: #Reads that align 2 times
			starting_position=int((1.-random.random()/4.)*ref_length)
			if (ref_length-starting_position)<=read_len:
				starting_position=ref_length-read_len
			current_read=copy.copy(ref[starting_position:starting_position+read_len])
			align2 += 1
		else: # Reads that align 0 times
			read_trial=""
			for i in range(read_len): #Create a trial read
				read_trial=read_trial+random.choice(letters)
			while ref.find(read_trial)!=-1:
				read_trial=""
				for i in range(read_len):
					read_trial=read_trial+random.choice(letters)
			current_read=copy.copy(read_trial)
			align0 += 1
		reads_fl.write(current_read+"\n")

print("reference length: {}\nnumberreads: {}\nread length: {}\naligns 0: {}\naligns 1: {}\naligns 2: {}\n".format(ref_length,nreads,read_len,align0/nreads,align1/nreads,align2/nreads))


