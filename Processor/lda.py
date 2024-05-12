# %%
import nltk
import re
import string
import spacy
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel
from abc import ABC, abstractmethod
from typing import List

import warnings
warnings.filterwarnings("ignore",category=DeprecationWarning)

# %%
class TopicModel(ABC):
    @abstractmethod
    def __init__(self, data):
        pass
    
    @abstractmethod
    def preprocess(self):
        pass
    
    @abstractmethod
    def build_model(self):
        pass
    
    @abstractmethod
    def evaluate_model(self):
        pass
    
    @abstractmethod
    def get_topics(self):
        pass
    
    @abstractmethod
    def get_topic_distribution(self):
        pass



# %%
class LDA(TopicModel):
    def __init__(self, data: List[str], num_topics: int):
        self.data = data
        self.num_topics = num_topics
        self.data_sentences = None
        self.data_words = None
        self.data_words_nostops = None
        self.stop_words = None
        self.bigram_model = None
        self.trigram_model = None
        self.data_lemmatized = None
        nltk.download('stopwords')
        nltk.download('punkt')
        self.stop_words = nltk.corpus.stopwords.words('english')  
        if 'en_core_web_trf' not in spacy.util.get_installed_models():
            print("Downloading model 'en_core_web_trf'")
            spacy.cli.download("en_core_web_trf")
        self.id2word = None
        self.corpus = None
        self.lda_model = None 
    def _cleanup_text(self):
        # Convert to lowercase
        self.data = [sent.lower() for sent in self.data]
        # # Remove Emails
        self.data = [re.sub('\S*@\S*\s?', '', sent) for sent in self.data]
        # Remove new line characters
        self.data = [re.sub('\s+', ' ', sent) for sent in self.data]
        # Remove distracting single quotes
        self.data = [re.sub("\'", "", sent) for sent in self.data]
        self.data_sentences = self.data

    
    def _sent_to_words(self, sentences):
        for sentence in sentences:
            yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))  # deacc=True removes punctuations
        
    def _build_trigrams_and_bigrams(self):
        bigram = gensim.models.Phrases(self.data_words, min_count=5, threshold=100) # higher threshold fewer phrases.
        bigram_mod = gensim.models.phrases.Phraser(bigram)
        trigram = gensim.models.Phrases(bigram[self.data_words], threshold=100)  
        trigram_mod = gensim.models.phrases.Phraser(trigram)
        self.bigram_model = bigram_mod
        self.trigram_model = trigram_mod

    def _remove_stopwords(self, text):
        return [[word for word in simple_preprocess(str(doc)) if word not in self.stop_words] for doc in text]

    def _make_bigrams(self, text):
        return [self.bigram_model[doc] for doc in text]
    
    def _make_trigrams(self, text):
        return [self.trigram_model[self.bigram_model[doc]] for doc in text]

    def _lemmatization(self, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
        nlp = spacy.load('en_core_web_trf', disable=['parser', 'ner'])
        texts_out = []
        for sent in self.data_words_nostops:
            doc = nlp(" ".join(sent)) 
            texts_out.append([token.lemma_ for token in doc if token.pos_ in allowed_postags])
        return texts_out
    
    def _create_corpus(self):
        self.id2word = corpora.Dictionary(self.data_lemmatized)
        self.corpus = [self.id2word.doc2bow(text) for text in self.data_lemmatized]

    def build_model(self):
        self.lda_model = gensim.models.ldamodel.LdaModel(corpus=self.corpus,
                                           id2word=self.id2word,
                                           random_state=100,
                                           num_topics=self.num_topics,
                                           update_every=1,
                                           chunksize=100,
                                           passes=10,
                                           alpha='auto',
                                           per_word_topics=True)
        
    def evaluate_model(self):
        coherence_model_lda = CoherenceModel(model=self.lda_model, texts=self.data_lemmatized, dictionary=self.id2word, coherence='c_v')
        coherence_lda = coherence_model_lda.get_coherence()
        print('\nCoherence Score: ', coherence_lda)
    
    def get_topics(self):
        return self.lda_model.show_topics(formatted=False)
    
    def get_topic_distribution(self):
        return self.lda_model.get_document_topics(self.corpus)


    def preprocess(self):
        self._cleanup_text()
        print(self.data)
        self.data_words = list(self._sent_to_words(self.data_sentences))
        print(self.data_words)
        self.data_words_nostops = self._remove_stopwords(self.data_words)
        print(self.data_words_nostops)
        self._build_trigrams_and_bigrams()
        self.data_lemmatized = self._lemmatization()
        print(self.data_lemmatized)
        self._create_corpus()
        
# %%
if __file__ == "__main__":
    doc_contents = []
    file_names = ["doc1.txt", "doc2.txt", "doc3.txt"]

    for file_name in file_names:
        with open("../Data/" + file_name, "r") as file:
            doc_contents.append(file.read())
    print(doc_contents)
    lda = LDA(doc_contents, 3)

    # %%
    lda.preprocess()
    lda.build_model()
    lda.evaluate_model()

    # %%
    lda.get_topics()


