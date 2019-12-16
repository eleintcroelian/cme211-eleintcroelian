#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include "Stock.hpp"

Stock::Stock(std::vector<double> price_vec, std::string tckr)
{
    this->price_vec = price_vec;
    this->tckr = tckr;
}
void Stock::dailyReturn()
{
    double p_t;
    double p_t_p;
    for (unsigned int i = 1; i != this->price_vec.size(); i++)
    {
        p_t = price_vec[i];
        p_t_p = price_vec[i - 1];
        this->dailyvec.push_back((p_t - p_t_p) / p_t_p);
    }
}

void Stock::meanReturn()
{
    double avg = 0.;
    for (const auto &i : this->dailyvec)
        avg += i;
    this->meanreturn = avg / (double)this->dailyvec.size();
}

void Stock::varReturn()
{
    int n = (int)this->dailyvec.size();
    double sum = 0.;
//--functionality_1
//--Should be summing over every element of dailyvec rather than
//--only n-1 of them (note the sum in Equation 3 starts from 0).
//--START
    for (unsigned int i = 0; i != this->dailyvec.size() - 1; i++)
//--END
    {
        sum += (this->dailyvec[i] - this->meanreturn) * (this->dailyvec[i] - this->meanreturn);
    }
    this->var = sum / (n - 1);
}

void Stock::PrintResults()
{
    std::cout << this->tckr << std::endl;
    std::cout << this->meanreturn << std::endl;
    std::cout << this->var << std::endl;
}

void Stock::SaveResults()
{

    std::ofstream resultfile ("results.txt");
    resultfile << this->tckr << std::endl;
    resultfile << this->meanreturn << std::endl;
    resultfile << this->var << std::endl;
    resultfile.close();

}

//--design_0
//--Good use of printing and save methods.
//--END

//--design_0
//--Excellent.
//--Coding: 59/60
//--END
