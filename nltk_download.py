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

nltk.download()