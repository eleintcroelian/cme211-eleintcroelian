#include <vector>
#include <string>

class Stock
{
private:
    std::vector<double> price_vec;
    std::vector<double> dailyvec;
    std::string tckr;
    double meanreturn;
    double var;

public:
    /* public member variables */

    //constructor
    Stock(std::vector<double> price_vec, std::string tckr);

    //calculate daily return
    void dailyReturn(/*add args if neccecary*/);

    //calculate mean return
    void meanReturn(/*add args if neccecary*/);

    //calculate return variance
    void varReturn(/*add args if neccecary*/);

    //Print results
    void PrintResults();
    //Save results
    void SaveResults();
};
