#include <vector>
#include <iostream>
#include <cmath>
std::vector<double> csr_vec_mult(std::vector<double> val,
                                 std::vector<int> row_idx,
                                 std::vector<int> col_idx,
                                 std::vector<double> x)
{
    const auto n = x.size();
    std::vector<double> y(n, 0.);
    for (unsigned int i = 0; i < n; i++)
    {
        for (unsigned int j = static_cast<unsigned int>(row_idx[i]); j < static_cast<unsigned int>(row_idx[i + 1]); j++)
        {
            y[i] = y[i] + val[j] * x[static_cast<unsigned int>(col_idx[j])];
        }
    }
    return y;
}

std::vector<double> csr_T_vec_mult(std::vector<double> val,
                                   std::vector<int> row_idx,
                                   std::vector<int> col_idx,
                                   std::vector<double> x)
{
    auto n = x.size();
    std::vector<double> y(n, 0.);
    for (unsigned int j = 0; j < static_cast<unsigned int>(n); j++)
    {
        for (unsigned int i = static_cast<unsigned int>(row_idx[j]); i < static_cast<unsigned int>(row_idx[j + 1]); i++)
        {
            y[static_cast<unsigned int>(col_idx[i])] = y[static_cast<unsigned int>(col_idx[i])] + val[i] * x[j];
        }
    }
    return y;
}

std::vector<double> vec_subtract(std::vector<double> a,
                                 std::vector<double> b)
{
    auto n = a.size();
    std::vector<double> y(n);
    for (unsigned int i = 0; i < static_cast<unsigned int>(n); i++)
    {
        y[i] = a[i] - b[i];
    }
    return y;
}

std::vector<double> vec_add(std::vector<double> a,
                            std::vector<double> b)
{
    auto n = a.size();
    std::vector<double> y(n);
    for (unsigned int i = 0; i < static_cast<unsigned int>(n); i++)
    {
        y[i] = a[i] + b[i];
    }
    return y;
}

double l2norm(std::vector<double> a)
{
    auto n = a.size();
    double norm = 0.;
    for (unsigned int i = 0; i < n; i++)
    {
        norm = norm + a[i] * a[i];
    }
    return std::sqrt(norm);
}

double vec_T_vec_mult(std::vector<double> a,
                      std::vector<double> b)
{
    auto n = a.size();
    double y = 0.;
    for (unsigned int i = 0; i < static_cast<unsigned int>(n); i++)
    {
        y = y + a[i] * b[i];
    }
    return y;
}
std::vector<double> vec_sca_mult(double b,
                                 std::vector<double> a)
{
    auto n = a.size();
    std::vector<double> y(n);
    for (unsigned int i = 0; i < static_cast<unsigned int>(n); i++)
    {
        y[i] = b*a[i];
    }
    return y;
}