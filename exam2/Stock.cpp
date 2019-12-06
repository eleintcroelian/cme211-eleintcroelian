#include <iostream>
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
    for (auto &i : this->dailyvec)
        avg += i;
    this->meanreturn = avg / (double)this->dailyvec.size();
}

void Stock::varReturn()
{
    int n = (int)this->dailyvec.size();
    //std::cout << n << std::endl;
    double sum = 0.;
    for (unsigned int i = 0; i != this->dailyvec.size() - 1; i++)
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