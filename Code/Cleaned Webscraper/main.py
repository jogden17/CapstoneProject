import headlineScraper
import articleScraper
import time

startTime = time.time()
lastTime = startTime

realTime = True
headlines = headlineScraper.getHeadlines(realTime)
print("Headlines Scraped, took {} seconds".format(time.time() - lastTime))
lastTime = time.time()
fileName = headlineScraper.getArticles(headlines, realTime)
print("Article Scraped, took {} seconds".format(time.time() - lastTime))

lastTime = time.time()
databaseName = articleScraper.createDatabase(fileName, realTime)
print("Database Created, took {} seconds".format(time.time() - lastTime))

print("Scraping complete, took {} seconds".format(time.time() - startTime))
