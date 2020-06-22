# app/errors/routes.py

from . import errors_bp
from flask import render_template, jsonify
from werkzeug.exceptions import HTTPException

@errors_bp.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@errors_bp.app_errorhandler(401)
def unathorized(e):
    return jsonify(error=str(e)), 401


@errors_bp.app_errorhandler(HTTPException)
def handle_exception(e):
    return render_template('500.html', msj=str(e)), 500
