from trend_analyzer import predict_trends

# Sample articles for testing
articles = [
    {
        'title': 'Startup X Secures Series A Funding',
        'link': 'http://example.com/startup-x-funding',
        'bullets': [
            'Startup X has secured a Series A funding round.',
            'The investment will be used for market expansion.'
        ]
    },
    {
        'title': 'Company Y Opens New Office',
        'link': 'http://example.com/company-y-expansion',
        'bullets': [
            'Company Y is expanding by opening a new office in Europe.',
            'This move aims to increase their global reach.'
        ]
    }
]

# Predict trends
predicted_articles = predict_trends(articles)

# Display results
for article in predicted_articles:
    print(f"Title: {article['title']}")
    print(f"Predicted Trend: {article['trend']}\n")
