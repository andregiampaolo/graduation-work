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

bp = Blueprint('docs', __name__, url_prefix='/docs')


@bp.route('/import-resume')
def import_resume():
    # read json file
    with open('app/resume.json','r', encoding='utf-8') as f:
        data = json.load(f)

    db = get_db() # get database connection
    #insert data on sqlite
    for item in data['content']:
        # if data['content'][item] != '':
        db.execute(
                'INSERT INTO docs (user_code, experience) VALUES (?, ?)',
                (item, data['content'][item])
            )
        db.commit()

    return render_template('docs/insert-docs-db.html')