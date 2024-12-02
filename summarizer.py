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



raw_data = """
<div id="t3_1gu82vv-post-rtjson-content" class="md text-14" style="--emote-size: 20px">
    <p>
    Every now and then I check my little trading app and have a look at the stocks. And sometimes, a certain exercise stock on the trending tab would catch my eye. A black logo with a simple white circle design. I know that business, it's that exercise bike company Pelaton. Quickly scanning the name I see letters that confirm my assumption.
  </p><p>
    "Holy shit, this stock is going mental, I didn't realise Peloton made so much money" I think to myself. This happens occasionally throughout the year and Peloton is apparently a 100 billion dollar company. 🚀🚀🚀
  </p><p>
    Anyway, last week I took an extra second to actually fucking read. What the fuck is Palantir.
  </p>
  </div>
"""

raw_data_2 = """
<span class="hgKElc">Face with Tears of Joy (😂) is an emoji depicting <b>a face crying with laughter</b>.</span>"""

raw_data_3 = """
<p>
    The wind though! The wind! I love Riverside, it’s my favorite park, and I continue to be tricked every damn day with the idea that “when I loop back the wind will be on my back.” 😆
  </p>
"""

raw_data_4 = """
<p>
    I was surprised how quiet park was last night exactly around when you are talking about.    It was only my second run back since NYC and I have many friends who still haven't run.   It'll pickup a bit next couple weeks but from now until Boston etc training kicks off, it's def a lull.    I enjoy it (but I'm also a large man so I totally get that it's different).
  </p>
"""

raw_data_5 = """
<div id="-post-rtjson-content" class="py-0 xs:mx-xs mx-2xs inline-block max-w-full" style="--emote-size: 20px">
    <p>
    I haven't run since the marathon. I'm planning to do a few miles this weekend...
  </p><p>
    There are something like 15K New Yorkers who ran the marathon. Nearly all of them will be doing training programs, those programs prescribe ~35-50+ miles of running per week, including a weekend "long run".
  </p><p>
    The marathon was on November 3. All those people who were always training for the last 4 months are taking a couple weeks of necessary, well-deserved recovery.
  </p>
  </div>
"""

raw_data_6 = """
<div id="-post-rtjson-content" class="py-0 xs:mx-xs mx-2xs inline-block max-w-full" style="--emote-size: 20px">
    <p>
    Yes that's the end of that you will not see that many runners outside most of them was marathon training and a lot of them don't like cold weather running outside isn't for everyone 😉
  </p>
  </div>
"""

summarizer_pipeline(raw_data_3)