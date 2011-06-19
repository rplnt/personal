#include <iostream>
#include <iomanip>
#include <vector>
#include <algorithm>
#include <cmath>
#include "knight.h"

//_NO_BRUTE_ na zapnutie sikovnejsieho hladania
#define _NO_BRUTE_

using namespace std;


/* konstruktor */
Knight::Knight(int x) {
  this->term = 0;
  if ( x<1 ) x=1;
  this->size = x;
  this->board = new int*[x];
  this->path = new int*[x*x];

  vector<int> hello(3);
  hello[0] = 0;
  
  /* nastavenie vektoru s moznostami pohybu (zleee) */
  hello[1]= 1; hello[2]=-2; this->shift.push_back(hello);
  hello[1]= 2; hello[2]=-1; this->shift.push_back(hello);
  hello[1]= 2; hello[2]= 1; this->shift.push_back(hello);
  hello[1]= 1; hello[2]= 2; this->shift.push_back(hello);
  hello[1]=-1; hello[2]= 2; this->shift.push_back(hello);
  hello[1]=-2; hello[2]= 1; this->shift.push_back(hello);
  hello[1]=-2; hello[2]=-1; this->shift.push_back(hello);
  hello[1]=-1; hello[2]=-2; this->shift.push_back(hello);

  /* alokovanie pamate */
  for (int i=0;i<x;i++)
    this->board[i] = new int[x];

  for(int i=0;i<x*x;i++)
    this->path[i] = new int[2];

}


/* Pozera o 2 kroky dopredu (Warnsdorff's algorithm) */
int Knight::nextstep(const int x,const int y) {

  if ( this->isOccupied(x,y) ) return 0;
  int a=0;

  for(int i=0;i<8;i++) 
    if ( !this->isOccupied(x+this->shift[i][1],y+this->shift[i][2]) ) a++;

  return a;
}

/* vynulovanie */
void Knight::clean(int x) {
  for(int n=0;n<x;n++) {
    for(int m=0;m<x;m++)
      this->board[m][n]=0;
  }
}

/* pozera ci je policko volne */
bool Knight::isOccupied(const int x, const int y) {
  return (x>this->size || y>this->size
    || x<1 || y<1 || this->board[x-1][y-1] != 0);
}


/* hladanie cesty */
bool Knight::runTour(int x,int y) {

  if ( this->term==0 ) {
    this->clean(this->size);
    this->it = 0;
    this->cycle_count = 0;
    this->term = 1;
  }

  if ( this->it==this->size*this->size ) {
    if ( this->size==0 ) return 0;
    cout << endl << "Pocet navstivenych policok: " << this->cycle_count << endl;
    this->term=0;
    return 1;
    }

  if ( this->isOccupied(x,y) ) return 0; //zle policko

  /* stupili sme na dobre policko, zapiseme co treba */
  if (this->cycle_count!=0 ) this->term++;
  this->cycle_count++;
  path[this->it][0] = x;
  path[this->it][1] = y;
  this->it++;
  board[x-1][y-1] = this->it;


#ifdef _NO_BRUTE_ //vypnutie bruteforce metody :D
  for (int i=0;i<8;i++)
    this->shift[i][0]=this->nextstep(x+this->shift[i][1],y+this->shift[i][2]);
  sort(this->shift.begin(),this->shift.end());
#endif

  /* Haskell style */
  for (int i=0;i<8;i++)
    if (this->runTour(x+this->shift[i][1],y+this->shift[i][2])) return 1;

  /* mazeme co sme napachali a vraciame sa spat */
  this->it--;
  this->term--;
  board[x-1][y-1] = 0;
  
  return 0;
}


/* ^.^ */
int** Knight::getmoves() {
  return this->path;
}

/* kontrola cesty zadana polom - snad to neni popletene :P */
bool Knight::checkTour(int** gpath, int gsize) {

  /*
    mozem iba predpokladat, ze vstup je spravny a pre celu plochu
    nakolko sa do funkcie neposiela velkost 'testovanej' dosky.
    tj. o ciastocne riesenia metoda nekontroluje
      ani zo vstupnych udajov nema ako
    nekontrolujem ani ci sedia tie dva udaje
      zadanie sa tomu moc nevenovalo
    tak snad to je ok :)
  */
    

  int sw_x,sw_y;
  int xsize;

  xsize = int(sqrt(gsize));

  /* skaceme ok? */
  for (int i=0;i+1<gsize;i++) {
    sw_x = gpath[i][0]-gpath[i+1][0];
    sw_y = gpath[i][1]-gpath[i+1][1];
    if ( sw_x<0 ) sw_x=0-sw_x; if ( sw_y<0 ) sw_y=0-sw_y;
    if ( sw_x==sw_y || !(( sw_x==1 && sw_y==2) || (sw_x==2 && sw_y==1)) )
      return 0;
  }
  
  /* vyrobenie test-dosky */
  this->testboard = new int*[xsize];
  for (int i=0;i<xsize;i++)
    this->testboard[i] = new int[xsize];
    
  for(int n=0;n<xsize;n++) {
    for(int m=0;m<xsize;m++)
      this->testboard[m][n]=0;
  }
  
  /* zaplnili sme dosku? */
  for (int i=0;i<gsize;i++) {
    sw_x = gpath[i][0];
    sw_y = gpath[i][1];
    
    if ( sw_x<1 || sw_y<1 || sw_x>xsize || sw_y>xsize )
      return 0;
    if ( this->testboard[sw_x-1][sw_y-1]==1 )
      return 0;
      
    this->testboard[sw_x-1][sw_y-1] = 1;
  }
  
  
  for (int i=0;i<this->size;i++)
    delete[] this->testboard[i];
  delete[] this->testboard;
  
  return 1;
}


/* vykreslovac sachovnice - teoreticky kresli pekne do 62*62 :P */
ostream& operator <<(ostream& out, const Knight& obj) {
  int w;
  if ( obj.size>31 ) w = 7;
    else if ( obj.size>15 ) w = 6;
    else w = 5;

  out << endl << setw(w+3) << " 1";
  for (int i=1;i<obj.size;i++)
    out << setw(w-1) << i+1;

  out << endl << setw(4) << " " << setfill('-') << setw(obj.size*(w-1)+3) << " ";
  out << endl << setfill(' ') << setw(4) << "|" << endl;

  for (int y=0;y<obj.size;y++) {
    out << setw(2) << char(y+'A') << " |";
    for (int x=0;x<obj.size;x++)
      out << setw(w-1) << obj.board[x][y];
    out << endl << setw(4) << "|" << endl;
  }
  
  return out;
}


/* pretazenie operatoru '<' na sortovanie vektorov podla nulteho prvku */
bool operator < (const vector<int> &a, const vector<int> &b) {
  return (a[0] < b[0]);
}


/* destruktor */
Knight::~Knight() {
  for (int i=0;i<this->size;i++)
    delete[] this->board[i];
  delete[] this->board;

  for (int i=0;i<this->size*this->size;i++)
    delete[] this->path[i];
  delete[] this->path;
}

