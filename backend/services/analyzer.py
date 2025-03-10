from typing import Dict, Any, List
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.tag import pos_tag
from nltk.chunk import ne_chunk
from collections import Counter

class NewsAnalyzer:
    def __init__(self):
        # Download required NLTK data
        try:
            nltk.data.find('vader_lexicon')
            nltk.data.find('punkt')
            nltk.data.find('stopwords')
            nltk.data.find('averaged_perceptron_tagger')
            nltk.data.find('maxent_ne_chunker')
            nltk.data.find('words')
        except LookupError:
            nltk.download('vader_lexicon')
            nltk.download('punkt')
            nltk.download('stopwords')
            nltk.download('averaged_perceptron_tagger')
            nltk.download('maxent_ne_chunker')
            nltk.download('words')
        
        self.sia = SentimentIntensityAnalyzer()
        self.stop_words = set(stopwords.words('english'))
        
        # Topic keywords for classification
        self.topic_keywords = {
            'politics': ['government', 'minister', 'election', 'party', 'parliament', 'political', 'vote', 'democracy'],
            'sports': ['cricket', 'football', 'game', 'player', 'tournament', 'match', 'sport', 'team', 'championship'],
            'business': ['market', 'economy', 'company', 'stock', 'business', 'trade', 'investment', 'financial'],
            'technology': ['technology', 'digital', 'software', 'internet', 'cyber', 'tech', 'AI', 'innovation'],
            'entertainment': ['movie', 'film', 'music', 'actor', 'celebrity', 'entertainment', 'star', 'cinema'],
            'health': ['health', 'medical', 'hospital', 'disease', 'treatment', 'doctor', 'patient', 'healthcare'],
            'agriculture': ['farm', 'crop', 'agriculture', 'farmer', 'harvest', 'cultivation', 'agricultural', 'farming']
        }

    def analyze_article(self, article_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze the content of a news article.
        
        Args:
            article_data (Dict[str, Any]): Dictionary containing article data
            
        Returns:
            Dict[str, Any]: Dictionary containing analysis results
        """
        try:
            content = article_data["content"]
            
            # Perform sentiment analysis
            sentiment_scores = self.sia.polarity_scores(content)
            
            # Classify topic
            topic = self._classify_topic(content)
            
            # Generate summary (first few sentences, max 150 words)
            summary = self._generate_summary(content)
            
            # Extract entities (people and locations)
            entities = self._extract_entities(content)
            
            return {
                "title": article_data["title"],
                "topic": topic,
                "summary": summary,
                "sentiment": sentiment_scores["compound"],
                "entities": entities
            }
        except Exception as e:
            raise Exception(f"Failed to analyze article: {str(e)}")

    def _classify_topic(self, text: str) -> str:
        """Classify the topic of the article based on keyword frequency."""
        words = word_tokenize(text.lower())
        words = [w for w in words if w.isalnum() and w not in self.stop_words]
        
        topic_scores = {}
        for topic, keywords in self.topic_keywords.items():
            score = sum(1 for word in words if word in keywords)
            topic_scores[topic] = score
        
        # Return the topic with highest score, or 'general' if no clear topic
        max_score = max(topic_scores.values())
        if max_score > 0:
            return max(topic_scores.items(), key=lambda x: x[1])[0]
        return 'general'

    def _generate_summary(self, text: str, max_words: int = 150) -> str:
        """Generate a summary of the text within word limit."""
        sentences = sent_tokenize(text)
        summary = []
        word_count = 0
        
        for sentence in sentences:
            words = word_tokenize(sentence)
            if word_count + len(words) <= max_words:
                summary.append(sentence)
                word_count += len(words)
            else:
                break
        
        return ' '.join(summary)

    def _extract_entities(self, text: str) -> Dict[str, List[str]]:
        """Extract named entities (people and locations) from the text."""
        sentences = nltk.sent_tokenize(text)
        entities = {'people': set(), 'locations': set()}
        
        for sentence in sentences:
            words = nltk.word_tokenize(sentence)
            tagged = nltk.pos_tag(words)
            named_entities = ne_chunk(tagged)
            
            for chunk in named_entities:
                if hasattr(chunk, 'label'):
                    name = ' '.join(c[0] for c in chunk)
                    if chunk.label() == 'PERSON':
                        entities['people'].add(name)
                    elif chunk.label() in ('GPE', 'LOCATION'):
                        entities['locations'].add(name)
        
        return {
            'people': list(entities['people']),
            'locations': list(entities['locations'])
        }

    def _extract_keywords(self, text: str, num_keywords: int = 10) -> List[str]:
        """
        Extract the most important keywords from the text.
        
        Args:
            text (str): The text to analyze
            num_keywords (int): Number of keywords to extract
            
        Returns:
            List[str]: List of keywords
        """
        # Tokenize and clean text
        tokens = word_tokenize(text.lower())
        tokens = [token for token in tokens if token.isalnum() and token not in self.stop_words]
        
        # Count word frequencies
        word_freq = Counter(tokens)
        
        # Get most common words
        keywords = [word for word, _ in word_freq.most_common(num_keywords)]
        
        return keywords 