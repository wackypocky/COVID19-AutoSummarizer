# COVID19-RequestsForAid

A text summarization project with the goal automatically summarizing articles scraped from Google containing "requests for aid" or information about how people can help in the COVID-19 crisis. Sentences are prioritized based on relevance and word importance.

## Install

You will need to first install the packages in requirements.txt using:
```
pip install -r requirements.txt
```
Then run
```
python3 nltk_download.py
```
to install the required nltk packages. You may select the packages manually, or download the entire nltk library.
<br />
<br />
## Error Handling

If you encounter the following error (where "path_to_pythonrouge" is the location of pythonrouge on your computer) when running evaluation.py
```
subprocess.CalledProcessError: Command '['perl', 'path_to_pythonrouge/pythonrouge/RELEASE-1.5.5/ROUGE-1.5.5.pl', '-e', '[path_to_pythonrouge]/pythonrouge/RELEASE-1.5.5/data', '-a', '-n', '1', '-2', '4', '-u', '-x', '-l', '100', '-m', '-s', '-f', 'B', '-r', '1000', '-p', '0.5', '/tmp/tmpev7m7vla/setting.xml']' returned non-zero exit status 79.
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
<br />

## Usage

To scrape articles from Google based on a search query and save the title and body of the article into a text file:
```
python scraper.py search_query max_num_results
```
where:
<br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;search_query = the string query to Google Search on
<br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;max_num_results = the integer maximum number of desired results
<br />
To summarize an article with the preferred number of sentences:
```
python summarizer.py file_path summary_length
```
where:
<br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;file_path = path to the file you would like to summarize
<br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;summary_length = the number of sentences in generated summary
