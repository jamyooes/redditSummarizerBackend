# Module to scrape Reddit and do some basic preprocessing on the scraped comments.
import praw
import re
from bs4 import BeautifulSoup
from markdown import markdown

# client id and client secret are for some burner reddit account I made just for this project so I don't mind leaking these on github.
# we can just create a new account if these get blocked.
reddit = praw.Reddit(
    client_id="Dq0Qip1EfTHzpqrNWHVRlg",
    client_secret="k1hYJU0D6LwbflEiJfy5fd19NG3ADA",
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246",
)

def remove_emojis(text):
    emoj = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642" 
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
                      "]+", re.UNICODE)
    return re.sub(emoj, '', text)

def scrape_reddit(url):
    thread = reddit.submission(url=url)
    thread.comments.sort = "top" # we can change this or maybe we just get everything and choose N random comments?
    thread.comments.replace_more(limit=10)
    concatenated = ""
    for comment in thread.comments:
        concatenated += comment.body + " "
    concatenated = re.sub('\s+', ' ', concatenated)
    html = markdown(concatenated)
    text = ''.join(BeautifulSoup(html, features="lxml").findAll(text=True))
    text = re.sub(r'http\S+', '', text)
    text = remove_emojis(text)
    text = text[:-1]
    return text