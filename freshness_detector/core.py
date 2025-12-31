"""
Freshness Detector - Core Module
Temporal decay modeling for AI training data freshness

Based on research from Infrastructure Observatory
"""
import math
from datetime import datetime, timezone
from dataclasses import dataclass
from typing import Dict, List, Optional, Union
import json


@dataclass
class DecayPolicy:
    """
    Decay policy defining how information degrades over time
    
    Attributes:
        lambda_per_day: Decay rate (higher = faster decay)
        floor: Minimum confidence threshold
        name: Human-readable policy name
        description: Policy explanation
    """
    lambda_per_day: float
    floor: float
    name: str
    description: str = ""
    
    @classmethod
    def get_policy(cls, topic_type: str) -> 'DecayPolicy':
        """
        Get predefined decay policy for content type
        
        Args:
            topic_type: Type of content (news, science, code, etc.)
            
        Returns:
            DecayPolicy instance
            
        Examples:
            >>> policy = DecayPolicy.get_policy("news")
            >>> policy.lambda_per_day
            0.1
        """
        policies = {
            "news": cls(
                lambda_per_day=0.10,
                floor=0.05,
                name="Fast decay (news)",
                description="News and current events become stale quickly"
            ),
            "science": cls(
                lambda_per_day=0.002,
                floor=0.30,
                name="Slow decay (science)",
                description="Scientific facts change slowly"
            ),
            "code": cls(
                lambda_per_day=0.005,
                floor=0.20,
                name="Medium decay (code)",
                description="Code examples and APIs evolve moderately"
            ),
            "legal": cls(
                lambda_per_day=0.001,
                floor=0.40,
                name="Very slow decay (legal)",
                description="Legal precedents are highly stable"
            ),
            "history": cls(
                lambda_per_day=0.0,
                floor=1.00,
                name="No decay (history)",
                description="Historical facts don't change"
            ),
            "medical": cls(
                lambda_per_day=0.015,
                floor=0.25,
                name="Medical guidelines",
                description="Medical knowledge updates regularly"
            ),
            "ai_training": cls(
                lambda_per_day=0.02,
                floor=0.15,
                name="AI training data",
                description="AI/ML best practices evolve rapidly"
            ),
            "social_media": cls(
                lambda_per_day=0.15,
                floor=0.02,
                name="Social media content",
                description="Social media trends change extremely fast"
            ),
            "financial": cls(
                lambda_per_day=0.08,
                floor=0.10,
                name="Financial data",
                description="Market data and financial info changes quickly"
            ),
        }
        return policies.get(topic_type.lower(), cls(
            lambda_per_day=0.01,
            floor=0.20,
            name="Default decay",
            description="General purpose decay rate"
        ))
    
    @classmethod
    def list_policies(cls) -> List[str]:
        """List all available policy types"""
        return [
            "news", "science", "code", "legal", "history",
            "medical", "ai_training", "social_media", "financial"
        ]


def age_in_days(timestamp: Union[str, datetime]) -> float:
    """
    Calculate age in days from timestamp to now
    
    Args:
        timestamp: ISO format string or datetime object
        
    Returns:
        Age in days (float)
        
    Examples:
        >>> from datetime import datetime, timedelta
        >>> ts = datetime.now() - timedelta(days=30)
        >>> age = age_in_days(ts)
        >>> 29.9 < age < 30.1
        True
    """
    if isinstance(timestamp, str):
        # Handle various ISO formats
        timestamp = timestamp.replace('Z', '+00:00')
        timestamp = datetime.fromisoformat(timestamp)
    
    if timestamp.tzinfo is None:
        timestamp = timestamp.replace(tzinfo=timezone.utc)
    
    now = datetime.now(timezone.utc)
    delta = now - timestamp
    return max(0.0, delta.total_seconds() / 86400.0)


def calculate_freshness(
    initial_confidence: float,
    capture_timestamp: Union[str, datetime],
    topic_type: str = "ai_training",
    custom_lambda: Optional[float] = None,
    custom_floor: Optional[float] = None
) -> float:
    """
    Calculate current freshness (confidence) of information using exponential decay
    
    Formula: C(t) = max(floor, C₀ × e^(-λ × t))
    
    Where:
    - C(t) = Current confidence
    - C₀ = Initial confidence
    - λ = Decay rate (lambda_per_day)
    - t = Time in days
    - floor = Minimum confidence threshold
    
    Args:
        initial_confidence: Initial confidence score (0.0-1.0)
        capture_timestamp: When information was captured
        topic_type: Type of content (affects decay rate)
        custom_lambda: Override decay rate (optional)
        custom_floor: Override minimum confidence (optional)
        
    Returns:
        Current confidence score (0.0-1.0)
        
    Examples:
        >>> calculate_freshness(0.9, "2025-01-01", "news")
        # Returns lower confidence for old news
        
        >>> calculate_freshness(0.9, "2025-01-01", "history")
        0.9  # History doesn't decay
    """
    # Input validation
    if not 0.0 <= initial_confidence <= 1.0:
        raise ValueError(f"initial_confidence must be between 0 and 1, got {initial_confidence}")
    
    # Get policy or use custom parameters
    if custom_lambda is not None and custom_floor is not None:
        lambda_val = custom_lambda
        floor = custom_floor
    else:
        policy = DecayPolicy.get_policy(topic_type)
        lambda_val = policy.lambda_per_day
        floor = policy.floor
    
    # Calculate age
    days = age_in_days(capture_timestamp)
    
    # Apply exponential decay
    decayed = initial_confidence * math.exp(-lambda_val * days)
    
    # Apply floor and ceiling
    return max(floor, min(1.0, decayed))


def check_dataset(
    dataset_path: str,
    topic_type: str = "ai_training",
    threshold: float = 0.3,
    timestamp_fields: Optional[List[str]] = None,
    confidence_field: str = "confidence"
) -> Dict:
    """
    Analyze a dataset for stale entries
    
    Args:
        dataset_path: Path to JSON or JSONL file
        topic_type: Content type for decay calculation
        threshold: Minimum acceptable confidence
        timestamp_fields: List of field names to check for timestamps
        confidence_field: Field name containing initial confidence
        
    Returns:
        Dictionary with analysis results
        
    Example:
        >>> results = check_dataset("training_data.json", threshold=0.4)
        >>> print(results['summary'])
        Dataset: 1000 entries
        Stale entries: 234 (23.4%)
        Average confidence: 0.67
    """
    if timestamp_fields is None:
        timestamp_fields = ["timestamp", "created_at", "date", "captured_at", "updated_at"]
    
    try:
        with open(dataset_path, 'r', encoding='utf-8') as f:
            # Try to load as JSON array
            try:
                data = json.load(f)
                if not isinstance(data, list):
                    data = [data]
            except json.JSONDecodeError:
                # Try JSONL format
                f.seek(0)
                data = [json.loads(line) for line in f if line.strip()]
        
        results = {
            "total_entries": 0,
            "stale_entries": 0,
            "fresh_entries": 0,
            "no_timestamp": 0,
            "average_confidence": 0.0,
            "min_confidence": 1.0,
            "max_confidence": 0.0,
            "alerts": [],
            "summary": "",
            "policy": DecayPolicy.get_policy(topic_type).name
        }
        
        confidences = []
        
        for i, entry in enumerate(data):
            results["total_entries"] += 1
            
            # Find timestamp field
            timestamp = None
            for field in timestamp_fields:
                if field in entry:
                    timestamp = entry[field]
                    break
            
            if not timestamp:
                results["no_timestamp"] += 1
                continue
            
            # Get initial confidence (default to 1.0)
            initial_conf = entry.get(confidence_field, 1.0)
            
            # Calculate current confidence
            try:
                current_conf = calculate_freshness(initial_conf, timestamp, topic_type)
                confidences.append(current_conf)
                
                # Update min/max
                results["min_confidence"] = min(results["min_confidence"], current_conf)
                results["max_confidence"] = max(results["max_confidence"], current_conf)
                
                # Check if stale
                if current_conf < threshold:
                    results["stale_entries"] += 1
                    age = age_in_days(timestamp)
                    results["alerts"].append({
                        "index": i,
                        "timestamp": str(timestamp),
                        "age_days": round(age, 1),
                        "confidence": round(current_conf, 3),
                        "reason": f"Confidence {current_conf:.1%} below threshold {threshold:.0%}"
                    })
                else:
                    results["fresh_entries"] += 1
                    
            except Exception as e:
                # Skip entries with invalid timestamps
                results["no_timestamp"] += 1
                continue
        
        # Calculate average
        if confidences:
            results["average_confidence"] = sum(confidences) / len(confidences)
        
        # Generate summary
        total = results["total_entries"]
        stale = results["stale_entries"]
        fresh = results["fresh_entries"]
        no_ts = results["no_timestamp"]
        
        results["summary"] = (
            f"Dataset Analysis Results\n"
            f"{'='*50}\n"
            f"Total entries: {total}\n"
            f"Fresh entries: {fresh} ({fresh/max(1,total):.1%})\n"
            f"Stale entries: {stale} ({stale/max(1,total):.1%})\n"
            f"No timestamp: {no_ts} ({no_ts/max(1,total):.1%})\n"
            f"Average confidence: {results['average_confidence']:.1%}\n"
            f"Confidence range: {results['min_confidence']:.1%} - {results['max_confidence']:.1%}\n"
            f"Decay policy: {results['policy']}\n"
            f"Threshold: {threshold:.0%}\n"
            f"Alerts: {len(results['alerts'])} entries need review"
        )
        
        return results
        
    except FileNotFoundError:
        return {
            "error": f"File not found: {dataset_path}",
            "summary": f"Error: Could not find file {dataset_path}"
        }
    except Exception as e:
        return {
            "error": str(e),
            "summary": f"Error analyzing dataset: {e}"
        }


def batch_check(
    entries: List[Dict],
    topic_type: str = "ai_training",
    threshold: float = 0.3
) -> Dict:
    """
    Check a list of entries (in-memory) for staleness
    
    Useful for integrating into ML pipelines
    
    Args:
        entries: List of dictionaries with timestamp and optional confidence
        topic_type: Content type
        threshold: Staleness threshold
        
    Returns:
        Analysis results dictionary
        
    Example:
        >>> data = [
        ...     {"text": "Example", "timestamp": "2025-01-01", "confidence": 0.9},
        ...     {"text": "Another", "timestamp": "2024-01-01", "confidence": 0.8}
        ... ]
        >>> results = batch_check(data, threshold=0.5)
        >>> results['stale_entries']
        1
    """
    results = {
        "total_entries": len(entries),
        "stale_entries": 0,
        "fresh_entries": 0,
        "stale_indices": [],
        "confidences": []
    }
    
    for i, entry in enumerate(entries):
        timestamp = entry.get("timestamp") or entry.get("created_at") or entry.get("date")
        if not timestamp:
            continue
            
        initial_conf = entry.get("confidence", 1.0)
        current_conf = calculate_freshness(initial_conf, timestamp, topic_type)
        
        results["confidences"].append(current_conf)
        
        if current_conf < threshold:
            results["stale_entries"] += 1
            results["stale_indices"].append(i)
        else:
            results["fresh_entries"] += 1
    
    return results
