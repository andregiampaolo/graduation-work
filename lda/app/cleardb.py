# -*- coding: utf-8 -*-
import functools
import json
import os
from pprint import pprint

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from app.db import get_db

bp = Blueprint('cleardb', __name__, url_prefix='/cleardb')


@bp.route('/clear-db')
def clear_db():
    db = get_db() # get database connection
    # clear database 

    # db.execute('DELETE FROM topics_terms;')
    # db.execute('DROP TABLE topics_terms;')

    db.execute('DELETE FROM docs_topics;')
    # db.execute('DROP TABLE IF EXISTS docs_topics;')

    db.execute('DELETE FROM docs_terms;')
    # db.execute('DROP TABLE IF EXISTS docs_terms;')

    db.execute('DELETE FROM topics;')
    # db.execute('DROP TABLE IF EXISTS topics;')

    db.execute('DELETE FROM terms;')
    # db.execute('DROP TABLE IF EXISTS terms;')

    db.commit()


    return render_template('cleardb/clear-db.html')