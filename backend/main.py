from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from services.scraper import NewsScraper
from services.analyzer import NewsAnalyzer

app = FastAPI(title="News Aggregator API",
             description="API for scraping and analyzing news articles",
             version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ArticleAnalysis(BaseModel):
    title: str
    url: str
    topic: str
    summary: str
    sentiment: float
    entities: dict

@app.get("/")
async def root():
    return {"message": "Welcome to the News Aggregator API"}

@app.get("/analyze-news", response_model=List[ArticleAnalysis])
async def analyze_news():
    try:
        # Initialize services
        scraper = NewsScraper()
        analyzer = NewsAnalyzer()
        
        # Scrape articles from all sources
        articles = scraper.scrape_all_sources()
        
        # Analyze each article
        analyzed_articles = []
        for article in articles:
            if article:  # Check if article was successfully scraped
                analysis = analyzer.analyze_article(article)
                analysis['url'] = article['url']  # Add URL to the analysis
                analyzed_articles.append(analysis)
        
        return analyzed_articles
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 