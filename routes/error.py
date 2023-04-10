from flask import Blueprint, render_template

from models.Logger import logger


# API ==========================================================================
error = Blueprint("error", __name__)

@error.app_errorhandler(404)
def page_not_found(e):
    logger.error(f"404 Error :{e}")
    return render_template('404.html'), 404



# wild card route
# @error.route('/<path:path>')
# def catch_all(path):
#     return render_template('404.html'), 404
