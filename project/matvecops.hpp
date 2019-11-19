#ifndef MATVECOPS_HPP
#define MATVECOPS_HPP

#include <vector>

/* Function that implements the CG algorithm for a linear system
 *
 * Ax = b
 *
 * where A is in CSR format.  The starting guess for the solution
 * is provided in x, and the solver runs a maximum number of iterations
 * equal to the size of the linear system.  Function returns the
 * number of iterations to converge the solution to the specified
 * tolerance, or -1 if the solver did not converge.
 */

std::vector<double> csr_vec_mult(std::vector<double> val,
                                 std::vector<int> row_idx,
                                 std::vector<int> col_idx,
                                 std::vector<double> x);

std::vector<double> csr_T_vec_mult(std::vector<double> val,
                                   std::vector<int> row_idx,
                                   std::vector<int> col_idx,
                                   std::vector<double> x);

std::vector<double> vec_subtract(std::vector<double> a,
                                 std::vector<double> b);

std::vector<double> vec_add(std::vector<double> a,
                            std::vector<double> b);

double vec_T_vec_mult(std::vector<double> a,
                      std::vector<double> b);

std::vector<double> vec_sca_mult(double b,
                                 std::vector<double> a);

double l2norm(std::vector<double> a);

#endif /* MATVECOPS_HPP */