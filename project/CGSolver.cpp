#include <iostream>
#include <fstream>
#include <vector>
#include <cmath>
#include "matvecops.hpp"
#include "CGSolver.hpp"

int CGSolver(std::vector<double> &val,
             std::vector<int> &row_ptr,
             std::vector<int> &col_idx,
             std::vector<double> &b,
             std::vector<double> &x,
             double tol)
{
    std::vector<double> Ax = csr_vec_mult(val, row_ptr, col_idx, x);
    std::vector<double> r_0 = vec_subtract(b, Ax);
    std::vector<double> x_next;
    std::vector<double> r_next;
    std::vector<double> Ap_0;
    std::vector<double> p_0 = r_0;
    std::vector<double> p_next;
    double r_0_norm = l2norm(r_0);
    double r_next_norm;
    int niter = 0;
    int nitermax = 50;
    double alpha;
    double beta;
    while (niter < nitermax)
    {
        niter++;
        alpha = vec_T_vec_mult(r_0, r_0) / vec_T_vec_mult(p_0, csr_vec_mult(val, row_ptr, col_idx, p_0));
        x_next = vec_add(x, vec_sca_mult(alpha, p_0));
        Ap_0 = csr_vec_mult(val, row_ptr, col_idx, p_0);
        r_next = vec_subtract(r_0, vec_sca_mult(alpha, Ap_0));
        r_next_norm = l2norm(r_next);
        double criteria = r_next_norm - r_0_norm;
        if (std::abs (criteria) < tol)
        {
            break;
        }
        beta = vec_T_vec_mult(r_next, r_next) / vec_T_vec_mult(r_0, r_0);
        p_next = vec_add(r_next, vec_sca_mult(beta, p_0));
        p_0 = p_next;
        x = x_next;
        r_0 = r_next;
        r_0_norm = l2norm(r_0);
    }
    if (niter<nitermax)
    {
        return niter;
    }
    else
    {
        return -1;
    }
}