import urllib.request
import pandas as pd
# pytrends found here https://github.com/GeneralMills/pytrends?tab=readme-ov-file#realtime-search-trends
from pytrends.request import TrendReq
# gnews found here https://github.com/ranahaani/GNews
from gnews import GNews

# gets the final redirect link from the google news link
def finalLink(startLink):
    # open a connection to a URL using urllib
    webUrl = urllib.request.urlopen(startLink)

    # read the data from the URL and print it
    data = str(webUrl.read())

    # pull the final link from the html code
    linkStart = data.rfind('http')
    data = data[linkStart:]
    linkEnd = data.find('"')
    secondLinkEnd = data.find('\\')

    if secondLinkEnd < linkEnd: linkEnd = secondLinkEnd

    data = data[:linkEnd]
    return data

def getHeadlines(realTime):
    # This code pulls the realtime or past 24h search trends from Google Trends
    pytrends = TrendReq(hl='en-US', tz=360)

    if realTime:
        # realtime search trends for the United States in the "Top News" category. More specific than 24 hour trends
        headlines = pytrends.realtime_trending_searches(pn='US')#, cat='h')
        titles = headlines['title']

    else:
        # This searches the trends of the last 24 hours. More broad than realtime
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

    print("Number of Headlines: ", len(keywords))
    return keywords

def getArticles(keywords, realTime):
    linkDatabase = pd.DataFrame()
    linkDatabase['Headline'] = keywords
    linkHolder = []
    for i in keywords:
        # searches english language publications in America over the past two days
        google_news = GNews(language='en', country='US', period='2d')#, proxy=proxy)
        news = google_news.get_news(i)

        links = []
        for j in news:
            links.append(finalLink(j['url']))

        linkHolder.append(links)

    linkDatabase['Links'] = linkHolder

    if realTime:
        fileName = 'RealTime_HeadlinesAndLinks.csv'

    else:
        fileName = '24H_HeadlinesAndLinks.csv'

    linkDatabase.to_csv(fileName, index=False)
    return fileName
