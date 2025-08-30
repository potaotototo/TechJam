# Peanut BERTer

A machine learning solution for assessing the quality and relevancy of location-based reviews.

## Overview

Online platforms host massive volumes of reviews, but many are off-topic, generic, or even spam, making it difficult for businesses and users to extract meaningful insights. **Peanut BERTer** tackles this challenge by evaluating reviews along two key dimensions to surface genuine, valuable feedback.

## Key Features

### 🎯 Dual Assessment Framework

**1. Relevance Scoring**
- Measures whether reviews meaningfully discuss the business
- Uses semantic similarity between review text and business description
- Powered by `sentence-transformers/all-MiniLM-L6-v2`

**2. Spam Detection** 
- Identifies duplicated or inauthentic reviews
- Detects unusually high similarity between reviews posted across different businesses
- Uses the same transformer model for consistency

### 🔍 Quality Filtering Rules

Our solution applies three essential filtering rules:

1. **No Promotions** - Reviews should not contain promotional links
2. **No Irrelevant Content** - Reviews must be about the location, not unrelated topics  
3. **No Rant Without Visits** - Rants/complaints must come from actual visitors (inferred via content/metadata)

### 🌍 Advanced Processing Capabilities

- **Multilingual Support** - Automatic language detection and translation to English for consistent processing
- **Efficient Data Pipeline** - Handles raw gzipped JSONL review files and converts to optimized Parquet storage
- **Comprehensive Metrics** - Built-in evaluation framework for model performance assessment

## Development Environment

### Primary Tools
- **Google Colab** - Collaborative development, GPU acceleration, and Drive integration
- **VSCode & Jupyter** - Local prototyping and debugging

### APIs Used
- **OpenAI GPT-4o** - Experimentation with labeling and refinement
- **Hugging Face MarianMT** - Multilingual translation capabilities

## Technical Stack

### Data Handling
- `pandas`, `numpy` - Core data manipulation
- `pyarrow` - Efficient columnar data storage
- `orjson`, `gzip`, `glob` - File processing utilities

### Machine Learning & NLP
- `PyTorch` - Deep learning framework
- `Hugging Face Transformers` - Transformer model ecosystem
- `SentenceTransformers` - Semantic similarity modeling
- `scikit-learn` - Classical ML utilities

### Language Processing
- `langdetect` - Automatic language identification
- `MarianMTModel` & `MarianTokenizer` - Neural machine translation
- `regex`, `unicodedata` - Text preprocessing

### Visualization & Evaluation
- `sklearn` - Classification metrics and evaluation
- `matplotlib` - Data visualization

### Workflow Utilities
- `tqdm` - Progress tracking for long-running processes
- `gc` - Memory cleanup and optimization

## Datasets & Models

### Data Assets
- **Google Local Reviews Dataset** - Raw review data source
- **Custom Labeled Dataset** - Manually annotated data for relevancy and spam detection evaluation

### Pre-trained Models
- **`sentence-transformers/all-MiniLM-L6-v2`** - Semantic similarity for relevancy scoring and spam detection
- **`twitter-roberta-base-sentiment`** - Sentiment analysis capabilities

## Solution Focus

Our solution specifically addresses the **relevancy** portion of review quality assessment, focusing on:
- ✅ Filtering out irrelevant and spammy reviews
- ✅ Surfacing reviews that provide genuine value to businesses and users
- ✅ Maintaining high precision in quality assessment

## Getting Started

[Add installation and usage instructions here]

## Contributing

[Add contribution guidelines here]

## License

[Add license information here]