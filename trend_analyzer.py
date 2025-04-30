from typing import List, Dict
import logging
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define trend keywords and their corresponding labels
TREND_KEYWORDS = {
    'Likely to Raise Funding': [
        'funding', 'raise', 'investment', 'series', 'round', 'venture', 'capital',
        'seed', 'angel', 'investor', 'backing', 'funded', 'financing', 'valuation',
        'equity', 'stake', 'fund', 'backer', 'lead investor', 'co-investor'
    ],
    'Expansion Plans': [
        'expand', 'expansion', 'growth', 'scale', 'new market', 'international',
        'global', 'region', 'territory', 'location', 'office', 'presence',
        'geographic', 'country', 'city', 'market entry', 'localization',
        'regional', 'territorial', 'expansion strategy'
    ],
    'Hiring Activity': [
        'hire', 'hiring', 'recruit', 'job', 'position', 'employee', 'team',
        'workforce', 'staff', 'talent', 'headcount', 'role', 'career',
        'opportunity', 'vacancy', 'opening', 'recruitment', 'talent acquisition',
        'job posting', 'career growth'
    ],
    'Product Launch': [
        'launch', 'release', 'product', 'feature', 'update', 'version',
        'new offering', 'platform', 'service', 'solution', 'beta', 'alpha',
        'preview', 'early access', 'rollout', 'deployment', 'announcement',
        'introduction', 'unveiling'
    ],
    'Partnership': [
        'partner', 'partnership', 'collaborate', 'alliance', 'joint venture',
        'strategic', 'deal', 'agreement', 'cooperation', 'integration',
        'ecosystem', 'network', 'channel', 'distribution', 'reseller',
        'technology partner', 'business partner'
    ],
    'Acquisition': [
        'acquire', 'acquisition', 'buy', 'purchase', 'takeover', 'merge',
        'merger', 'consolidation', 'buyout', 'deal', 'transaction',
        'integration', 'combine', 'unite', 'join forces'
    ],
    'Technology Innovation': [
        'innovation', 'technology', 'ai', 'artificial intelligence', 'machine learning',
        'blockchain', 'cloud', 'saas', 'software', 'hardware', 'research',
        'development', 'patent', 'intellectual property', 'breakthrough',
        'cutting-edge', 'next-gen', 'revolutionary'
    ],
    'Market Leadership': [
        'leader', 'leadership', 'market leader', 'industry leader', 'pioneer',
        'first-mover', 'dominant', 'top', 'best', 'award', 'recognition',
        'achievement', 'milestone', 'benchmark', 'standard'
    ],
    'Customer Growth': [
        'customer', 'user', 'subscriber', 'client', 'base', 'growth',
        'adoption', 'onboarding', 'retention', 'satisfaction', 'feedback',
        'testimonial', 'case study', 'success story', 'reference'
    ],
    'Regulatory Compliance': [
        'compliance', 'regulation', 'certification', 'standard', 'policy',
        'guideline', 'requirement', 'approval', 'authorization', 'license',
        'permit', 'accreditation', 'audit', 'inspection'
    ]
}

def analyze_text_for_trends(text: str) -> List[str]:
    """
    Analyze text to find matching trends.
    
    Args:
        text: Text to analyze
        
    Returns:
        List of detected trends
    """
    text = text.lower()
    trend_matches = {}
    
    for trend, keywords in TREND_KEYWORDS.items():
        matches = sum(1 for keyword in keywords if re.search(r'\b' + keyword + r'\b', text))
        if matches > 0:
            trend_matches[trend] = matches
            
    # Sort trends by number of matches
    sorted_trends = sorted(trend_matches.items(), key=lambda x: x[1], reverse=True)
    
    # Return top trends (those with at least 2 matches)
    return [trend for trend, matches in sorted_trends if matches >= 2]

def predict_trends(bullet_points: List[str]) -> List[str]:
    """
    Analyze bullet points to detect trends.
    
    Args:
        bullet_points: List of bullet point strings
        
    Returns:
        List of detected trends
    """
    try:
        # Combine all bullet points into a single text
        text = ' '.join(bullet_points)
        
        # Analyze for trends
        trends = analyze_text_for_trends(text)
        
        if not trends:
            return ["No significant trends detected"]
            
        # Format trends nicely
        return [f"{trend}" for trend in trends]
        
    except Exception as e:
        logger.error(f"Error analyzing trends: {str(e)}")
        return ["Error analyzing trends"]

if __name__ == "__main__":
    # Example usage
    sample_bullets = [
        "Company secured $10M in Series A funding.",
        "Plans to expand to new markets in Asia.",
        "Hiring 50 new employees across departments.",
        "Launching new AI-powered platform next month.",
        "Partnership with major tech companies announced."
    ]
    
    trends = predict_trends(sample_bullets)
    print("\nDetected Trends:")
    for trend in trends:
        print(f"• {trend}") 

#########
