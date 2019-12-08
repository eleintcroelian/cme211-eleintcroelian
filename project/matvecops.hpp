#ifndef MATVECOPS_HPP
#define MATVECOPS_HPP
#include <vector>

/* Function for a matrix times vector operation(Ax=y) for 
   a CSR matrix and a vector. Gets CSR matrix vectors and 
   x as input and returns the resultant vector y.
 */

std::vector<double> csr_vec_mult(const std::vector<double> &val,
                                 const std::vector<int> &row_idx,
                                 const std::vector<int> &col_idx,
                                 const std::vector<double> &x);
/* Function for a transpose of matrix times vector operation(Ax=y) 
    for a CSR matrix and a vector. Gets CSR matrix vectors and 
    x as input and returns the resultant vector y.
 */
std::vector<double> csr_T_vec_mult(const std::vector<double> &val,
                                   const std::vector<int> &row_idx,
                                   const std::vector<int> &col_idx,
                                   const std::vector<double> &x);
/* Function for elementvise subtraction of two vectors (a - b = y).
    Gets a and b as input vectors and outputs y, the resultant 
    vector.
 */
std::vector<double> vec_subtract(const std::vector<double> &a,
                                 const std::vector<double> &b);
/* Function for elementvise addition of two vectors (a + b = y).
    Gets a and b as input vectors and outputs y, the resultant 
    vector.
 */
std::vector<double> vec_add(const std::vector<double> &a,
                            const std::vector<double> &b);
/* Function for transpose of vector times vector (a_T x b = y).
    Gets a and b as input vectors and outputs y, the resultant 
    scalar.
 */
double vec_T_vec_mult(const std::vector<double> &a,
                      const std::vector<double> &b);
/* Function for multiplication of a vector by a scalar (b x a = y.
    Gets a as input vector and b as scalar input, outputs y, the 
    resultant vector.
 */
std::vector<double> vec_sca_mult(const double &b,
                                 const std::vector<double> &a);
/* Function for l2 norm of a vector. Gets a as input vector outputs
    norm.
 */

double l2norm(const std::vector<double> &a);

#endif /* MATVECOPS_HPP */