"""Advanced evaluation metrics beyond BLEU."""
import numpy as np
from typing import List, Dict
from collections import Counter
import math


def meteor_score(reference: List[str], hypothesis: List[str]) -> float:
    """
    Calculate METEOR score (simplified version).
    
    Args:
        reference: Reference caption words
        hypothesis: Generated caption words
        
    Returns:
        METEOR score
    """
    # Exact matches
    matches = sum(1 for word in hypothesis if word in reference)
    
    if matches == 0:
        return 0.0
    
    precision = matches / len(hypothesis) if hypothesis else 0
    recall = matches / len(reference) if reference else 0
    
    # Harmonic mean
    if precision + recall == 0:
        return 0.0
    
    f_mean = (10 * precision * recall) / (recall + 9 * precision)
    
    # Penalty for word order differences
    chunks = 1
    penalty = 0.5 * (chunks / matches) ** 3
    
    return f_mean * (1 - penalty)


def cider_score(references: List[List[str]], hypothesis: List[str]) -> float:
    """
    Calculate CIDEr score (simplified version).
    
    Args:
        references: List of reference captions
        hypothesis: Generated caption
        
    Returns:
        CIDEr score
    """
    def get_ngrams(words: List[str], n: int) -> Counter:
        """Get n-grams from words."""
        return Counter([tuple(words[i:i+n]) for i in range(len(words)-n+1)])
    
    # Calculate for n=1 to 4
    scores = []
    
    for n in range(1, 5):
        hyp_ngrams = get_ngrams(hypothesis, n)
        
        if not hyp_ngrams:
            continue
        
        # Average over references
        ref_scores = []
        for ref in references:
            ref_ngrams = get_ngrams(ref, n)
            
            # Calculate cosine similarity
            common = sum((hyp_ngrams & ref_ngrams).values())
            hyp_norm = math.sqrt(sum(v**2 for v in hyp_ngrams.values()))
            ref_norm = math.sqrt(sum(v**2 for v in ref_ngrams.values()))
            
            if hyp_norm * ref_norm > 0:
                ref_scores.append(common / (hyp_norm * ref_norm))
        
        if ref_scores:
            scores.append(np.mean(ref_scores))
    
    return np.mean(scores) if scores else 0.0


def rouge_l_score(reference: List[str], hypothesis: List[str]) -> float:
    """
    Calculate ROUGE-L score (Longest Common Subsequence).
    
    Args:
        reference: Reference caption words
        hypothesis: Generated caption words
        
    Returns:
        ROUGE-L F1 score
    """
    def lcs_length(x: List[str], y: List[str]) -> int:
        """Calculate longest common subsequence length."""
        m, n = len(x), len(y)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if x[i-1] == y[j-1]:
                    dp[i][j] = dp[i-1][j-1] + 1
                else:
                    dp[i][j] = max(dp[i-1][j], dp[i][j-1])
        
        return dp[m][n]
    
    lcs_len = lcs_length(reference, hypothesis)
    
    if lcs_len == 0:
        return 0.0
    
    precision = lcs_len / len(hypothesis) if hypothesis else 0
    recall = lcs_len / len(reference) if reference else 0
    
    if precision + recall == 0:
        return 0.0
    
    f1 = (2 * precision * recall) / (precision + recall)
    return f1


def diversity_score(captions: List[str]) -> Dict[str, float]:
    """
    Calculate diversity metrics for generated captions.
    
    Args:
        captions: List of generated captions
        
    Returns:
        Dictionary with diversity metrics
    """
    all_words = []
    all_bigrams = []
    
    for caption in captions:
        words = caption.split()
        all_words.extend(words)
        
        # Bigrams
        bigrams = [f"{words[i]}_{words[i+1]}" for i in range(len(words)-1)]
        all_bigrams.extend(bigrams)
    
    # Calculate diversity
    unique_words = len(set(all_words))
    total_words = len(all_words)
    
    unique_bigrams = len(set(all_bigrams))
    total_bigrams = len(all_bigrams)
    
    return {
        "unique_words": unique_words,
        "total_words": total_words,
        "word_diversity": unique_words / total_words if total_words > 0 else 0,
        "unique_bigrams": unique_bigrams,
        "total_bigrams": total_bigrams,
        "bigram_diversity": unique_bigrams / total_bigrams if total_bigrams > 0 else 0
    }


def semantic_similarity(reference: List[str], hypothesis: List[str]) -> float:
    """
    Calculate semantic similarity using word overlap.
    
    Args:
        reference: Reference caption words
        hypothesis: Generated caption words
        
    Returns:
        Jaccard similarity score
    """
    ref_set = set(reference)
    hyp_set = set(hypothesis)
    
    intersection = len(ref_set & hyp_set)
    union = len(ref_set | hyp_set)
    
    return intersection / union if union > 0 else 0.0


class AdvancedEvaluator:
    """Advanced evaluation metrics calculator."""
    
    def __init__(self):
        """Initialize evaluator."""
        self.metrics = {}
    
    def evaluate(
        self,
        references: List[List[List[str]]],
        hypotheses: List[List[str]]
    ) -> Dict[str, float]:
        """
        Evaluate captions with multiple metrics.
        
        Args:
            references: List of reference captions for each image
            hypotheses: List of generated captions
            
        Returns:
            Dictionary of metric scores
        """
        meteor_scores = []
        cider_scores = []
        rouge_scores = []
        semantic_scores = []
        
        for refs, hyp in zip(references, hypotheses):
            # METEOR (use first reference)
            meteor_scores.append(meteor_score(refs[0], hyp))
            
            # CIDEr (use all references)
            cider_scores.append(cider_score(refs, hyp))
            
            # ROUGE-L (use first reference)
            rouge_scores.append(rouge_l_score(refs[0], hyp))
            
            # Semantic similarity (use first reference)
            semantic_scores.append(semantic_similarity(refs[0], hyp))
        
        # Calculate diversity
        caption_strings = [' '.join(hyp) for hyp in hypotheses]
        diversity = diversity_score(caption_strings)
        
        return {
            "meteor": np.mean(meteor_scores),
            "cider": np.mean(cider_scores),
            "rouge_l": np.mean(rouge_scores),
            "semantic_similarity": np.mean(semantic_scores),
            **diversity
        }
