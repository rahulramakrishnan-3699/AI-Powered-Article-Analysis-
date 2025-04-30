import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import logging
import re
from urllib.parse import urljoin

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def clean_text(text: str) -> str:
    """Clean and normalize text content"""
    if not text:
        return ""
    # Remove extra whitespace and normalize
    text = ' '.join(text.split())
    return text.strip()

def is_valid_article_link(href: str) -> bool:
    """Check if a link is likely to be an article"""
    if not href:
        return False
    
    # Common patterns for article URLs
    article_patterns = [
        r'/\d{4}/',  # Year pattern
        r'/article/',
        r'/story/',
        r'/news/',
        r'/posts?/',
        r'/\d{4}/\d{2}/',  # Year/month pattern
        r'/blog/',
    ]
    
    return any(re.search(pattern, href.lower()) for pattern in article_patterns)

def scrape_articles(url: str) -> List[Dict[str, str]]:
    """
    Scrapes articles from various news websites.
    
    Args:
        url (str): The URL of the news website to scrape
        
    Returns:
        List[Dict[str, str]]: List of dictionaries containing article information
        Each dictionary contains 'title' and 'content' keys
    """
    articles = []
    
    try:
        # Add headers to mimic a browser request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Fetch the main page
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find potential article links
        article_links = []
        for a in soup.find_all('a', href=True):
            href = a['href']
            # Make relative URLs absolute
            full_url = urljoin(url, href)
            
            # Check if it's likely an article link
            if is_valid_article_link(href):
                article_links.append((full_url, a.get_text()))
        
        # Remove duplicates while preserving order
        article_links = list(dict.fromkeys(article_links))
        
        # Limit to first 10 articles
        article_links = article_links[:10]
        
        logger.info(f"Found {len(article_links)} potential articles")
        
        # Process each article
        for article_url, link_text in article_links:
            try:
                # Fetch article page
                article_response = requests.get(article_url, headers=headers, timeout=10)
                article_response.raise_for_status()
                article_soup = BeautifulSoup(article_response.text, 'html.parser')
                
                # Try different methods to find the title
                title = None
                # Method 1: Look for article headline
                headline = article_soup.find(['h1', 'h2'], class_=re.compile(r'headline|title|article-title|post-title', re.I))
                if headline:
                    title = clean_text(headline.get_text())
                # Method 2: Use the link text if it's long enough
                elif len(link_text) > 20:
                    title = clean_text(link_text)
                # Method 3: Look for the first h1
                elif article_soup.h1:
                    title = clean_text(article_soup.h1.get_text())
                
                if not title:
                    continue
                
                # Try different methods to find the content
                content = ""
                # Method 1: Look for article body
                article_body = article_soup.find(['article', 'div'], class_=re.compile(r'article-body|post-content|entry-content|article-content', re.I))
                if article_body:
                    # Get all paragraphs from the article body
                    paragraphs = article_body.find_all('p')
                    content = '\n'.join(clean_text(p.get_text()) for p in paragraphs if len(clean_text(p.get_text())) > 50)
                
                # Method 2: If no article body found, try to find main content area
                if not content:
                    main_content = article_soup.find(['main', 'div'], class_=re.compile(r'main-content|content|post', re.I))
                    if main_content:
                        paragraphs = main_content.find_all('p')
                        content = '\n'.join(clean_text(p.get_text()) for p in paragraphs if len(clean_text(p.get_text())) > 50)
                
                # Method 3: Last resort - get all paragraphs from the page
                if not content:
                    paragraphs = article_soup.find_all('p')
                    content = '\n'.join(clean_text(p.get_text()) for p in paragraphs if len(clean_text(p.get_text())) > 50)
                
                if content:
                    articles.append({
                        'title': title,
                        'content': content
                    })
                    logger.info(f"Successfully scraped article: {title[:50]}...")
                
            except Exception as e:
                logger.warning(f"Error processing article {article_url}: {str(e)}")
                continue
                
    except requests.RequestException as e:
        logger.error(f"Failed to fetch from {url}: {str(e)}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return []
    
    logger.info(f"Successfully scraped {len(articles)} articles")
    return articles

if __name__ == "__main__":
    # Example usage
    test_url = "https://techcrunch.com"
    articles = scrape_articles(test_url)
    for i, article in enumerate(articles, 1):
        print(f"\nArticle {i}:")
        print(f"Title: {article['title'][:100]}...")
        print(f"Content length: {len(article['content'])} characters")
