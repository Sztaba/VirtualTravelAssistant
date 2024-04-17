import basic

sentence = "John likes to watch movies. Mary likes movies too."

def bag_of_words(sentence) -> None:
    words = basic.preprocessKinds(sentence)
    bow = {}
    for key in words:
        bow[key] = words.count(key)

bag_of_words(sentence)
