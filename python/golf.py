'''
My submission to the codegolf challenge. The task was to create a shortest possible
program in a language of choice that would count days between two dates without
using any date/time libraries.
'''
import re
a=re.split('[-, ]',raw_input())
def c(x):return x[0]
def f(x,y=3):return(1if x%400==0 or x%100!=0and x%4==0 else 0)if y>2 else 0
t=[31,28,31,30,31,30,31,31,30,31,30,31]
[q,w,e],[i,o,p]=sorted([map(int,[a[x][:4],a[x][4:6],a[x][6:]])for x in[0,1]],key=c)
print sum(map(f,range(q,i)))+(i-q)*365+p+sum(t[:o-1])-e-sum(t[:w-1])+f(i,o)-f(q,w)if 0<w<13and 0<e<32and 0<o<13and 0<p<32and(e<=t[w-1]or(f(q)and e==29))and(p<=t[o-1]or(f(i)and p==29))else 'E'
