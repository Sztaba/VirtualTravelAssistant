from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# import nltk
# nltk.download('wordnet')
# nltk.download('punkt')

ex = "architecture,historic_architecture,interesting_places,destroyed_objects"


def preprocess(text: str) -> str:
    s = text.replace('_', ' ').replace(',', ' ')
    return s


def tokenize(text: str) -> list[str]:
    words = word_tokenize(text)
    lemmatizer = WordNetLemmatizer()
    lemmatized_words = [lemmatizer.lemmatize(word) for word in words]
    return lemmatized_words

# print(preprocessKinds(ex))
