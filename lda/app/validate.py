# -*- coding: utf-8 -*-
import functools
import json
import os

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from app.db import get_db

bp = Blueprint('validate', __name__, url_prefix='/validate')


@bp.route('/start')
def start():

    return render_template('validate/start-validate.html')