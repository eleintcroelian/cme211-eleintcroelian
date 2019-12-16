• What data members (attributes, variables) does the Stock class have? Are they public
or private, and justify your choice.

Stock class has 5 private data members:

std::vector<double> price_vec;
std::vector<double> dailyvec;
std::string tckr;
double meanreturn;
double var;

I preferred to encapsulate all the data as private members in Stock, to avoid
any intrusion of the class's users while the calculations are held.

• What arguments do your dailyReturn and meanReturn functions accept, and why?

None of the methods, including dailyReturn and meanReturn do not accept any arguments.
All the variables are stored inside the class and calculations are held using local
variables and these stored private members. This eases the use of the class since no type
or size declarations are required using the methods while errors due to inputs are avoided.

• What considerations did you make to minimize repetitive calls?

I have written Stock.cpp fully encapsulated, thus there are no repetitions of data structure creation. All of the vectors used are created once, and then used multiple times if necessary.
This way, there is no copying etc.

• Discuss whether the keyword new appears in your program, and why this is appropriate.

new does not appear in the program but the Vector class is used in which new and delete[] are used automatically. Memory management of the program should not be a matter for the user this way.

• Discuss ONE of the following: (1) an aspect of your program that you are proud of or
(2) a possible improvement to your program, or (3) if you did not finish the assignment,
the next step needed to fix the program.

(2) Error handling is skipped due to time limit and assumptions in the exam handout. However, a proper use of this program would require many error handling steps to be included. Multiple flags can be implemented to determine which state the class is at in a given point. At this time,
the squence of the code requires these steps after constructing the class:

    stock.dailyReturn();
    stock.meanReturn();
    stock.varReturn();
    stock.PrintResults(); 

#--writeup_0
#--Good consideration! A general way to require these functions
#--to be called is to call them in the constructor. But since
#--we outlined the calculations step in the provided main.cpp,
#--this wasn't necessary.
#--START
However, if one these steps are missed, the results would be inaccurate. Thus, a check for the any missing step would be critical. Also, a check for the memory allocation with -fsanitizer would be helpful.
#--END

I have used a makefile which uses these commands:

g++ -c -o main.o main.cpp  -O3 -std=c++11 -Wall -Wextra -Wconversion
g++ -c -o Stock.o Stock.cpp  -O3 -std=c++11 -Wall -Wextra -Wconversion
g++ -o main main.o Stock.o

#--writeup_0
#--Readme: 15/15
#--END
