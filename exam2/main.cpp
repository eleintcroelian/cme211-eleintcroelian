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
        // Reading the input file
        double data;
        std::vector<double> data_vector;
        while (f >> data)
        {
            data_vector.push_back(data);
        }
        f.close();
        std::string tckr = argv[2];
        Stock stock(data_vector, tckr); // Constructing the class
        stock.dailyReturn();            // Calculating daily returns
        stock.meanReturn();             // Calculating mean returns
        stock.varReturn();              // Calculating variance of returns
        stock.SaveResults();            // Saves results in results.txt
        return 0;
    }
    f.close();
    return 1;
}