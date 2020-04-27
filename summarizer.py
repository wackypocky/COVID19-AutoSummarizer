#!/usr/bin/env python
# summarizer.py

import re
import nltk
from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk.corpus import wordnet, stopwords
from nltk import RegexpParser
from collections import defaultdict


"""
Remove stopwords from sentences. Returns modified sentences.
"""
def remove_stopwords(sentences):
    stop_words = set(stopwords.words('english'))
    filtered_sentences = []
    for sent in sentences:
        filtered_sent = [(w,t) for (w,t) in sent if not w.lower() in stop_words]
        filtered_sentences.append(filtered_sent)
    return filtered_sentences


"""
Prepocess raw text data in file_name by segmenting the text into
sentences, and tokenizing all of the words. Uses POS-tagging to
return a list of lists of tuples, where the tuples contain a
word and its POS tag.
"""
def preprocess(file_name):

    f = open(file_name, 'r')

    # protect certain characters from splitting
    raw_text = re.sub(r'(@)', r'_\1_', f.read())

    # tokenize and add POS tags
    sentences = nltk.sent_tokenize(raw_text)
    sentences = [nltk.word_tokenize(sent) for sent in sentences]
    sentences = [nltk.pos_tag(sent) for sent in sentences]
    sentences = remove_stopwords(sentences)
    return sentences


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


"""
Produce lemmas of all the words in each of the sentences.
Returns a list of lists of tuples, where the first element is the
lemma of the original word, and the second element is the POS tag.
"""
def lemmatize(sentences):

    lemmatizer = WordNetLemmatizer()
    lemmatized = []
    for sent in sentences:
        new_sent = []
        for word, tag in sent:
            wordnet_tag = get_wordnet_tag(tag)
            new_sent.append((lemmatizer.lemmatize(word, wordnet_tag), tag))
        lemmatized.append(new_sent)
    return lemmatized


"""
Produce stems of all the words in each of the sentences.
Returns a list of lists of tuples, where the first element is the
stem of the original word, and the second element is the POS tag.
"""
def stem(sentences):

    stemmer = PorterStemmer()
    stemmed = []
    for sent in sentences:
        new_sent = []
        for word, tag in sent:
            new_sent.append((stemmer.stem(word), tag))
        stemmed.append(new_sent)
    return stemmed


"""
Print side-by-side comparsion of lemmatization and stemming.
"""
def lemma_vs_stem(sentences, lemmatized_sentences, stemmed_sentences):
    for i in range(len(lemmatized_sentences)):
        for j in range(len(lemmatized_sentences[i])):
            print(sentences[i][j][0], lemmatized_sentences[i][j][0],
                  stemmed_sentences[i][j][0])


"""
Return a new set of POS-tagged words that have been
chunked into NN, NNP, or VP clusters.
"""
def chunk(sentences):
    grammar = r"""
        NN:     {<DT|PP\$>?<JJ>*<NN>}   # chunk determiner/possessive, adjectives and noun
                {<DT|PP\$>?<JJ>*<NNS>}
        NNP:    {<NNP>+}                # chunk sequences of proper nouns
                {<NNP>*<NNPS>}
        VP:     {<VB>}                  # chunk any kind of verb
                {<VBD>}
                {<VBN>}
                {<VBG>}
                {<VBP>}
                {<VBZ>}
"""
    chunk_parser = RegexpParser(grammar)
    chunked = []
    for sent in sentences:
        new_sent = []
        tree = chunk_parser.parse(sent)
        for subtree in tree.subtrees(lambda t: t.height() == 2):
            new_word = ' '.join([w for (w, t) in subtree.leaves()])
            new_tag = subtree.label()
            new_sent.append((new_word, new_tag))
        chunked.append(new_sent)
    return chunked


"""
Calculate the frequencies of all unique terms in the sentences.
Returns a dict of terms that map to integer frequencies.
"""
def get_term_freqs(sentences):
    term_freqs = defaultdict(int)
    for sent in sentences:
        for pair in sent:
            term_freqs[pair] += 1
    return term_freqs


"""
Calculate the weight of a term within term_freqs. Returns a
float weight value.
"""
def get_term_weight(term, term_freqs):
    term_freq = term_freqs[term]
    n = len(term_freqs)
    term_weight = term_freq * 1000.0 / float(n)
    return term_weight


"""
Main function.
"""
def main():
    sentences = preprocess('covid.txt')
    lemmatized_sentences = lemmatize(sentences)
    stemmed_sentences = stem(lemmatized_sentences)
    chunked_sentences = chunk(stemmed_sentences)
    freqs = get_term_freqs(chunked_sentences)
    for key, value in sorted(freqs.items(), reverse=True, key=lambda item: item[1]):
        print(key, value)


if __name__ == '__main__':
    main()
