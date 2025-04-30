from typing import List, Dict
import logging
from transformers import pipeline
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the summarization pipeline
try:
    summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
    logger.info("Successfully loaded DistilBART model")
except Exception as e:
    logger.error(f"Error loading model: {str(e)}")
    summarizer = None

def chunk_text(text: str, max_chunk_size: int = 1000) -> List[str]:
    """Split text into smaller chunks for processing."""
    words = text.split()
    chunks = []
    current_chunk = []
    current_size = 0
    
    for word in words:
        if current_size + len(word) + 1 > max_chunk_size:
            chunks.append(' '.join(current_chunk))
            current_chunk = [word]
            current_size = len(word)
        else:
            current_chunk.append(word)
            current_size += len(word) + 1
    
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    
    return chunks

def combine_related_sentences(sentences: List[str]) -> List[str]:
    """Combine related sentences into coherent bullet points."""
    combined = []
    current_sentence = ""
    
    for sentence in sentences:
        # Strip any existing bullet points and clean the sentence
        clean_sentence = re.sub(r'^[•\-\*]\s*', '', sentence.strip())
        
        # Check if this is a continuation (starts with lowercase or connecting words)
        connecting_words = ['and', 'or', 'but', 'nor', 'for', 'yet', 'so', 'as', 'while']
        is_continuation = (
            clean_sentence[0].islower() if clean_sentence else False or
            any(clean_sentence.lower().startswith(word + ' ') for word in connecting_words)
        )
        
        if is_continuation and current_sentence:
            # Add to current sentence
            current_sentence += " " + clean_sentence
        else:
            # Save previous sentence if exists
            if current_sentence:
                combined.append(current_sentence)
            # Start new sentence
            current_sentence = clean_sentence
    
    # Add the last sentence
    if current_sentence:
        combined.append(current_sentence)
    
    return combined

def summarize_text(text: str) -> List[str]:
    """
    Summarize a piece of text into bullet points.
    
    Args:
        text: The text to summarize
        
    Returns:
        List of bullet points
    """
    if not text or not summarizer:
        return []
    
    try:
        # Split text into chunks if it's too long
        chunks = chunk_text(text)
        summaries = []
        
        for chunk in chunks:
            # Skip if chunk is too short
            if len(chunk.split()) < 30:
                continue
                
            # Summarize the chunk
            summary = summarizer(chunk,
                               max_length=130,
                               min_length=30,
                               do_sample=False)[0]['summary_text']
            
            summaries.append(summary.strip())
        
        # Combine all summaries
        combined_summary = ' '.join(summaries)
        
        # Split into sentences
        sentences = [s.strip() + '.' for s in combined_summary.split('.') if s.strip()]
        
        # Combine related sentences
        bullet_points = combine_related_sentences(sentences)
        
        # Format and limit to 4 main points
        formatted_points = [f"• {point}" for point in bullet_points if point][:4]
        
        return formatted_points
        
    except Exception as e:
        logger.error(f"Error summarizing text: {str(e)}")
        return []

def summarize_articles(content: str) -> List[str]:
    """
    Generate bullet-point summaries from article content.
    
    Args:
        content: The article content to summarize
        
    Returns:
        List of bullet points summarizing the content
    """
    try:
        return summarize_text(content)
    except Exception as e:
        logger.error(f"Error processing article content: {str(e)}")
        return []

if __name__ == "__main__":
    # Example usage
    sample_content = """
    In a groundbreaking development, researchers have discovered a new way to implement quantum computing that could revolutionize the field. 
    The team, led by Dr. Sarah Johnson at MIT, has developed a novel approach that addresses the long-standing problem of quantum decoherence. 
    This breakthrough could lead to more stable quantum computers that can operate at room temperature, a significant advancement over current systems that require extreme cooling.
    The research, published in Nature, demonstrates a 90% improvement in quantum bit stability compared to existing methods. 
    Industry experts suggest this could accelerate the development of practical quantum computers by several years.
    Major tech companies have already expressed interest in implementing this new technology, with potential applications ranging from drug discovery to climate modeling.
    """
    
    bullet_points = summarize_articles(sample_content)
    print("Summary Bullet Points:")
    for point in bullet_points:
        print(point)
