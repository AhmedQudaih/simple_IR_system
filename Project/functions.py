import numpy as np
import os
import nltk
import natsort
from nltk.stem import PorterStemmer
from nltk.tokenize import TweetTokenizer
from natsort import natsorted
import string
import nltk
import re
from nltk.corpus import stopwords
import math


def convert(string1):
    li = re.split(pattern = r"[ \n]", string = string1)
    return li  

def txttokenizer (string1):
    words = []
    str1 = string1
    en_stops = set(stopwords.words('english')) 
    all_words = convert(str1)
    for word in all_words:
        if word not in en_stops:
            if (word != ''):
                words.append(word)
    return words


def preprocessingtxt(query):
    tokens= txttokenizer(query)
    tokens = [word.lower() for word in tokens]
    return tokens


def constract(folder):
    folder_names = "documents"
    fileno = 0
    pos_index = {}
    file_names = natsorted(os.listdir(folder))
    for file_name in file_names:
        doc = open(folder+"\\"+  file_name,"r")
        stuff= doc.read()
        final_token_list = preprocessingtxt(stuff)
        for pos, term in enumerate(final_token_list):
            if term in pos_index:
                if fileno in pos_index[term][1]:
                    pos_index[term][1][fileno].append(pos)
                else:
                    pos_index[term][0] = pos_index[term][0] + 1
                    pos_index[term][1][fileno] = [pos]
            else:
                pos_index[term] = []
                pos_index[term].append(1)
                pos_index[term].append({})
                pos_index[term][1][fileno] = [pos]
        fileno += 1
    return pos_index

def intersection(term1,term2):
    Finalresult =[]
    i=0
    j=0
    frequency =0
    Finalresult.append(frequency)
    Finalresult.append({})
    documents1 =list (term1[1].keys())
    documents2 =list (term2[1].keys())
    

    while ( i < len(term1[1]) and j < len(term2[1])):
        document1 = term1[1][documents1[i]] 
        document2 = term2[1][documents2[j]]
        if ( documents1[i] == documents2[j]):
            c=0
            pos_res_list = [] 
            pos_list_1 = document1
            pos_list_2 = document2
            k=0
            while ( k < len(pos_list_1) ):
                l = 0
                while (l < len(pos_list_2)) :
                    if ( pos_list_2[l] - pos_list_1[k] == 1):
                        pos_res_list.append(pos_list_2[l])
                        if (c == 0):
                            frequency = frequency +1
                            c=c+1
                        break
                    elif (pos_list_2[l] < pos_list_1[k]):
                        l = l+1
                    elif (pos_list_2[l] > pos_list_1[k]): 
                        break
                    elif(pos_list_2[l] == pos_list_1[k]):
                        print("!!!!Same words cannot be followed!!!!")
                        exit()
                k=k+1
                
            Finalresult[0] = frequency
            Finalresult[1][documents2[j]] = pos_res_list
            i=i+1
            j=j+1
            
        else:
            if documents1[i] < documents2[j]:
                i=i+1
            else:
                j=j+1

    return Finalresult




def find_query(query,pos_index):
    terms= preprocessingtxt(query)
    if (len(terms)==0):
            print("Not exists")
            return 0
    for term in terms:
        if not (term in pos_index):
            print("Not exists")
            return 0
    finalresult = pos_index[terms[0]]
    medresult = pos_index[terms[0]]
    x=0
    y=1
    i=1
    newword=[]
    if (len(terms) == 1):
        return finalresult
    while (i < len(terms)):
        medresult = finalresult
        newword = pos_index[terms[y]]
        finalresult = intersection(medresult,newword)
        y=y+1
        i=i+1
    return finalresult
            

def findtf(document):
    con = {}
    for word in document:
        info =[]
        if word in con :
            con[word][0]['tf']= con[word][0]['tf'] +1
        else:
            info.append({'tf': 1})
            con[word] = info
    return con

def findtfwt(document):
    for term in document:
        document[term].append({'tfwt': 1+math.log10(document[term][0]['tf'])})
    return document

def add_df(document,pos_index):
    for term in document:
        if not term in pos_index:
            document[term].append({'df':0})
        else: 
            document[term].append({'df':pos_index[term][0]})
    return document

def find_idf(document,n):
    for term in document:
        x=document[term][2]['df']
        if x == 0:
            document[term].append({'idf':0}) 
        else:   
            document[term].append({'idf':math.log10(n/x)})
    return document

def find_wt(document):
    for term in document:
        document[term].append({"wt":document[term][3]['idf']*document[term][1]['tfwt']})

    return document


def find_length (document):
    scores=[]
    wts = []
    sqrwts = 0
    for term in document:
        wts.append(document[term][4]['wt'])
    for i in wts:
        sqrwts= sqrwts + (i*i)
    lenght = math.sqrt(sqrwts)
    for term in document:
        document[term].append({'length':lenght})
    return document

def find_norm(document):
    for term in document:
            if(document[term][4]['wt'] == 0):
                document[term].append({'norm':0 })
            else:
                document[term].append({'norm':document[term][4]['wt']/document[term][5]['length']})
    return document

  
def find_args (folder,pos_index,query):
    folder_names = "documents"
    fileno = 0
    allterms=list(pos_index.keys())
    scores={}
    matrix=[]
    file_names = natsorted(os.listdir(folder))
    n = len (list (file_names))
    final_token_list = preprocessingtxt(query)
    queryargs = findtf(final_token_list)
    queryargs = findtfwt(queryargs)
    queryargs = add_df(queryargs,pos_index)
    queryargs = find_idf(queryargs,n)
    queryargs = find_wt(queryargs)
    queryargs = find_length(queryargs)
    queryargs = find_norm(queryargs)
    #print ("Query Norm ->",queryargs)
    for file_name in file_names:
        doc = open(folder+"\\"+  file_name,"r")
        stuff= doc.read()
        final_token_list = preprocessingtxt(stuff)
        args = findtf(final_token_list)
        args = findtfwt(args)
        args = add_df(args,pos_index)
        args = find_idf(args,n)
        agrs = find_wt(args)
        args = find_length(args)
        args = find_norm(args)
        #print("Norm args->",args)
        matrix.append([args])
        score = []
        for termQ in queryargs:
            for termD in args:
                if(termD == termQ):
                    score.append(queryargs[termQ][6]['norm'] * args[termD][6]['norm'])
                    break
        sum=0
        for v in score:
            sum = sum +v
        scores[file_name]=sum
    ilist =[]
    s=0
    for fl in file_names:
        ilist.append(s)
        s=s+1
    print("\t",end='')
    for name in file_names:
        print(name,"\t",end='')
    print("\n")
    for ter in allterms:
        print(ter[0:5],"\t",end='')
        for i in ilist:
            if (ter in matrix[i][0].keys()):
                print("%.2f"%matrix[i][0][ter][4]['wt'],'\t\t',end='')
            else:
                print(0,'\t\t',end='')
            i = i+1
        print("\n")
    return scores

   
pos_index= constract("D:\Abdoo\Level 3\Semester 1\IR\Project\documents")
print(pos_index)
#print(find_args ('D:\Abdoo\Level 3\Semester 1\IR\Project\documents',pos_index,'cairo in egypt'))