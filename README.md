# COVID19-RequestsForAid

A text summarization project with the goal automatically summarizing articles scraped from Google containing "requests for aid" or information about how people can help in the COVID-19 crisis. Sentences are prioritized based on relevance and word importance.

## Usage

You will need to first install the packages in requirements.txt using:
```
pip install -r requirements.txt 
```

To scrape articles from Google based on a search query and save the title and body of the article into a text file:
```
python scraper.py [query] [number of search results to return]
```

To summarize an article with the preferred number of sentences:
```
python summarizer.py [/path/to/file] [summary length]
```