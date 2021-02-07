# -*- coding: utf-8 -*-
import json
import os
from pprint import pprint

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from app.db import get_db

bp = Blueprint('docstopics', __name__, url_prefix='/docstopics')

def get_all_docs():
    db = get_db()
    all_docs =  db.execute('SELECT * FROM docs').fetchall()
    docs = {}
    for doc in all_docs:
        docs[doc['user_code']] = doc['experience']
    return docs


@bp.route('/show-docs')
def show_docs():

    db = get_db() # get database connection

    # recuperando todos os documentos cadastrados no sistema
    all_docs = get_all_docs()

    # recuperando todos os tópicos vinculados aos documentos
    docs_topics_sql = db.execute(
        'SELECT '
        '    doc.user_code, '
        '    dt.topics_id, '
        '    top.topic, '
        '    dt.percent '
        'FROM docs_topics AS dt '
        'INNER JOIN topics AS top '
        '    ON dt.topics_id = top.id '
        'INNER JOIN docs AS doc '
        '    ON dt.docs_id = doc.id '
        'WHERE dt.percent != 0.0 '
        'ORDER BY dt.docs_id,dt.percent DESC '
    ).fetchall()

    docs_topics = {}
    user_code = ""
    for doc in docs_topics_sql:

        topic_string = 'Tópico '+doc['topic'].encode('utf-8').zfill(2)

        # isto quer dizer que é uma nova chave
        if user_code != doc['user_code']:
            user_code = doc['user_code']
            docs_topics[doc['user_code']] = [{
                "topic_id":doc['topics_id'], 
                "topic": topic_string, 
                "percent":  doc['percent']
            }]
        else:
            # adiciona
            docs_topics[doc['user_code']].append({
                "topic_id":doc['topics_id'], 
                "topic": topic_string, 
                "percent":  doc['percent']
            })

    total_docs = len(all_docs)
    return render_template('docs-topics/show-docs.html', all_docs=all_docs, docs_topics=docs_topics, total_docs=total_docs)
