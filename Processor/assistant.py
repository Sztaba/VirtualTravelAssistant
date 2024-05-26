import pandas as pd

from Processor import basic

def getPoisForGivenWords(pois, words: list[str]):
    selectedPois = []
    for poi in pois:
        kinds = basic.preprocessAndTokenize(poi["kinds"])
        # print(words, kinds)
        if [i for i in words if i in kinds]:
            # print("!!!!", words, kinds)
            selectedPois.append(poi)
    return selectedPois

def getPoisForWeightedLsaPerTopic(pois, lsa: pd.DataFrame):
    final_dict = {}
    selected_pois_all_topics = []
    for c in lsa:
        selectedPois = []
        words = list(lsa[c].drop('Total TF-IDF score'))
        print(words)
        for poi in pois:
            kinds = basic.preprocessAndTokenize(poi["kinds"])
            found_words = [i for i in words if i in kinds]
            if found_words:
                print("!!!!", found_words, kinds)
                selectedPois.append(poi)
        final_dict[c] = selectedPois
    return final_dict

def getPoisForWeightedLsaAllTopics(pois, lsa: pd.DataFrame):
    selected_pois = []
    words_list = []
    for c in lsa:
        words = list(lsa[c].drop('Total TF-IDF score'))
        words_list.extend(words)
    for poi in pois:
        kinds = basic.preprocessAndTokenize(poi["kinds"])
        found_words = [i for i in words_list if i in kinds]
        if len(found_words) > 1:
            print("!!!!", found_words, kinds)
            selected_pois.append(poi)
    return selected_pois

def getPoisForTfidf(pois, tfidf: pd.DataFrame):
    filtered_tfIdf = tfidf[tfidf['tfidf'] > 0].sort_values(by="tfidf", ascending=False)
    selected_pois = []
    tfidf_sum = []
    for poi in pois:
        kinds = basic.preprocessAndTokenize(poi["kinds"])
        filtered = tfidf[(tfidf['term'].isin(kinds)) & (tfidf['tfidf'] > 0)]
        words = filtered['term'].tolist()
        if len(words) > 1:
            # print("!!!!", filtered, kinds)
            selected_pois.append({'tfidf_total':filtered['tfidf'].sum(), 'poi': poi})
    sorted_list = sorted(selected_pois, key=lambda x: x['tfidf_total'], reverse=True)
    return sorted_list

def getListOfPoisShort(pois) -> list[dict]:
    pois_list = []
    for poi in pois:
        pois_list.append({'name': poi['name'], 'kinds': poi['kinds'], 'point': poi['point']})
    return pois_list