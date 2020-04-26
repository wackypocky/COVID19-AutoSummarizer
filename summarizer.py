#!/usr/bin/env python
# summarizer.py

import nltk

# Prepocess raw text data in file_name by segmenting the text into
# sentences, and tokenizing all of the words. Uses POS-tagging to
# return a list of lists of tuples, where the tuples contain a
# word and its POS tag.
def preprocess(file_name):
    f = open(file_name, 'r')
    raw_text = f.read()
    sentences = nltk.sent_tokenize(raw_text)
    sentences = [nltk.word_tokenize(sent) for sent in sentences]
    sentences = [nltk.pos_tag(sent) for sent in sentences]
    print(sentences)

if __name__ == '__main__':
    preprocess('covid.txt')