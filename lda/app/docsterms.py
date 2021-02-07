# -*- coding: utf-8 -*-
import json
import os
from pprint import pprint

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from app.db import get_db

bp = Blueprint('docsterms', __name__, url_prefix='/docsterms')


@bp.route('/show-terms')
def show_terms():

    db = get_db() # get database connection
    terms = db.execute('SELECT * FROM terms ORDER BY term').fetchall()
    vocabulary = {}
    vocabulary['Numeros'] = []
    letter = 'a'
    for term in terms:
        
        item = (term['id'],term['term']) # criando uma tupla
        first_letter = term['term'][0] # recuperando a primeira letra
        
        if first_letter.isdigit(): # é um número?
            vocabulary['Numeros'].append(item)
        else:
            # a primeira letra já foi mapeada?
            if first_letter in vocabulary:
                vocabulary[first_letter].append(item)
            else:
                vocabulary[first_letter] = [item]
    total_terms = len(terms)
    return render_template('docs-terms/show-terms.html', vocabulary=vocabulary, terms=terms, total_terms = total_terms)


@bp.route('<int:id_term>/show-document-by-term')
def show_document_by_term(id_term):

    db = get_db()

    term = db.execute('SELECT term FROM terms WHERE id = ?',(id_term,)).fetchone()

    # recupera todo os ids dos documentos vinculados ao termo
    docs_terms = db.execute(
            'SELECT docs_id, quantity'
            ' FROM docs_terms'
            ' WHERE terms_id = ?',
            (id_term,)
        ).fetchall()

    # montando a string com os documentos
    docs = []
    
    for value in docs_terms:
        dic_doc = {}
        doc = db.execute(
            'SELECT * FROM docs where id IN (?)',(value['docs_id'],)
        ).fetchone()
        dic_doc['quantity'] = value['quantity']
        dic_doc['user_code'] = doc['user_code']
        dic_doc['experience'] = doc['experience']
        docs.append(dic_doc)

    return render_template('docs-terms/show-document-by-term.html', id_term=id_term, term=term['term'], docs=docs)
