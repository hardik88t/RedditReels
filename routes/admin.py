# import blueprint
from flask import Blueprint




admin = Blueprint("admin", __name__)


@admin.route("/admin")
def adminpage():
    return "admin"