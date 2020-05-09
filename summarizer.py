#!/usr/bin/env python
# summarizer.py

import re
import sys
import math
import nltk
from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk.corpus import wordnet, stopwords
from nltk import RegexpParser
import collections
from collections import defaultdict

TITLE = ""
DATE = ""
REGION = ""

_surrogates = re.compile(r"[\uDC80-\uDCFF]")

def detect_decoding_errors_line(l, _s=_surrogates.finditer):
    """Return decoding errors in a line of text

    Works with text lines decoded with the surrogateescape
    error handler.

    Returns a list of (pos, byte) tuples

    """
    # DC80 - DCFF encode bad bytes 80-FF
    return [(m.start(), bytes([ord(m.group()) - 0xDC00]))
            for m in _s(l)]

"""
Converts nltk-form parts of speech to wordnet-form parts of speech to allow for proper comparison.
"""
def nltk_to_wn_pos(nltk_pos):
    translation = {
        'NN': 'n',
        'NNS': 'n',
        'NNP': 'n',
        'NNPS': 'n',
        'PRP': 'n',
        'VB': 'v',
        'VBD': 'v',
        'VBG': 'v',
        'VBN': 'v',
        'VBP': 'v',
        'VBZ': 'v',
        'JJ': 'a',
        'JJR': 'a',
        'JJS': 'a',
        'RB': 'r',
        'RBR': 'r',
        'RBS': 'r',
    }

    return translation.get(nltk_pos, -1)


"""
Returns a list of amplifiers corresponding to sentences related to the search query.
"""
def get_search_weights(sentences, query, pos):
    THRESHOLD = 0.76
    query_syns = wordnet.synsets(query, pos=pos)
    weights = []

    for sentence in sentences:
        score = 1
        for word in sentence:
            if nltk_to_wn_pos(word[1]) == pos:
                word_syns = wordnet.synsets(word[0], pos=pos)
                for word_syn in word_syns:
                    for query_syn in query_syns:
                        if word_syn.lemmas()[0].name() == word[0]:
                            sim = word_syn.wup_similarity(query_syn)
                        else:
                            sim = 0
                        if sim is not None and sim > THRESHOLD:
                            # print(word[0], sim)
                            score += sim
        weights.append(score)

    return weights


"""
Enable/disable query-based summarization
"""
def ask_search():
    enable = False
    response = input(
        'Would you like to summarize based on a certain term? [y][any other key]\n')

    if response == 'y':
        enable = True

    if not enable:
        return enable, None, None

    query = input('Enter your term:\n')
    pos = input(
        'Enter your term\'s part of speech (noun=n, verb=v, adjective=a, adverb=r):\n')

    return enable, query, pos


"""
Remove stopwords from sentences. Returns modified sentences.
"""
def remove_stopwords(sentences):
    stop_words = set(stopwords.words('english'))
    filtered_sentences = []
    for sent in sentences:
        filtered_sent = [(w, t)
                         for (w, t) in sent if not w.lower() in stop_words]
        filtered_sentences.append(filtered_sent)
    return filtered_sentences


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
        with open(file_name, 'r', encoding="utf8", errors="surrogateescape") as f:
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
def get_term_weight(term, term_freqs, sentences):
    term_freq = term_freqs[term]
    num_sentences = len(sentences)
    term_SF = 0
    for sent in sentences:
        if term in sent:
            term_SF += 1
    term_ISF = math.log(num_sentences / float(term_SF))
    return term_freq * term_ISF


"""
Calculate the weights of each sentence in the list of sentences,
using term_freqs. Returns a list of float weights.
"""
def get_sentence_weights(sentences, term_freqs):
    weights = []
    for sent in sentences:
        sent_weight = 0
        for term in sent:
            sent_weight += get_term_weight(term, term_freqs, sentences)
        weights.append(sent_weight)
    return weights


"""
Main function.
"""
def main():

    if len(sys.argv) != 3:
        print("Usage: python summarizer.py file_path summary_length",
              file=sys.stderr)
        print("    file_path: the string path to the file you would like to summarize", file=sys.stderr)
        print("    summary_length: the integer number of sentences in generated summary", file=sys.stderr)
        sys.exit(1)

    filepath = sys.argv[1]

    if not sys.argv[2].isdigit():
        print("Summary length must be an integer", file=sys.stderr)
        sys.exit(1)

    num_sentences = int(sys.argv[2])

    # Preprocessing
    sentences, og_sentences = preprocess(filepath, num_sentences)

    # Prompt user for keyword
    search_mode, query, pos = ask_search()

    # Lemmatization and Stemming
    lemmatized_sentences = lemmatize(sentences)
    stemmed_sentences = stem(lemmatized_sentences)

    # Noun-verb chunking and frequency calculation
    chunked_sentences = chunk(stemmed_sentences)
    freqs = get_term_freqs(chunked_sentences)
    sentence_weights = get_sentence_weights(chunked_sentences, freqs)

    # Add keyword weights if search is enabled
    if search_mode:
        search_weights = get_search_weights(lemmatized_sentences, query, pos)
        sentence_weights = [a*b for a,
                            b in zip(sentence_weights, search_weights)]

    # Rank sentences based on weights
    ranked_sentence = sorted(
        ((sentence_weights[i], s) for i, s in enumerate(og_sentences)), reverse=True)

    # Derive original ordering of sentences
    summary = []
    for i in range(num_sentences):
        summary.append(ranked_sentence[i][1])

    index_map = {}  # mapping of original index to current index
    for ind, sentence in enumerate(summary):
        og_index = og_sentences.index(sentence)
        index_map[og_index] = ind

    # Output summary
    sorted_indices = collections.OrderedDict(sorted(index_map.items()))
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
