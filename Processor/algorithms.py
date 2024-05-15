import pandas as pd
from nltk.tokenize import RegexpTokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
import basic


def bag_of_words(documents: list[str]) -> pd.DataFrame:
    bow = {}
    for i, d in enumerate(documents):
        words = basic.tokenize(basic.preprocess(d))
        for key in words:
            bow[key] = bow.get(key, [0] * (len(documents) + 1))
            bow[key][i] += 1
            bow[key][len(documents)] += 1
    columns = ['doc' + str(i + 1) for i in range(len(documents))]
    columns.append('total')
    bow_df = pd.DataFrame.from_dict(bow, orient='index', columns=columns)
    return bow_df

def lsa(documents: list[str]) -> pd.DataFrame:
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
    return pd.DataFrame(lsa_out)

def tfidf(documents: list[str]) -> {}:
    tokenizer = RegexpTokenizer(r'\w+')
    tfidf_vectorizer = TfidfVectorizer(lowercase=True,
                                       stop_words='english',
                                       ngram_range=(1, 1),
                                       tokenizer=tokenizer.tokenize)
    tfidf_vector = tfidf_vectorizer.fit_transform(documents)
    text_titles = ["doc" + str(i + 1) for i in range(len(documents))]
    tfidf_df = pd.DataFrame(tfidf_vector.toarray(), index=text_titles,
                            columns=tfidf_vectorizer.get_feature_names_out())
    # tfidf_df.loc['00_Document Frequency'] = (tfidf_df > 0).sum()
    tfidf_df.stack().reset_index()
    tfidf_df = tfidf_df.stack().reset_index()
    tfidf_df = tfidf_df.rename(columns={0: 'tfidf', 'level_0': 'document', 'level_1': 'term', 'level_2': 'term'})
    # top_tfidf = tfidf_df.sort_values(by=['document', 'tfidf'], ascending=[True, False]).groupby(['document']).head(10)
    return tfidf_df

def all_algorithms(doc_list: list[str], display: bool = False, save_csv: bool = False) -> dict[str:pd.DataFrame]:
    bow_out = bag_of_words(doc_list)
    lsa_out = lsa(doc_list)
    tfidf_out = tfidf(doc_list)

    if display:
        print("\nBag of Words algorithm:\n\n", bow_out)
        print("\n\nLatent Semantic Indexing/Analysis algorithm:\n\n", lsa_out)
        print("\n\nTerm Frequency-Inverse Document Frequency algorithm:\n\n", tfidf_out)
    if save_csv:
        bow_out.to_csv("../Data/BoW_output.csv")
        lsa_out.to_csv("../Data/LSA_output.csv")
        tfidf_out.to_csv("../Data/TF-IDF_output.csv")
    return {'BoW': bow_out, 'LSA': lsa_out, 'TF-IDF': tfidf_out}
