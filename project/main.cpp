#include <iostream>
#include <fstream>
#include <iomanip>
#include "COO2CSR.hpp"
#include "matvecops.hpp"
#include "CGSolver.hpp"
#include <vector>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    if (argc < 3)
    {
        /* Confirms that appropriate command line 
        arguments were provided and if not provides 
        a usage message and exits. */
        std::cout << "Usage:" << std::endl
                  << "./main <input matrix file name>"
                  << " <output solution file name>"
                  << std::endl;
        return 1;
    }
    std::ifstream f(argv[1]);
    if (f.is_open())
    {
        unsigned int n;
        unsigned int m;
        f >> n >> m;
        // First line of COO matrix contains the matrix size nxm
        std::vector<int> i_idx;
        std::vector<int> j_idx;
        std::vector<double> val;
        int row, col;
        double value;
        while (f >> row >> col >> value)
        {
            // Other lines contain row and column numbers
            // of nonzero terms of matrix and they are stored
            // in vectors
            i_idx.push_back(row);
            j_idx.push_back(col);
            val.push_back(value);
        }
        COO2CSR(val, i_idx, j_idx);
        // COO matrix is converted to CSR
        std::vector<double> b(n, 0.);
        std::vector<double> x(n, 1.);
        // b is the right hand side and x is the initial guess
        double tol = 1e-5;
        // tol is the tolerance for how close solution needs to be 
        // to the exact solution
        int niter = CGSolver(val, i_idx, j_idx, b, x, tol);
        // Matrix is solved by CGSolver and the number of iterations
        // for convergence is returned. If matrix did not converge,
        // return value is -1
        if (niter == -1)
        {
            std::cout << "CGSolver Failed to converge." << std::endl;
            return 0;
            // If solver does not converge, exits
        }
        else
        {
            std::cout << "SUCCESS: CG solver converged in " << niter
                      << " iterations." << std::endl;
        }
        //Solution is written to the file specified as 2nd input argument
        std::ofstream solution;
        solution.open(argv[2]);
        if (solution.is_open())
        {
            // format is scientific notation with 4 decimal places
            solution << std::scientific;
            solution << std::setprecision(4);
            for (unsigned int n = 0; n < x.size(); n++)
            {
                solution << x[n] << std::scientific << std::endl;
            }
            solution.close();
        }
    f.close();
    }
    return 0;
}