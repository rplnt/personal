/***************************************************************************
** knightmain.C
** testovaci soubor
*/
#include <iostream>
#include <ctime>
#include <iomanip>

#include "knight.h"
using namespace std;

int main(void) {

    int chessBoardSize;//velikost sachovnice
    int returnValue=0;//navratova hodnota
    int x=0,y=0;
    cout<<"Velikost sachovnice: ";
    cin>>chessBoardSize;
    clock_t startTime=0,finishTime=0;//slouzi k mereni spotrebovaneho casu

    Knight Jezdec(chessBoardSize);
while (1) {
    //testovani nalezeni cesty, reseni existuje.
    if(chessBoardSize<1)chessBoardSize=1;
    cout<<"\nZadejte pocatecni souradnice v poradi x y (od 1 do "<<
      chessBoardSize<<"): ";
    cin>>x>>y;
    startTime=clock();
    if (Jezdec.runTour(x,y)) {
        finishTime=clock();
        cout<<Jezdec<<endl;
        cout<<"Casova narocnost: "<<finishTime-startTime<<endl;
    }
    else {
        cout << "Reseni nenalezeno."<<endl;
        returnValue=1;
    }
    
  }
    //testovani funkcnosti checkTour(int **,int)
    
/*
    for ( int i=0; i<Jezdec.size*Jezdec.size; i++)
      cout << setw(3) << i+1 << ":  " << Jezdec.path[i][0] << " " << Jezdec.path[i][1] << endl;
      
      
      cout << endl << endl << "   _";


    for ( int j=0; j<Jezdec.size; j++ )
        cout << "_"  << j+1 << "__";
cout << endl;
    for ( int i=0; i<Jezdec.size; i++ ) {
      cout << i+1 << " | ";
      for ( int j=0; j<Jezdec.size; j++ )
        cout << setw(3) << Jezdec.board[i][j] << " ";
      cout << endl;
    }
      */
      
#ifdef CHECK
    if(returnValue)return returnValue;
    if (Jezdec.checkTour(Jezdec.getmoves(),chessBoardSize*chessBoardSize)){
        cout<<"Cesta jezdce po sachovnici odpovida zadani"<<endl;
    }
    else {
        cout<<"Cesta je chybna"<<endl;
        returnValue=2;
    }
#endif

    return returnValue;
}


