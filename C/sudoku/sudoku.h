#ifndef _SUDOKU_
#define _SUDOKU_

#include <set>


class Sudoku {

private:
  int sizeOfSide;
  std::set<char> symbols;
  char **p_data;
  bool isSquare(int);

public:
  Sudoku(int sizeOfSide = 9, const char *symbols = "123456789") throw (int);
  Sudoku(const Sudoku& source);
  ~Sudoku();

  void setType(int sizeOfSide, const char *symbols) throw (int);
  int getSizeOfSide() const;
  const std::set<char>& getSymbols() const;
  char getAt(int x, int y) const throw (int);
  void setAt(int x, int y, char symbol) throw (int);
  bool isFilled() const;
  bool isSolved() const;
  
  friend std::ostream& operator<<(std::ostream& os, const Sudoku& sudOut);
  friend std::istream& operator>>(std::istream& is, Sudoku& sudIn);
  
  void test();
  
};

#endif

