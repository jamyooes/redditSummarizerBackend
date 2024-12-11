# Reddit Summarizer
This is all the backend logic for the project
Frontend is set up here https://github.com/jamyooes/redditsummarizer/tree/main

##  Project Description (from textdata)
In this project, we’ll build a chrome extension that will summarize threads from Reddit. At a very high level, the extension can be activated when a user is on a Reddit thread. It will then send a request to the backend which will scrape some number of top level comments and concatenate them together to serve as input into our text summarization model which will generate a brief summary of the provided comments. Preprocessing comments will include all standard procedures of text cleaning (removing emojis, html tags, etc.) stemming words, and removing stop words.

We will use a few different text summarization methods potentially including Luhn, Edmunson, and Latent Semantic Analysis. In order to determine the best output among models, the general idea is that the summary most relevant to the original input will be the best summary. We can use measures such as TF-IDF (vectorize summaries, and compare cosine similarities between each summary and the original input), and BM25 (use the original input as a query and rank the summaries as “documents”) among others. If time allows and just for fun we can also call an LLM library (if we can find a free one) and ask it to summarize although I heavily suspect this will always be evaluated as the best summary.

We can evaluate our approach via annotation. We will have a set of annotation guidelines for what determines a “good” summary. Then we can have humans write some summaries and mix this into a pool of machine generated summaries. Then a different set of humans will annotate (score) the summaries without knowing which ones are human/machine written. If the machine summaries are comparable to the human summaries score-wise, then we’ve both evaluated and demonstrated the effectiveness of our approach.

## User Guide
Clone the repo
```bash
git clone https://github.com/jamyooes/redditSummarizerBackend.git
```

Change directory 
```bash
cd redditSummarizerBackend
```

Install virtualenv (If not installed)
```bash
pip install virtualenv
```

Create virtual environment
```bash
python -m venv /env
```

Activate virtual Environment
Reference this [link](https://docs.python.org/3/library/venv.html#how-venvs-work) to activate virtual environment. Dependent on your current shell.

Install all the package dependencies for this repo
```bash
pip install -r requirements.txt
```

Run the backend code
```bash
python api.py
```

Ensure that the extension has been set up following instructions from this repo
https://github.com/jamyooes/redditsummarizer/tree/main

## High Level Logic
Assumptions:
User has set up the extension and activated the backend code 

The user will be on a reddit page comment thread and click on summarize thread.

![image](https://github.com/user-attachments/assets/1556dabf-5ec4-497a-a744-1d931ea5bbbd)

If the page is not a reddit page comment thread it will return the following error

![image](https://github.com/user-attachments/assets/82ae4ae3-971a-480b-9ca4-88c92bd616a3)

If the backend code is not active then it will return the following error

![image](https://github.com/user-attachments/assets/60fff8fe-b052-4579-b2c7-40e3ad773ce5)

With the backend code running (api.py) active, the frontend will send a post request to the API.
api.py will recieve the post request and process the reddit thread by scraping the text, then summarize the text, then compare the text for the best summary and return the best summary back to the extension.
