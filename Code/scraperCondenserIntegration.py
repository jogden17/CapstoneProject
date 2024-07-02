import pandas as pd
import condenser
import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"

import time

startTime = time.time()
lastTime = startTime

fileName = "24H_ArticleDatabase.csv"
df = pd.read_csv(fileName)
toc = condenser.tableOfContents(df)

maxArticles = 20
sumLen = 100
summaries = []
for i in toc['Index']:
    text = condenser.createFile(df, i, maxArticles)
    print("File Created, took {} seconds".format(time.time() - lastTime))
    lastTime = time.time()

    #firstSummary = condenser.summarize(text, sumLen/2)
    firstSummary = condenser.firstSummary(text, 150)

    print("First Summary, took {} seconds".format(time.time() - lastTime))
    lastTime = time.time()

    #secondSummary = condenser.firstSummary(next, 225)
    secondSummary = condenser.firstSummary(firstSummary, 200)

    print(secondSummary)
    print("Second Summary, took {} seconds".format(time.time() - lastTime))
    lastTime = time.time()

    finalSummary = condenser.summarize(secondSummary, sumLen)
    print(finalSummary)
    print("Final Summary, took {} seconds".format(time.time() - lastTime))
    summaries.append(finalSummary)

pd.DataFrame(summaries).to_csv('summaries.csv', index=False)
