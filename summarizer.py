#!/usr/bin/env python
# summarizer.py

import nltk
from nltk.stem import WordNetLemmatizer, PorterStemmer
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

def stem(sentences):
    
    stemmer = PorterStemmer()
    stemmed = []
    for sent in sentences:
        new_sent = []
        for word,tag in sent:
            new_sent.append((stemmer.stem(word), tag))
        stemmed.append(new_sent)
    return stemmed

def lemmatize(sentences):

    lemmatizer = WordNetLemmatizer()
    lemmatized = []
    for sent in sentences:
        new_sent = []
        for word,tag in sent:
            wordnet_tag = get_wordnet_tag(tag)
            new_sent.append((lemmatizer.lemmatize(word, wordnet_tag), tag))
        lemmatized.append(new_sent)
    return lemmatized


"""
Print side-by-side comparsion of lemmatization and stemming.
"""
def lemma_vs_stem():
    print(len(sentences))
    print(len(lemmatized_sentences))
    print(len(stemmed_sentences))
    for i in range(len(lemmatized_sentences)):
        for j in range(len(lemmatized_sentences[i])):
            print(sentences[i][j][0], lemmatized_sentences[i][j][0], stemmed_sentences[i][j][0])


if __name__ == '__main__':
    sentences = preprocess('covid.txt')
    lemmatized_sentences = lemmatize(sentences)
    stemmed_sentences = stem(sentences)