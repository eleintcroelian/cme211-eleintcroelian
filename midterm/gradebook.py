import copy,sys

if len(sys.argv) >6 or len(sys.argv)<5:

    print('Usage:$ python3 gradebook.py grades_file output_file m k [w_1 w_2 ... w_k]\n')
    sys.exit(0)
grades_file=copy.copy(sys.argv[1])
output_file=copy.copy(sys.argv[2])
m=int(sys.argv[3])
k=int(sys.argv[4])

# saving input to variables

if len(sys.argv)==6:
    weight_str=sys.argv[5].replace('[', ' ').replace(']', ' ').replace(',', ' ').split()
    weights=[float(i) for i in weight_str]
    if sum(weights) !=1.0:
        print('Weights should sum up to 1.0\n')
        sys.exit(0)
else:
    weights=[1/k]*k

#Sanitizing weights input

def compute_assignment_scores(scores,weights,k,m):
    ''' Gets m,k and raw scores weights (as lists) and calculates the weighted
       sum of each homework. Returns a list of final homework grades.
    '''
    weighted_hws=[0]*m
    for hw_n in range(m):
        current_hw=scores[(hw_n)*k:(hw_n)*k+k]
        weightedsum=sum(i[0] * i[1] for i in zip(current_hw, weights))
        weighted_hws[hw_n]=weightedsum
    return weighted_hws

def read_data(grades_file,m,k):
    '''Reads input grades_file and creates two dictionarys that are in the
      student_hw[student id]=[raw homework data]
      student_exam[student id]=[two exam scores]
    '''
    student_hw={}
    student_exam={}
    with open(grades_file,'r') as f:
        for line in f:
            suid=copy.copy(line.split()[0])
            student_hw[suid]=[]
            student_exam[suid]=[float(line.split()[-2]),float(line.split()[-1])]
            for column in range(m*k):
                student_hw[suid].append(float(line.split()[column+1]))
    return (student_hw,student_exam)

def find_lowest(hws,k,m,weights):
    '''gets weighted hw data and finds minimum, removes it and returns removed list
       with the index of removed homework.
    '''
    final_hw={}
    removed_hw={}
    for suid in hws.keys():
        weighted_hws=compute_assignment_scores(hws[suid],weights,k,m)
        min_hw_index=weighted_hws.index(min(weighted_hws))
        weighted_hws.remove(min(weighted_hws))
        final_hw[suid]=weighted_hws
        removed_hw[suid]=min_hw_index
    return(final_hw,removed_hw)

def calculate_final(final_hw,removed_hw,exams,m):
    '''calculates the final grade of students with 50% of overall homework and 50% of 
       overall exam grades. returns a dictionary of [suid]=[final grade]
    '''
    final_grades={}
    for suid in final_hw.keys():
        final_grades[suid]=sum(final_hw[suid])/(m-1)*0.5+sum(exams[suid])/2.*0.5
    return final_grades

def write_sorted(final_grades,output_file,removed_hw):
    '''Writes the final grades to output file also with the lowest hw # which is removed.
    '''
    sorted_final_grades = sorted(((value, key) for (key,value) in final_grades.items()),reverse=True)
    with open(output_file,'w') as f:
        for (grade,suid) in sorted_final_grades:
            f.write('{} {} {:6.3f}\n'.format(suid,removed_hw[suid],grade))

(hws,exams)=read_data(grades_file,m,k)
##read input data write to hws,exams
(f_hw,r_hw)=find_lowest(hws,k,m,weights)
##compute weighted homework grades, find lowest, remove it
final_grades=calculate_final(f_hw,r_hw,exams,m)
##calculate final grade from weighted hws and exams
write_sorted(final_grades,output_file,r_hw)
##write the results to output file
