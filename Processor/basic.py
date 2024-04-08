from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
# import nltk

# nltk.download('wordnet')
# nltk.download('punkt')

ex = "architecture,historic_architecture,interesting_places,destroyed_objects"


def preprocessKinds(str):
    str = str.replace('_', ' ').replace(',', ' ')
    words = word_tokenize(str)
    lemmatizer = WordNetLemmatizer()
    lemmatized_words = [lemmatizer.lemmatize(word) for word in words]
    return lemmatized_words


# print(preprocessKinds(ex))
