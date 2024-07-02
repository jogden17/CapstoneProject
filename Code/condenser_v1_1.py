import pandas as pd
import time
from transformers import pipeline
import nltk

# Downloading stopwords
nltk.download('stopwords')
nltk.download('punkt')
from collections import Counter  # Imports the Counter class from the collections module, used for counting the frequency of words in a text.
from nltk.corpus import stopwords  # Imports the stop words list from the NLTK corpus
# corpus is a large collection of text or speech data used for statistical analysis

from nltk.tokenize import sent_tokenize, word_tokenize  # Imports the sentence tokenizer and word tokenizer from the NLTK tokenizer module.


# Sentence tokenizer is for splitting text into sentences
# word tokenizer is for splitting sentences into words

# this function would take 2 inputs, one being the text, and the other being the summary which would contain the number of lines
def extractiveSummary(text, n):
    # Tokenize the text into individual sentences
    sentences = sent_tokenize(text)

    # Tokenize each sentence into individual words and remove stopwords
    stop_words = set(stopwords.words('english'))
    # the following line would tokenize each sentence from sentences into individual words using the word_tokenize function of nltk.tokenize module
    # Then removes any stop words and non-alphanumeric characters from the resulting list of words and converts them all to lowercase
    words = [word.lower() for word in word_tokenize(text) if word.lower() not in stop_words and word.isalnum()]

    # Compute the frequency of each word
    word_freq = Counter(words)

    # Compute the score for each sentence based on the frequency of its words
    # After this block of code is executed, sentence_scores will contain the scores of each sentence in the given text,
    # where each score is a sum of the frequency counts of its constituent words

    # empty dictionary to store the scores for each sentence
    sentence_scores = {}

    for sentence in sentences:
        sentence_words = [word.lower() for word in word_tokenize(sentence) if
                          word.lower() not in stop_words and word.isalnum()]
        sentence_score = sum([word_freq[word] for word in sentence_words])
        if len(sentence_words) < 25:
            sentence_scores[sentence] = sentence_score

    # checks if the length of the sentence_words list is less than 20 (parameter can be adjusted based on the desired length of summary sentences)
    # If condition -> true, score of the current sentence is added to the sentence_scores dictionary with the sentence itself as the key
    # This is to filter out very short sentences that may not provide meaningful information for summary generation

    # Select the top n sentences with the highest scores
    summary_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:n]
    summary = ' '.join(summary_sentences)

    return summary

from sentence_transformers import SentenceTransformer
import numpy as np

def euclidean_distance(vec1, vec2):
    # Ensure the vectors are numpy arrays
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)

    # Check if the vectors have the same dimensions
    if vec1.shape != vec2.shape:
        raise ValueError("Vectors must have the same dimensions.")

    # Calculate the Euclidean distance
    distance = np.linalg.norm(vec1 - vec2)
    return distance

def removeRelatedSentences(text, simThresh):
    # break into 240 word sections and
    sentences = text.split('.')

    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    embeddings = model.encode(sentences)

    removals = []
    for i in embeddings:
        j = 0
        closeness = []
        remove = []
        while j < len(embeddings):
            dis = euclidean_distance(i, embeddings[j])
            closeness.append(dis)
            if dis < simThresh and dis != 0.0:
                remove.append(j)
            j += 1

        removals.append(remove)

    for i in removals:
        for j in i:
            removals[j] = []


    keepSent = []
    i = 0
    while i < len(removals):
        if len(removals[i]) > 0:
            keepSent.append(sentences[i])
        i += 1

    holder = str(' '.join(keepSent))
    holder = holder.replace('\n', '')
    return str(holder)

def bookSumarizer(text):
    summarizer = pipeline("summarization", model="pszemraj/led-base-book-summary", device="mps")

    summary = summarizer(text, min_length=500, do_sample=False)[0]['summary_text']
    return summary

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
        text = text + str(df['ArticleBodyText'][index]) # + remove_stopwords(str(df['ArticleBodyText'][index])) # can replace 'Summary' with 'ArticleBodyText'
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

def firstSummary(text, sumLen):
    # Load pre-trained BART model and tokenizer
    # model found here https://huggingface.co/facebook/bart-large-cnn
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device="mps")

    lengths = []
    #text = text.replace(',', '.')
    sentences = text.split('.')
    for s in sentences:
        lengths.append(len(s.split())+5)

    df = pd.DataFrame()
    df['Sentence'] = sentences
    df['Length'] = lengths

    chunks = []
    totLen = df['Length'].sum()

    cap = totLen / ((totLen+100) / 750.0)
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
    #random.shuffle(chunks)
    for c in chunks:
        summary += summarizer(c, max_length=(sumLen+100), min_length=sumLen, do_sample=False)[0]['summary_text'] + "\n"

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
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device="mps")

    summary = summarizer(text, min_length=sumLen, do_sample=False)[0]['summary_text']
    return summary
