# -*- coding: utf-8 -*-
import functools
import json
import os
import random

from flask import request

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from app.db import get_db

bp = Blueprint('wordintrusion', __name__, url_prefix='/word-intrusion')


# recuperando os ids de todos os tópicos
def get_topic_ids(quantity):
    db = get_db()
    topics = db.execute(
        'SELECT id FROM topics'
    ).fetchall()

    list_id_topics = []

    for topic in topics:
        list_id_topics.append(topic['id'])

    id_topics = []

    for i in range(quantity):
        id_topic = random.choice(list_id_topics)
        id_topics.append(id_topic)
        list_id_topics.remove(id_topic)

    return id_topics

# recuperando as cinco palavras mais representativas de um tópico
def get_terms_from_topic(topic_id, order='DESC', quantity=5):
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
        # print('Id do termo: ',term['id'], '- termo: ', term['term'],' - porcentagem', term['percent'])
        terms.append(term['term'])

    return terms

# recuperando uma palavra intrusa
def get_word_intrusion(topic_id):
    # escolhendo um tópico diferente do que foi proposto
    list_id_topics = get_topic_ids(20)
    id_topic = random.choice(list_id_topics)
    while id_topic == topic_id:
        id_topic = random.choice(list_id_topics)
    
    five_unimportant_terms = get_terms_from_topic(id_topic,'DESC',quantity=1)
    return random.choice(five_unimportant_terms)

# salvando o teste no banco de dados
def save_test_on_database(validate_id, id_topic, list_words):
    db = get_db()
    # criando as variáveis para salvar no banco de dados
    topic_name = "topic_"+str(id_topic)
    word_one       = list_words[0]
    word_two       = list_words[1]
    word_three     = list_words[2]
    word_four      = list_words[3]
    word_five      = list_words[4]
    word_intrusion = list_words[5]

    db.execute(
            'INSERT INTO word_intrusion '
            '(validate_id, topic_name, word_one, word_two, word_three, word_four, word_five, word_intrusion, hit_answer) '
            'VALUES (?,?,?,?,?,?,?,?,?)',
            (validate_id, topic_name, word_one, word_two, word_three, word_four, word_five, word_intrusion,0)
        )
    db.commit()

# recuperando os dados de uma validação baseado no nome do tópico
def get_data_from_validate_word_intrusion(validate_id,topic_name):
    print('Nome do tópico:', topic_name)
    db = get_db()
    word_intrusion = db.execute(
        'SELECT * '
        'FROM word_intrusion '
        'WHERE validate_id = ? AND topic_name = ?',
        (validate_id, topic_name, )
    ).fetchone()
    return word_intrusion

# altera o campo de 'resposta correta'(hit answer) para 1
def save_correct_answer(word_intrusion_id):
    db = get_db()
    db.execute('UPDATE word_intrusion '
        'SET hit_answer = 1 '
        'WHERE id = ?',
        (word_intrusion_id, )
    ).fetchone()
    db.commit()

# recuperando todos os dados da validação
def get_word_intrusion_validate_by_validate(validate_id):
    db = get_db()
    word_intrusion = db.execute(
        'SELECT * '
        'FROM word_intrusion '
        'WHERE validate_id = ?',
        (validate_id, )
    ).fetchall()
    return word_intrusion

@bp.route('test', methods=['GET','POST'])
def test():
    user_name = request.form['user_name']
    number = random.choice(range(20000))
    

    
    db = get_db() # get database connection
    
    # save user will do validation
    try:
        db.execute('INSERT INTO validate (user_name) VALUES (?)', (user_name, ))
        db.commit()
    except:
        print('nome do usuário: ',user_name)
        user_name = user_name+str(number)
        db.execute('INSERT INTO validate (user_name) VALUES (?)', (user_name, ))
        db.commit()
        

    # recuperando a validação
    validate = db.execute( 'SELECT * FROM validate WHERE user_name = ?',(user_name, )).fetchone()
    # montando o array com as 5 palavras mais representativas de um tópico
    list_intrusion = {}
    for id_topic in get_topic_ids(24):
        list_intrusion[id_topic] = get_terms_from_topic(id_topic)
        # escolhendo uma palavra intrusa que faz parte de outro tópico
        list_intrusion[id_topic].append(get_word_intrusion(id_topic))
        # salvando no banco de dados
        save_test_on_database(validate['id'], id_topic, list_intrusion[id_topic])
        # misturando os valores
        random.shuffle(list_intrusion[id_topic])

    # acessar id do usuário: validate['user_name']
    return render_template('word-intrusion/test.html', validate_id=validate['id'], user_name=validate['user_name'], list_intrusion=list_intrusion)

@bp.route('save', methods=['GET','POST'])
def save():
    form_data = request.form
    # recuperando o id da validação
    validate_id = form_data['validate_id']
    # salvando os dados
    for topic_name in form_data:
        word_intrusion = get_data_from_validate_word_intrusion(validate_id, topic_name)
        if word_intrusion != None: # isto indica que existe um tópico com este nome
            if word_intrusion['word_intrusion'] == form_data[topic_name]:
                # quer dizer que ele acertou a palavra intrusa
                save_correct_answer(word_intrusion['id'])
    word_intrusion = get_word_intrusion_validate_by_validate(validate_id)

    # calculando a porcentagem de acerto
    total_answer = 0
    total_hit_answer = 0
    for answer in word_intrusion:
        total_answer = total_answer + 1
        if answer['hit_answer']:
            total_hit_answer = total_hit_answer + 1
    
    percent_hit_answer = total_hit_answer * 100 / total_answer

    return render_template('word-intrusion/result.html', word_intrusion=word_intrusion, response=form_data, percent_hit_answer=percent_hit_answer, validate_id=validate_id)
    