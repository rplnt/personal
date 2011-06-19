#include <iostream>
#include "zlomek.h"

#include <limits>

using namespace std;

int main() {

  fraction a;
  fraction b;
  double d;
  


  int op;
  
  while ( true ) {

    try {

      cin >> a;
      cin >> b;
      cout << a << " " << b << endl;
      cout << "| 1:+ | 2:- | 3:* | 4:/ | 5: f2d | 6: d2f | 9: quit |" << endl;
    //v  cout << a-2 << " " << 2-a << " " << a+2 << " " << 2+a << endl;
      //cout << a*-1 << " " << -1*a << " " << a/2 << " " << 2/a << endl << endl;
      do {
        cin >> op;
        switch (op) {
          case 1: cout << a << " + " << b << " = " << a+b << endl; break;
          case 2: cout << a << " - " << b << " = " << a-b << endl; break;
          case 3: cout << a << " * " << b << " = " << a*b << endl; break;
          case 4: cout << a << " / " << b << " = " << a/b << endl; break;
          case 5: cout << a << " = " << fract2double(a) << endl
                       << b << " = " << fract2double(b) << endl; break;
          case 6: cin >> d;
                  cout << double2fract(d); break;
          default: break;
       }
      }  while ( op!=9 );

    } catch (int x) {
      cout << "Exception: " << x << endl;
      return 1;
    }
  }
  
  return 0;
}

