from __future__ import division
import json
files=open("parse_train.dat",'r').read().splitlines()

Ncount={}
Bcount={}
Ucount={}
counts={}
NoneTerminal=[]
Terminal=[]
def count(word):
    if word in Terminal:
        return counts[word]
    return 0
def calcount():
    c=open("cfg.counts",'r')
    b=c.read().splitlines()
    c.close()
    for line in b:
        words=line.split(' ')
        if (words[1]=="NONTERMINAL"):
            Ncount.setdefault(words[2],int(words[0]))
            NoneTerminal.append(words[2])
            
        if (words[1]=="UNARYRULE"):
            Ucount.setdefault(','.join(words[2:]),int(words[0]))
            counts.setdefault(words[3],0)
            counts[words[3]]+=int(words[0])
            Terminal.append(words[3])
            
        if (words[1]=="BINARYRULE"):
            Bcount.setdefault(','.join(words[2:]),int(words[0]))
            
def change(tree):
    if (tree[1] in Terminal):
        if (count(tree[1])<5):
            #print tree[1]
            tree[1]="_RARE_"
            
        return tree
    tree[1]=change(tree[1])
    tree[2]=change(tree[2])
    return tree


Output=open("parsetrain.counts.change",'w')
calcount()
for line in files:
    tree=json.loads(line)
    line=json.dumps(change(tree))
    Output.write(line+"\r\n");
Output.close()
