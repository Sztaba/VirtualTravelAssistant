from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from textblob import TextBlob
import inflect

def plural_to_singular(word):
    p = inflect.engine()
    singular_word = p.singular_noun(word)
    if singular_word:
        return singular_word
    else:
        return word

# def plural_to_singular(word):
#     singular_word = TextBlob(word).singularize()
#     return singular_word
def preprocessAndTokenize(text: str) -> list[str]:
    preproccessed = preprocess(text)
    return tokenize(preproccessed)

def preprocess(text: str) -> str:
    s = text.replace('_', ' ').replace(',', ' ')
    return s


def tokenize(text: str) -> list[str]:
    words = word_tokenize(text)
    lemmatizer = WordNetLemmatizer()
    lemmatized_words = [plural_to_singular(lemmatizer.lemmatize(word)) for word in words]
    return lemmatized_words


# ex = "architecture,historic_architecture,interesting_places,destroyed_objects"
# print(preprocessKinds(ex))
