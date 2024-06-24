import pandas as pd
import time
#from transformers import BartTokenizer, BartForConditionalGeneration
from transformers import pipeline

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
    text = ""
    j = 0
    while headline == df['Headlines'][index] and j < numArticles:
        text = text + str(df['ArticleBodyText'][index]) # can replace 'Summary' with 'ArticleBodyText'
        index += 1
        j += 1

    return text

# summarizes every row in a dataframe
def summarizeAll(sumLen, df):
    summary = []
    lastTime = time.time()
    for article in df['ArticleBodyText']:
        text = str(article)
        summary.append(summarize(text, sumLen))
        print("Summary Created, took {} seconds".format(time.time() - lastTime))
        lastTime = time.time()

    return summary

# summarize a piece of text
def summarize(text, sumLen):
    """# Tokenize and summarize the input text using BART
    inputs = tokenizer.encode("summarize: " + text, return_tensors="pt", max_length=1024, truncation=True)
    summary_ids = model.generate(inputs, max_length=sumLen+100, min_length=int(sumLen/2), length_penalty=1.0, num_beams=4, early_stopping=True)

    # Decode and output the summary
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)"""

    # Load pre-trained BART model and tokenizer
    # model found here https://huggingface.co/facebook/bart-large-cnn
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

    lengths = []
    sentences = text.split('.')
    for s in sentences:
        lengths.append(len(s.split())+1)

    df = pd.DataFrame()
    df['Sentence'] = sentences
    df['Length'] = lengths

    chunks = []
    totLen = df['Length'].sum()
    cap = totLen / ((totLen+50) / 600)
    tot = 0
    chunk = ""
    for i in range(len(df)):
        tot += df['Length'][i]
        if tot >= cap:
            tot = 0
            tot += df['Length'][i]
            chunks.append(chunk)
            chunk = ""

        chunk += df['Sentence'][i]

    summary = ""
    for c in chunks:
        summary += summarizer(c, max_length=sumLen+100, min_length=int(sumLen/2), do_sample=False)[0]['summary_text'] + "\n"

    return summary
