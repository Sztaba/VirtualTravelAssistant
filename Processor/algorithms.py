import basic
import pandas as pd


def bag_of_words(documents: []) -> {}:
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


doc_contents = []
file_names = ["doc1.txt", "doc2.txt", "doc3.txt"]

for file_name in file_names:
    with open("../Data/" + file_name, "r") as file:
        doc_contents.append(file.read())

print(bag_of_words(doc_contents))
