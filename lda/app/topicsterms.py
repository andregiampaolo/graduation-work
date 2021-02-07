# -*- coding: utf-8 -*-
import json
import os
from pprint import pprint

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from app.db import get_db

bp = Blueprint('topicsterms', __name__, url_prefix='/topicsterms')


@bp.route('/show-topics')
def show_topics():

    db = get_db() # get database connection
    # terms = db.execute('SELECT * FROM topics').fetchall()
    # for value in terms:
    #     print(valeu['id'], value['terms'])

    # https://stackoverflow.com/questions/18778844/group-concat-in-sqlite
    topics = db.execute(
            'SELECT  '
            '    top.id as "topic_id", '
            '    top.topic, '
            '    t.id as id_term, '
            '    t.term,  '
            '    tt.percent, '
            '    GROUP_CONCAT(t.term) as "termos" '
            'FROM topics_terms AS tt '
            'INNER JOIN topics AS top '
            '    ON tt.topics_id = top.id '
            'INNER JOIN terms AS t '
            '    ON tt.terms_id = t.id '
            'GROUP BY tt.topics_id '
        ).fetchall()





    # recuperando os documentos que possuem maior percentual no tópico
    topics_ids = db.execute('SELECT id from topics').fetchall()

    docs_topics = {}

    for topic in topics_ids:
        doc = db.execute(
            'SELECT  '
            'doc.user_code AS "user_code", '
            'dt.percent AS "percent" '
            'FROM docs_topics AS dt '
            'INNER JOIN docs as doc '
            '    ON dt.docs_id = doc.id '
            'WHERE '
            '    dt.topics_id = ? AND '
            '    dt.percent > 0.70 '
            'ORDER BY dt.percent DESC',
            (topic['id'], )
        ).fetchall()

        docs_topics[topic['id']] = doc

    # print(docs_topics)

    return render_template('topics-terms/show-topics.html', topics=topics, docs_topics=docs_topics)


# @bp.route('<int:id_term>/show-document-by-term')
# def show_document_by_term(id_term):

#     db = get_db()

#     term = db.execute('SELECT term FROM terms WHERE id = ?',(id_term,)).fetchone()

#     # recupera todo os ids dos documentos vinculados ao termo
#     docs_terms = db.execute(
#             'SELECT docs_id, quantity'
#             ' FROM docs_terms'
#             ' WHERE terms_id = ?',
#             (id_term,)
#         ).fetchall()

#     # montando a string com os documentos
#     docs = []
    
#     for value in docs_terms:
#         dic_doc = {}
#         doc = db.execute(
#             'SELECT * FROM docs where id IN (?)',(value['docs_id'],)
#         ).fetchone()
#         dic_doc['quantity'] = value['quantity']
#         dic_doc['user_code'] = doc['user_code']
#         dic_doc['experience'] = doc['experience']
#         docs.append(dic_doc)

#     return render_template('docs-terms/show-document-by-term.html', id_term=id_term, term=term['term'], docs=docs)
