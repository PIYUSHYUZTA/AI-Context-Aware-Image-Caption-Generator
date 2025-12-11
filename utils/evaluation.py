"""Evaluation metrics and utilities."""
from typing import Dict, List, Tuple
from nltk.translate.bleu_score import corpus_bleu, sentence_bleu
from nltk.translate.meteor_score import meteor_score
from rouge_score import rouge_scorer
import numpy as np
from utils.logger import logger


def calculate_bleu_scores(
    references: List[List[List[str]]],
    hypotheses: List[List[str]]
) -> Dict[str, float]:
    """Calculate BLEU scores.
    
    Args:
        references: List of reference captions (multiple per image)
        hypotheses: List of generated captions
        
    Returns:
        Dictionary of BLEU scores
    """
    try:
        bleu1 = corpus_bleu(references, hypotheses, weights=(1.0, 0, 0, 0))
        bleu2 = corpus_bleu(references, hypotheses, weights=(0.5, 0.5, 0, 0))
        bleu3 = corpus_bleu(references, hypotheses, weights=(0.33, 0.33, 0.33, 0))
        bleu4 = corpus_bleu(references, hypotheses, weights=(0.25, 0.25, 0.25, 0.25))
        
        return {
            'BLEU-1': bleu1,
            'BLEU-2': bleu2,
            'BLEU-3': bleu3,
            'BLEU-4': bleu4
        }
    except Exception as e:
        logger.error(f"Error calculating BLEU scores: {e}")
        return {}


def calculate_meteor_score(
    references: List[str],
    hypothesis: str
) -> float:
    """Calculate METEOR score for single prediction.
    
    Args:
        references: List of reference captions
        hypothesis: Generated caption
        
    Returns:
        METEOR score
    """
    try:
        # METEOR expects tokenized strings
        return meteor_score(references, hypothesis)
    except Exception as e:
        logger.error(f"Error calculating METEOR score: {e}")
        return 0.0


def calculate_rouge_scores(
    reference: str,
    hypothesis: str
) -> Dict[str, float]:
    """Calculate ROUGE scores.
    
    Args:
        reference: Reference caption
        hypothesis: Generated caption
        
    Returns:
        Dictionary of ROUGE scores
    """
    try:
        scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
        scores = scorer.score(reference, hypothesis)
        
        return {
            'ROUGE-1': scores['rouge1'].fmeasure,
            'ROUGE-2': scores['rouge2'].fmeasure,
            'ROUGE-L': scores['rougeL'].fmeasure
        }
    except Exception as e:
        logger.error(f"Error calculating ROUGE scores: {e}")
        return {}


class EvaluationMetrics:
    """Comprehensive evaluation metrics calculator."""
    
    def __init__(self):
        """Initialize metrics calculator."""
        self.reset()
    
    def reset(self):
        """Reset all metrics."""
        self.references = []
        self.hypotheses = []
    
    def add_prediction(
        self,
        reference_captions: List[str],
        generated_caption: str
    ):
        """Add a prediction for evaluation.
        
        Args:
            reference_captions: List of reference captions
            generated_caption: Generated caption
        """
        # Tokenize
        refs = [ref.split() for ref in reference_captions]
        hyp = generated_caption.split()
        
        self.references.append(refs)
        self.hypotheses.append(hyp)
    
    def compute_metrics(self) -> Dict[str, float]:
        """Compute all evaluation metrics.
        
        Returns:
            Dictionary of metric scores
        """
        if not self.references or not self.hypotheses:
            logger.warning("No predictions to evaluate")
            return {}
        
        metrics = {}
        
        # BLEU scores
        bleu_scores = calculate_bleu_scores(self.references, self.hypotheses)
        metrics.update(bleu_scores)
        
        logger.info(f"Computed metrics for {len(self.references)} predictions")
        return metrics
    
    def print_metrics(self):
        """Print computed metrics."""
        metrics = self.compute_metrics()
        
        print("\n" + "="*50)
        print("EVALUATION METRICS")
        print("="*50)
        
        for metric, score in metrics.items():
            print(f"{metric:15s}: {score:.4f}")
        
        print("="*50 + "\n")
