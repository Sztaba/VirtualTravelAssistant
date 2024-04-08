from Processor import basic

def getPoisForGivenWords(pois, words):
    selectedPois = []
    words = basic.preprocessKinds(words)
    for poi in pois:
        kinds = basic.preprocessKinds(poi["kinds"])
        # print(words, kinds)
        if [i for i in words if i in kinds]:
            selectedPois.append(poi)
    return selectedPois
