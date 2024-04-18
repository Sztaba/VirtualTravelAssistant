import basic
import pandas as pd
from nltk.tokenize import RegexpTokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD


def bag_of_words(documents: list[str]) -> pd.DataFrame:
    bow = {}
    for i, d in enumerate(documents):
        words = basic.preprocessKinds(d)
        for key in words:
            bow[key] = bow.get(key, [0] * (len(documents) + 1))
            bow[key][i] += 1
            bow[key][len(documents)] += 1
    columns = ['doc' + str(i + 1) for i in range(len(documents))]
    columns.append('total')
    bow_df = pd.DataFrame.from_dict(bow, orient='index', columns=columns)
    return bow_df


def lsa(documents: list[str]) -> {}:
    tokenizer = RegexpTokenizer(r'\w+')
    tfidf = TfidfVectorizer(lowercase=True,
                            stop_words='english',
                            ngram_range=(1, 1),
                            tokenizer=tokenizer.tokenize)
    train_data = tfidf.fit_transform(documents)

    num_components = 5
    lsa = TruncatedSVD(n_components=num_components, n_iter=100, random_state=42)
    lsa.fit_transform(train_data)
    terms = tfidf.get_feature_names_out()
    lsa_out = {}
    for index, component in enumerate(lsa.components_):
        zipped = zip(terms, component)
        top_terms_key = sorted(zipped, key=lambda t: t[1], reverse=True)[:5]
        top_terms_list = list(dict(top_terms_key).keys())
        lsa_out["Topic " + str(index)] = top_terms_list
    return lsa_out


doc_contents = []
file_names = ["doc1.txt", "doc2.txt", "doc3.txt"]

for file_name in file_names:
    with open("../Data/" + file_name, "r") as file:
        doc_contents.append(file.read())

print("\nBag of Words algorithm:\n\n", bag_of_words(doc_contents))
print("\n\nLatent Semantic Indexing/Analysis algorithm:\n\n", pd.DataFrame(lsa(doc_contents)))
