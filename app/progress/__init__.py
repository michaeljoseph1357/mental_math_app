from flask import Blueprint

progress = Blueprint('progress', __name__, template_folder='templates')

from . import routes  # Import routes to register them with the blueprint
