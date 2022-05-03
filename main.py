from pydoc import doc
from fastapi import FastAPI
from newsapi import NewsApiClient

# for text preprocessing
import re
import spacy

from nltk.corpus import stopwords 
from nltk.stem.wordnet import WordNetLemmatizer
import string

# import numpy for matrix operation
import numpy as np

# Importing Gensim
import gensim
from gensim import corpora

# to suppress warnings
from warnings import filterwarnings
filterwarnings('ignore')

newsapi = NewsApiClient(api_key='95b1fb3ce561467d9ffff81d954940a6')

app = FastAPI()

@app.get("/")
async def root():
    return "Hello NewsQuicky"


@app.get("/top-headlines/")
async def getTopHeadlines():
    top_headlines = newsapi.get_top_headlines(language='en')
    return top_headlines

@app.get("/top-headlines/{country}")
async def getTopHeadlinesOfCountry(country: str):
    top_headlines_country = newsapi.get_top_headlines(country=country,
                                                    language='en')
    return top_headlines_country

@app.get("/top-headlines/{category}")
async def getTopHeadlinesOfCategory(category: str):
    top_headlines_category = newsapi.get_top_headlines(category=category,
                                                        language='en')
    return top_headlines_category

@app.get("/everything/{fromDate}/{toDate}")
async def getEverything(fromDate: str, toDate: str):
    everything_from_to = newsapi.get_everything(language='en', from_param=fromDate, to=toDate)
    return everything_from_to


@app.get("/test")
async def lda():
    d1 = 'I want to watch a movie this weekend.'
    d2 =  'I went shopping yesterday. New Zealand won the World Test Championship by beating India by eight wickets at Southampton.'
    d3 =  'I don’t watch cricket. Netflix and Amazon Prime have very good movies to watch.'
    d4 =  'Movies are a nice way to chill however, this time I would like to paint and read some good books. It’s been long!'
    d5 =  'This blueberry milkshake is so good! Try reading Dr. Joe Dispenza’s books. His work'

    corpus = [d1]
    print(corpus)

    clean_corpus = [clean(doc).split() for doc in corpus]

    dict_ = corpora.Dictionary(clean_corpus)

    doc_term_matrix = [dict_.doc2bow(i) for i in clean_corpus]

    print(dict_)


    Lda = gensim.models.ldamodel.LdaModel

    ldamodel = Lda(doc_term_matrix, num_topics=6, id2word = dict_, passes=1, random_state=0, eval_every=None)

    count = 0
    for i in ldamodel[doc_term_matrix]:
        print("doc : ",count,i)
        count += 1

    return ldamodel.print_topics(num_topics=6, num_words=5)



# One function for all the steps:
def clean(doc):
    stop = set(stopwords.words('english'))

    exclude = set(string.punctuation)

    lemma = WordNetLemmatizer()
    
    # convert text into lower case + split into words
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    
    # remove any stop words present
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)  
    
    # remove punctuations + normalize the text
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())  
    return normalized