#ifndef _ZLOMEK_H_
#define _ZLOMEK_H_

#include <iostream>
#include <limits>
#include <cmath>



/* is a+b safe? */
#define safePlus(a,b) \
  cout << a << " " << b << endl; \
  if ( !( (((a)>0)&&((b)<0)) || (((a)<0)&&((b)>0))) && (a) && (b) ) {\
    if ( (a)>0 ) { \
      if ( (a) > std::numeric_limits<int>::max()-(b) ) throw 1; \
    } else { \
      if ( (a) < std::numeric_limits<int>::min()-(b) ) throw -1; \
    } \
  }


/* is a*b safe? */
#define safeMulti(a,b) \
  if ( (a) && (b) ) \
  if (((((a)>0) && ((b)>0)) || (((a)<0) && ((b)<0))) ?\
  ((fabs((a)) > fabs(std::numeric_limits<int>::max()/(b))) ||\
  (fabs((b)) > fabs(std::numeric_limits<int>::max()/(a)))) :\
  (((a)<(std::numeric_limits<int>::min()+1)/(b)) ||\
  ((b)<std::numeric_limits<int>::max()/(a)))) throw a;



class fraction{
  public:
    fraction();
    fraction(int n);
    fraction(int n, int d) throw (int);
    fraction(const fraction &obj);
    int num();
    int denom();
    ~fraction();
    friend double fract2double(fraction obj);
    friend std::ostream& operator<<(std::ostream& os, const fraction& frac);
    friend std::istream& operator>>(std::istream& is, fraction& frac)
      throw (int);

    fraction operator-();
    fraction operator-(fraction obj);
    friend fraction operator-(int left,fraction obj);
    
    fraction operator+(fraction obj);
    friend fraction operator+(int left,fraction obj);
    
    fraction operator*(fraction obj);
    friend fraction operator*(int left,fraction obj);
    
    fraction operator/(fraction obj) throw (int);
    friend fraction operator/(int left,fraction obj) throw (int);

  private:
    int numerator,denominator;
    void simplify();
    int gcd(int n,int d);
};


fraction operator-(int left,fraction obj);
fraction operator+(int left,fraction obj);
fraction operator*(int left,fraction obj);
fraction operator/(int left,fraction obj) throw (int);
std::ostream& operator<<(std::ostream& os, const fraction& frac);
std::istream& operator>>(std::istream& is, fraction& frac) throw (int);


fraction double2fract(double dbl);
double fract2double(fraction obj);



#endif

