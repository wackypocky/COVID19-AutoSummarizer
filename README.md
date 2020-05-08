# COVID19-RequestsForAid

A text summarization project with the goal automatically summarizing articles scraped from Google containing "requests for aid" or information about how people can help in the COVID-19 crisis. Sentences are prioritized based on relevance and word importance.

## Usage

You will need to first install the packages in requirements.txt using:
```
pip install -r requirements.txt 
```

To scrape articles from Google based on a search query and save the title and body of the article into a text file:
```
python scraper.py [search_query] [max_num_results]
    search_query: the string query to Google Search on
    max_num_results: the integer maximum number of desired results
```

To summarize an article with the preferred number of sentences:
```
Usage: python summarizer.py [file_path] [summary_length]
    file_path: path to the file you would like to summarize
    summary_length: the number of sentences in generated summary
```