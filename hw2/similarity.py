import copy,math,sys,time                               #__ Importing the modules to be used.

t0 = time.time()                #__ Starting the timer

if len(sys.argv) >4 or len(sys.argv)<3: #__ Checking if the input arguments are as desired.
    print('Usage: $python3 similarity.py <data_file> <output_file> [user_thresh (default = 5)]\n')
    sys.exit(0)
data_file=copy.copy(sys.argv[1])
output_file=copy.copy(sys.argv[2])
if len(sys.argv)==4:
    user_thresh=int(copy.copy(sys.argv[3]))
else:
    user_thresh=5

#data_file="/home/mc/Dropbox/stanford classes/Fall 19/CME 211/hw2/ml-100k/u.data"
#output_file="/home/mc/Dropbox/stanford classes/Fall 19/CME 211/hw2/ml-100k/output.txt"
#user_thresh=5

def assigntodict_movie_to_user_rating(file):
    dict_data={}
    with open(file) as f:
        for line in f:
            if line=='\n':
                break
            if int(line.split()[1]) in dict_data:
                dict_data[int(line.split()[1])].append(int(line.split()[0]))
                dict_data[int(line.split()[1])].append(int(line.split()[2]))
            else:
                dict_data[int(line.split()[1])]=[int(line.split()[0]),int(line.split()[2])]
    return dict_data

def assigntodict_user_to_movie_rating(file):
    dict_data={}
    with open(file) as f:
        for line in f:
            if line=='\n':
                break
            if int(line.split()[0]) in dict_data:
                dict_data[int(line.split()[0])].append((int(line.split()[1]),int(line.split()[2])))
            else:
                dict_data[int(line.split()[0])]=[(int(line.split()[1]),int(line.split()[2]))]
    return dict_data

def assigntodict_user_movie_to_rating(file):
    dict_data={}
    with open(file) as f:
        for line in f:
            if line=='\n':
                break
            dict_data[(int(line.split()[0]),int(line.split()[1]))]=int(line.split()[2])
    return dict_data

def cosinesimilarity(users_a,users_b,dict_data_user_movie,avg_a,avg_b,movie_a,movie_b):
	sum1=0
	sum2=0
	sum3=0
	for common_user in users_a & users_b:
		r_a=dict_data_user_movie[(common_user,movie_a)]
		r_b=dict_data_user_movie[(common_user,movie_b)]
		sum1=sum1+(r_a-avg_a)*(r_b-avg_b)
		sum2=sum2+(r_a-avg_a)*(r_a-avg_a)
		sum3=sum3+(r_b-avg_b)*(r_b-avg_b)
	try:
		P_a_b=sum1/math.sqrt(sum2*sum3)
	except ZeroDivisionError:
		P_a_b=0
	return P_a_b

dict_user=assigntodict_user_to_movie_rating(data_file)
dict_data=assigntodict_movie_to_user_rating(data_file)
dict_data_users=assigntodict_movie_to_user_rating(data_file)
dict_data_ratings=assigntodict_movie_to_user_rating(data_file)
dict_data_avg=assigntodict_movie_to_user_rating(data_file)
dict_data_user_movie=assigntodict_user_movie_to_rating(data_file)

for movies in dict_data_users:
    dict_data_users[movies]=set(dict_data_users[movies][::2])
for movies in dict_data:
    dict_data[movies]=tuple(dict_data[movies])
for movies in dict_data_ratings:
    dict_data_ratings[movies]=dict_data_ratings[movies][1::2]
for movies in dict_data_avg:
    dict_data_avg[movies]=sum(dict_data_avg[movies][1::2])/(len(dict_data_avg[movies][1::2]))
output=open(output_file,'w')
for movie_a in sorted(dict_data.keys()): #Looping over movies reviewed
    output.write(str(movie_a))
    P_a_b_current=-2
    common_user_current=0
    most_similar=-1
    if len(dict_data_users[movie_a])<user_thresh:
        output.write("\n")
        continue
    for movie_b in dict_data.keys(): #Looping over movies again
        if movie_a==movie_b: #Skip the same movie to avoid comparing it by itself
            continue
        common_user_number=len(dict_data_users[movie_a] & dict_data_users[movie_b])
        if common_user_number<user_thresh:
            continue
        else:
            P_a_b_new=cosinesimilarity(dict_data_users[movie_a],
            dict_data_users[movie_b],dict_data_user_movie,dict_data_avg[movie_a],
            dict_data_avg[movie_b],movie_a,movie_b)
        if P_a_b_new>P_a_b_current:
            P_a_b_current=P_a_b_new
            most_similar=movie_b
            common_user_current=common_user_number
    if P_a_b_current>0 and common_user_current>user_thresh and most_similar != -1:
        output.write(" ("+str(most_similar)+\
        ", "+str(round(P_a_b_current,5))+\
        ", "+str(common_user_current)+") \n")
    else:
        output.write("\n")
output.close()
t1=time.time()
print('Elapsed Time = {}'.format(t1-t0))


