#include <vector>
#include <iostream>
#include <cmath>
#include "sparse.hpp"
#include "COO2CSR.hpp"

void SparseMatrix::Resize(int nrows, int ncols)
{
    this->nrows = nrows; // updates row and column numbers
    this->ncols = ncols;
}
void SparseMatrix::AddEntry(int i, int j, double val)
{
    i_idx.push_back(i); //adds row and column indices and the value
    j_idx.push_back(j);
    a.push_back(val);
}
void SparseMatrix::ConvertToCSR()
{
    COO2CSR(a, i_idx, j_idx); // using provided function to convert
    CSRflag = true;           // matrix from COO to CSR format
}