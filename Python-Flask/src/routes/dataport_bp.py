from flask import Blueprint
from controllers.dataport_controller import dataport

dataport_bp = Blueprint('dataport_bp', __name__)

dataport_bp.route('/', methods=['POST'])(dataport)
