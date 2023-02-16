"""
Initialize app
"""

from flask import Flask, render_template


def create_app():
    app = Flask(__name__)
    with app.app_context():
        from .main import main as main_blueprint
        app.register_blueprint(main_blueprint)

        @app.errorhandler(404)
        def pageNotFound(error):
            page_title = f"{error.code} - page not found !"
            return render_template(
                'page/error.html',
                page_title=page_title,
                error=error
            ), 404

        @app.errorhandler(500)
        def internalServerError(error):
            page_title = f"{error.code} - few things went wrong"
            return render_template(
                'page/error.html',
                page_title=page_title,
                error=error
            ), 500

        @app.errorhandler(400)
        def keyError(error):
            page_title = f"{error.code} - invalid request resulted in KeyError."
            return render_template(
                'page/error.html',
                page_title=page_title,
                error=error
            ), 400

        return app
