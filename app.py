import streamlit as st
from scraper import scrape_articles
from summarizer import summarize_articles
from trend_analyzer import predict_trends
import traceback
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="Article Analyzer",
    page_icon="📰",
    layout="wide"
)

# Custom styling - minimal with reduced spacing
st.markdown("""
    <style>
    .main {
        padding: 1rem;
    }
    p {
        margin-bottom: 0.5rem;
    }
    .stMarkdown {
        line-height: 1.2;
    }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.title("📰 Article Analyzer")
st.markdown("""
Enter a URL to analyze articles. For each article in the URL, the tool will:
- Extract the article content
- Generate a bullet-point summary
- Identify key trends in the article's content
""")

# URL input
url = st.text_input(
    "Enter URL",
    placeholder="https://example.com/news",
    help="Enter the URL of a webpage containing articles you want to analyze"
)

def process_url(url):
    """Process the URL and return analyzed articles"""
    try:
        # Step 1: Scrape articles
        with st.spinner("Scraping articles..."):
            articles = scrape_articles(url)
            if not articles:
                st.warning("No articles found at the provided URL.")
                return None
            st.success(f"Found {len(articles)} articles!")

        # Step 2: Process each article
        with st.spinner("Analyzing articles..."):
            processed_articles = []
            
            for article in articles:
                try:
                    # Generate summary and limit to 4 bullet points
                    bullet_points = summarize_articles(article['content'])[:4]
                    
                    # Analyze trends for this specific article
                    clean_points = [point.replace('• ', '') for point in bullet_points]
                    article_trends = predict_trends(clean_points)
                    
                    processed_articles.append({
                        'title': article['title'],
                        'summary': bullet_points,
                        'trends': article_trends
                    })
                    
                except Exception as e:
                    logger.error(f"Error processing article '{article.get('title', 'Unknown')}': {str(e)}")
                    continue

            if not processed_articles:
                st.error("Failed to process any articles.")
                return None

            st.success("Analysis complete!")
            return processed_articles

    except Exception as e:
        logger.error(f"Error in process_url: {str(e)}")
        st.error("An error occurred during processing")
        with st.expander("Error Details"):
            st.code(traceback.format_exc())
        return None

# Process button
if st.button("Analyze", type="primary"):
    if not url:
        st.error("Please enter a URL to analyze")
    else:
        try:
            articles = process_url(url)
            
            if articles:
                st.header("Analysis Results")
                
                for i, article in enumerate(articles, 1):
                    # Article title
                    st.markdown(f"**Article {i}: {article['title']}**")
                    
                    # Summary section
                    st.markdown("**Summary:**")
                    for point in article['summary']:
                        st.markdown(point)
                    
                    # Trends section - inline
                    trends_text = ", ".join(trend.replace('Found trend: ', '') for trend in article['trends'])
                    st.markdown(f"**Detected Trends:** {trends_text}")
                    
                    # Add minimal spacing between articles
                    st.markdown("---")

        except Exception as e:
            logger.error(f"Error in main execution: {str(e)}")
            st.error("An error occurred while processing the URL")
            with st.expander("Error Details"):
                st.code(traceback.format_exc())
            st.info("Please check the URL and try again, or contact support if the problem persists.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>Article Analyzer | Built with Streamlit</p>
</div>
""", unsafe_allow_html=True) 