# -*- coding: cp936 -*-
from __future__ import division
from math import sqrt
import random
import csv
fr={}
en={}
corpus=[]
countE={} #翻译英文计数
countP={} #翻译词对计数
countF={} #翻译四个词的词对计数
countT={} #翻译三个词的计数
delta={}  #临时参数
t={}      #参数t
q={}      #参数q
ne={}
ewords={}
fwords={}
enInput = open('corpus.en','r')
frInput = open('corpus.es','r')
ens = enInput.read().splitlines()
frs = frInput.read().splitlines()
enInput.close()
frInput.close()

count=len(ens);


for i in range(count):
    print i
    ens[i]="NULL "+ens[i]
    corpus.append([ens[i],frs[i]])
    s1=ens[i].split(' ')
    for ss in s1:
        ewords.setdefault(ss,0)
        ewords[ss]+=1
        countE.setdefault(ss,0)
        
    s2=frs[i].split(' ')
    for ss in s2:
        fwords.setdefault(ss,0)
        fwords[ss]+=1
        
    for k in range(len(s1)):
        ne.setdefault(s1[k],[])
        for j in range(len(s2)):
            if not (s2[j] in ne[s1[k]]):
                ne[s1[k]].append(s2[j]);
            countF.setdefault(k,{})
            countF[k].setdefault(j+1,{})
            countF[k][j+1].setdefault(len(s1),{})
            countF[k][j+1][len(s1)].setdefault(len(s2),0)
            
            countT.setdefault(j+1,{})
            countT[j+1].setdefault(len(s1),{})
            countT[j+1][len(s1)].setdefault(len(s2),0)
            
            q.setdefault(k,{})
            q[k].setdefault(j+1,{})
            q[k][j+1].setdefault(len(s1),{})
            q[k][j+1][len(s1)].setdefault(len(s2),random.random())

            delta.setdefault(i,{})
            delta[i].setdefault(j+1,{})
            delta[i][j+1].setdefault(k,0)
                
    #ne.setdefault('NULL',[]):
    #for j in range(len(s2)):
    #    if not ne['NULL'].has_key(s2[j]):
    #        ne['NULL'].append(s2[j])
            
for e in ne:
    for f in ne[e]:
        t.setdefault(f,{})
        t[f].setdefault(e,0)
        t[f][e]=1/len(ne[e])
        countP.setdefault(e,{})
        countP[e].setdefault(f,0)

def setzero():
    for i in countE:
        countE[i]=0
    for i in countP:
        for j in countP[i]:
            countP[i][j]=0
    for i in countF:
        for j in countF[i]:
            for k in countF[i][j]:
                for  d in countF[i][j][k]:
                    countF[i][j][k][d]=0
    for i in countT:
        for j in countT[i]:
            for k in countT[i][j]:
                countT[i][j][k]=0

for S in range(5):
    setzero()
    for k in range(count):
        print k
        s1=ens[k].split(' ')
        s2=frs[k].split(' ')
        for i in range(len(s2)):
            sums=0;
            for j in range(len(s1)):
                delta.setdefault(k,{})
                delta[k].setdefault(i+1,{})
                delta[k][i+1].setdefault(j,0)
                q.setdefault(j,{})
                q[j].setdefault(i+1,{})
                q[j][i+1].setdefault(len(s1),{})
                q[j][i+1][len(s1)].setdefault(len(s2),random.random())
                
                #print q[j][i+1][len(s1)][len(s2)],t[s2[i]][s1[j]]
                #print q[j][i][len(s1)][len(s2)]
                sums+=q[j][i+1][len(s1)][len(s2)]*t[s2[i]][s1[j]]
                
            for j in range(len(s1)):
                delta[k][i+1][j]=q[j][i+1][len(s1)][len(s2)]*t[s2[i]][s1[j]]/sums
                countP[s1[j]][s2[i]]+=delta[k][i+1][j]
                countE[s1[j]]+=delta[k][i+1][j]
                countF[j][i+1][len(s1)][len(s2)]+=delta[k][i+1][j]
                countT.setdefault(k,{})
                countT[k].setdefault(len(s1),{})
                countT[k][len(s1)].setdefault(len(s2),0)
                countT[k][len(s1)][len(s2)]+=delta[k][i+1][j]
    for f in t:
        for e in t[f]:
            if  countE[e]!=0:
                t[f][e]=countP[e][f]/countE[e]
            else:
                t[f][e]=0.000000000000001
    for j in q:
        for i in q[j]:
            for l in q[j][i]:
                for m in q[j][i][l]:
                    if countT[i][l][m]!=0:
                        q[j][i][l][m]=countF[j][i][l][m]/countT[i][l][m]
                    else:
                        q[j][i][l][m]=0.000000000000001

enInput = open('test.en','r')
frInput = open('test.es','r')
Output = open('alignment_test.p1.out','w')
worke = enInput.read().splitlines()
works = frInput.read().splitlines()
for i in range(len(works)):
    worke[i]="NULL "+worke[i]
    s1=worke[i].split(' ')
    s2=works[i].split(' ')
    for j in range(len(s2)):
        maxs=0
        point=0;
        for k in range(len(s1)):
            t.setdefault(s2[j],{})
            t[s2[j]].setdefault(s1[k],0)
            #q.setdefault(k,{})
            #q[k].setdefault(j,{})
            #q[k][j].setdefault(len(s1),{})
            #q[k][j][len(s1)].setdefault(len(s2),0)
            
            if (t[s2[j]][s1[k]]>maxs):
                maxs=t[s2[j]]
                point=k
        
        if (point!=0):
            Output.write(str(i+1)+" "+str(point)+" "+str(j+1)+"\n")
enInput.close()
frInput.close()

