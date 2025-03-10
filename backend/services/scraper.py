import requests
from bs4 import BeautifulSoup
from typing import Dict, Any, List
import nltk
from nltk.tokenize import sent_tokenize
from urllib.parse import urljoin

class NewsScraper:
    def __init__(self):
        # Download required NLTK data
        try:
            nltk.data.find('punkt')
        except LookupError:
            nltk.download('punkt')
        
        self.news_sources = {
            'timesofindia': {
                'url': 'https://timesofindia.indiatimes.com/?loc=in',
                'article_selector': '.main-content article',
                'title_selector': 'h1',
                'content_selector': '.article-body, .content'
            },
            'thehindu': {
                'url': 'https://www.thehindu.com/sport/',
                'article_selector': '.article',
                'title_selector': 'h1.title',
                'content_selector': '.article-content'
            },
            'hindustantimes': {
                'url': 'https://www.hindustantimes.com/',
                'article_selector': '.article',
                'title_selector': 'h1',
                'content_selector': '.article-body'
            }
        }

        # Sample articles for testing with full content
        self.sample_articles = [
            {
                "title": "India's Economic Growth Surges in Q4",
                "content": """India's economy showed remarkable resilience in the fourth quarter, with GDP growth reaching 8.4%. The manufacturing sector led the expansion, followed by services and agriculture. The Finance Minister attributed the growth to robust domestic demand and government initiatives.

The Reserve Bank of India expects this momentum to continue into the next fiscal year, projecting a growth rate between 7.5% and 8%. Several key factors contributed to this growth:

1. Manufacturing Sector Performance:
- Industrial production increased by 12.5%
- Export growth in manufacturing reached 15%
- Employment in the sector grew by 9%

2. Services Sector Highlights:
- IT services revenue up by 18%
- Financial services grew by 14%
- Tourism sector showed 25% recovery

3. Agricultural Growth:
- Record food grain production
- Agricultural exports increased by 22%
- Farm income rose by 11%

Several states, including Maharashtra and Gujarat, reported significant industrial growth. Maharashtra's industrial output grew by 13.2%, while Gujarat recorded 11.8% growth. The government's PLI scheme has attracted investments worth $27 billion across various sectors.

Foreign investors have shown increased interest in Indian markets, with FDI reaching new highs of $87 billion. The stock market indices have also reflected this optimism, with both Sensex and Nifty touching record levels.

Economists predict this growth trajectory will help India maintain its position as the fastest-growing major economy. However, they also caution about potential challenges from global economic uncertainties and inflationary pressures.""",
                "url": "https://example.com/india-economy"
            },
            {
                "title": "Major Cricket Tournament Announced",
                "content": """The International Cricket Council has announced a new tournament format for 2024, bringing significant changes to international cricket. The tournament will feature teams from 12 countries competing across multiple venues in India, marking one of the most ambitious cricket events in recent history.

Tournament Structure:
1. Format:
- 12 teams divided into two groups
- Round-robin format in initial stages
- Top two teams from each group advance to semifinals
- Final to be held at Narendra Modi Stadium, Ahmedabad

2. Participating Nations:
- Traditional powerhouses: India, Australia, England
- Strong contenders: South Africa, New Zealand, Pakistan
- Emerging teams: Afghanistan, Bangladesh, West Indies
- Qualifier winners: Ireland, Zimbabwe, Netherlands

Former captain MS Dhoni will serve as a mentor to the Indian team, bringing his vast experience and tactical acumen. Under his guidance, the team will focus on:
- Developing young talent
- Strategic planning for different conditions
- Mental preparation for high-pressure situations

The tournament is expected to boost local economies in host cities including Mumbai, Delhi, and Chennai. Economic experts predict:
- Tourism revenue increase of $300 million
- Creation of 20,000 temporary jobs
- Significant boost to hospitality sector

Team selections have sparked debates among cricket experts, with several young players getting their first international opportunity. Notable selections include:
- Three uncapped players in the Indian squad
- Return of veteran players in Australian team
- Experimental combinations in England's lineup

The tournament will also feature:
- Advanced technology for decision reviews
- Bio-secure bubbles for player safety
- Innovative broadcast technology
- Fan engagement initiatives

This tournament is seen as a crucial step in cricket's global expansion strategy and development of the sport in emerging markets.""",
                "url": "https://example.com/cricket-tournament"
            },
            {
                "title": "Agricultural Reform Bill Passed",
                "content": """Parliament has passed a comprehensive agricultural reform bill aimed at modernizing farming practices across India. The bill, which received bipartisan support, includes provisions for technology adoption, sustainable farming, and direct market access for farmers.

Key Components of the Bill:

1. Technology Integration:
- Digital marketplace for agricultural products
- Smart farming initiatives using IoT devices
- Weather monitoring and prediction systems
- Drone technology for crop assessment

2. Sustainable Farming Practices:
- Organic farming incentives
- Water conservation techniques
- Soil health management programs
- Crop rotation guidelines

3. Market Access Reforms:
- Direct farmer-to-consumer platforms
- Elimination of middlemen
- Interstate trade facilitation
- Export promotion initiatives

Several states including Punjab and Haryana have already begun implementing pilot programs. Early results show:
- 15% increase in farmer income
- 20% reduction in water usage
- 30% improvement in crop yield
- 25% decrease in post-harvest losses

Farmer organizations have largely welcomed the reforms, though some have expressed concerns about implementation. The main points of discussion include:

Implementation Timeline:
- Phase 1: Digital infrastructure setup (6 months)
- Phase 2: Training and capacity building (1 year)
- Phase 3: Full market integration (2 years)
- Phase 4: International market access (3 years)

Support Mechanisms:
- Financial assistance for technology adoption
- Training programs for farmers
- Infrastructure development
- Market linkage support

The Ministry of Agriculture estimates that these changes will benefit over 50 million farmers across India. The expected outcomes include:
- 40% increase in average farm income by 2025
- 30% reduction in water consumption
- 25% increase in organic farming adoption
- 35% improvement in supply chain efficiency

Environmental Impact:
- Reduced chemical fertilizer usage
- Lower groundwater depletion
- Increased biodiversity
- Better soil health management

The bill also addresses climate change adaptation and resilience building in the agricultural sector.""",
                "url": "https://example.com/agri-reform"
            }
        ]

    def scrape_all_sources(self) -> List[Dict[str, Any]]:
        """
        Return sample articles for testing.
        
        Returns:
            List[Dict[str, Any]]: List of sample articles
        """
        return self.sample_articles

    def scrape_source(self, source: str) -> List[Dict[str, Any]]:
        """
        Scrape articles from a specific news source.
        
        Args:
            source (str): Source identifier
            
        Returns:
            List[Dict[str, Any]]: List of articles from the source
        """
        config = self.news_sources[source]
        articles = []
        
        try:
            # Fetch the webpage
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(config['url'], headers=headers)
            response.raise_for_status()
            
            # Parse with BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find all article links
            article_elements = soup.select(config['article_selector'])
            
            for element in article_elements[:5]:  # Limit to 5 articles per source
                try:
                    # Find article link
                    link = element.find('a')
                    if not link:
                        continue
                        
                    article_url = urljoin(config['url'], link['href'])
                    article_data = self.scrape_article(article_url, config)
                    if article_data:
                        articles.append(article_data)
                except Exception as e:
                    print(f"Error scraping article: {str(e)}")
                    continue
            
        except Exception as e:
            raise Exception(f"Failed to scrape {source}: {str(e)}")
            
        return articles

    def scrape_article(self, url: str, config: Dict[str, str] = None) -> Dict[str, Any]:
        """
        Scrape and parse a news article from the given URL.
        
        Args:
            url (str): The URL of the news article to scrape
            config (Dict[str, str]): Configuration for the news source
            
        Returns:
            Dict[str, Any]: Dictionary containing article data
        """
        try:
            # Fetch the webpage
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            # Parse with BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract title
            title = ''
            if config and config['title_selector']:
                title_elem = soup.select_one(config['title_selector'])
                if title_elem:
                    title = title_elem.get_text().strip()
            
            if not title:
                title_tags = ['h1', 'h2']
                for tag in title_tags:
                    title_elem = soup.find(tag)
                    if title_elem:
                        title = title_elem.get_text().strip()
                        break
            
            # Extract content
            content = ''
            if config and config['content_selector']:
                content_elem = soup.select_one(config['content_selector'])
                if content_elem:
                    # Remove script and style elements
                    for elem in content_elem(['script', 'style']):
                        elem.decompose()
                    content = content_elem.get_text().strip()
            
            if not content:
                # Fallback to paragraphs
                paragraphs = soup.find_all('p')
                content = ' '.join([p.get_text().strip() for p in paragraphs])
            
            if not title or not content:
                return None
            
            return {
                "title": title,
                "content": content,
                "url": url
            }
        except Exception as e:
            print(f"Failed to scrape article {url}: {str(e)}")
            return None 