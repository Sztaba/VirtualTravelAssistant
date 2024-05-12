from FormDataAgregator import FormDataAgregator, FormCSV
url ="https://docs.google.com/spreadsheets/d/1PqjRuyqeDIWK5SMlIMgkXdOzOWDCPiII3YPLeGwH-WI/export?format=csv"


form_agg = FormDataAgregator(FormCSV(url))
rand = form_agg.get_random_single_row()
print(rand)
ex = rand['places']
ex = ex[list(ex.keys())[0]]
ex = set(ex.split(', '))

with open("../Data/doc1.txt", 'w') as f:
    for e in ex:
        f.write(e + ' ')

