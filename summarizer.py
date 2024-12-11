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
    """
    Clean the text from emojis and html tags

    Args:
        raw_data (string) : The raw data to clean out html tags and emojis

    Returns:
        summary  (string) : Returns a string without any html tags or emojis.
    """
    removed_html = re.sub(r"<[^>]*>", "", raw_data)
    remove_emoji = emoji.replace_emoji(removed_html, "")
    return remove_emoji

def summarizer(text):
    """
    Summarize the original text into a shorter form using three different summarizers
    LSA, LexRank and TextRank. Sumy handles the stopwords internally using the utility 
    features. 

    Args:
        text (string) : cleaned text without emojis and html tags

    Returns:
        summary_list  (list of strings) : Returns a list of strings with summaries of the original text
    """
    from sumy.parsers.plaintext import PlaintextParser
    from sumy.nlp.tokenizers import Tokenizer
    from sumy.nlp.stemmers import Stemmer
    from sumy.summarizers.lsa import LsaSummarizer
    from sumy.summarizers.lex_rank import LexRankSummarizer
    from sumy.summarizers.text_rank import TextRankSummarizer
    from sumy.utils import get_stop_words

    # Parse the input
    parser = PlaintextParser.from_string(text, Tokenizer("english"))

    # Summarizers used for this module
    algorithms = {
        "LSA": LsaSummarizer(Stemmer("english")),
        "LexRank": LexRankSummarizer(Stemmer("english")),
        "TextRank": TextRankSummarizer(Stemmer("english"))
    }
    # Output for the summarizer
    summary_list = []
    # Generate summaries
    for name, summarizer in algorithms.items():
        # print(f"Summary using {name}:")
        output = ""
        summarizer.stop_words = get_stop_words("english") # work with stop words
        # LexRank tends to generate shorter summaries, so have it use a larger number of sentences.
        if name == "LexRank":
            num_sentences = 4
        else:
            num_sentences = 1
        summary = summarizer(parser.document, num_sentences) # summarize the comment in 4 sentences
        for sentence in summary:
            # print(sentence)
            output += str(sentence) # Loop through the sentences if present
        # print("-" * 40)
        summary_list.append(output)
    return summary_list

