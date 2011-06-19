/* 
"Only a life lived for others is a life worthwhile."
 - Albert Einstein
*/
#include <stdio.h>
#include <stdlib.h>
#include <ncurses.h>
#include <unistd.h>

char pattern[40][23][2]; //eh..

/* funkcia vracia pocet 'zivych' susednych buniek */
int neighbors(int x, int y, int m, int n, int ab) {
  int a,b,c;

  if ( pattern[x][y][ab]=='o' ) c = 0; else c = 1;
  if ( x==0 ) x = m-1; else x--;
  if ( y==0 ) y = n-1; else y--;

  for (a=0;a<3;a++) {
    for (b=0;b<3;b++) {
      if ( pattern[(x+a)%m][(y+b)%n][ab]=='o' ) c++;
      }
    }

  return c-1;
}

void fin() {
  printw("Stlac lubovolnu klavesu.\n");
  nodelay(stdscr, FALSE);
  getch();
  refresh();
  endwin();
  }
  

int main(int argc, char *argv[]) {
  int i=1, s, count=0, alive, id=0, uslpc=512, k;
  int x, y, ny, mx, h, w, offsetx=0, offsety=0, ab=0;
  char cell,key;
  
  /* kontrola vstupnych parametrov */
  if ( argc != 4 ) {
     printf("Zle zadane vstupne parametre, zadajte ich nasledovne:\n");
     printf("%s vstupny_subor pocet_riadkov pocet_stlpcov\n",argv[0]);
     return 2;
     } else {
     mx = atoi(argv[3]); // x - stlpce
     ny = atoi(argv[2]); // y - riadky
     }
  if ( ny<1 || ny>23 ) {
     printf("Pocet riadkov musi byt v intervale <1,23>\n");
     return 3;
     }
  if ( mx<1 || mx>40 ) {
     printf("Pocet stlpcov musi byt v intervale <1,40>\n");
     return 4;
     }

  /* 'vyzabijanie' potrebnej casti pola */
  for (y=0;y<ny;y++) {
    for (x=0;x<mx;x++) {
      pattern[x][y][0] = ' ';
      pattern[x][y][1] = ' ';
      }
    }
  x = 0; y = 0;

  /* otvorenie suboru */
  FILE *in;
  in = fopen(argv[1],"r");
  if ( in==NULL ) {
     printf("Nepodarilo sa otvorit vstupny subor!\n");
     return 1;
     }

  /* citanie a kontrola suboru */
  do {
    s = fscanf(in, "%c", &cell);

    if ( x==mx+1 ) {
      printf("Prilis mnoho znakov v %d. riadku\n",y+1);
      fclose(in);
      return 5;
      }

    if ( s!=EOF ) {   
      if ( cell==10 ) {
        y++;
        x = 0;
        }
      else if ( cell=='o' ) {
        pattern[x][y][ab] = cell;
        count++;
        x++;
        }
      else if ( cell==' ' ) x++;
      else {
        printf("Nevhodne znaky v subore (pouzivajte iba 'o' a ' ')\n");
        fclose(in);
        return 5;
        }
      }

    if ( y==ny ) s=EOF; //skonci citanie suboru

    } while ( s!=EOF );

  s = 1;
  fclose(in);

  if ( count==0 ) {
    printf("Organizmus neobsahuje ziadne zive bunky\n");
    return 6;
    }

  /* ncurses vecae */
  initscr();
  cbreak();
  noecho();
  keypad(stdscr, TRUE);
  getmaxyx(stdscr, h, w);

  // vycentrovanie 'pola'
  //if ( h>ny && w>mx ) {
  //  offsetx = (w-mx)/2;
  //  offsety = (h-ny)/2;
  //  }

  move(0,0);
  printw("Program LIFEc\n\n Ovladanie:\n <-,-> pre zmenu rychlosti\n");
  printw(" Enter pre ukoncenie\n");
  printw(" \nprogram spustite stlacenim lubovolnej klavesy...");
  refresh();
  getch();
  nodelay(stdscr, TRUE);


  /* hlavny cyklus */  
  while ( s!=0 ) {

    clear();
    key = getch();
    //attrset(A_STANDOUT);

    /* cyklus vypisuje aktualny stav na obrazovku
       a zaroven  pocita  dalsiu generaciu buniek */
    for (y=0;y<ny;y++) {
      move(y+offsety,offsetx);
      for (x=0;x<mx;x++) {
        cell = pattern[x][y][ab];
        printw("%c ",cell);
        alive = neighbors(x,y,mx,ny,ab);
        if ( cell==' ' && alive==3 ) { //birth
          cell = 'o';
          count++;
          }
        else if ( cell=='o' && ( alive==2 || alive==3 ) ); //life
        else {
          if ( cell=='o' ) count--; //death
          cell = ' ';
          }
        pattern[x][y][(ab+1)%2] = cell;
        if ( pattern[x][y][ab] == cell ) id++;
        }
      }

    //attrset(A_NORMAL);
    move (ny+1,0); //move(h-1,0);

    if ( count==0 ) {
      printw("Organizmus v nasledujucej - %d. generacii vymre. \n",i+1);
      fin();
      return 6;
      }

    if ( id==mx*ny ) {
      printw("Organizmus zostava od %d. generacie nemenny. \n", i-1);
      fin();
      return 7;
      } else id = 0;

    if ( key==10 ) {
      printw("Posledna - %d. generacia ma %d buniek. \n", i, count);
      fin();
      s = 0;
      } else {
      printw("Takto vyzera %3d. generacia, ",i);
      printw("ktora obsahuje %3d buniek. delay=%4dms",count,uslpc);
      refresh();
      for (k=0;k<uslpc;k++) usleep(999); // usleep obmedzenie na aise
      }

    i++;
    ab = (ab+1)%2;

    if ( key==4 && uslpc>1 ) uslpc /= 2;
    if ( key==5 && uslpc<8000 ) uslpc *= 2;

    } //konec

  return 0;
}

