from cgi import test
from pydoc import doc
from turtle import title
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

from sqlalchemy import over
filterwarnings('ignore')

newsapi = NewsApiClient(api_key='95b1fb3ce561467d9ffff81d954940a6')
newsapiCounter = 0

class Object(object):
    pass
class Quelle(object):
    id: str
    name: str
class Artikel(object):
    author: str
    title: str
    description: str
    released: str
    url: str
    image: str
    source: Quelle


app = FastAPI()


@app.get("/")
async def root():
    return "Hello NewsQuicky"


@app.get("/top-headlines/")
async def getTopHeadlines():
    global newsapiCounter
    newsapiCounter += 1
    changeAPIToken()
    top_headlines = newsapi.get_top_headlines(language='en')
    filteredResponse = filterResponse(top_headlines)
    alogrithmResponse = lda(top_headlines)
    return alogrithmResponse, filteredResponse

@app.get("/top-headlines/{country}")
async def getTopHeadlinesOfCountry(country: str):
    global newsapiCounter
    newsapiCounter += 1
    changeAPIToken()
    top_headlines_country = newsapi.get_top_headlines(country=country, language='en')
    filteredResponse = filterResponse(top_headlines_country)
    alogrithmResponse = lda(top_headlines_country)
    return alogrithmResponse, filteredResponse 

@app.get("/top-headlines/{category}")
async def getTopHeadlinesOfCategory(category: str):
    global newsapiCounter
    newsapiCounter += 1
    changeAPIToken()
    top_headlines_category = newsapi.get_top_headlines(category=category, language='en')
    filteredResponse = filterResponse(top_headlines_category)
    alogrithmResponse = lda(top_headlines_category)
    return alogrithmResponse, filteredResponse                                                

@app.get("/everything/{fromDate}/{toDate}")
async def getEverything(fromDate: str, toDate: str):
    global newsapiCounter
    newsapiCounter += 1
    changeAPIToken()
    everything_from_to = newsapi.get_everything(language='en', from_param=fromDate, to=toDate)
    filteredResponse = filterResponse(everything_from_to)
    alogrithmResponse = lda(everything_from_to)
    return alogrithmResponse, filteredResponse

@app.get("/testing")
async def testing():
    global newsapiCounter
    newsapiCounter += 1
    return changeAPIToken()


def lda(response):
    overallFinalArray = []
    allTitlesInArray = getTitleFromArticles(response)

    for yeet in allTitlesInArray:
        corpus = [yeet]

        clean_corpus = [clean(doc).split() for doc in corpus]

        dict_ = corpora.Dictionary(clean_corpus)

        doc_term_matrix = [dict_.doc2bow(i) for i in clean_corpus]

        Lda = gensim.models.ldamodel.LdaModel

        ldamodel = Lda(doc_term_matrix, num_topics=1, id2word = dict_, passes=1, random_state=0, eval_every=None)

        topic = ldamodel.show_topics(formatted=True, num_topics=1, num_words=5)[0][1]
        txt = topic.split(' + ')
        for i in txt:
            test = i.split('*')
            adji = test[1]
            result = re.search('\"(.*)\"', adji)
            if any(x.value == result.group(1) for x in overallFinalArray):
                verarschig = [x.value for x in overallFinalArray].index(result.group(1))
                overallFinalArray[verarschig].times = overallFinalArray[verarschig].times + 1
            else:
                b = Object()
                b.times = 1
                b.value = result.group(1)
                overallFinalArray.append(b)

    return overallFinalArray

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

def getTitleFromArticles(response):
    titleArray = []
    for x in response['articles']:
        titleArray.append(x['title'])
    return titleArray

def filterResponse(response):
    newsArticles = []
    for x in response['articles']:
        a = Artikel()
        b = Quelle()
        if x['author'] == None:
            a.author = "No Author"
        else:
            a.author = x['author']

        a.title = x['title']
        a.description = x['description']
        a.released = x['publishedAt']
        a.url = x['url']
        a.image = x['urlToImage']
        b.id = x['source']['id']
        b.name = x['source']['name']
        a.source = b

        newsArticles.append(a)
    return newsArticles

def changeAPIToken():
    global newsapi
    global newsapiCounter
    if newsapiCounter == 100:
        newsapi = NewsApiClient(api_key='f1d4b9b6452540569ad465d34528a183')
    elif newsapiCounter == 200:
        newsapi = NewsApiClient(api_key='7697e19289784c4b90a6154d1e72714d')
    elif newsapiCounter == 300:
        newsapi = NewsApiClient(api_key='8ab302232d804bc38a9d7b5127b8287f')
    else:
        None