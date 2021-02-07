# -*- coding: utf-8 -*-
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

'''
Websites que utilizei de base:

Base do algoritmo: https://datascienceplus.com/evaluation-of-topic-modeling-topic-coherence/


Não utilizei muito:
http://www.machinelearningplus.com/nlp/topic-modeling-gensim-python/#17howtofindtheoptimalnumberoftopicsforlda
https://rstudio-pubs-static.s3.amazonaws.com/79360_850b2a69980c4488b1db95987a24867a.html

Stopwords: https://pypi.org/project/stop-words/#basic-usage

calculo da distancia: http://dataconomy.com/2015/04/implementing-the-five-most-popular-similarity-measures-in-python/

Levenshtein: https://pypi.org/project/python-Levenshtein/#documentation

word 2 vec:
http://kavita-ganesan.com/gensim-word2vec-tutorial-starter-code/#.W2jDgNhKiqQ
http://methodmatters.blogspot.com/2017/11/using-word2vec-to-analyze-word.html
https://medium.com/swlh/playing-with-word-vectors-308ab2faa519


Como recuperar vinculos entre documentos, topicos e termos:
https://github.com/RaRe-Technologies/gensim/blob/develop/docs/notebooks/topic_methods.ipynb
'''


# Import required packages
import numpy as np
import logging
import pyLDAvis.gensim
import json
import warnings
warnings.filterwarnings('ignore')  # To ignore all warnings that arise here to enhance clarity

from gensim.models.coherencemodel import CoherenceModel
from gensim.models.ldamodel import LdaModel
from gensim.corpora.dictionary import Dictionary
from numpy import array
import pandas as pd


# from nltk.stem.wordnet import WordNetLemmatizer
# from nltk.tokenize import RegexpTokenizer

# import nltk
# nltk.download('wordnet')

bp = Blueprint('lda_gensim', __name__, url_prefix='/lda-gensim')

from app.db import get_db

def clear_database():
    db = get_db()
    db.execute('DELETE FROM docs;')
    db.execute('DELETE FROM terms;')
    db.execute('DELETE FROM docs_terms;')
    db.execute('DELETE FROM topics;')
    db.execute('DELETE FROM sqlite_sequence;')
    db.commit()
    

def insert_docs(df):
    db = get_db()
    keys = df.index.values
    index_key = 0
    for content in df.content.values:
        db.execute('INSERT INTO docs (id, user_code, experience) VALUES (?,?,?)',(index_key,int(keys[index_key]),content, ))
        db.commit()
        index_key = index_key + 1


def docs_preprocessor(docs):
    tokenizer = RegexpTokenizer(r'\w+')
    for idx in range(len(docs)):
        docs[idx] = docs[idx].lower()  # Convert to lowercase.
        docs[idx] = tokenizer.tokenize(docs[idx])  # Split into words.

    # Remove numbers, but not words that contain numbers.
    docs = [[token for token in doc if not token.isdigit()] for doc in docs]
    
    # Remove words that are only one character.
    docs = [[token for token in doc if len(token) > 3] for doc in docs]
    
    # remove stop words
    stop_words_br = ['a','agora','ainda','alguém','algum','alguma','algumas','alguns','ampla','amplas','amplo','amplos','ante','antes','ao','aos','após','aquela','aquelas','aquele','aqueles','aquilo','as','até','através','cada','coisa','coisas','com','como','contra','contudo','da','daquele','daqueles','das','de','dela','delas','dele','deles','depois','dessa','dessas','desse','desses','desta','destas','deste','destes','deve','devem','devendo','dever','deverá','deverão','deveria','deveriam','devia','deviam','disse','disso','disto','dito','diz','dizem','do','dos','e','é','ela','elas','ele','eles','em','enquanto','entre','era','essa','essas','esse','esses','esta','está','estamos','estão','estas','estava','estavam','estávamos','este','estes','estou','eu','fazendo','fazer','feita','feitas','feito','feitos','foi','for','foram','fosse','fossem','grande','grandes','há','isso','isto','já','la','lá','lhe','lhes','lo','mas','me','mesma','mesmas','mesmo','mesmos','meu','meus','minha','minhas','muita','muitas','muito','muitos','na','não','nas','nem','nenhum','nessa','nessas','nesta','nestas','ninguém','no','nos','nós','nossa','nossas','nosso','nossos','num','numa','nunca','o','os','ou','outra','outras','outro','outros','para','pela','pelas','pelo','pelos','pequena','pequenas','pequeno','pequenos','per','perante','pode','pude','podendo','poder','poderia','poderiam','podia','podiam','pois','por','porém','porque','posso','pouca','poucas','pouco','poucos','primeiro','primeiros','própria','próprias','próprio','próprios','quais','qual','quando','quanto','quantos','que','quem','são','se','seja','sejam','sem','sempre','sendo','será','serão','seu','seus','si','sido','só','sob','sobre','sua','suas','talvez','também','tampouco','te','tem','tendo','tenha','ter','teu','teus','ti','tido','tinha','tinham','toda','todas','todavia','todo','todos','tu','tua','tuas','tudo','última','últimas','último','últimos','um','uma','umas','uns','vendo','ver','vez','vindo','vir','vos','vós','mais','à','ser','você','às','têm','havia','tenho','vocês','estive','esteve','estivemos','estiveram','estivera','estivéramos','esteja','estejamos','estejam','estivesse','estivéssemos','estivessem','estiver','estivermos','estiverem','hei','havemos','hão','houve','houvemos','houveram','houvera','houvéramos','haja','hajamos','hajam','houvesse','houvéssemos','houvessem','houver','houvermos','houverem','houverei','houverá','houveremos','houverão','houveria','houveríamos','houveriam','sou','somos','éramos','eram','fui','fomos','fora','fôramos','sejamos','fôssemos','formos','forem','serei','seremos','seria','seríamos','seriam','temos','tém','tínhamos','tive','teve','tivemos','tiveram','tivera','tivéramos','tenhamos','tenham','tivesse','tivéssemos','tivessem','tiver','tivermos','tiverem','terei','terá','teremos','terão','teria','teríamos','teriam','acerca','adeus','alem','algmas','algo','ali','além','ambas','ambos','ano','anos','aonde','apenas','apoio','apontar','apos','aqui','assim','atrás','aí','baixo','bastante','bem','boa','boas','bom','bons','breve','caminho','catorze','cedo','cento','certamente','certeza','cima','cinco','comprido','conhecido','conselho','corrente','cuja','cujas','cujo','cujos','custa','cá','daquela','daquelas','dar','debaixo','demais','dentro','desde','desligado','dez','dezanove','dezasseis','dezassete','dezoito','dia','diante','direita','dispoe','dispoem','diversa','diversas','diversos','dizer','dois','doze','duas','durante','dá','dão','dúvida','embora','entao','então','estado','estar','estará','estiveste','estivestes','estás','exemplo','falta','fará','favor','faz','fazeis','fazem','fazemos','fazes','fazia','faço','fez','fim','final','forma','foste','fostes','geral','grupo','ha','hoje','hora','horas','iniciar','inicio','ir','irá','ista','iste','lado','ligado','local','logo','longe','lugar','maior','maioria','maiorias','mal','mediante','meio','menor','menos','meses','mil','momento','máximo','mês','nada','nao','naquela','naquelas','naquele','naqueles','nenhuma','nesse','nesses','neste','nestes','noite','nome','nova','novas','nove','novo','novos','numas','nuns','nível','número','obra','obrigada','obrigado','oitava','oitavo','oito','onde','ontem','onze','parece','parte','partir','paucas','pegar','perto','pessoas','podem','poderá','ponto','pontos','porquê','portanto','posição','possivelmente','possível','povo','primeira','primeiras','promeiro','propios','proprio','próxima','próximas','próximo','próximos','puderam','pôde','põe','põem','qualquer','quarta','quarto','quatro','quer','quereis','querem','queremas','queres','quero','questão','quieto','quinta','quinto','quinze','quáis','quê','relação','sabe','sabem','saber','segunda','segundo','sei','seis','sete','sexta','sexto','sim','sistema','sois','somente','sétima','sétimo','tal','tambem','tanta','tantas','tanto','tarde','tempo','tendes','tens','tentar','tentaram','tente','tentei','terceira','terceiro','tipo','tiveste','tivestes','trabalhar','trabalho','treze','três','tão','usa','usar','vai','vais','valor','veja','vem','vens','verdade','verdadeiro','vezes','viagem','vinte','vossa','vossas','vosso','vossos','vários','vão','vêm','zero','área','és']
    # http://snowball.tartarus.org/algorithms/portuguese/stop.txt
    # https://virtuati.com.br/cliente/knowledgebase/25/Lista-de-StopWords.html
    # https://github.com/stopwords-iso/stopwords-pt/blob/master/stopwords-pt.txt
    docs = [[word for word in doc if word not in stop_words_br ] for doc in docs]

    return docs


# inserindo os termos no banco de dados
def insert_terms(dictionary):
    db = get_db()
    for d in dictionary.items():
        db.execute('INSERT INTO terms (id, term) VALUES (?,?)',(d[0],d[1], ))
        db.commit()

# inserindo o vinculo entre documento e termo no banco de dados
def insert_doc_term(corpus):
    db = get_db()
    for doc_id, list_words in enumerate(corpus):
        for word in list_words:
            db.execute('INSERT INTO docs_terms (docs_id, terms_id, quantity) VALUES (?,?,?)',(doc_id,word[0],word[1] ))
            db.commit()

# inserindo os tópicos
def insert_topics(num_topics):
    db = get_db()
    for i in range(num_topics):
        db.execute('INSERT INTO topics (id, topic) VALUES (?,?)',(i,i))
        db.commit()

# inserindo a relação entre tópicos e termos
def insert_topics_terms(lda_model, number_topics, number_words):
    db = get_db()
    for topic_id in range(number_topics):
        list_words = lda_model.get_topic_terms(topicid=topic_id,topn=number_words)
        for term_id, percentage in list_words:
            db.execute('INSERT INTO topics_terms (topics_id, terms_id, percent) VALUES(?,?,?)',(topic_id,int(term_id), float(percentage)))
            db.commit()

def insert_docs_topics(model,corpus):
    db = get_db()
    for doc_id in range(len(corpus)):
        doc_topics, word_topics, phi_values = model.get_document_topics(corpus[doc_id], per_word_topics=True)
        for topic_id, percent in doc_topics:
            db.execute('INSERT INTO docs_topics (docs_id,topics_id,percent) VALUES (?,?,?)',(doc_id, int(topic_id), float(percent) ))
            db.commit()


@bp.route('/gensim')
def lda_gensim():

    print('Limpando o banco de dados')
    clear_database()

    # importando os dados para inserir no banco
    df = pd.read_json('app/resume.json')
    # inserindo os documentos no banco de dados
    print('Inserindo os documentos no banco')
    insert_docs(df)

    data = df.content.values.tolist()
    data = array(df.content)
    
    # executando funções de pré processamento
    docs = docs_preprocessor(data)

    dictionary = Dictionary(docs)
    # inserindo os termos no banco de dados
    print('Inserindo os termos no banco')
    insert_terms(dictionary)

    # criando uma matrix de frequencia de termo em documento
    corpus = [dictionary.doc2bow(doc) for doc in docs]
    # inserindo no banco de dados a matrix tf-idf (termo - documento)
    print('Inserindo o vinculo entre documento e termo')
    insert_doc_term(corpus)


    # Set parameters.
    num_topics = 24
    chunksize = 500 
    passes = 20 
    iterations = 400
    eval_every = 1 
    

    # Make a index to word dictionary.
    temp = dictionary[0]  # only to "load" the dictionary.
    id2word = dictionary.id2token

    print('Rodando o LDA')
    lda_model = LdaModel(corpus=corpus, id2word=id2word, chunksize=chunksize, 
                       alpha='auto', eta='auto', 
                       iterations=iterations, num_topics=num_topics, 
                       passes=passes, eval_every=eval_every, 
                       )



    print('Inserindo os tópicos no banco de dados')
    insert_topics(num_topics)
    print('Inserindo o vinculo entre topicos e termos')
    insert_topics_terms(lda_model,num_topics,20)
    print('Inserindo os vinculos entre documento e tópicos')
    insert_docs_topics(lda_model,corpus)

    return render_template('/lda-gensim/result.html')