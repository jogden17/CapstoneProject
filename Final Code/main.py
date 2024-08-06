# Written by Jack Ogden, last updated 2024.08.05

import headlineScraper
import articleScraper
import condenser
import time

startTime = time.time()
lastTime = startTime

topics = ["WORLD", "NATION", "BUSINESS", "TECHNOLOGY", "ENTERTAINMENT", "SPORTS", "SCIENCE", "HEALTH"]
searchPeriod = '2d'
headlinesPerTopic = 15
maxArticles = 25
minArticles = 5
sumLen = 110

# Web Scraping
headlines = headlineScraper.getHeadlines(topics, headlinesPerTopic, searchPeriod)
print("Headlines Scraped, took {} seconds".format(time.time() - lastTime))
lastTime = time.time()
fileNames = headlineScraper.getArticles(topics, headlines, searchPeriod)
print("Article Scraped, took {} seconds".format(time.time() - lastTime))

lastTime = time.time()
databaseNames = articleScraper.createDatabase(fileNames, topics)
print("Database Created, took {} seconds".format(time.time() - lastTime))

print("Scraping complete, took {} seconds".format(time.time() - startTime))

#databaseNames = ['./ArticleBody/WORLD_ArticleBody.csv', './ArticleBody/NATION_ArticleBody.csv', './ArticleBody/BUSINESS_ArticleBody.csv', './ArticleBody/TECHNOLOGY_ArticleBody.csv', './ArticleBody/ENTERTAINMENT_ArticleBody.csv', './ArticleBody/SPORTS_ArticleBody.csv', './ArticleBody/SCIENCE_ArticleBody.csv', './ArticleBody/HEALTH_ArticleBody.csv']

# Condensation
lastTime = time.time()
#summaries = condenser.genSummaries(databaseNames, topics, maxArticles, sumLen, minArticles) # gen summaries locally
summaries = condenser.genSummariesExternal(databaseNames, topics, maxArticles, sumLen, minArticles) # gen summary externally
print("Condensation complete, took {} seconds".format(time.time() - lastTime))
