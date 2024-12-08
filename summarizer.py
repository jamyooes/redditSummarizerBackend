'''
This module will perform the following:
Clean the output (stop words, html tags, emojis, etc.)
Use sumy to use 2 or more text summarization methods on the text
Output the summaries to the comparison component
'''
import emoji
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
    summary_list = summarizer(cleaned_data)
    # for summary in summary_list:
    #   print("\n" + summary)
    return summary_list


def text_cleaning(raw_data):
    removed_html = re.sub(r"<[^>]*>", "", raw_data)
    remove_emoji = emoji.replace_emoji(removed_html, "")
    return remove_emoji

def summarizer(text):
    from sumy.parsers.plaintext import PlaintextParser
    from sumy.nlp.tokenizers import Tokenizer
    from sumy.nlp.stemmers import Stemmer
    from sumy.summarizers.lsa import LsaSummarizer
    from sumy.summarizers.lex_rank import LexRankSummarizer
    from sumy.summarizers.text_rank import TextRankSummarizer
    from sumy.utils import get_stop_words

    # Parse the input
    parser = PlaintextParser.from_string(text, Tokenizer("english"))

    # Summarizers
    algorithms = {
        "LSA": LsaSummarizer(Stemmer("english")),
        "LexRank": LexRankSummarizer(Stemmer("english")),
        "TextRank": TextRankSummarizer(Stemmer("english"))
    }
    # output for the summarizer
    summary_list = []
    # Generate summaries
    for name, summarizer in algorithms.items():
        print(f"Summary using {name}:")
        output = ""
        summarizer.stop_words = get_stop_words("english")
        summary = summarizer(parser.document, 2)
        for sentence in summary:
            print(sentence)
            output += str(sentence)
        print("-" * 40)
        summary_list.append(output)
    return summary_list

