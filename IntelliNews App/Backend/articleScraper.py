# Written by Jack Ogden, last updated 2024.07.30

import pandas as pd
# newspaper3k found here https://newspaper.readthedocs.io/en/latest/
from newspaper import Article, ArticleException

def createDatabase(fileNames, topics):
    q = 0
    files = []
    for fileName in fileNames:
        topic = topics[q]
        q += 1
        df = pd.read_csv(fileName)
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

                try:
                    article.download()
                    article.parse()
                except ArticleException:
                    print(f"Failed to download {i}")
                    failed_links.append(i)
                    continue  # skip this link and move on to the next one

                articleBody = article.text
                articleBodyText.append(articleBody)

            print("% of failed retrievals", (float(len(failed_links)) / len(links)))

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
        file = './ArticleBody/'+topic+'_ArticleBody.csv'
        files.append(file)

        dfs.to_csv(file, index=False)

    return files
