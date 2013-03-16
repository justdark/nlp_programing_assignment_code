'''
  change and count the disfrequent words
'''

file_object = open('gene.counts','r')
#file_object = open('gene.counts.change','r')
text = file_object.read().splitlines()
file_object.close()
O={}
I_GENE={}
wordlist=[]
countss=0
countO=0
countI=0
O['_RARE_']=0
I_GENE['_RARE_']=0
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

def isfrequent(word,k):
    if word=='_RARE_':
        return False;
    O.setdefault(word,0)
    I_GENE.setdefault(word,0)
    if k==1:
        if O[word]+I_GENE[word]<5:
            O['_RARE_']+=O[word];
            I_GENE['_RARE_']+=I_GENE[word];
            return True
        return False
    if k==2:
        if O[word]+I_GENE[word]<5:
            return True
        return False

    
for line in text:
    count(line)
countO=0
countI=0
for o in O:
    countO+=O[o]
for i in I_GENE:
    countI+=I_GENE[i]
    

for line in text:
    s=line
    ss=s.split(' ')
    if (ss[1]=='WORDTAG'):
        isfrequent(ss[3],1)




#fileInput = open('gene.test','r')
#fileOutput = open('gene_test.p1.out','w')
fileInput = open('gene.dev','r')
fileOutput = open('gene_dev.p1.out','w')
text = fileInput.read().splitlines()

key=''
print O['_RARE_'],countO,I_GENE['_RARE_'],countI
if O['_RARE_']/countO>I_GENE['_RARE_']/countI:
    key='O'
else:
    key='I-GENE'
asd=0;
for line in text:
    word=line;
    if word=='':
        fileOutput.write('\n') 
    else:
        if isfrequent(word,2):
            fileOutput.write(word+' '+key+'\n')
        else:
            #print word,O[word],I_GENE[word]
            if O[word]/countO>I_GENE[word]/countI:
                fileOutput.write(word+' '+'O'+'\n')
            else:
                fileOutput.write(word+' '+'I-GENE'+'\n')
                asd+=1
print asd
fileInput.close()
fileOutput.close()


'''
#fileInput = open('gene.test','r')
#fileOutput = open('gene_test.p1.out','w')
fileInput = open('gene.dev','r')
fileOutput = open('gene_dev.p1.out','w')
text = fileInput.read().splitlines()
countO=0
countI=0
for o in O:
    countO+=O[o]
for i in I_GENE:
    countI+=I_GENE[i]
key=''
print O['_RARE_'],countO,I_GENE['_RARE_'],countI
if O['_RARE_']/countO>I_GENE['_RARE_']/countI:
    key='O'
else:
    key='I-GENE'


for line in text:
    word=line;
    if word=='':
        fileOutput.write('\n') 
    else:
        if isfrequent(word):
            fileOutput.write(word+' '+key+'\n')
        else:
            #print word,O[word],I_GENE[word]
            if O[word]/countO>=I_GENE[word]/countI:
                fileOutput.write(word+' '+'O'+'\n')
            else:
                fileOutput.write(word+' '+'I-GENE'+'\n')

fileInput.close()
fileOutput.close()
'''
