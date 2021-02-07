# -*- coding: utf-8 -*-
from flask import (
    Blueprint, render_template, request
)

from pprint import pprint

from app.db import get_db

bp = Blueprint('report', __name__, url_prefix='/report')

def get_validates():
    db = get_db()
    validates = db.execute('SELECT * FROM validate').fetchall()
    return validates


def get_percentage_word_intrusion(validate_id):
    db = get_db()
    word_intrusion = db.execute(
        'SELECT * '
        'FROM word_intrusion '
        'WHERE validate_id = ?',
        (validate_id, )
    ).fetchall()

    # calculando a porcentagem de acerto
    total_answer = 0
    total_hit_answer = 0
    for answer in word_intrusion:
        total_answer = total_answer + 1
        if answer['hit_answer']:
            total_hit_answer = total_hit_answer + 1
    
    if total_answer != 0:
        percent_hit_answer = total_hit_answer * 100 / total_answer
    else:
        percent_hit_answer = 0

    return percent_hit_answer


def get_percentage_topic_intrusion(validate_id):
    db = get_db()
    topic_intrusion = db.execute(
        'SELECT * '
        'FROM topic_intrusion '
        'WHERE validate_id = ?',
        (validate_id, )
    ).fetchall()

    total_documents = 0
    total_hit_answer = 0
    for topic in topic_intrusion:
        total_documents = total_documents + 1
        if topic['hit_answer']:
            total_hit_answer = total_hit_answer + 1
    
    if total_documents != 0:
        percent_hit_answer = total_hit_answer * 100 / total_documents
    else:
        percent_hit_answer = 0


    return percent_hit_answer



@bp.route('/report')
def report():
    
    validates = get_validates()

    validate_word_intrusion = {}
    validate_topic_intrusion = {}
    
    if bool(validates):
        for validate in validates:
            percentage_word_intrusion = get_percentage_word_intrusion(validate['id'])
            percentage_topic_intrusion = get_percentage_topic_intrusion(validate['id'])
            validate_word_intrusion[validate['user_name']] = (percentage_word_intrusion, percentage_topic_intrusion)

    return render_template('report/report.html', validate_word_intrusion=validate_word_intrusion)