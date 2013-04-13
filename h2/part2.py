from __future__ import division
import json

Ncount={}
Bcount={}
Bs={}
Ucount={}
qB={}
qU={}
counts={}
NoneTerminal=[]
Terminal=[]
def count(word):
    if word in Terminal:
        return counts[word]
    return 0
def calcount():
    c=open("parse_train.counts.out",'r')
    b=c.read().splitlines()
    c.close()
    for line in b:
        words=line.split(' ')
        if (words[1]=="NONTERMINAL"):
            Ncount.setdefault(words[2],int(words[0]))
            NoneTerminal.append(words[2])
            
        if (words[1]=="UNARYRULE"):
            Ucount.setdefault('~'.join(words[2:]),int(words[0]))
            counts.setdefault(words[3],0)
            counts[words[3]]+=int(words[0])
            Terminal.append(words[3])
            
        if (words[1]=="BINARYRULE"):
            Bcount.setdefault('~'.join(words[2:]),int(words[0]))
            Bs.setdefault(words[2],[])
            #print '~'.join(words[2:])
            Bs[words[2]].append([words[3],words[4]])
pi={}
pt={}
words=[]
a=1;
def make_tree(t,i,j,X):
    # i,j
    #sss=raw_input()
    pi.setdefault(i,{})
    pi[i].setdefault(j,{})
    pi[i][j].setdefault(X,-1)
    pt.setdefault(i,{})
    pt[i].setdefault(j,{})
    pt[i][j].setdefault(X,[])
    
    if (pi[i][j][X]!=-1):
        return (pt[i][j][X],pi[i][j][X])
    if (i==j):
        qU.setdefault(X,{});
        if count(words[i])<5:
            word='_RARE_'
        else:
            word=words[i]
        qU[X].setdefault(word,0)
        return ([X,words[i]],qU[X][word]);
    mins=0;
    tree=[]
    Bs.setdefault(X,[]);
    for k in range(i,j):
        for u in Bs[X]:
                #print X,Bs[X]
                #print u
                (t1,p1)=make_tree(t+1,i,k,u[0]);
                (t2,p2)=make_tree(t+1,k+1,j,u[1]);
                #print "t1==",t1
                #print "p1==",p1
                #print "t2==",t2
                #print "p2==",p2
                if (mins<(p1*p2*qB[X][u[0]][u[1]])):
                    tree=[X,t1,t2]
                    mins=p1*p2*qB[X][u[0]][u[1]];
    pi[i][j][X]=mins;
    pt[i][j][X]=tree;
    
    return (tree,mins)
def predict():
    n=len(words)
    pi.clear();
    pt.clear();
    for i in range(n):
        for u in Ucount:
            if u.split('~')[1]==words[i]:
                pi.setdefault(i,{})
                pi[i].setdefault(i,{})
                pt.setdefault(i,{})
                pt[i].setdefault(i,{})
                uu=u.split('~')
                pi[i][i].setdefault(uu[0],qU[uu[0]][uu[1]]);
                pt[i][i].setdefault(uu[0],[uu[0],uu[1]]);
                #pi.setdefault(str(i)+'~'+str(i)+'~'+str('words[i]'),qU[u])
    (tree,p)=make_tree(1,0,n-1,"SBARQ")
    return tree

calcount()
for R in Bcount:
    u=R.split('~')
    qB.setdefault(u[0],{})
    qB[u[0]].setdefault(u[1],{})
    qB[u[0]][u[1]].setdefault(u[2],Bcount[R]/Ncount[u[0]])
for R in Ucount:
    u=R.split('~')
    qU.setdefault(u[0],{})
    qU[u[0]].setdefault(u[1],Ucount[R]/Ncount[u[0]])
    
FileInput=open("parse_test.dat",'r').read().splitlines()
FileOutput=open("parse_test.p2.out",'w')

print "asdd"
for line in FileInput:
    words=line.split(' ');
    tree=predict()
    print tree
    FileOutput.write(json.dumps(tree)+"\n");
FileOutput.close()






















