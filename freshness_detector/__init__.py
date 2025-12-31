"""
Freshness Detector - AI Training Data Quality Tool

Detect stale training data that causes AI hallucinations.
Models information decay over time using exponential decay.

Based on research from Infrastructure Observatory.
"""

from .core import (
    calculate_freshness,
    check_dataset,
    batch_check,
    DecayPolicy,
    age_in_days
)
from .cli import main

__version__ = "0.1.0"
__author__ = "Infrastructure Observatory"
__license__ = "MIT"
__all__ = [
    "calculate_freshness",
    "check_dataset",
    "batch_check",
    "DecayPolicy",
    "age_in_days",
    "main"
]
