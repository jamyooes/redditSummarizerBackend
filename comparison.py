from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from rank_bm25 import BM25Okapi
import numpy as np


def compare_summaries(original_text, summaries):
    """
    Compares a list of summaries against the original text using TF-IDF and normalized BM25. It then combines these
    scores to identify the best summary.

    Args:
        original_text (str): The original text.
        summaries (list): A list of generated summaries to be compared.

    Returns:
        dict: A dictionary containing TF-IDF cosine similarities, BM25 score, and average scores from TF-IDF and BM25.
    """
    if not original_text or not summaries:
        raise ValueError("Original text and summaries cannot be empty.")

    tfidf_similarities = compute_tfidf(original_text, summaries)
    bm25_scores = compute_bm25(original_text, summaries)

    bm25_scores_normalized = [score / max(bm25_scores) for score in bm25_scores]

    combined_scores = (
        tfidf_similarities + bm25_scores_normalized
    ) / 2  # assuming equal weight

    highest_score_index = np.argmax(combined_scores)
    best_summary = summaries[highest_score_index]
    print(f"The most relevant summary is:\n{best_summary}")

    scores = {
        "tfidf_similarities": np.array(tfidf_similarities),
        "bm25_scores": np.array(bm25_scores),
        "combined_score": np.array(combined_scores),
    }
    print(scores)
    return best_summary


def compute_tfidf(original_text, summaries):
    """
    Computes TF-IDF cosine similarities between the original text and each summary.

    Args:
        original_text (str): The original text.
        summaries (list): A list of generated summaries to be compared.

    Returns:
        numpy.ndarray: Cosine similarity scores for each summary.
    """
    vectorizer = TfidfVectorizer()
    all_texts = [original_text] + summaries
    tfidf_matrix = vectorizer.fit_transform(all_texts)
    similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])
    return similarities[0]


def compute_bm25(original_text, summaries):
    """
    Computes BM25 scores between the original text and each summary.

    Args:
        original_text (str): The original text.
        summaries (list): A list of generated summaries to be compared.

    Returns:
        numpy.ndarray: BM25 scores for each summary.
    """
    tokenized_summaries = [summary.split() for summary in summaries]
    bm25 = BM25Okapi(tokenized_summaries)
    tokenized_original = original_text.split()
    bm25_scores = bm25.get_scores(tokenized_original)
    return bm25_scores
