import os
from flask import Flask, render_template

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'lda.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def index():
        return render_template('home/index.html')

    from . import db
    db.init_app(app)

    from . import docs
    app.register_blueprint(docs.bp)

    from . import docsterms
    app.register_blueprint(docsterms.bp)

    from . import topicsterms
    app.register_blueprint(topicsterms.bp)

    from . import docstopics
    app.register_blueprint(docstopics.bp)

    from . import cleardb
    app.register_blueprint(cleardb.bp)

    from . import readdocs
    app.register_blueprint(readdocs.bp)

    from . import validate
    app.register_blueprint(validate.bp)

    from . import wordintrusion
    app.register_blueprint(wordintrusion.bp)

    from . import topicintrusion
    app.register_blueprint(topicintrusion.bp)

    from . import lda_gensim
    app.register_blueprint(lda_gensim.bp)

    from . import report
    app.register_blueprint(report.bp)


    return app