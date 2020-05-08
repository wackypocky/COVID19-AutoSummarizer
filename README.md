# COVID19-RequestsForAid

A text summarization project with the goal automatically summarizing articles scraped from Google containing "requests for aid" or information about how people can help in the COVID-19 crisis. Sentences are prioritized based on relevance and word importance.

## Usage

You will need to first install the packages in requirements.txt using:
```
pip install -r requirements.txt
```
Then run
```
python3 nltk_download.py
```
to install the required nltk packages. You may select the packages manually, or download the entire nltk library.

If pythonrouge raises an error while running evaluation.py, navigate to the pythonrouge directory (usually you can see where this is from the error prompt) and run the script in buildExceptionDB by copy/pasting it into your console or terminal.
<br />
<br />
To scrape articles from Google based on a search query and save the title and body of the article into a text file:
```
python scraper.py search_query max_num_results
```
where:
<br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;search_query = the string query to Google Search on
<br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;max_num_results = the integer maximum number of desired results

To summarize an article with the preferred number of sentences:
```
python summarizer.py file_path summary_length
```
where:
<br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;file_path = path to the file you would like to summarize
<br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;summary_length = the number of sentences in generated summary
