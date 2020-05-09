#!/usr/bin/env python
# evaluation.py

import subprocess
import os
import re
from noninteractive_summarizer import summarize
import collections
import nltk
from nltk.translate.bleu_score import corpus_bleu
from pythonrouge.pythonrouge import Pythonrouge

"""
Helper function to break file into tokenized sentences.
"""
def get_raw_sentences(file_name):
    f = open(file_name, 'r')
    sentences = nltk.sent_tokenize(f.read())
    return sentences

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
Main function.
"""
def main():
    cwd = os.getcwd()
    ogdir = os.listdir(cwd + "/eval_ogtext")
    refdir = os.listdir(cwd + "/eval_references")
    genrefdir = os.listdir(cwd+"/eval_generatedrefs")
    for file in ogdir:
        if file not in refdir:
            print("error: reference summary not found")
        else:

            ref_filename = "eval_references/" + file
            ref_sentences = get_raw_sentences(ref_filename)

            num_sentences = len(ref_sentences)
            with open(ref_filename, 'r') as f:
                ref_summary = f.read()

            if file[:-4] not in genrefdir:
                genref_summaries = []
            else:
                sumdirname= "eval_generatedrefs/" + file[:-4]
                sumdir = os.listdir(sumdirname)
                genref_summaries = []
                for sumfile in sumdir:
                    filename = sumdirname+"/"+sumfile
                    genref_sentences = get_raw_sentences(filename)
                    if len(genref_sentences) > num_sentences:
                        num_sentences = len(genref_sentences)
                    with open(filename, 'r') as f:
                        genref_summaries.append(f.read())

                ogfilepath = "eval_ogtext/" + file
                sorted_indices, summary = summarize(ogfilepath, num_sentences, False)
                gen_summary = ""
                for key, val in sorted_indices.items():
                    gen_summary += summary[val] + " "

                gen_filepath = "eval_gen_summaries/" + file
                with open(gen_filepath, "w") as f:
                    f.write(gen_summary)

                bleu_score, rouge_score = evaluate(gen_summary, ref_summary, genref_summaries)
                print(file + ":", "bleu - " + str(bleu_score) + ",", "rouge - " + str(rouge_score))

if __name__ == '__main__':
    main()
