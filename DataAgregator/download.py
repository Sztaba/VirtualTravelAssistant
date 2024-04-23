from FormDataAgregator import FormDataAgregator, FormCSV
url ="https://docs.google.com/spreadsheets/d/1PqjRuyqeDIWK5SMlIMgkXdOzOWDCPiII3YPLeGwH-WI/export?format=csv"


form_agg = FormDataAgregator(FormCSV(url))
# print(form_agg.get_data())
print(form_agg.get_random_single_row())


