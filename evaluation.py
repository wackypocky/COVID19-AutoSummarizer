import subprocess
import os
import re
from summarizer import preprocess, lemmatize, stem, chunk, get_term_freqs, get_sentence_weights, get_search_weights, get_raw_sentences
import collections
import nltk
from nltk.translate.bleu_score import corpus_bleu
from pythonrouge.pythonrouge import Pythonrouge


"""
Evaluation function.
"""
def evaluate(gen_summary, ref_summary, genref_summaries):
    references = []
    ref_subbed_sentences = re.sub(r'(@)', r'_\1_', ref_summary)
    ref_sentences = nltk.word_tokenize(ref_subbed_sentences)
    references.append(ref_sentences)

    for summary in genref_summaries:
        ref_subbed_sentences = re.sub(r'(@)', r'_\1_', summary)
        ref_sentences = nltk.word_tokenize(ref_subbed_sentences)
        references.append(ref_sentences)

    gen_subbed_sentences = re.sub(r'(@)', r'_\1_', gen_summary)
    gen_sentences = nltk.word_tokenize(gen_subbed_sentences)
    bleu_score = corpus_bleu([references], [gen_sentences], weights=(1, 0))

    rouge = Pythonrouge(summary_file_exist=False,
                    summary=[gen_sentences], reference=[references],
                    n_gram=1, ROUGE_SU4=True, ROUGE_L=False,
                    recall_only=False, stemming=True, stopwords=True,
                    word_level=True, use_cf=False, cf=95, scoring_formula='best',
                    resampling=True, samples=1000, favor=True, p=0.5)
    rouge_score = rouge.calc_score()
    return bleu_score, rouge_score


"""
Calls summarizer.py functions
"""
def summarize(filename, num_sentences):
    filepath = "corpus/" + filename
    search_mode = True
    query = "help"
    pos = "v"

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
    gen_summary = ""
    for key, val in sorted_indices.items():
        gen_summary += summary[val] + " "
    gen_filepath = "summaries/" + filename
    with open(gen_filepath, "w") as f:
        f.write(gen_summary)
    return gen_summary

"""
Main function.
"""
def main():
    cwd = os.getcwd()
    ogdir = os.listdir(cwd + "/corpus")
    refdir = os.listdir(cwd + "/references")
    genrefdir = os.listdir(cwd+"/generatedrefs")
    for file in ogdir:
        if file not in refdir:
            print("error")
        else:

            ref_filename = "references/" + file
            ref_sentences = get_raw_sentences(ref_filename)
            print(len(ref_sentences))
            num_sentences = len(ref_sentences)
            with open(ref_filename, 'r') as f:
                ref_summary = f.read()

            if file[:-4] not in genrefdir:
                genref_summaries = []
            else:
                sumdirname= "generatedrefs/" + file[:-4]
                sumdir = os.listdir(sumdirname)
                genref_summaries = []
                for sumfile in sumdir:
                    filename = sumdirname+"/"+sumfile
                    genref_sentences = get_raw_sentences(filename)
                    if len(genref_sentences) > num_sentences:
                        num_sentences = len(genref_sentences)
                    with open(filename, 'r') as f:
                        genref_summaries.append(f.read())
                gen_summary = summarize(file, num_sentences)
                bleu_score, rouge_score = evaluate(gen_summary, ref_summary, genref_summaries)
                print(file + ":", "bleu - " + str(bleu_score) + ",", "rouge - " + str(rouge_score))

if __name__ == '__main__':
    main()
