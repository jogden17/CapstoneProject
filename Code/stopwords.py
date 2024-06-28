import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Downloading stopwords
nltk.download('stopwords')
nltk.download('punkt')


# Function for removing stopwords
def remove_stopwords(text):
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(text)
    filtered_text = []
    for word in word_tokens:
        if word.lower() not in stop_words:
            filtered_text.append(word)
    return ' '.join(filtered_text)


