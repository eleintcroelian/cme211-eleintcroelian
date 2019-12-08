#include <vector>
#include <iostream>
#include <cmath>
std::vector<double> csr_vec_mult(const std::vector<double> &val,
                                 const std::vector<int> &row_idx,
                                 const std::vector<int> &col_idx,
                                 const std::vector<double> &x)
{
    const auto n = x.size();
    std::vector<double> y(n, 0.);
    for (unsigned int i = 0; i < n; i++)
    {
        // for each row i
        for (unsigned int j = static_cast<unsigned int>(row_idx[i]);
             j < static_cast<unsigned int>(row_idx[i + 1]); j++)
        {
            // variables with size_type and int are converted to unsigned int
            y[i] = y[i] + val[j] * x[static_cast<unsigned int>(col_idx[j])];
            // value is indexed with row_idx and x is indexed with col_idx
        }
    }
    return y;
}
std::vector<double> csr_T_vec_mult(const std::vector<double> &val,
                                   const std::vector<int> &row_idx,
                                   const std::vector<int> &col_idx,
                                   const std::vector<double> &x)
{
    auto n = x.size();
    std::vector<double> y(n, 0.);
    for (unsigned int j = 0; j < static_cast<unsigned int>(n); j++)
    {
        // variables with size_type and int are converted to unsigned int
        for (unsigned int i = static_cast<unsigned int>(row_idx[j]);
             i < static_cast<unsigned int>(row_idx[j + 1]); i++)
        {
            // Same as the above function, transpose of CSR matrix is 
            // found by switching indexes used for x and val
            y[static_cast<unsigned int>(col_idx[i])] =
                y[static_cast<unsigned int>(col_idx[i])] + val[i] * x[j];
        }
    }
    return y;
}

std::vector<double> vec_subtract(const std::vector<double> &a,
                                 const std::vector<double> &b)
{
    auto n = a.size();
    std::vector<double> y(n);
    for (unsigned int i = 0; i < static_cast<unsigned int>(n); i++)
    {
        // Elementvise subtraction
        y[i] = a[i] - b[i];
    }
    return y;
}

std::vector<double> vec_add(const std::vector<double> &a,
                            const std::vector<double> &b)
{
    auto n = a.size();
    std::vector<double> y(n);
    for (unsigned int i = 0; i < static_cast<unsigned int>(n); i++)
    {
        // Elementvise addition
        y[i] = a[i] + b[i];
    }
    return y;
}

double l2norm(const std::vector<double> &a)
{
    auto n = a.size();
    double norm = 0.;
    for (unsigned int i = 0; i < n; i++)
    {
        norm = norm + a[i] * a[i];
        //Summing squares of each element
    }
    return std::sqrt(norm);
    //Square root of the sum is L2 norm
}

double vec_T_vec_mult(const std::vector<double> &a,
                      const std::vector<double> &b)
{
    auto n = a.size();
    double y = 0.;
    for (unsigned int i = 0; i < static_cast<unsigned int>(n); i++)
    {
        y = y + a[i] * b[i];
        //aT x b
    }
    return y;
}
std::vector<double> vec_sca_mult(const double &b,
                                 const std::vector<double> &a)
{
    auto n = a.size();
    std::vector<double> y(n);
    for (unsigned int i = 0; i < static_cast<unsigned int>(n); i++)
    {
        y[i] = b * a[i];
        // b x a where b is a scalar and a is a vector
    }
    return y;
}