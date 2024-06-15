# using headlines and links database
import pandas as pd

df = pd.read_csv('HeadlinesAndLinks.csv')

topStory = df['Links'][2]
topStory = topStory.replace("[", "").replace("]", "")
topStory = topStory.split(", ")

links = []
for i in topStory:
    link = i.replace("'", "")
    links.append(link)

from newspaper import Article

articleBodyText = []
for i in links:
    article = Article(i)
    article.download()
    article.parse()
    articleBody = article.text
    articleBodyText.append(articleBody)

df = pd.DataFrame(links, articleBodyText)
df.to_csv('articleBodyText.csv')
