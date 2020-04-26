#!/usr/bin/env python
# summarizer.py

import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet

"""
Prepocess raw text data in file_name by segmenting the text into
sentences, and tokenizing all of the words. Uses POS-tagging to
return a list of lists of tuples, where the tuples contain a
word and its POS tag.
"""
def preprocess(file_name):

    f = open(file_name, 'r')
    raw_text = f.read()
    sentences = nltk.sent_tokenize(raw_text)
    sentences = [nltk.word_tokenize(sent) for sent in sentences]
    sentences = [nltk.pos_tag(sent) for sent in sentences]
    return sentences


# def noun_verb_chunking(sentences):
#     NOUN_VERB_TAGS = ['NN', 'NNS', 'NNP', 'NNPS', 'VB', 'VBD', 'VBG', \
#          'VBN', 'VBP', 'VBZ']
#     chunks = []
#     for sent in sentences:
#         for (word, tag) in sent:
#             if tag in NOUN_VERB_TAGS:
#                 chunks.append((word, tag))
#     return chunks


"""
Return the equivalent wordnet POS tag for the given nltk
POS tag.
"""
def get_wordnet_tag(nltk_tag):
    
    if nltk_tag.startswith('J'):
        return wordnet.ADJ
    elif nltk_tag.startswith('V'):
        return wordnet.VERB
    elif nltk_tag.startswith('N'):
        return wordnet.NOUN
    elif nltk_tag.startswith('R'):
        return wordnet.ADV
    else:
        # Use noun as a default POS tag in lemmatization
        return wordnet.NOUN

def lemmatize(sentences):

    lemmatizer = WordNetLemmatizer()
    lemmatized = []
    for sent in sentences:
        for (word,tag) in sent:
            wordnet_tag = get_wordnet_tag(tag)
            lemmatized.append((lemmatizer.lemmatize(word, wordnet_tag), tag))
            print(word, lemmatizer.lemmatize(word, wordnet_tag))
    return lemmatized


if __name__ == '__main__':
    sentences = preprocess('covid.txt')
    lemmatized_sentences = lemmatize(sentences)
    #print(lemmatized_sentences)



    # chunks = noun_verb_chunking(sentences)
    # print(chunks)