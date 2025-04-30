from summarizer import summarize_articles

# Sample articles list
articles = [
    {
        'title': 'Sample Article',
        'link': 'http://example.com',
        'summary': 'Artificial Intelligence (AI) is transforming industries by enabling new capabilities and efficiencies. Companies are investing heavily in AI research and development to stay competitive in the evolving market.'
    }
]

# Summarize articles
summarized_articles = summarize_articles(articles)

# Print summarized articles
for article in summarized_articles:
    print(f"Title: {article['title']}")
    print("Bullets:")
    for bullet in article['bullets']:
        print(f"- {bullet}")
