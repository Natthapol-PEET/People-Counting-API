from flask import Blueprint
# from controllers.manage_device_controller import show_device, delete_device, edit_device, \
#     register_match_device, delete_match_device, edit_match_device, show_match_device
from controllers.manage_device_controller import show_device, delete_device

manage_device_bp = Blueprint('manage_device_bp', __name__)
# manage_device_bp.route('/register_device', methods=['POST'])(register_device)
manage_device_bp.route('/show_device', methods=['GET', 'POST'])(show_device) 
manage_device_bp.route('/delete_device/<int:id>', methods=['GET'])(delete_device)

# manage_device_bp.route('/edit_device', methods=['PUT'])(edit_device) 

# manage_device_bp.route('/register_match_device', methods=['POST'])(register_match_device)
# manage_device_bp.route('/delete_match_device/<int:id>', methods=['DELETE'])(delete_match_device)
# manage_device_bp.route('/edit_match_device', methods=['PUT'])(edit_match_device)
# manage_device_bp.route('/show_match_device', methods=['GET'])(show_match_device)




