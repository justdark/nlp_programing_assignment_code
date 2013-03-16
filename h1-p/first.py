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

for line in text:
    count(line)

fileInput = open('gene.train','r')
fileOutput = open('gene.train.change','w')
text = fileInput.read().splitlines()

for line in text:
    ss=line.split(' ')
    if ss[0]=='':
        #fileOutput.write('\n')
        pass
    else:
        if isfrequent(ss[0])!='':
            ss[0]=isfrequent(ss[0])
    fileOutput.write(' '.join(ss)+'\n')
    #print s,O[s]

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
