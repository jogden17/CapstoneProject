# Written by Jack Ogden, last updated 2024.08.02

import pandas as pd
# gnews found here https://github.com/ranahaani/GNews
from gnews import GNews
from sentence_transformers import SentenceTransformer
import condenser
import googleNewsDecoder
import time

# removes similar articles
def removeRepeats(headlines):
    # model found here: https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    embeddings = model.encode(headlines)
    results = model.similarity(embeddings, embeddings)
    indices = []
    for i in range(len(results)):
        j = i
        while j < len(results[i]):
            if (results[i][j] > 0.5) and results[i][j] < .99:
                indices.append(j)
            j += 1

    holder = headlines.copy()
    for i in indices:
        if headlines[i] in holder:
            holder.remove(headlines[i])

    print(holder)
    return holder


# aggregates the top headlines from google news
def getHeadlines(topics, headlinesPerTopic, searchPeriod):
    google_news = GNews(language='en', country='US', period=searchPeriod)

    headlinesByTopic = []
    for topic in topics:
        news = google_news.get_news_by_topic(topic=topic)

        # only gets the top X headlines for each topic
        if len(news) > headlinesPerTopic:
            news = news[:headlinesPerTopic]

        # Formats headline title
        headlines = []
        for i in news:
            desc = i['description']
            title = condenser.makeTitle(desc)

            headlines.append(title)

        headlines = removeRepeats(headlines)
        headlinesByTopic.append(headlines)

    return headlinesByTopic

# gets the links to articles for each headline
def getArticles(topics, headlinesByTopic, searchPeriod):
    # searches english language publications in America over the past two days
    google_news = GNews(language='en', country='US', period=searchPeriod)

    files = []
    x = 0
    while x < len(topics):
        headlines = headlinesByTopic[x]
        topic = topics[x]
        print(topic)

        # for each headline get the links to the associated articles
        headlinesList = []
        linksList = []
        for i in headlines:
            news = google_news.get_news(i)

            # makes a list of the links
            links = []
            for j in news:
                time.sleep(2)
                links.append(googleNewsDecoder.decode_google_news_url(j['url']))

            print(i, ", Num Links:", len(links))
            headlinesList.append(i)
            linksList.append(links)

        # make a dataframe
        df = pd.DataFrame()
        df['Headline'] = headlinesList
        df['Links'] = linksList

        # turn dataframe into csv named after the topic
        fileName = './Headlines_Links/'+topic+'_HeadlinesLinks.csv'
        files.append(fileName)
        df.to_csv(fileName, index=False)

        x += 1

    return files
