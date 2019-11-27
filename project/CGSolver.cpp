#include <iostream>
#include <fstream>
#include <fstream>
#include <vector>
#include <cmath>
#include <stdio.h>
#include <sstream>
#include <iomanip>
#include "matvecops.hpp"
#include "CGSolver.hpp"
#include "sparse.hpp"

int CGSolver(SparseMatrix A,
             std::vector<double> &x,
             std::vector<double> b,
             std::string soln_prefix,
             double tol)
{
    // Ax is the matrix times initial guess
    std::vector<double> Ax = csr_vec_mult(A.a, A.i_idx, A.j_idx, x);
    // r0 is the initial residual
    std::vector<double> r_0 = vec_subtract(b, Ax);
    // Initializing variables
    std::vector<double> x_next;
    std::vector<double> r_next;
    std::vector<double> Ap_0;
    std::vector<double> p_0 = r_0;
    std::vector<double> p_next;
    double r_next_norm;
    int niter = 0;
    // nitermax is the maximum iterations allowed equal to size of linear
    // system
    int nitermax = static_cast<int>(x.size());
    double alpha;
    double beta;

    while (niter < nitermax + 1)
    {
        //update current iteration number
        niter++;
        // alpha found with (rnT rn)/(pnT A pn) where rn is r0 and pn is o0
        alpha = vec_T_vec_mult(r_0, r_0) /
                vec_T_vec_mult(p_0, csr_vec_mult(A.a, A.i_idx, A.j_idx, p_0));
        // next guess for x is calculated
        x_next = vec_add(x, vec_sca_mult(alpha, p_0));
        // matrix times p_0 is found
        Ap_0 = csr_vec_mult(A.a, A.i_idx, A.j_idx, p_0);
        // next residual is r0-alpha*p_n
        r_next = vec_subtract(r_0, vec_sca_mult(alpha, Ap_0));
        // norm is found for updated residual
        r_next_norm = l2norm(r_next);
        // criteria is the norm of next residual, which should
        // approach to zero if solution is converging
        if (((niter % 10 == 0) or (niter == 1)) and (r_next_norm > tol))
        {
            // writes results for first and in every 10 iterations
            // to a file with prefix taken as input
            std::stringstream outputstream;
            outputstream << std::setw(4) << std::setfill('0') << niter;
            std::string outputname = soln_prefix + outputstream.str() + ".txt";
            std::ofstream output(outputname);
            for (size_t i = 0; i < (x.size()); i++)
            {
                output << x_next[i] << std::endl;
            }
        }
        if (r_next_norm < tol)
        {
            // If solution is close enough, update x and
            // break loop, write the results
            std::stringstream outputstream;
            outputstream << std::setw(4) << std::setfill('0') << niter;
            std::string outputname = soln_prefix + outputstream.str() + ".txt";
            std::ofstream output(outputname);
            x = x_next;
            for (size_t i = 0; i < (x.size()); i++)
            {
                output << x_next[i] << std::endl;
            }
            break;
        }
        // Else, find beta and pn+1 for next iteration
        beta = vec_T_vec_mult(r_next, r_next) / vec_T_vec_mult(r_0, r_0);
        p_next = vec_add(r_next, vec_sca_mult(beta, p_0));
        // Update p_0,x,r_0, initial guesses of next iteration
        p_0 = p_next;
        x = x_next;
        r_0 = r_next;
    }
    if (niter < nitermax + 1)
    {
        return niter;
        // If solver converges before maximum iteration + 1
        // is reached, returns number of iterations
    }
    else
    {
        // Else, returns -1
        return -1;
    }
}