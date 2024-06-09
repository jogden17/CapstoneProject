# pytrends found here https://github.com/GeneralMills/pytrends?tab=readme-ov-file#realtime-search-trends
# This code pulls the realtime or past 24h search trends from Google Trends
from pytrends.request import TrendReq
pytrends = TrendReq(hl='en-US', tz=360)

# realtime search trends for the United States in the "Top News" category
#headlines = pytrends.realtime_trending_searches(pn='US')#, cat='h')
#titles = headlines['title']

# This searches the trends of the last 24 hours
headlines = pytrends.trending_searches(pn='united_states')
titles = headlines[0]

# gets keywords from trends used to search for articles
keywords = []
for i in titles:
    keys = i.split(", ")

    # formats the search query
    search = ""
    for j in keys:
        search = search + j + ", "
    search = search.removesuffix(", ")

    keywords.append(search)

print(len(keywords))


# gnews found here https://github.com/ranahaani/GNews
from gnews import GNews
import pandas as pd

linkDatabase = pd.DataFrame()
linkDatabase['Headline'] = keywords
linkHolder = []
for i in keywords:
    # searches english language publications in America over the past two days
    google_news = GNews(language='en', country='US', period='2d')#, proxy=proxy)
    news = google_news.get_news(i)
    print(i)
    print(len(news))
    if len(news) > 0: print(news[0]['url'])

    links = []
    for j in news:
        links.append(j['url'])

    linkHolder.append(links)

linkDatabase['Links'] = linkHolder
linkDatabase.to_csv('HeadlinesAndLinks.csv', index=False)

