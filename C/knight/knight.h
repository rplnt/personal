#ifndef KNIGHT_H
#define KNIGHT_H
#include <iostream>
#include <vector>

#define CHECK

class Knight{
  public:
    Knight(int);
    bool runTour(int,int);
    bool checkTour(int**, int);
    int** getmoves();
    void clean(int);
    friend std::ostream& operator <<(std::ostream&, const Knight&);
    friend bool operator < (const std::vector<int>&, const std::vector<int>&);
    int nextstep(const int,const int);
    bool isOccupied(const int,const int);
    ~Knight();
  private:
    std::vector<std::vector<int> > shift;
    int size,it,**path,**board,**testboard,term;
    long int cycle_count;
  };

#endif

