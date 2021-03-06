## packages installed
### gensim - Python library for topic modelling, document indexing and similarity retrieval with large corpora

## call data from csv and drop bad lines
import pandas as pd
import os

#data_text_full = pd.read_csv('/Users/kayeanndelasalas/Documents/Github/LDA/gigalife_reviews/reviews_reviews_com.smart.consumer.app_202003.csv', error_bad_lines=False, quoting=3) #data from kaggle
#data_text = data.drop(['publish_date'], axis=1)
#names=cols, skiprows=[0], quoting=3, quotechar='"'
data_text_full = pd.DataFrame()
path = '/Users/kayeanndelasalas/Documents/Github/LDA/gigalife_reviews/'
files = os.listdir(path)
cols = ['Package Name','App Version Code','App Version Name','Reviewer Language','Device','Review Submit Date and Time','Review Submit Millis Since Epoch','Review Last Update Date and Time','Review Last Update Millis Since Epoch','Star Rating','Review Title','Review Text','Developer Reply Date and Time','Developer Reply Millis Since Epoch','Developer Reply Text','Review Link']
for file in files:
    if not file.startswith('.'):
        try:
            a = str(path)+str(file)
            x = pd.read_csv(a, encoding = 'utf-8')
            data_text_full = data_text_full.append(x, ignore_index = True, sort = False)
        except pd.errors.EmptyDataError:
            print("Found empty file : "+str(i)+"-"+str(file))

data_good = data_text_full[data_text_full['Star Rating']>=3]
data_bad = data_text_full[data_text_full['Star Rating']<3]

data_text = data_bad[['Review Text']]
data_text.dropna(inplace=True)
data_text.reset_index(drop=True, inplace=True)
data_text = data_text[~data_text['Review Text'].astype(str).str.startswith('2020-')].reset_index(drop=True)
data_text['index'] = data_text.index
doc = data_text

##preprocess
import gensim
#from gensim.utils import simple_preprocess
#from gensim.parsing.preprocessing import STOPWORDS
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.stem.porter import *
import numpy as np
import nltk

np.random.seed(2018)
nltk.download('wordnet') #downloading nltk wordnet resource

## lemmatize - change to first person and present tense
## stem - get root word
stemmer = PorterStemmer()

def lemmatize_stemming(text):
    return stemmer.stem(WordNetLemmatizer().lemmatize(text, pos='v'))

def preprocess(text): ##check if not in stopword then lemmatize and stem
    result = []
    for token in gensim.utils.simple_preprocess(text):
        if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3:
            result.append(lemmatize_stemming(token))
    return result

## test lemmatization and stemming

# doc_sample = doc[doc['index'] == 4310].values[0][0]
# print('original document: ')
# words = []
# for word in doc_sample.split(' '):
#     words.append(word)
# print(words)
# print('\n\n tokenized and lemmatized document: ')
# print(preprocess(doc_sample))


processed_docs = doc['Review Text'].fillna('').astype(str).map(preprocess)

## create bag of words

dictionary = gensim.corpora.Dictionary(processed_docs)

##check dictionary

count = 0
  for k, v in dictionary.iteritems():
      print(k, v)
      count += 1
      if count > 10:
          break


## Filter out tokens that appear in
### less than 15 documents (absolute number) or
### more than 0.5 documents (fraction of total corpus size, not absolute number).
### after the above two steps, keep only the first 100000 most frequent tokens.

dictionary.filter_extremes(no_below=1, no_above=0.5, keep_n=10000)

## how many words and how many times those words appear for each doc

bow_corpus = [dictionary.doc2bow(x) for x in processed_docs]

#check
#bow_corpus[4310]

#bow_doc_4310 = bow_corpus[4310]
#for i in range(len(bow_doc_4310)):
#     print("Word {} (\"{}\") appears {} time.".format(bow_doc_4310[i][0],
#                                                dictionary[bow_doc_4310[i][0]],
#                                                      bow_doc_4310[i][1]))


## TFIDF
### term frequency–inverse document frequency
### numerical statistic that is intended to reflect how important a word is to a document in a collection or corpus

from gensim import corpora, models
tfidf = models.TfidfModel(bow_corpus)
corpus_tfidf = tfidf[bow_corpus]
from pprint import pprint
for x in corpus_tfidf:
    pprint(x)
    break

## Running LDA using bag of words
### Train our lda model using gensim.models.LdaMulticore

lda_model = gensim.models.LdaMulticore(bow_corpus, num_topics=4, id2word=dictionary, passes=2, workers=2)

for idx, topic in lda_model.print_topics(-1):
    print('Topic: {} \nWords: {}'.format(idx, topic))

## Running LDA using TFIDF

lda_model_tfidf = gensim.models.LdaMulticore(corpus_tfidf, num_topics=4, id2word=dictionary, passes=2, workers=4)
for idx, topic in lda_model_tfidf.print_topics(-1):
    print('Topic: {} Word: {}'.format(idx, topic))

## performance evaluation bag of words
#processed_docs[4310]

for index, score in sorted(lda_model[bow_corpus[0]], key=lambda tup: -1*tup[1]):
    print("\nScore: {}\t \nTopic: {}".format(score, lda_model.print_topic(index, 10)))

## performance evaluation tfidf

for index, score in sorted(lda_model_tfidf[bow_corpus[0]], key=lambda tup: -1*tup[1]):
    print("\nScore: {}\t \nTopic: {}".format(score, lda_model_tfidf.print_topic(index, 10)))

## testing
# unseen_document = 'How a Pentagon deal became an identity crisis for Google'
# bow_vector = dictionary.doc2bow(preprocess(unseen_document))
# for index, score in sorted(lda_model[bow_vector], key=lambda tup: -1*tup[1]):
#     print("Score: {}\t Topic: {}".format(score, lda_model.print_topic(index, 5)))
