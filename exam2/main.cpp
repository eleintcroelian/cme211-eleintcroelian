#include <vector>
#include <string>
#include <fstream>
#include <iostream>

#include "Stock.hpp"

int main(int argc, char *argv[])
{

    std::ifstream f(argv[1]);
    if (f.is_open())
    {
        double data;
        std::vector<double> data_vector;
        while (f >> data)
        {
            data_vector.push_back(data);
        }

        std::string tckr= argv[2];

        Stock stock(data_vector,tckr);

        stock.dailyReturn();
        stock.meanReturn();
        stock.varReturn();
        stock.PrintResults();
        //std::cout << data_vector.size() << std::endl;
    

    }
    /* Import prices to std::vector<double> */

    /* Call the Stock class constructor */

    /* Perform reqired calculations */

    /* Write out to results.txt */
}
