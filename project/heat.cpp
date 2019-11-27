#include <fstream>
#include <iostream>
#include <math.h>
#include <boost/multi_array.hpp>
#include "CGSolver.hpp"
#include "heat.hpp"

int HeatEquation2D::Setup(std::string inputfile)
{
    std::ifstream input_file;
    input_file.open(inputfile);
    if (input_file.is_open())
    {
        // updating input variables by reading from input file
        input_file >> this->length >> this->width >> this->h;
        input_file >> this->Tc >> this->Th;
        input_file.close();
        // nx is the number of nodes in x direction
        this->n_x = int(length / h) + 1;
        // ny is the number of nodes in y direction
        this->n_y = int(width / h) + 1;
        // number of unknows is equal to total nodes
        // minus boundary conditions
        this->n_unk = (n_x - 1) * (n_y - 2);
        // update the size of A matrix
        this->A.Resize(this->n_unk, this->n_unk);
        // update size of b vector and fill it with zeros
        this->b.resize((unsigned int)n_unk, 1);
        std::fill(this->b.begin(), this->b.end(), 0.);
        // update size of boundary condition vector which
        // contains a nonzero value for boundary nodes
        // and zero for an interior node
        this->BC.resize((unsigned int)n_y * (unsigned int)n_x, 1);
        std::fill(this->BC.begin(), this->BC.end(), 0.);
        // M is the node numbering matrix
        boost::multi_array<int, 2> M(boost::extents[n_y][n_x]);
        int count = 1;

        for (int i = 1; i < n_y - 1; i++)
        {
            for (int j = 0; j < n_x - 1; j++)
            {
                // starting from the bottom left unknown node, start numbering
                // nodes in row order
                M[i][j] = count;
                count++;
            }
        }
        for (int i = 1; i < n_y - 1; i++)
        {
            // fills the right most column which is used to find periodic BCs
            M[i][n_x - 1] = count;
            count++;
        }
        for (int j = 0; j < n_x; j++)
        {
            // Bottom boundary condition nodes
            M[n_y - 1][j] = count;
            count++;
        }
        for (int j = 0; j < n_x; j++)
        {
            // Top boundary conditions
            M[0][j] = count;
            count++;
        }
        for (int i = (n_y - 2) * n_x; i < (n_y - 1) * n_x; i++)
        {
            // Filling appropriate nodes in BC vector with isothermal BC
            BC[(unsigned int)i] = this->Th;
        }
        double k = 0.;
        for (int i = (n_y - 1) * n_x; i < n_y * n_x; i++)
        {
            // Filling appropriate nodes in BC vector with gaussian BC
            BC[(unsigned int)i] = -this->Tc * (exp(-10. * pow(k - this->length / 2., 2.)) - 2.);
            k = k + this->h;
        }
        // Building sparse matrix -A row by row
        int row = 0;
        for (int i = 1; i < n_y - 1; i++)
        {
            for (int j = 0; j < n_x - 1; j++)
            {
                // Adding 4*u(i,j)
                A.AddEntry(row, M[i][j] - 1, 4 / pow(h, 2));
                // Adding -u(i-1,j), if it is a boundary condition, it is added to -b vector
                if (M[i - 1][j] <= n_unk)
                {
                    A.AddEntry(row, M[i - 1][j] - 1, -1 / pow(h, 2));
                }
                else
                {
                    b[(size_t)row] = b[(size_t)row] + BC[(size_t)M[i - 1][j] - 1] / pow(h, 2);
                }
                // Adding -u(i+1,j), if it is a boundary condition, it is added to -b vector
                if (M[i + 1][j] <= n_unk)
                {
                    A.AddEntry(row, M[i + 1][j] - 1, -1 / pow(h, 2));
                }
                else
                {
                    b[(size_t)row] = b[(size_t)row] + BC[(size_t)M[i + 1][j] - 1] / pow(h, 2);
                }
                // Adding -u(i,j+1), if it is a periodic bc, corresponding node in same row is chosen
                if (M[i][j] % (n_x - 1) == 0)
                {
                    A.AddEntry(row, M[i][0] - 1, -1 / pow(h, 2));
                }
                else if (M[i][j + 1] <= n_unk)
                {
                    A.AddEntry(row, M[i][j + 1] - 1, -1 / pow(h, 2));
                }
                // Adding -u(i,j-1), if it is a periodic bc, corresponding node in same row is chosen
                if (M[i][j] % (n_x - 1) == 1)
                {
                    A.AddEntry(row, M[i][n_x - 2] - 1, -1 / pow(h, 2));
                }
                else if (M[i][j - 1] <= n_unk)
                {
                    A.AddEntry(row, M[i][j - 1] - 1, -1 / pow(h, 2));
                }
                row++;
            }
        }
        return 0;
    }
    else
    {
        std::cout << "Unable to open input file." << std::endl;
        return 1;
    }
}
int HeatEquation2D::Solve(std::string soln_prefix)
{   
    // initializing initial guess vector x and filling it with zeros
    std::vector<double> x;
    x.resize((unsigned int)this->n_unk, 1);
    std::fill(x.begin(), x.end(), 0.);
    std::cout << std::endl;
    // converting A to CSR format
    A.ConvertToCSR();
    // calling CGSolver to find x in place while writing it in output files
    int niter = CGSolver(this->A, x, this->b, soln_prefix, 1e-5);

    if (niter != -1)
    {
        // If solution converges, niter != -1
        return 0;
    }
    else
    {
        // Else, niter will be returned as -1
        return 1;
    }
}