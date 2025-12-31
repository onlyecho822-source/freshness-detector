# Freshness Detector 🧪

**Detect stale AI training data before it causes hallucinations.**

[![PyPI version](https://badge.fury.io/py/freshness-detector.svg)](https://badge.fury.io/py/freshness-detector)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## The Problem

**91% of ML models degrade over time** ([MIT/Harvard Study, 2023](https://www.nannyml.com/blog/91-of-ml-perfomance-degrade-in-time)).

One major cause: **stale training data**. Information that was accurate when captured becomes outdated, but models trained on it don't know this.

**Examples:**
- Medical AI trained on 2022 COVID guidelines (outdated)
- Code completion trained on Python 3.8 examples (old syntax)
- News summarization trained on 2023 events (stale context)
- Financial models trained on pre-2024 market data (irrelevant)

**Current solutions:**
- ❌ Retrain on fixed schedules (wasteful or too slow)
- ❌ Wait for performance degradation (reactive)
- ❌ Manual data audits (doesn't scale)

---

## The Solution

**Freshness Detector** uses **temporal decay modeling** to calculate how "fresh" your training data is right now.

**Key features:**
- 🧮 **Mathematical decay model** - Exponential confidence degradation over time
- 📊 **Multiple decay policies** - Different rates for news, science, code, medical data, etc.
- 🔍 **Dataset analysis** - Scan entire datasets for stale entries
- 🐍 **Python API + CLI** - Use in notebooks or CI/CD pipelines
- ⚡ **Lightweight** - No dependencies beyond Python stdlib + dateutil

---

## Installation

```bash
pip install freshness-detector
```

---

## Quick Start

### CLI Usage

**Calculate freshness of a single data point:**

```bash
freshness calculate --confidence 0.9 --timestamp "2024-01-01" --topic ai_training
```

Output:
```
🧪 Freshness Analysis
==================================================
Initial confidence: 90.0%
Capture timestamp:  2024-01-01
Age:                365.0 days
Topic type:         ai_training
Decay policy:       AI training data
Decay rate (λ):     0.0200 per day
Floor:              15.0%
==================================================
Current confidence: 15.0%
⚠️  WARNING: Data is STALE (< 30% confidence)
```

**Check an entire dataset:**

```bash
freshness check training_data.json --threshold 0.4 --verbose
```

**List all decay policies:**

```bash
freshness policies
```

---

### Python API

**Basic usage:**

```python
from freshness_detector import calculate_freshness

# Check if data is still fresh
confidence = calculate_freshness(
    initial_confidence=0.95,
    capture_timestamp="2024-06-01",
    topic_type="ai_training"
)

print(f"Current confidence: {confidence:.1%}")
# Output: Current confidence: 45.2%

if confidence < 0.5:
    print("⚠️  Time to retrain!")
```

**Analyze a dataset:**

```python
from freshness_detector import check_dataset

results = check_dataset(
    "training_data.json",
    topic_type="ai_training",
    threshold=0.3
)

print(results["summary"])
print(f"Stale entries: {results['stale_entries']}")
print(f"Average confidence: {results['average_confidence']:.1%}")
```

**Batch processing (in-memory):**

```python
from freshness_detector import batch_check

data = [
    {"text": "Example 1", "timestamp": "2025-01-01", "confidence": 0.9},
    {"text": "Example 2", "timestamp": "2023-01-01", "confidence": 0.85},
]

results = batch_check(data, threshold=0.5)
print(f"Stale entries: {results['stale_entries']}")
print(f"Stale indices: {results['stale_indices']}")
```

**Custom decay parameters:**

```python
from freshness_detector import calculate_freshness

# Use custom decay rate and floor
confidence = calculate_freshness(
    initial_confidence=0.9,
    capture_timestamp="2024-01-01",
    topic_type="ai_training",
    custom_lambda=0.03,  # Faster decay
    custom_floor=0.1     # Lower minimum
)
```

---

## Decay Policies

Different types of information decay at different rates:

| Topic Type | Decay Rate (λ) | Floor | Half-life | Description |
|------------|---------------|-------|-----------|-------------|
| `news` | 0.10 | 5% | ~7 days | News and current events |
| `social_media` | 0.15 | 2% | ~5 days | Social media trends |
| `financial` | 0.08 | 10% | ~9 days | Market data |
| `ai_training` | 0.02 | 15% | ~35 days | AI/ML best practices |
| `medical` | 0.015 | 25% | ~46 days | Medical guidelines |
| `code` | 0.005 | 20% | ~139 days | Code examples/APIs |
| `science` | 0.002 | 30% | ~347 days | Scientific facts |
| `legal` | 0.001 | 40% | ~693 days | Legal precedents |
| `history` | 0.0 | 100% | ∞ | Historical facts |

**Formula:** `C(t) = max(floor, C₀ × e^(-λ × t))`

Where:
- `C(t)` = Current confidence
- `C₀` = Initial confidence
- `λ` = Decay rate (lambda_per_day)
- `t` = Time in days
- `floor` = Minimum confidence threshold

---

## Use Cases

### 1. **ML Pipeline Integration**

```python
from freshness_detector import batch_check

# Before training
results = batch_check(training_data, threshold=0.5)

if results['stale_entries'] > len(training_data) * 0.1:
    print("⚠️  More than 10% of data is stale!")
    # Trigger data refresh pipeline
```

### 2. **CI/CD Data Quality Checks**

```bash
# In your CI pipeline
freshness check data/training_set.json --threshold 0.4
# Exit code 1 if stale entries found
```

### 3. **Model Retraining Scheduler**

```python
from freshness_detector import calculate_freshness
from datetime import datetime

last_training_date = "2024-06-01"
current_conf = calculate_freshness(1.0, last_training_date, "ai_training")

if current_conf < 0.6:
    trigger_retraining()
```

### 4. **Dataset Documentation**

```python
# Generate freshness report for dataset README
results = check_dataset("dataset.json")
print(results["summary"])
# Add to dataset card / model card
```

---

## Dataset Format

**JSON format:**

```json
[
  {
    "text": "Training example 1",
    "timestamp": "2025-01-01",
    "confidence": 0.95
  },
  {
    "text": "Training example 2",
    "timestamp": "2024-06-01",
    "confidence": 0.90
  }
]
```

**JSONL format:**

```jsonl
{"text": "Example 1", "timestamp": "2025-01-01", "confidence": 0.95}
{"text": "Example 2", "timestamp": "2024-06-01", "confidence": 0.90}
```

**Supported timestamp fields:**
- `timestamp`
- `created_at`
- `date`
- `captured_at`
- `updated_at`

**Confidence field (optional):**
- `confidence` (defaults to 1.0 if not present)

---

## Research Background

This tool is based on research from [Infrastructure Observatory](https://github.com/onlyecho822-source/infrastructure-observatory) on temporal integrity in AI systems.

**Key insight:** Information has a "half-life" - the time it takes for confidence to drop to 50%. By modeling this decay mathematically, we can predict when training data becomes unreliable.

**Academic foundation:**
- Exponential decay models (physics, chemistry)
- Information theory (Shannon entropy)
- Temporal data quality (data engineering)

**Related work:**
- [MIT/Harvard Study: 91% of ML models degrade over time](https://www.nannyml.com/blog/91-of-ml-perfomance-degrade-in-time)
- [Training on Yesterday's Truth: The Hidden Cost of Stale Data](https://www.linkedin.com/pulse/training-yesterdays-truth-hidden-cost-stale-data-andre-rjyce)
- [Data Freshness in Data Observability](https://www.siffletdata.com/blog/data-freshness)

---

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

**Development setup:**

```bash
git clone https://github.com/onlyecho822-source/freshness-detector.git
cd freshness-detector
pip install -e ".[dev]"
pytest
```

---

## License

MIT License - see [LICENSE](LICENSE) file for details.

---

## Citation

If you use Freshness Detector in academic work, please cite:

```bibtex
@software{freshness_detector_2025,
  author = {Infrastructure Observatory},
  title = {Freshness Detector: Temporal Decay Modeling for AI Training Data},
  year = {2025},
  url = {https://github.com/onlyecho822-source/freshness-detector}
}
```

---

## Support

- 🐛 **Bug reports:** [GitHub Issues](https://github.com/onlyecho822-source/freshness-detector/issues)
- 💬 **Discussions:** [GitHub Discussions](https://github.com/onlyecho822-source/freshness-detector/discussions)
- 📧 **Email:** research@infrastructure-observatory.org

---

## Roadmap

**v0.2.0 (Q1 2026):**
- [ ] Pandas DataFrame support
- [ ] Visualization tools (decay curves)
- [ ] Custom policy builder
- [ ] Integration with popular ML frameworks (HuggingFace, PyTorch)

**v0.3.0 (Q2 2026):**
- [ ] Automated retraining recommendations
- [ ] Cost-benefit analysis (retrain vs. accept degradation)
- [ ] Multi-source data freshness aggregation

**Future:**
- [ ] Real-time monitoring dashboard
- [ ] Cloud service integration (S3, GCS, Azure)
- [ ] LLM-specific decay models

---

## Acknowledgments

Built with insights from:
- Echo Universe temporal integrity research
- Data quality engineering best practices
- ML operations (MLOps) community feedback

**Special thanks to:**
- MIT/Harvard research team for model degradation study
- Data observability community for freshness metrics
- Early adopters and contributors

---

**Made with ❤️ by [Infrastructure Observatory](https://github.com/onlyecho822-source/infrastructure-observatory)**

*Keeping AI models honest, one timestamp at a time.*
