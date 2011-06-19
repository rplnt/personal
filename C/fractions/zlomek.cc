#include <iostream>
#include "zlomek.h"

using namespace std;




/* ################ fraction ################# */

 /* empty constructor */
fraction::fraction() {
 //is empty
}


/* constructor n/1 */
fraction::fraction(int n) {
  this->numerator = n;
  this->denominator = 1;
}


/* constructor n/d */
fraction::fraction(int n, int d) throw (int) {
  if ( d==0 ) throw 0;

  this->numerator = n;
  this->denominator = d;
  this->simplify();
}


/* copy constructor */
fraction::fraction(const fraction &obj) {
  this->numerator = obj.numerator;
  this->denominator = obj.denominator;
}


/* empty destructor */
fraction::~fraction() {
  //is also empty
}





/* ################ fraction method's & friends ################# */

/* get numerator */
int fraction::num() {
  return this->numerator;
}


/* get denominator */
int fraction::denom() {
  return this->denominator;
}


/* reduce the fraction */
void fraction::simplify() {
  int divisor = this->gcd(this->numerator, this->denominator);

  this->numerator /= divisor;
  this->denominator /= divisor;

  if ( this->denominator < 0 ) {
    this->denominator = -this->denominator;
    this->numerator = -this->numerator;
  }
}


/* find greatest common divisor - euclidean's algorithm */
int fraction::gcd(int n, int d) {
  return ( d==0 ? n : this->gcd(d, n%d) ); //wiki
}


/* todo */
fraction double2fract(double dbl) {
  return fraction((int)(dbl*10000), 10000);
}


/* return double value of given fraction */
double fract2double(fraction obj) {
  return (double)obj.numerator/(double)obj.denominator;
}





/* ################ fraction's operators overloading ################# */

/* unary minus */
fraction fraction::operator-() {
  return fraction(-numerator,denominator);
  }


/* int-fract */
fraction operator-(int left,fraction obj) {
  return -obj+left;
}


/* int+fract */
fraction operator+(int left,fraction obj) {
  return obj+left;
}


/* int*fract */
fraction operator*(int left,fraction obj) {
  safeMulti(left,obj.numerator);
  return fraction((left*obj.numerator),obj.denominator);
}


/* int/fract */
fraction operator/(int left,fraction obj) throw (int) {
  if ( obj.numerator==0 ) throw 0;
  safeMulti(left,obj.denominator);
  return fraction((left*obj.denominator),obj.numerator);
}


/* fract+fract */
fraction fraction::operator+(fraction obj) {
  int left,right;

  safeMulti(this->numerator,obj.denominator);
  left = this->numerator*obj.denominator;
  safeMulti(obj.numerator,this->denominator);
  right = obj.numerator*this->denominator;

  safePlus(left,right);
  safeMulti(this->denominator,obj.denominator);
  
  return fraction((left+right),this->denominator*obj.denominator);
}


/* fract-fract */
fraction fraction::operator-(fraction obj) {
  return *this+(-obj);
}


/* fract*fract */
fraction fraction::operator*(fraction obj) {
  if ( this->numerator==0 || obj.numerator==0 ) return fraction(0,1);
  safeMulti(this->numerator,obj.numerator);
  safeMulti(this->denominator,obj.denominator);
  
  int n = (this->numerator*obj.numerator);
  int d = (this->denominator*obj.denominator);
  
  return  fraction(n,d);
  }


/* fract/fract */
fraction fraction::operator/(fraction obj) throw (int) {
  if ( obj.numerator==0 ) throw 0;
  fraction temp(obj.denominator,obj.numerator);

  return *this*temp;
}





/* ################ in/out streams for fraction ################# */

/* fraction ostream */
ostream& operator<<(ostream& os, const fraction& frac) {
  os << frac.numerator << "/" << frac.denominator;
  return os;
}


/* fraction istream */
istream& operator>>(istream& is, fraction& frac) throw (int) {
  int n,d;
  is >> n >> d;
  if ( d == 0 ) throw 0;
  
  frac.numerator = n;
  frac.denominator = d;
  
  frac.simplify();

  return is;
}

