import subprocess
import os
import re
from summarizer import lemmatize, stem, chunk, get_term_freqs, get_sentence_weights, get_search_weights, remove_stopwords

import collections
import nltk
from nltk.corpus import wordnet, stopwords
import argparse
import sys

TITLE = ""
DATE = ""
REGION = ""

"""
Prepocess raw text data in file_name by segmenting the text into
sentences, and tokenizing all of the words. Uses POS-tagging to
return a list of lists of tuples, where the tuples contain a
word and its POS tag.
"""
def preprocess(file_name, num_sentences):

    global TITLE
    global DATE
    global REGION

    try:
        with open(file_name, 'r') as f:
            TITLE = f.readline()  # title of article
            DATE = f.readline()
            REGION = f.readline()
            # list of tags, each tag is a string with format 'tag_freq_relevanceScore'
            tags = f.readline()
            # read rest of file
            raw_text = f.read()
    except Exception as e:
        print("An error occurred when processing your file:\n" +
              str(e), file=sys.stderr)
        sys.exit(1)

    # protect certain characters from splitting
    subbed_sentences = re.sub(r'(@)', r'_\1_', raw_text)

    # tokenize
    og_sentences = nltk.sent_tokenize(raw_text)
    sentences = nltk.sent_tokenize(subbed_sentences)

    # check if there are more sentences than needed
    if len(sentences) < num_sentences:
        print("Text has fewer (or equal number of) sentences than requested summary:")
        print(raw_text)
        exit(0)

    # tokenize and add POS tags
    sentences = [nltk.word_tokenize(sent) for sent in sentences]
    sentences = [nltk.pos_tag(sent) for sent in sentences]
    sentences = remove_stopwords(sentences)
    return sentences, og_sentences

"""
Calls summarizer.py function
"""
def summarize(filepath, num_sentences, search_mode, query=None, pos=None):
    sentences, og_sentences = preprocess(filepath, num_sentences)
    lemmatized_sentences = lemmatize(sentences)
    stemmed_sentences = stem(lemmatized_sentences)
    chunked_sentences = chunk(stemmed_sentences)
    freqs = get_term_freqs(chunked_sentences)
    sentence_weights = get_sentence_weights(chunked_sentences, freqs)
    if search_mode:
        search_weights = get_search_weights(lemmatized_sentences, query, pos)
        sentence_weights = [a*b for a,b in zip(sentence_weights, search_weights)]

    average_weight = sum(sentence_weights) / len(sentence_weights)
    ranked_sentence = sorted(((sentence_weights[i],s) for i,s in enumerate(og_sentences)), reverse=True)

    summary = []
    for i in range(num_sentences):
        summary.append(ranked_sentence[i][1])

    index_map = {} # mapping of original index to current index
    for ind, sentence in enumerate(summary):
        og_index = og_sentences.index(sentence)
        index_map[og_index] = ind

    sorted_indices = collections.OrderedDict(sorted(index_map.items()))
    return sorted_indices, summary

"""
Main function.
"""
def main():
    parser = argparse.ArgumentParser(description='Non-interactive Summarizer')

    # optional arguments
    parser.add_argument('-s', action='store_true', default=False,
                    dest='search_mode',
                    help='Turn search_mode on')

    parser.add_argument('-q', action='store', dest='query',
                    help='Query to Google Search')

    parser.add_argument('-p', action='store', dest='pos',
                    help='Part of speech of the query passed to -q (noun=n, verb=v, adjective=a, adverb=r)')

    # required arguments
    parser.add_argument('file_path', action="store", type=str, help="The string path to the text file you would like to summarize")
    parser.add_argument('summary_length', action="store", type=int, help="The integer number of sentences desired in generated summary")

    args = parser.parse_args()
    if args.search_mode and (args.query is None or args.pos is None):
        parser.error("-s requires -q [query] and -p [pos].")

    sorted_indices, summary = summarize(args.file_path, args.summary_length, args.search_mode, args.query, args.pos)
    print("Title:", TITLE, end="")
    if DATE != 'n/a\n':
        print("Published on:", DATE, end="")
    if REGION != 'n/a\n':
        print("Location:", REGION, end="")
    print()
    print("Summary of Text:")
    for key, val in sorted_indices.items():
        print(summary[val] + " ")

if __name__ == '__main__':
    main()
