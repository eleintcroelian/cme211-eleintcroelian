#ifndef SPARSE_HPP
#define SPARSE_HPP

#include <vector>

class SparseMatrix
{
public:
  std::vector<int> i_idx;
  std::vector<int> j_idx;
  std::vector<double> a;

private:
  int ncols;
  int nrows;
  bool CSRflag = false;

public:
  /* Method to modify sparse matrix dimensions */
  void Resize(int nrows, int ncols);

  /* Method to add entry to matrix in COO format */
  void AddEntry(int i, int j, double val);

  /* Method to convert COO matrix to CSR format using provided function */
  void ConvertToCSR();
};
#endif /* SPARSE_HPP */
