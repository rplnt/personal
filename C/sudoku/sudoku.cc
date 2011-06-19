#include <iostream>
#include <set>
#include <cmath>
#include <utility>
#include <string>
#include "sudoku.h"

using namespace std;


  /* Konstruktor 
   * Vyhazuje vyjimku typu int, jestli:
   * 1 - Parameter sizeOfSide je rovny 0, 1, nebo neni druhou mocninou nejakeho
   *   prirozeneho cisla
   * 2 - Delka vstupniho parametru symbols s odstranenymi duplicitami znaku
   *   se nerovna hodnote sizeOfSide.
   * 3 - Mezera se nachazi mezi znaky vstupniho parametru symbols
   */
Sudoku::Sudoku(int sizeOfSide, const char *symbols) throw (int) {

  if ( sizeOfSide<2 || !isSquare(sizeOfSide) ) throw 1;

  for ( int i=0,n=0;n<sizeOfSide;i++) {
    if ( symbols[i]==' ' ) throw 3;
    if ( this->symbols.insert(symbols[i]).second ) n++;
  }

  if ( !sizeOfSide==this->symbols.size() ) throw 2;

  this->p_data = new char*[sizeOfSide];
  for(int i=0;i<sizeOfSide;i++)
    this->p_data[i] = new char[sizeOfSide];

  for(int y=0;y<sizeOfSide;y++)
    for(int x=0;x<sizeOfSide;x++)
      this->p_data[x][y] = ' ';

  this->sizeOfSide = sizeOfSide;
}


  /* Kopirovaci konstruktor */
Sudoku::Sudoku(const Sudoku& source) {

  this->p_data = new char*[source.sizeOfSide];
  for(int i=0;i<source.sizeOfSide;i++)
    this->p_data[i] = new char[source.sizeOfSide];

  this->symbols = source.symbols;

  this->sizeOfSide = source.sizeOfSide;

  for(int y=0;y<this->sizeOfSide;y++)
    for(int x=0;x<this->sizeOfSide;x++)
      this->p_data[x][y] = source.p_data[x][y];
}


  /* zistuje ci je cislo druha mocnina nejakeho cisla */
bool Sudoku::isSquare(int size) {
  if ( size < 1 ) return false;
  if ( (int)(sqrt(size)*sqrt(size))==size ) return true;
  return false;
}


  /* kopirovaci konstruktor
   *
   * Vyhazuje vyjimku typu int, jestli:
   * 1 - Parametr sizeOfSide je rovny 0, 1, nebo neni druhou mocninou nejakeho
   *   prirozeneho cisla.
   * 2 - Delka vstupniho parametru symbols s odstranenymi duplicitami znaku
   *   se nerovna hodnote sizeOfSide.
   * 3 - Mezera se nachazi mezi znaky vstupniho parametru symbols
   */
void Sudoku::setType(int sizeOfSide, const char *symbols) throw (int) {

  if ( sizeOfSide<2 || !isSquare(sizeOfSide) ) throw 1;

  this->symbols.clear();

  for ( int i=0,n=0;n<sizeOfSide;i++) {
    if ( symbols[i]==' ' ) throw 3;
    if ( this->symbols.insert(symbols[i]).second ) n++;
  }

  if ( !sizeOfSide==this->symbols.size() ) throw 2;

  for (int i=0;i<this->sizeOfSide;i++)
    delete[] this->p_data[i];
  delete[] this->p_data;

  this->p_data = new char*[sizeOfSide];
  for(int i=0;i<sizeOfSide;i++)
    this->p_data[i] = new char[sizeOfSide];

  for(int y=0;y<sizeOfSide;y++)
    for(int x=0;x<sizeOfSide;x++)
      this->p_data[x][y] = ' ';

  this->sizeOfSide = sizeOfSide;
}


  /* Vraci velikost hraciho pole (mereno v poctu policek) */
int Sudoku::getSizeOfSide() const {
  return this->sizeOfSide;
}


  /* Vraci mnozinu obsahujici symboly pouzivane v dane variante */
const set<char>& Sudoku::getSymbols() const {
  return this->symbols;
}


  /* Vraci znak [x, y]
   *
   * Vyhazuje vyjimku typu int, jestli:
   * 1 - Parametr x nebo parametr y jsou mensi nez nula,
   * 2 - vetsi nebo rovne nez delka strany hraciho pole
   */
char Sudoku::getAt(int x, int y) const throw (int) {

  if ( x<0 || y<0 ) throw 1;
  if ( x>=this->sizeOfSide || y>=this->sizeOfSide ) throw 2;

  return p_data[x][y];
}


  /* Nastavuje znak [x, y]
   *
   * Vyhazuje vyjimku typu int, jestli:
   * 1 - Parametr x nebo parametr y jsou mensi nez nula,
   * 2 - vetsi nebo rovne nez delka strany hraciho pole
   * 3 - Parametr symbol neni ani mezera ani znak platny pro danou variantu.
   */
void Sudoku::setAt(int x, int y, char symbol) throw (int) {

  if ( x<0 || y<0 ) throw 1;
  if ( x>=this->sizeOfSide || y>=this->sizeOfSide ) throw 2;
  if ( symbol!=' ' && this->symbols.find(symbol)==this->symbols.end() ) throw 3;

  p_data[x][y] = symbol;
}


  /* Vraci true, jestli jsou vsechna policka vyplnena (zadne neni ' ') */
bool Sudoku::isFilled() const {

  for(int y=0;y<this->sizeOfSide;y++)
    for(int x=0;x<this->sizeOfSide;x++)
      if ( this->p_data[x][y] == ' ' ) return false;

  return true;
}


  /* Vraci true, jestli jsou vsechna policka vyplnena spravne (zadne kolize) */
bool Sudoku::isSolved() const {

  int sqRoot = (int)sqrt(this->sizeOfSide);
  set<char> symb;

  /* riadky */
  for(int y=0;y<this->sizeOfSide;y++) {
    for(int x=0;x<this->sizeOfSide;x++)
      symb.insert(this->p_data[x][y]);
    if ( symb != this->symbols ) return false;
    symb.clear();
  }

  /* stlpce */
  for(int x=0;x<this->sizeOfSide;x++) {
    for(int y=0;y<this->sizeOfSide;y++)
      symb.insert(this->p_data[x][y]);
    if ( symb != this->symbols ) return false;
    symb.clear();
  }

  /* bloky */
  for(int i=0,pos_x=0,pos_y=0;i<this->sizeOfSide;i++) {

    for(int y=pos_y;y<pos_y+sqRoot;y++)
      for(int x=pos_x;x<pos_x+sqRoot;x++)
        symb.insert(this->p_data[x][y]);

    if ( symb != this->symbols ) return false;
    symb.clear();

    pos_x += sqRoot;
    if ( pos_x == this->sizeOfSide ) {
      pos_x = 0;
      pos_y += sqRoot;
    }
  }
  
  return true;
}


  /* Do streamu vypise obsah hraciho pole */
ostream& operator<<(std::ostream& os, const Sudoku& sudOut) {

  set<char>::iterator it;

  os << sudOut.sizeOfSide << " ";
  for (it=sudOut.symbols.begin();it!=sudOut.symbols.end();it++)
    os << *it;
  os << endl << endl;

  for(int y=0;y<sudOut.sizeOfSide;y++) {
    for(int x=0;x<sudOut.sizeOfSide;x++)
      os << sudOut.p_data[x][y];
    os << endl;
  }

  return os;
}


  /* Ze streamu nacte obsah hraciho pole */
istream& operator>>(std::istream& is, Sudoku& sudIn) {

  int size;
  string symb;
  char **temp_data;

  is >> size >> symb;

  temp_data = new char*[size];
  for(int i=0;i<size;i++)
    temp_data[i] = new char[size];

  for(int y=0;y<size;y++)
    for(int x=0;x<size;x++)
      is >> temp_data[x][y];

  /* Tu je snad vsetko dobre nacitane a mozme zmenit objekt */

  for (int i=0;i<sudIn.sizeOfSide;i++)
    delete[] sudIn.p_data[i];
  delete[] sudIn.p_data;

  sudIn.p_data = new char*[size];
  for(int i=0;i<size;i++)
    sudIn.p_data[i] = new char[size];

  for(int y=0;y<size;y++)
    for(int x=0;x<size;x++)
      sudIn.p_data[x][y] = temp_data[x][y];

  sudIn.sizeOfSide = size;
  sudIn.symbols.clear();
  for(int i=0;i<(int)symb.size();i++)
    sudIn.symbols.insert(symb[i]);

  for (int i=0;i<size;i++)
    delete[] temp_data[i];
  delete[] temp_data;
  
  return is;
}


  /* destruktor */
Sudoku::~Sudoku() {
  for (int i=0;i<this->sizeOfSide;i++)
    delete[] this->p_data[i];
  delete[] this->p_data;
}

