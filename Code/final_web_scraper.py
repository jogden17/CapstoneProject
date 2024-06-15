"""
# using headlines and links database
import pandas as pd

df = pd.read_csv('HeadlinesAndLinks.csv')


topStory = df['Links'][0]
topStory = topStory.replace("[", "").replace("]", "")
topStory = topStory.split(", ")

topHeadline = df['Headline'][0]

links = []
for i in topStory:
    link = i.replace("'", "")
    links.append(link)

import time
from newspaper import Article, ArticleException

articleBodyText = []
failed_links = []
for i in links:
    article = Article(i)
    for _ in range(2):  # try 2 times
        try:
            article.download()
            article.parse()
        except ArticleException:
            print(f"Download failed for {i}, retrying...")
            time.sleep(5)  # wait for 5 seconds before retrying
        else:
            break  # if download and parse are successful, exit the loop
    else:
        print(f"Failed to download {i} after 2 attempts, skipping...")
        failed_links.append(i)
        continue  # skip this link and move on to the next one
    articleBody = article.text
    articleBodyText.append(articleBody)

for j in failed_links:
    links.remove(j)

headlines = [topHeadline for i in range(len(links))]
df = pd.DataFrame(articleBodyText, links, headlines)
df.to_csv('articleBodyText.csv')
"""

import pandas as pd
import time
from newspaper import Article, ArticleException

df = pd.read_csv('HeadlinesAndLinks.csv')
dfs = pd.DataFrame()
for x in range(len(df)):
    topStory = df["Links"][x]
    topStory = topStory.replace("[", "").replace("]", "")
    topStory = topStory.split(", ")

    topHeadline = df["Headline"][x]

    links = []
    for i in topStory:
        link = i.replace("'", "")
        links.append(link)

    articleBodyText = []
    failed_links = []
    for i in links:
        article = Article(i)
        for _ in range(2):  # try 2 times
            try:
                article.download()
                article.parse()
            except ArticleException:
                print(f"Download failed for {i}, retrying...")
                time.sleep(5)  # wait for 5 seconds before retrying
            else:
                break  # if download and parse are successful, exit the loop
        else:
            print(f"Failed to download {i} after 2 attempts, skipping...")
            failed_links.append(i)
            continue  # skip this link and move on to the next one
        articleBody = article.text
        articleBodyText.append(articleBody)

    for j in failed_links:
        links.remove(j)
    headlines = [topHeadline for i in range(len(links))]

    # Create DataFrame
    df1 = pd.DataFrame({
        'Headlines': headlines,
        'Links': links,
        'ArticleBodyText': articleBodyText
    })

    dfs = pd.concat([dfs, df1], ignore_index=True)

# Save DataFrame to csv
dfs.to_csv('articleBodyText.csv')