from gensim.models import KeyedVectors
import numpy as np
import gensim
from nltk.corpus import stopwords
import textwrap

# load text
filename = 'OriginalToBesummarized.txt'
file = open(filename, 'rt', encoding='utf-8')
originaltexts = file.readlines()
file.close()
#print(originaltexts[0])
print(len(originaltexts))

summary=open("ReferenceSummary.txt","a", encoding='utf-8')
for i in range(len(originaltexts)):
    listsentences=originaltexts[i].split('. ')
    #print(listsentences[0])
    def sent_to_words(sentences):
        for sentence in sentences:
            yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))   # deacc=True removes punctuations

    listwordssentences = list(sent_to_words(listsentences))
    #print(listwordssentences)
    #print(len(listwordssentences))

    # Define functions for removing stopwords
    def remove_stopwords(texts):
        stop_words = stopwords.words('english')
        return [[word for word in gensim.utils.simple_preprocess(str(doc)) if word not in stop_words] for doc in texts]
    nonstopwords=remove_stopwords(listsentences)
    #print(nonstopwords)
    #print(len(nonstopwords))

    wordcount=[]
    for j in range(len(nonstopwords)):
        for m in range(len(nonstopwords[j])):
            wordcount.append(nonstopwords[j][m])
    #print(wordcount)
    #print(len(wordcount))

    wordfreq = {}
    unwanted_chars = ".,-_ (and so on)"
    for raw_word in wordcount:
        word = raw_word.strip(unwanted_chars)
        if word not in wordfreq:
            wordfreq[word] = 0
        wordfreq[word] += 1
    #print(wordfreq)
    m=len(wordfreq)-5                                                          #5 is just to use only top 5 frequent words and can be changed as per the users need
    topfivefrequentwords=sorted(wordfreq.items(), key = lambda x : x[1])[m:].copy()  #list of top 5 frequent words
    #print(topfivefrequentwords)

    confirmtopfive=[]
    for b in range(len(topfivefrequentwords)):
        if topfivefrequentwords[b][1]>2:                                       #how many times the frequent words are frequent, here we consider words that occured three or more times
            confirmtopfive.append(topfivefrequentwords[b][0])
    #print(confirmtopfive)

    filename = 'GoogleNews-vectors-negative300.bin'                            # Word2Vec based WETS
    #filename = 'glove.840B.300d.txt.word2vec.bin'                             # GloVe based WETS
    #filename = 'cc.en.300.vec.bin'                                            # FastText based WETS

    model = KeyedVectors.load_word2vec_format(filename, binary=True)
    embwords = list(model.wv.vocab)

    firstsentwordsinwordvec=[]
    for m in range(len(nonstopwords[0])):
        if nonstopwords[0][m] in embwords:
            firstsentwordsinwordvec.append(nonstopwords[0][m])
    #print(firstsentwordsinwordvec)
    #print(len(firstsentwordsinwordvec))
    for n in range(len(confirmtopfive)):
        if confirmtopfive[n] in embwords:
            firstsentwordsinwordvec.append(confirmtopfive[n])
    #print(firstsentwordsinwordvec)
    #print(len(firstsentwordsinwordvec))

    othersentnonredundant=[]
    for h in range(len(nonstopwords)-1):
        k=h+1
        nonrepeatedwords=np.setdiff1d(nonstopwords[k],firstsentwordsinwordvec) #Removing words of other sentences that exist in the first sentence to discourage redundancy
        othersentnonredundant.append(nonrepeatedwords)
    #print(othersentnonredundant)
    #print(len(othersentnonredundant))

    othersentwordsinwordvec=[]
    for r in range(len(othersentnonredundant)):
        l=[]
        for m in range(len(othersentnonredundant[r])):
            if othersentnonredundant[r][m] in embwords:                        #Check existance of words in the vocabulalry of word embedding
                l.append(othersentnonredundant[r][m])
        othersentwordsinwordvec.append(l)
    #print(othersentwordsinwordvec[0])
    #print(len(othersentwordsinwordvec[0]))
    #print(len(othersentwordsinwordvec))


    totlen=0
    for p in range(len(othersentwordsinwordvec)):
        totlen=totlen+len(othersentwordsinwordvec[p])
    totlen=totlen+len(firstsentwordsinwordvec)                                 #Total words after preprocessing: words of first sentence + words of other sentences
    #print(totlen)

    relevance=[]
    for u in range(len(othersentwordsinwordvec)):
        weight=0.0
        relevancescore=0.0
        sentweight=0.0
        for n in range(len(othersentwordsinwordvec[u])):
            result=[model.wv.similarity(othersentwordsinwordvec[u][n],word) for word in firstsentwordsinwordvec]
            weight=max(result)
            sentweight=sentweight+weight
        if len(othersentwordsinwordvec[u])>0:
            relevancescore=sentweight/len(othersentwordsinwordvec[u])
        else:
            relevancescore=0.0

        relevance.append(relevancescore)

    #print(relevance)
    ordertop=relevance.copy()
    def Nmaxelements(list1, N):                                                #This function helps to the top salient sentence in order
        final_list = []

        for x in range(0, N):
            max1 = 0

            for t in range(len(list1)):
                if list1[t] > max1:
                    max1 = list1[t];

            list1.remove(max1);
            final_list.append(max1)

        return final_list

    percentrequired=0.5                                                        #This is to show that length of the summary should be at least half of the original text
    compressionratio=len(listsentences)*percentrequired
    comressionration=int(compressionratio)
    mostimportantsentindexedfscore=Nmaxelements(ordertop,comressionration)
    #print(mostimportantsentindexedfscore)
    #print("\n")
    #print(relevance)
    #print("\n")

    #print(listsentences[0])

    summary.write(listsentences[0])
    #summary.write(". ")
    for w in range(len(mostimportantsentindexedfscore)):
        locatetopsen=(relevance.index(mostimportantsentindexedfscore[w])+1)
        #print(listsentences[locatetopsen])
        my_wrap = textwrap.TextWrapper(width = 150)                            #It shows number of words that the user need to have in the summary, here for example 200, it can be changed.
        wrap_list = my_wrap.wrap(text=listsentences[locatetopsen])
        summary.write(str(wrap_list))
        #summary.write(". ")
    summary.write("\n")
summary.close()
print("DONE!")
