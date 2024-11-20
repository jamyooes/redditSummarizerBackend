'''
This module will perform the following:
Clean the output (stop words, html tags, emojis, etc.)
Use sumy to use 2 or more text summarization methods on the text
Output the summaries to the comparison component
'''
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re

def summarizer_pipeline(raw_data):
    """
    Main Pipeline for the summarizer
    
    Args:
        raw_data (string) : The raw data for the text to summarize from the parser
    
    Returns:
        summary  (string) : Returns a summary for the text.
    """
    cleaned_data = text_cleaning(raw_data)
    summary = summarizer(cleaned_data)
    pass


def text_cleaning(raw_data):
    removed_html = re.sub(r"<[^>]*>", "", raw_data)
    # nltk.download('stopwords')
    # nltk.download('punkt_tab')
    # stop_words = set(stopwords.words('english'))
    # word_tokens = word_tokenize(removed_html)
    # filtered_sentence = [w.lower() for w in word_tokens if not w.lower() in stop_words]
    # filtered_sentence = ", ".join(filtered_sentence)
    # print(filtered_sentence)
    return removed_html

def summarizer(text):
    from sumy.parsers.plaintext import PlaintextParser
    from sumy.nlp.tokenizers import Tokenizer
    from sumy.nlp.stemmers import Stemmer
    from sumy.summarizers.lsa import LsaSummarizer
    from sumy.summarizers.lex_rank import LexRankSummarizer
    from sumy.summarizers.text_rank import TextRankSummarizer

    # Parse the input
    parser = PlaintextParser.from_string(text, Tokenizer("english"))

    # Summarizers
    algorithms = {
        "LSA": LsaSummarizer(),
        "LexRank": LexRankSummarizer(),
        "TextRank": TextRankSummarizer()
    }

    # Generate summaries
    for name, summarizer in algorithms.items():
        print(f"Summary using {name}:")
        summary = summarizer(parser.document, 2)
        for sentence in summary:
            print(sentence)
        print("-" * 40)



raw_data = """
<div id="t3_1gu82vv-post-rtjson-content" class="md text-14" style="--emote-size: 20px">
    <p>
    Every now and then I check my little trading app and have a look at the stocks. And sometimes, a certain exercise stock on the trending tab would catch my eye. A black logo with a simple white circle design. I know that business, it's that exercise bike company Pelaton. Quickly scanning the name I see letters that confirm my assumption.
  </p><p>
    "Holy shit, this stock is going mental, I didn't realise Peloton made so much money" I think to myself. This happens occasionally throughout the year and Peloton is apparently a 100 billion dollar company.
  </p><p>
    Anyway, last week I took an extra second to actually fucking read. What the fuck is Palantir.
  </p>
  </div>
"""

summarizer_pipeline(raw_data)