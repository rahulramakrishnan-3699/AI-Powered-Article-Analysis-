import logging
from typing import List, Dict
from scraper import scrape_articles
from summarizer import summarize_articles
from trend_analyzer import predict_trends

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def run_pipeline() -> List[Dict]:
    """
    Run the complete competitive intelligence pipeline.
    
    Returns:
        List[Dict]: List of processed articles with summaries and trends
    """
    try:
        # Step 1: Scrape articles
        logger.info("Starting article scraping...")
        articles = scrape_articles()
        logger.info(f"Successfully scraped {len(articles)} articles")
        
        if not articles:
            logger.warning("No articles were scraped. Check the scraper implementation.")
            return []
            
        # Log the first article for debugging
        if articles:
            logger.info(f"First article title: {articles[0].get('title', 'No title')}")
            logger.info(f"First article link: {articles[0].get('link', 'No link')}")
        
        # Step 2: Summarize articles
        logger.info("Generating article summaries...")
        summarized_articles = summarize_articles(articles)
        logger.info(f"Successfully generated summaries for {len(summarized_articles)} articles")
        
        if not summarized_articles:
            logger.warning("No articles were summarized. Check the summarizer implementation.")
            return []
            
        # Log the first summarized article for debugging
        if summarized_articles:
            logger.info(f"First article bullets: {summarized_articles[0].get('bullets', [])}")
        
        # Step 3: Predict trends
        logger.info("Analyzing trends...")
        analyzed_articles = predict_trends(summarized_articles)
        logger.info(f"Successfully analyzed trends for {len(analyzed_articles)} articles")
        
        if not analyzed_articles:
            logger.warning("No articles were analyzed for trends. Check the trend analyzer implementation.")
            return []
            
        # Log the first analyzed article for debugging
        if analyzed_articles:
            logger.info(f"First article trend: {analyzed_articles[0].get('trend', 'No trend')}")
        
        return analyzed_articles
        
    except Exception as e:
        logger.error(f"Pipeline failed: {str(e)}")
        return []

def display_results(articles: List[Dict]) -> None:
    """
    Display the results in a formatted way.
    
    Args:
        articles: List of processed articles
    """
    if not articles:
        print("\nNo articles to display.")
        return
        
    print("\n=== Competitive Intelligence Report ===\n")
    
    for i, article in enumerate(articles, 1):
        print(f"Article {i}:")
        print(f"Title: {article['title']}")
        print(f"Link: {article['link']}")
        print("\nSummary:")
        for bullet in article.get('bullets', []):
            print(f"  {bullet}")
        print(f"\nDetected Trend: {article.get('trend', 'No trend detected')}")
        print("\n" + "="*50 + "\n")

def main():
    """Main function to run the competitive intelligence pipeline."""
    try:
        # Run the pipeline
        articles = run_pipeline()
        # Display results
        display_results(articles)
        
    except KeyboardInterrupt:
        logger.info("Pipeline interrupted by user")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    main() 