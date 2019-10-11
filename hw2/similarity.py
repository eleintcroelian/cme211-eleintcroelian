import copy,math,sys,time       # Importing the modules to be used.

t0 = time.time()                # Starting the timer

if len(sys.argv) >4 or len(sys.argv)<3:
    # Checking if the input arguments are as desired.
    print('Usage: $python3 similarity.py <data_file> <output_file>\
 [user_thresh (default = 5)]\n')
    sys.exit(0)
data_file=copy.copy(sys.argv[1])
output_file=copy.copy(sys.argv[2])

if len(sys.argv)==4: # If the thresh value is available from user, assign it
    user_thresh=int(copy.copy(sys.argv[3]))
else:                # If not, its the default value
    user_thresh=5

def assign_to_dict_i_jk(file,i,j,k):

   # Gets the file destination as input, reads the file line by line and
   # creates a dictionary with keys as the i th column and a list containing
   # j th column and k th column as values. If the dictionary contains the key
   # already, the j th column and the k th column are appended to the list.
   # If the line read is an empty line, it is skipped. Returns the
   # dictionary as output after all lines are read.

    dict_data={}
    with open(file,'r') as f:
        for line in f:
            if line=='\n':
                continue
            if int(line.split()[i]) in dict_data:
                dict_data[int(line.split()[i])].append(int(line.split()[j]))
                dict_data[int(line.split()[i])].append(int(line.split()[k]))
            else:
                dict_data[int(line.split()[i])]=[int(line.split()[j]),
                          int(line.split()[k])]
    return dict_data

def assigntodict_user_movie_to_rating(file):
   # Gets the file destination as input, reads the file line by line and
   # creates a dictionary with keys as a tuple of first column and second
   # column (user-movie ids) with third column as values (ratings).
   # If the line read is an empty line, it is skipped. Returns the
   # dictionary as output after all lines are read.
    dict_data={}
    with open(file,'r') as f:
        for line in f:
            if line=='\n':
                break
            dict_data[(int(line.split()[0]),int(line.split()[1]))]=\
            int(line.split()[2])
    return dict_data

def cosinesimilarity(users_a,users_b,dict_data_user_movie,avg_a,avg_b,
                     movie_a,movie_b):
  # Gets user ids who rated movies a and b and the ratings respectively,
  # the average ratings and the ids of movies a and b as input, giving the
  # cosine similarity P_a_b as output. If there is a zero denominator,
  # the value is returned as 0.0.
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

dict_user=assign_to_dict_i_jk(data_file,0,1,2)
# Creates a dictionary with {user id}:[movie id-rating - movie id-rating...]
dict_data_movies=assign_to_dict_i_jk(data_file,1,0,2)
# Creates a dictionary with {movie id}:[user id-rating - user id-rating...]
dict_data_users=assign_to_dict_i_jk(data_file,1,0,2)
# Creates a dictionary with {movie id}:[user id-rating - user id-rating...]
dict_data_ratings=assign_to_dict_i_jk(data_file,1,0,2)
# Creates a dictionary with {movie id}:[user id-rating - user id-rating...]
dict_data_avg=assign_to_dict_i_jk(data_file,1,0,2)
# Creates a dictionary with {movie id}:[user id-rating - user id-rating...]
dict_data_user_movie=assigntodict_user_movie_to_rating(data_file)
# Creates a dictionary with {(user id - movie id)}: rating
for movies in dict_data_users:
    dict_data_users[movies]=set(dict_data_users[movies][::2])
    # eliminates movie ids from the dictionary value and converts to a set
for movies in dict_data_ratings:
    dict_data_ratings[movies]=dict_data_ratings[movies][1::2]
    #eliminates user ids from the dictionary
for movies in dict_data_avg:
    dict_data_avg[movies]=sum(dict_data_avg[movies][1::2])/\
    (len(dict_data_avg[movies][1::2]))
    #calculates the average of all ratings for each key (movie id)

output=open(output_file,'w')

for movie_a in sorted(dict_data_movies.keys()):
			       #Looping over movies reviewed
    output.write(str(movie_a)) #writes the movie id to file
    P_a_b_current=-2 #initializing similarity coefficient and common user
    common_user_current=0
    most_similar=-1 #initializing the most similar movie id
    if len(dict_data_users[movie_a])<user_thresh:
        #skip movie if there is not enough reviews
        output.write("\n")
        continue
    for movie_b in dict_data_movies.keys(): #Looping over movies again
        if movie_a==movie_b:
            #Skip the same movie to avoid comparing it by itself
            continue
        common_user_number=len(dict_data_users[movie_a] &\
                               dict_data_users[movie_b])
        #number of common users rated both movies
        if common_user_number<user_thresh:
        #skip this comparison if there are not enough common users rated
            continue
        else:
            P_a_b_new=cosinesimilarity(dict_data_users[movie_a],
            dict_data_users[movie_b],dict_data_user_movie,
            dict_data_avg[movie_a],
            dict_data_avg[movie_b],movie_a,movie_b)
            #get similarity coefficient
        if P_a_b_new>P_a_b_current:
            #if the coefficient is bigger than the previous comparison,
            #assign it as the highest and mark the movie compared as most
            #similar
            P_a_b_current=P_a_b_new
            most_similar=movie_b
            common_user_current=common_user_number
    if P_a_b_current>0 and common_user_current>=user_thresh\
                       and most_similar != -1:
        #check if there is a similar movie with enough common users, if yes,
        #write (most similar movie id, similarity coef.,# of common users )
        output.write(" ("+str(most_similar)+\
        ", "+str(round(P_a_b_current,2))+\
        ", "+str(common_user_current)+") \n")
    else:
        output.write("\n")
output.close()
t1=time.time()
#report the results
print('Input MovieLens file: '+data_file)
print('Output file for similarity data: '+output_file)
print('Minimum number of common users: {}'.format(user_thresh))
print('Read {} lines with total of {} movies and {} users'\
      .format(len(dict_data_user_movie), len(dict_data_avg),len(dict_user)))
print('Computed similarities in {} seconds'.format(round(t1-t0,3)))
