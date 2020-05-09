#!/usr/bin/env python
# nltk_download.py

# BEFORE running this script, and ensure that you have downloaded
# the requirements in requirments.txt. Then, when you run this
# script, a GUI will appear. Click 'download' to download the nltk
# library files in your home directory.

import nltk
import ssl
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

print("======================================================================================================================")
print("\033[96m\033[1mACTION REQUIRED:\033[0m")
print("Please navigate to the NLTK downloader window now (it may have popped up behind other open windows).")
print("Go to the 'All Packages' tab and install the required packages: \033[1maveraged_perceptron_tagger, punkt, stopwords, wordnet\033[0m.")
print("After installing, you may close the pop up to resume script execution.")

nltk.download()
print("======================================================================================================================")
