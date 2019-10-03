import sys, random, copy, string

if len(sys.argv) != 4:
	print('Usage:\n $ python3 processdata.py <ref_file> <reads_file> <align_file>\n')
	sys.exit(0)

ref_file=copy.copy(sys.argv[1])
reads_file=copy.copy(sys.argv[2])
align_file=copy.copy(sys.argv[3])

with open(ref_file,'r') as ref_f:
	ref=ref_f.read()
ref=ref[:-1]

align0=0
align1=0
align2=0

with open(align_file,'w') as align_f:
	with open(reads_file,'r') as reads_f:
		for i,line in enumerate(reads_f):
			#print("Read number: {}".format(i+1))
			counter=0
			current_read=line[:-1]
			current_place=ref.find(current_read)
			#print('First place found: {}'.format(current_place)) #debug
			align_f.write(current_read)
			if current_place == -1:
				align_f.write(" -1\n")
				align0 += 1
				continue
			while current_place != -1:
				counter += 1
				#print('counter increased')
				align_f.write(" "+str(current_place))
				next_search=current_place+len(line)
				current_place=ref.find(current_read,next_search,len(ref))
				#print("Next Trial : {}".format(current_place)) #debug
			align_f.write("\n")

			if counter == 1:
				align1 += 1
			elif counter == 2:
				align2 += 1
			#print(counter)

print("\naligns 0: {}\naligns 1: {}\naligns 2: {}\n".format(align0/(i+1),align1/(i+1),align2/(i+1)))
