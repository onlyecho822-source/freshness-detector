from setuptools import setup, find_packages
import os

# Read README for long description
readme_path = os.path.join(os.path.dirname(__file__), "README.md")
if os.path.exists(readme_path):
    with open(readme_path, "r", encoding="utf-8") as fh:
        long_description = fh.read()
else:
    long_description = "Freshness Detector - Detect stale AI training data using temporal decay modeling"

setup(
    name="freshness-detector",
    version="0.1.0",
    author="Infrastructure Observatory",
    author_email="research@infrastructure-observatory.org",
    description="Detect stale training data for AI models using temporal decay",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/infrastructure-observatory/freshness-detector",
    project_urls={
        "Bug Reports": "https://github.com/infrastructure-observatory/freshness-detector/issues",
        "Source": "https://github.com/infrastructure-observatory/freshness-detector",
        "Documentation": "https://github.com/infrastructure-observatory/freshness-detector#readme",
    },
    packages=find_packages(exclude=["tests", "tests.*", "examples", "docs"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "python-dateutil>=2.8.2",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "freshness=freshness_detector.cli:main",
        ],
    },
    keywords="ai machine-learning data-quality training-data staleness temporal-decay ml-ops",
    zip_safe=False,
)
