# -*- coding: utf-8 -*-
# encoding=utf-8

import functools
import json
import os
import random



from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from app.db import get_db

bp = Blueprint('topicintrusion', __name__, url_prefix='/topic-intrusion')

# recuperando tudo sobre o documento
def get_doc(doc_id):
    db = get_db()
    return db.execute('SELECT * FROM docs WHERE id = ?', (doc_id, )).fetchone()
    

# retorna uma lista de ids de documentos de forma randomica
def get_list_random_ids_from_docs(quantity=4):
    db = get_db()
    docs = db.execute('SELECT id FROM docs').fetchall()

    list_docs_id = []
    for doc in docs:
        list_docs_id.append(doc['id'])

    random_ids = []
    for i in range(quantity):
        random_ids.append(random.choice(list_docs_id))

    return random_ids

''' retorna uma lista de tópicos vinculados ao documento
    doc_id, id do documento que deseja 
    order = DESC|ASC. 
        DESC = tópicos mais vinculados
        ASC = tópicos menos vinculados
    quantity = retorna a quantidade desejada

'''
def get_list_topics_from_docs(doc_id,order = 'DESC', quantity = 1):
    db = get_db()
    topics = db.execute(
        'SELECT topics_id FROM docs_topics '
        'WHERE docs_id = ? '
        'ORDER BY percent '+order+' '
        'LIMIT '+str(quantity),
        (doc_id, )
        ).fetchall()

    # montando um array com a lista    
    list_topics_id = []
    for topic in topics:
        list_topics_id.append(topic['topics_id'])
    
    return list_topics_id


# retorna o id de um tópico com pouca porcentagem vinculada a um documento
def get_topic_intrusion(doc_id):
    list_topics_id = get_list_topics_from_docs(doc_id=doc_id,order='ASC',quantity=5)
    return random.choice(list_topics_id)

# recuperando as palavras representativas de um tópico
def get_terms_link_topic(topic_id, order='DESC',quantity=8):
    db = get_db()
    topic_terms = db.execute(
        'SELECT * '
        'FROM topics_terms AS tt ' 
        'INNER JOIN terms AS te '
            'ON tt.terms_id = te.id '
        'WHERE tt.topics_id = ?'
        'ORDER BY tt.percent '+order+
        ' LIMIT '+str(quantity),
        (topic_id, )
    ).fetchall()

    terms = []
    for term in topic_terms:
        terms.append(term['term'].encode('ascii', 'ignore'))
    string_terms = ','.join(str(e) for e in terms)

    return string_terms

def save_topic_intrusion(validate_id,doc_id,topic_intrusion):
    db = get_db()
    topics_ids = list(topic_intrusion.keys())
    db.execute(
        'INSERT INTO topic_intrusion '
        '(validate_id, docs_id, topic_one, topic_one_list_word, topic_two, topic_two_list_word, topic_three, topic_three_list_word, topic_intrusion, topic_intrusion_list_word ,hit_answer ) '
        'VALUES(?,?,?,?,?,?,?,?,?,?,?)',
        (validate_id, doc_id, topics_ids[0], topic_intrusion[topics_ids[0]], topics_ids[1], topic_intrusion[topics_ids[1]], topics_ids[2], topic_intrusion[topics_ids[2]], topics_ids[3], topic_intrusion[topics_ids[3]] , 0)
    )
    db.commit()

def get_data_from_validate_topic_intrusion(validate_id, doc_id):
    db = get_db()
    return db.execute('SELECT * FROM topic_intrusion '
        'WHERE validate_id = ? AND docs_id = ?', (validate_id, doc_id)
        ).fetchone()

# altera o campo de 'resposta correta'(hit answer) para 1
def save_correct_answer(topic_intrusion_id):
    db = get_db()
    db.execute('UPDATE topic_intrusion '
        'SET hit_answer = 1 '
        'WHERE id = ?',
        (topic_intrusion_id, )
    ).fetchone()
    db.commit()

# recuperando todos os dados da validação
def get_topic_intrusion_by_validate(validate_id):
    db = get_db()
    return db.execute(
        'SELECT * '
        'FROM topic_intrusion '
        'WHERE validate_id = ?',
        (validate_id, )
    ).fetchall()



@bp.route('test', methods=['GET','POST'])
def test():

    validate_id = request.form['validate_id']

    data = {}

    # recuperando ids dos documentos de forma aleatória
    docs_id = get_list_random_ids_from_docs(quantity=5)

    for doc_id in docs_id:
        data[doc_id] = {}

        # recuperando tudo sobre o documento
        doc = get_doc(doc_id)
        data[doc_id]['doc'] = {'user_code': doc['user_code'], 'experience': doc['experience']}
        
        # recuperando os tópicos mais vinculados ao documento
        list_topics_id = get_list_topics_from_docs(doc_id=doc_id,order='DESC',quantity=3)

        # recuperando as palavras mais vinculadas a cada um destes tópicos
        data_topics = {}
        for topic_id in list_topics_id:
            terms = get_terms_link_topic(topic_id)
            str_topic = "topic_"+str(topic_id)
            data_topics[str_topic] = terms

        # recuperando um tópico com pouco vinculo com o documento
        topic_intrusion_id = get_topic_intrusion(doc_id) 
        # enquanto existir um tópico igual, ele seleciona outro
        while topic_intrusion_id in list_topics_id:
            topic_intrusion_id = get_topic_intrusion(doc_id)
        # recupera os termos do tópico intruso
        terms_intrusion = get_terms_link_topic(topic_intrusion_id)
        
        str_topic = "topic_"+str(topic_intrusion_id)
        # adicionando os dados do tópico intruso
        data_topics[str_topic] = terms_intrusion
        
        # vinculando os tópicos ao dicitionario de documento
        data[doc_id]['topics'] = data_topics

        #salvando a validação de tópicos
        save_topic_intrusion(validate_id, doc_id, data_topics)
    
    print(data)
    return render_template('topic-intrusion/test.html', validate_id=validate_id, data=data)

@bp.route('save', methods=['POST'])
def save():
    form_data = request.form
    # recuperando o id da validação
    validate_id = form_data['validate_id']
    # salvando os dados
    for doc_id in form_data:
        topic_intrusion = get_data_from_validate_topic_intrusion(validate_id, doc_id)
        if topic_intrusion != None: # isto indica que existe um tópico com este nome
            if topic_intrusion['topic_intrusion'] == form_data[doc_id]:
                # quer dizer que ele acertou a palavra intrusa
                save_correct_answer(topic_intrusion['id'])
    topic_intrusion = get_topic_intrusion_by_validate(validate_id)

    total_documents = 0
    total_hit_answer = 0
    for topic in topic_intrusion:
        total_documents = total_documents + 1
        if topic['hit_answer']:
            total_hit_answer = total_hit_answer + 1

    percent_hit_answer = total_hit_answer * 100 / total_documents
        

    return render_template('topic-intrusion/result.html', topic_intrusion=topic_intrusion, percent_hit_answer=percent_hit_answer)