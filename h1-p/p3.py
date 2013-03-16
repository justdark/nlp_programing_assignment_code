'''
  change and count the disfrequent words
'''
from __future__ import division
#file_object = open('gene.counts','r')
file_object = open('gene.counts.change','r')
text = file_object.read().splitlines()
file_object.close()
TagCount=[]
O={}
I_GENE={}
pi={}
pi[0]={'*':{'*':float(0)}}
countO=0
countI=0
def count(s):
    '''
        read data
    '''
    ss=s.split(' ')
    if (ss[1]=='WORDTAG'):
        if (ss[2]=='O'):
            O[ss[3]]=int(ss[0])
            I_GENE.setdefault(ss[3],0)
        if (ss[2]=='I-GENE'):
            #print int(ss[0])
            I_GENE[ss[3]]=int(ss[0])
            O.setdefault(ss[3],0)
    if (ss[1]!='WORDTAG'):
        TagCount.append(s);
        
def numer(word):
    for i in word:
        if i<='9' and i>='0':
            return True;
    return False
def allC(word):
    return word.isupper()
def lastC(word):
    return word[len(word)-1].isupper()

def isfrequent(word):
    O.setdefault(word,0)
    I_GENE.setdefault(word,0)
    if O[word]+I_GENE[word]<5:
        if numer(word):
            return "_Numeric_"
        if allC(word):
            return "_All_Capitals_"
        if lastC(word):
            return "_Last_Capital_"
        return '_RARE_'
    return ''

def c(s1='',s2='',s3=''):
    for line in TagCount:
        ss=line.split(' ')
        if s3=='':
            if (ss[1]=='2-GRAM' and ss[2]==s1 and ss[3]==s2):
                return int(ss[0])
        else:
            if (ss[1]=='3-GRAM' and ss[2]==s1 and ss[3]==s2 and ss[4]==s3):
                return int(ss[0])
    return 0;
               
def q(s3='',s1='',s2=''):
    return c(s1,s2,s3)/c(s1,s2,'')
def e(s1,s2):
    word=s1
    if isfrequent(word)!='':
        s1=isfrequent(word)
    if (s2=='I-GENE'):
        return I_GENE[s1]/countI;
    else:
        return O[s1]/countO;
for line in text:
    count(line)


fileInput = open('gene.test','r')
fileOutput = open('gene_test.p3.out','w')
#fileInput = open('gene.dev','r')
#fileOutput = open('gene_dev.p1.out','w')
text = fileInput.read().splitlines()

for o in O:
    countO+=O[o]
for i in I_GENE:
    countI+=I_GENE[i]
print countO,countI
print e('Ischemic',O)
key=''
#print O['_RARE_'],countO,I_GENE['_RARE_'],countI
#if O['_RARE_']/countO>I_GENE['_RARE_']/countI:
if O['_RARE_']/countO>I_GENE['_RARE_']/countI:
    key='O'
else:
    key='I-GENE'
ele=['O','I-GENE']
zeroele=['*']
eles=['O','I-GENE','STOP','*']
asd=0;
sentence='a'
#print c('*','*','I-GENE')
for line in text:
    word=line;
    if word!='':
        sentence=sentence+' '+word;
    if word=='':
        s=sentence.split(' ')
        sentence='a'
        ans={};
        pi={}
        bp={}
        for i in range(0,1000):
            ihough={}
            for ii in eles:
                iihough={}
                for iii in eles:
                    iihough[iii]=0;
                ihough[ii]=iihough
            pi[i]=ihough
            
        for i in range(0,1000):
            ihough={}
            for ii in eles:
                iihough={}
                for iii in eles:
                    iihough[iii]='';
                ihough[ii]=iihough
            bp[i]=ihough
            
        pi[0]['*']['*']=float(1)
        for k in range(1,len(s)):
            #print e(s[k],'O'),e(s[k],'I-GENE')
            if k==1:
                skd1=zeroele
                skd2=zeroele
                sk=ele
            else:
                if k==2:
                    skd1=ele
                    skd2=zeroele
                    sk=ele
                else:
                    skd1=ele
                    skd2=ele
                    sk=ele
            flag=1;
            for u in skd1:
                for v in sk:
                    temp=''
                    for w in skd2:
                        #print w
                        #print 'pi['+str(k-1)+']['+w+']['+u+']\t---',pi[k-1][w][u]
                        #print 'q('+v+','+w+','+u+')---------',q(v,w,u)
                        #print 'e('+s[k]+','+v+')--------',e(s[k],v)
                        #print  'pi['+str(k)+']['+u+']['+v+']\t---',pi[k-1][w][u]*q(v,w,u)*e(s[k],v)
                        #print k,w,u,v
                        #print pi[k-1][w][u]*q(v,w,u)*e(s[k],v)
                        #content = raw_input("input:")
                        if (pi[k-1][w][u]*q(v,w,u)*e(s[k],v)>pi[k][u][v]):
                            pi[k][u][v]=pi[k-1][w][u]*q(v,w,u)*e(s[k],v)
                            temp=w;
                    if pi[k][u][v]<0.0000000000001:
                        flag=0;
                    bp[k][u][v]=temp;
                    #print 'bp['+str(k)+']['+u+']['+v+']==',temp;
                    #print k,u,v,temp
                    #print k,u,v,pi[k][u][v]
                    #content = raw_input("")
            if flag==0:
                for u in skd1:
                    for v in sk:
                        pi[k][u][v]=pi[k][u][v]*10000000000;
                   
        temp_num=0;
        for u in ele:
            for v in ele:
                if (pi[len(s)-1][u][v]*q('STOP',u,v)>temp_num):
                    temp_num=pi[len(s)-1][u][v]*q('STOP',u,v);
                    ans[len(s)-1]=v;
                    ans[len(s)-2]=u;
        #print ans[len(s)-1],ans[len(s)-2]
        #content = raw_input("input:")
        for i in range(len(s)-3,0,-1):
            #print i
            #print bp[i+2][ans[i+1]][ans[i+2]];
            ans[i]=bp[i+2][ans[i+1]][ans[i+2]];
        for i in range(1,len(s)):
            fileOutput.write(s[i]+' '+ans[i]+'\n')
        fileOutput.write('\n')       

        '''
        fileOutput.write('\n') 
    else:
        if (e(word,'O')>e(word,'I-GENE')):
            fileOutput.write(word+' '+'O'+'\n')
        else:
            fileOutput.write(word+' '+'I-GENE'+'\n')
            #fileOutput.write(word+' '+'I-GENE'+' O:'+str(O[word]/countO)+' I:'+str(I_GENE[word]/countI)+'\n')
            asd+=1
        '''
print q('I-GENE','O','I-GENE')
fileInput.close()
fileOutput.close()

