# News Aggregator Backend API

This is the backend API for the News Aggregator project. It provides endpoints for scraping and analyzing news articles.

## Features

- Article scraping using newspaper3k
- Text analysis including:
  - Sentiment analysis
  - Keyword extraction
  - Article summarization

## Setup

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the API

Start the FastAPI server:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

## API Endpoints

### GET /
- Welcome message
- Returns: `{"message": "Welcome to the News Aggregator API"}`

### POST /analyze
- Analyzes a news article from a given URL
- Request body:
```json
{
    "url": "https://example.com/news-article"
}
```
- Returns:
```json
{
    "title": "Article Title",
    "content": "Article Content",
    "summary": "Article Summary",
    "keywords": ["keyword1", "keyword2", ...],
    "sentiment": 0.5
}
```

## Error Handling

The API includes proper error handling for:
- Invalid URLs
- Failed article scraping
- Analysis errors

All errors return appropriate HTTP status codes and error messages. 