from flask import (
    Blueprint, render_template, request
)

from pprint import pprint

from app.db import get_db

bp = Blueprint('readdocs', __name__, url_prefix='/readdocs')

@bp.route('/read-docs')
def read_docs():
    db = get_db() # get database connection
    docs = db.execute('SELECT * FROM docs')

    json_docs = {}

    for doc in docs:
        json_docs[str(doc['id'])] = doc['experience']


    print(json_docs)

    # print(docs)
    # print('pulou')
    # pprint(docs)

    return render_template('readdocs/readdocs.html')