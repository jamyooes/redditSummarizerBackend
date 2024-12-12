# Reddit Summarizer
This is all the backend logic for the project
Frontend is set up here https://github.com/jamyooes/redditsummarizer/tree/main

##  Project Description (from textdata)
In this project, we’ll build a chrome extension that will summarize threads from Reddit. At a very high level, the extension can be activated when a user is on a Reddit thread. It will then send a request to the backend which will scrape some number of top level comments and concatenate them together to serve as input into our text summarization model which will generate a brief summary of the provided comments. Preprocessing comments will include all standard procedures of text cleaning (removing emojis, html tags, etc.) stemming words, and removing stop words.

We will use a few different text summarization methods potentially including Luhn, Edmunson, and Latent Semantic Analysis. In order to determine the best output among models, the general idea is that the summary most relevant to the original input will be the best summary. We can use measures such as TF-IDF (vectorize summaries, and compare cosine similarities between each summary and the original input), and BM25 (use the original input as a query and rank the summaries as “documents”) among others. If time allows and just for fun we can also call an LLM library (if we can find a free one) and ask it to summarize although I heavily suspect this will always be evaluated as the best summary.

We can evaluate our approach via annotation. We will have a set of annotation guidelines for what determines a “good” summary. Then we can have humans write some summaries and mix this into a pool of machine generated summaries. Then a different set of humans will annotate (score) the summaries without knowing which ones are human/machine written. If the machine summaries are comparable to the human summaries score-wise, then we’ve both evaluated and demonstrated the effectiveness of our approach.

## User Guide

Ensure that the extension has been set up following instructions from this repo
https://github.com/jamyooes/redditsummarizer/tree/main

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
python -m venv env
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

If there is any confusions follow the demo-video guide from the text data submission

## Sample outputs
The front end will be a simple extension

![image](https://github.com/user-attachments/assets/d1474825-473f-416c-9f8f-217948ed582d)

Clicking the button on a non-reddit comment thread will return an error:

![image](https://github.com/user-attachments/assets/71cbf33d-c9cf-4dd6-9fce-69168e6bb70f)

Clicking the button on a reddit comment thread without the api code running will return:

![image](https://github.com/user-attachments/assets/8286e25d-ae44-4e07-bd25-dbc82c228674)

Clicking the button on a reddit comment thread with the api code running will return a summary:

![image](https://github.com/user-attachments/assets/cbabff1a-8d06-4c58-bd68-88c09e27283d)

If there are any issues with the extension after clicking the summarize, please refresh.

## High Level Logic
Assumptions:
The python api.py script is running and the extension has been set up.

The workflow would go as follows:
With the backend code running (api.py) active, the user will be on an URL and follow the cases above from the sample outputs.

If the user clicks on the summarize thread button on a reddit comment thread, then the frontend will send a post request to the backend with the current URL as the payload.

api.py will recieve the post request and process the URL: 

### 1.Scraping the text
Use the PRAW packaged, which is a python reddit API, for scrapping the user's comments given the URL from the frontend.
We set up the text for the summarizer with the top submissions to not overload the API limits.
The comments are processed by removing emojis and then sent to the summarizer module. 

### 2.Summarize the text
The summarizer will clean the text from the scarping module for html tags, emojis, and stopwords.
The summarizer will use 3 algorithms using the sumy package (LSA, Lex rank, Text rank)
The LSA and Text rank will return 1 sentence, while the Lex rank will return 4 sentences, as the lex rank generally returns shorter summaries.
The summarizer will output a summary for each algorithm and save it in a list.

### 3.Compare the text for the best summary
The comparison module will use TFIDF weighting and BM25 scoring normallized in order to compare the original text with all the summaries.
The summary with the highest score will have the best summary. 
The best summary will be sent as output to the payload for the frontend

### 4.Return as a payload to the fronend the best summary back to the extension.
The returned summary will be displayed in the extension.
As shown in the sample outputs.

# Evaluation

In order to evaluate the effectiveness of our project, we generated summaries for 10 Reddit threads and also manually wrote out 10 summaries and had two separate reviewers review each anonymized summary and score each one from a scale of 1-3 with 1 being the worst and 3 being the best (link to the scoring spreadsheet here: https://docs.google.com/spreadsheets/d/1Ko7uKOdAt4U9tnt5U7KboJmcR_ifIcA3Zs4FG18ii_4/edit?usp=sharing). On average, the machine generated summaries scored a 2.3 and human written summaries scored a 2.45 which are quite comparable scores. Even though human generated summaries scored higher, the amount of time saved by having a machine generate the summaries still makes this tool a potentially valuable asset.
