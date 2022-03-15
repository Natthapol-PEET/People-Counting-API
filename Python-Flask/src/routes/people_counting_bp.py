from flask import Blueprint
from controllers.people_counting_controller import index, counting, counting_by_id, counting_by_area, summary, callback
from controllers.people_counting_controller import test


people_counting_bp = Blueprint('people_counting_bp', __name__)

# people_counting_bp.route('/', methods=['GET'])(index)
people_counting_bp.route('/counting', methods=['GET'])(counting)
people_counting_bp.route('/counting/<int:id>', methods=['GET'])(counting_by_id)
people_counting_bp.route('/counting/<string:area>', methods=['GET'])(counting_by_area)
people_counting_bp.route('/summary', methods=['GET'])(summary)

# call to theading
people_counting_bp.route('/callback', methods=['POST'])(callback)

# test method
# people_counting_bp.route('/test', methods=['GET'])(test)
