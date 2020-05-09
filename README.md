# COVID19-AutoSummarizer

A text summarization project with the goal of automatically summarizing articles scraped from Google containing "requests for aid" or information about how people can help in the COVID-19 crisis. Sentences are prioritized based on relevance and word importance.

## Install

You will need to first install the packages in requirements.txt using:
```
pip3 install -r requirements.txt
```
Then run
```
python3 nltk_download.py
```
to install the required nltk packages. You may select the packages manually, or download the entire nltk library using the nltk GUI.


The required packages are:
- averaged_perceptron_tagger
- punkt
- stopwords
- wordnet          

## Usage

### Running a Test
To **run a test** through all functionalities (scraper, summarizer, and evaluation):
```
./RunMe
```
This will also install all dependencies from requirements.txt and run nltk_download.py.


You may need to run
```
chmod 700
```
on the RunMe file for execution permissions.


If you run into a subprocess error during evaluation, please see [Error Handling](#Error-Handling).




### Scraping
To **scrape** articles from Google based on a search query and save the title and body of the article into a text file:
```
python3 scraper.py search_query max_num_results
```
where:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;search_query = the string query to Google Search on

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;max_num_results = the integer maximum number of desired results




### Summarizing
To **summarize** an article with the preferred number of sentences:
```
python3 summarizer.py file_path summary_length
```
where:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;file_path = the string path to the file you would like to summarize

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;summary_length = the integer number of sentences in generated summary



Files input to the summarizer should have at least 5 lines:
```
Line 1: TITLE
Line 2: DATE_TIME
Line 3: LOCATION
Line 4: ARTICLE_TAGS
Line 5: content line 1
...
Line n: content line m
```
This is the format of articles produced by the scraper. If you would like to summarize articles that were not generated by the scraper, please ensure that you have the first 4 lines for TITLE, DATE_TIME, LOCATION, ARTICLE_TAGS. If any of those fields do not apply to your article, write n/a for that line.



### Evaluating
To **evaluate** the generated summaries in directory 'eval_gen_summaries' with BLEU and ROUGE scores:
```
python3 evaluation.py
```
Note that if you wish to add a new generated summary to the directory and evaluate it, you must add the corresponding original text file to the 'eval_ogtext' directory, and a reference summary file to the 'eval_references' directory. Both the original text file and the reference summary file MUST be named identically to the summary file you wish to evaluate.


If you wish to evaluate the generated summary against more than one reference summary, please add all additional summary text files to a subdirectory in the 'eval_generatedrefs' directory. Again, the subdirectory MUST be named identically to the summary file you wish to evaluate.



## Error Handling

If you encounter the following error (where "path_to_pythonrouge" is the location of pythonrouge on your computer) when running evaluation.py
```
subprocess.CalledProcessError: Command '['perl', 'path_to_pythonrouge/RELEASE-1.5.5/ROUGE-1.5.5.pl', '-e', '[path_to_pythonrouge]/pythonrouge/RELEASE-1.5.5/data', '-a', '-n', '1', '-2', '4', '-u', '-x', '-l', '100', '-m', '-s', '-f', 'B', '-r', '1000', '-p', '0.5', '/tmp/tmpev7m7vla/setting.xml']' returned non-zero exit status 79.
```
navigate to the pythonrouge directory with
```
cd path_to_pythonrouge
```
and run the following script:
```
cd RELEASE-1.5.5/data/
rm WordNet-2.0.exc.db
./WordNet-2.0-Exceptions/buildExeptionDB.pl ./WordNet-2.0-Exceptions ./smart_common_words.txt ./WordNet-2.0.exc.db
```
