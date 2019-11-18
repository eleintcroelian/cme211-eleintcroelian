//--design_0
//--As for Python, please list the includes in alphabetical order.
//--START
#include <iostream>
#include <fstream>
//--END

//--design_0
//--Good!
//--START
enum direction
/* Direction class representing 
where the user in maze is faced. */
{
    left,
    right,
    up,
    down
};
enum turn
/* Turn class to change direction of user.*/
{
    turn_left,
    turn_right,
    turn_back,
    turn_not
};
//--END
int main(int argc, char *argv[])
{
    if (argc < 3)
    {
        /* Confirms that appropriate command line 
        arguments were provided and if not provides 
        a usage message and exits. */
        std::cout << "Usage:" << std::endl
                  << "./mazesolver <maze file> <solution file>"
                  << std::endl;
        return 1;
    }

    std::ifstream f(argv[1]);
    if (f.is_open())
    {
        // Read the size of the data and make sure storage is sufficient
        int n_row, n_col;
        f >> n_row >> n_col;

        if (n_row > 1000 || n_col > 1000)
        /* Verifying that appropriate static array storage is available 
        for storing the maze. */
        {
            std::cout << "Not enough storage for the given maze file."
                      << std::endl;
            return 1;
        }

        int maze[1000][1000]; // Initialize an array with the max size
        for (int i = 0; i < n_row; i++)
        {
            for (int j = 0; j < n_col; j++)
            {
                maze[i][j] = 0; // Change all of its elements to 0
            }
        }
        int row;
        int column;
        while (f >> row >> column)
        {
            maze[row][column] = 1; // Grids with walls are assigned 1
        }
        f.close();
        int next_col_top;
        int entrance_index;
        for (int k = 0; k < n_col; k++)
        {
            /* Finds the maze entrance at the opening in the first 
            row and stores it as the first position in the
            solution file. */
            next_col_top = maze[0][k];
            if (next_col_top != 1)
            {
                entrance_index = k; //entrance index
            }
        }
        direction d = down;
        turn t = turn_not;
        int current_column = entrance_index;
        int current_row = 0;
        /* Start point is the entrance */
        int grid_right[2];
        int grid_left[2];
        int grid_ahead[2];
        int grid_behind[2];
        /* Initializing arrays to store grids around user */
        std::ofstream output;
        output.open(argv[2]);
        /* Open up a file to write with the name as 3rd argument */
        if (output.is_open())
        {
            output << current_row << ' ' << current_column
                   << std::endl;
            /* Write the entrance as the first line in solution */

            while (current_row != n_row - 1) //Loop until user reaches exit
            {
                switch (t)
                /* The turn direction command given from previous iteration is
                applied and direction is changed accordingly */

                {
                case turn_right:
                    switch (d)
                    {
                    case up:
                        d = right;
                        break;
                    case left:
                        d = up;
                        break;
                    case right:
                        d = down;
                        break;
                    case down:
                        d = left;
                        break;
                    }
                    break;
                case turn_left:
                    switch (d)
                    {
                    case up:
                        d = left;
                        break;
                    case left:
                        d = down;
                        break;
                    case right:
                        d = up;
                        break;
                    case down:
                        d = right;
                        break;
                    }
                    break;
                case turn_back:
                    switch (d)
                    {
                    case up:
                        d = down;
                        break;
                    case left:
                        d = right;
                        break;
                    case right:
                        d = left;
                        break;
                    case down:
                        d = up;
                        break;
                    }
                    break;
                case turn_not:
                    switch (d)
                    {
                    case up:
                        d = up;
                        break;
                    case left:
                        d = left;
                        break;
                    case right:
                        d = right;
                        break;
                    case down:
                        d = down;
                        break;
                    }
                    break;
                }
                switch (d)
                /* Depending on the direction user is facing, 
                the grids around it are stored */
                {
                case left:
                    grid_right[0] = current_row - 1;
                    grid_right[1] = current_column;
                    grid_left[0] = current_row + 1;
                    grid_left[1] = current_column;
                    grid_ahead[0] = current_row;
                    grid_ahead[1] = current_column - 1;
                    grid_behind[0] = current_row;
                    grid_behind[1] = current_column + 1;
                    break;
                case right:
                    grid_right[0] = current_row + 1;
                    grid_right[1] = current_column;
                    grid_left[0] = current_row - 1;
                    grid_left[1] = current_column;
                    grid_ahead[0] = current_row;
                    grid_ahead[1] = current_column + 1;
                    grid_behind[0] = current_row;
                    grid_behind[1] = current_column - 1;
                    break;
                case up:
                    grid_right[0] = current_row;
                    grid_right[1] = current_column + 1;
                    grid_left[0] = current_row;
                    grid_left[1] = current_column - 1;
                    grid_ahead[0] = current_row - 1;
                    grid_ahead[1] = current_column;
                    grid_behind[0] = current_row + 1;
                    grid_behind[1] = current_column;
                    break;
                case down:
                    grid_right[0] = current_row;
                    grid_right[1] = current_column - 1;
                    grid_left[0] = current_row;
                    grid_left[1] = current_column + 1;
                    grid_ahead[0] = current_row + 1;
                    grid_ahead[1] = current_column;
                    grid_behind[0] = current_row - 1;
                    grid_behind[1] = current_column;
                    break;
                }

                if (maze[grid_ahead[0]][grid_ahead[1]] != 1 &&
                    maze[grid_right[0]][grid_right[1]] == 1)
                /* If there is not a wall on the grid in front,
                    and if there is a wall at right side, keep 
                    walking straight. */
                {
                    current_row = grid_ahead[0];
                    current_column = grid_ahead[1];
                    t = turn_not;
                }
                else if (maze[grid_right[0]][grid_right[1]] != 1)
                /* Else, if there is no wall on right, go right
                    and turn right. */
                {
                    current_row = grid_right[0];
                    current_column = grid_right[1];
                    t = turn_right;
                }
                else if (maze[grid_left[0]][grid_left[1]] != 1)
                {
                    /* Else, if there is no wall on left, go left
                    and turn left. */
                    current_row = grid_left[0];
                    current_column = grid_left[1];
                    t = turn_left;
                }
                else if (maze[grid_behind[0]][grid_behind[1]] != 1)
                {
                    /* Else, go back and turn around. */
                    current_row = grid_behind[0];
                    current_column = grid_behind[1];
                    t = turn_back;
                }
                output << current_row << ' ' << current_column
                       << std::endl;
                /* Write the solution step found to the solution file */
            }
            output.close();
        }
    }
    return 0;
}

//--design_0
//--Good work! The code was a little long. Here's a neat simplification
//--for the turning mechanism. Suppose we enumerate in clockwise direction,
//--i.e., left, up, right, down.
//--Since these are internally represented by integers 0, 1, 2, 3, we can
//--simply add 1 to turn right (and subtract 1 to turn left).
//--The only thing we need to watch out for is turning 3 into 0, but we can
//--handle that case by using the modulo (%) operator: turning right is
//--then as easy as
//--  (d + 1) % 4
//--Similarly, turning left can be done with (d - 1) % 4. But since some
//--compilers return a negative number when a negative argument is passed to
//--to the module operator, we may use the equivalent
//--  (d + 3) % 4
//--to turn left.
//--You may also want to break down the long passage of code using functions
//--(not expected for this assignment).
//--Can you think of other ways of making the code more concise?
//--Using enum was a good start!
//--END
