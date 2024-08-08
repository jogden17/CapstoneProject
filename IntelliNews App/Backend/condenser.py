# Written by Jack Ogden, last updated 2024.08.05

import pandas as pd
import time
import torch
from transformers import pipeline
import math
import gc
import externalModel

#import os
#os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Gets the indices of the start of each headline
def tableOfContents(df):
    headlines = []
    index = []
    i = 0
    curHeadline = df["Headlines"][i]
    index.append(i)
    headlines.append(curHeadline)
    while i < len(df["Headlines"]):
        if curHeadline == df["Headlines"][i]:
            i += 1

        else:
            curHeadline = df["Headlines"][i]
            index.append(i)
            headlines.append(curHeadline)
            i += 1

    toc = pd.DataFrame()
    toc["Headlines"] = headlines
    toc["Index"] = index
    return toc

# combines the text of the articles into a single string
def createFile(df, index, numArticles):
    headline = df['Headlines'][index]
    links = []
    text = ""
    j = 0
    while index < len(df['Headlines']) and headline == df['Headlines'][index] and j < numArticles:
        text = text + str(removeAds(df['ArticleBodyText'][index]))
        links.append(df['Links'][index])
        index += 1
        j += 1

    return headline, text, links


# removes ads and other unwanted information from the article body text
def removeAds(text):
    sentence = str(text).split('.')
    final = []
    for i in sentence:
        if "vpv" not in str(i).lower() and "stream" not in str(i).lower() and "advertisement" not in str(i).lower() and "click here" not in str(i).lower():
            final.append(i)

    return str(' '.join(final))


# splits input text into chunks which fit inside the bart-large-cnn model context window
def chunk_by_chars(text, chunk_size=3500):
    textLength = len(text)
    numChunks = math.ceil(textLength/chunk_size)
    size = int(textLength/numChunks) + 21
    return [text[i:i + size] for i in range(0, len(text), size-20)]


# automates the summarization process
def genSummaries(fileNames, topics, maxArticles, sumLen, minArticles):
    files = []
    q = 0
    for fileName in fileNames:
        topic = topics[q]
        print(topic)
        q += 1
        df = pd.read_csv(fileName)
        toc = tableOfContents(df)
        lastTime = time.time()

        summaries = []
        headlineList = []
        linksList = []
        for i in toc['Index']:
            headline, text, links = createFile(df, i, maxArticles)
            if len(links) >= minArticles:
                headlineList.append(headline)
                linksList.append(links)
                print("File Created, took {} seconds".format(time.time() - lastTime))
                lastTime = time.time()

                firstSummary = firstSummarize(text, sumLen, 250)

                print(firstSummary)
                print("First Summary, took {} seconds".format(time.time() - lastTime))
                lastTime = time.time()
                print("Word Count: ", wordCount(firstSummary))
                summaries.append(firstSummary)

                gc.collect()
                torch.mps.empty_cache()

        df = pd.DataFrame()
        df['Headline'] = headlineList
        df['Summary'] = summaries
        df['Links'] = linksList

        file = '../FrontEnd/intellinews-client/public/CSVs/'+topic+'_Final.csv'
        files.append(file)
        df.to_csv(file, index=False)

    return files


# first stage of summarization process, a smaller model which produces lower quality results but is much more efficient
def firstSummarize(text, sumLen, stopLen):
    # model found here: https://huggingface.co/facebook/bart-large-cnn
    pipe = pipeline("summarization", model="facebook/bart-large-cnn", device='mps')

    summary = ""
    chunks = chunk_by_chars(text, 3500)
    print("Num Chunks: " + str(len(chunks)))
    if stopLen < 350:
        if len(chunks) == 1: sumLen = int(sumLen*1.5)

    else:
        if len(chunks) < 4: sumLen = int(sumLen * 1.5)

    for chunk in chunks:
        out = pipe(chunk, do_sample=False, min_length=sumLen, max_length=sumLen*2)
        summary += out[0]['summary_text']

    gc.collect()
    torch.mps.empty_cache()

    if wordCount(summary) > stopLen:
        summary = firstSummarize(summary, sumLen, stopLen)

    return summary


# second stage of summarization process which produces a higher quality text output
def finalSummarize(text):
    # model found here: https://huggingface.co/openai-community/gpt2-xl
    pipe = pipeline("text-generation", model="openai-community/gpt2-xl", device='mps')
    #pipe = pipeline("text-generation", model="Granther/Gemma-2-9B-Instruct-4Bit-GPTQ", trust_remote_code=True, device='mps')

    prompt = "In around 180 words, summarize the following text start by framing the context of the story, and ensure the removal of all political bias and repeating information, " + text

    generation_args = {
        "max_new_tokens": 500,
        "return_full_text": False,
        "do_sample": False,
        "repetition_penalty": 1.5,
    }

    out = pipe(prompt, **generation_args)
    final = out[0]["generated_text"]

    return final


def wordCount(text):
    return len(text.split())


# corrects the grammar of the summary
def correctSummaryGrammar(summary):
    sentences = summary.split(".")
    out = []
    for sentence in sentences:
        out.append(correctGrammar(sentence))

    output = " ".join(out)
    return output


# corrects minor mistakes made by the summarization process
def correctGrammar(text):
    # model can be found here: https://huggingface.co/vennify/t5-base-grammar-correction
    pipe = pipeline("text2text-generation", model="vennify/t5-base-grammar-correction", device='mps')
    out = pipe("grammar: " + text, max_length=150)
    result = out[0]["generated_text"]

    gc.collect()
    torch.mps.empty_cache()

    return result


# generates a headline for the summarized articles
def makeTitle(text):
    # model found here: https://huggingface.co/facebook/bart-large-cnn
    pipe = pipeline("summarization", model="facebook/bart-large-cnn", device='mps')

    out = pipe(text, do_sample=False, min_length=5, max_length=20)
    summary = out[0]['summary_text']

    gc.collect()
    torch.mps.empty_cache()

    summary = correctGrammar(summary)

    if summary[len(summary) - 1] == " ":
        if summary[len(summary) - 2] == ".":
            summary = summary[:len(summary) - 2]

        else:
            summary = summary[:len(summary) - 1]

    return summary


# generates summary using external model
def genSummariesExternal(fileNames, topics, maxArticles, sumLen, minArticles):
    files = []
    q = 0
    for fileName in fileNames:
        topic = topics[q]
        print(topic)
        q += 1
        df = pd.read_csv(fileName)
        toc = tableOfContents(df)
        lastTime = time.time()

        summaries = []
        headlineList = []
        linksList = []
        for i in toc['Index']:
            headline, text, links = createFile(df, i, maxArticles)
            if len(links) >= minArticles:
                headlineList.append(headline)
                linksList.append(links)
                print("File Created, took {} seconds".format(time.time() - lastTime))
                lastTime = time.time()

                firstSummary = firstSummarize(text, sumLen, 600)

                print(firstSummary)
                print("First Summary, took {} seconds".format(time.time() - lastTime))
                lastTime = time.time()
                print("Word Count: ", wordCount(firstSummary))

                gc.collect()
                torch.mps.empty_cache()

                finalSummary = externalModel.textGen(firstSummary)
                print("Final Summary, took {} seconds".format(time.time() - lastTime))
                lastTime = time.time()
                finalSummary = removeStart(finalSummary)
                summaries.append(finalSummary)

        df = pd.DataFrame()
        df['Headline'] = headlineList
        df['Summary'] = summaries
        df['Links'] = linksList

        file = '../FrontEnd/intellinews-client/public/CSVs/'+topic+'_Final.csv'
        files.append(file)
        df.to_csv(file, index=False)

    return files

# removes unwanted text from the start of the external model summary
def removeStart(text):
    index = text.find("newspaper article:")

    if index != -1:
        print("removed Start")
        return text[index+18:]
    else:
        return text
