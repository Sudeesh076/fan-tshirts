from flask import Blueprint, request, jsonify
from coredb.user import *
from helpers.Users import User, UserLogin, AdminLogin

user_api = Blueprint('user', __name__)



@user_api.route('/user', methods=['POST'])
def new_user():
    try:
        data = request.get_json()
        user = User.from_json(data)
        validate_unique_email_phone(user)
        record = add_user(user)
        return record.to_dict()
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@user_api.route('/login/user', methods=['POST'])
def loginUser():
    try:
        data = request.get_json()

        userLogin = UserLogin.from_json(data)
        userRecord = get_user_by_email(userLogin.email)
        authenticated = userLogin.validatePassword(userRecord.password)
        if authenticated:
            return userRecord.to_dict()
        else:
            return jsonify({"error": "Authentication Failed"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_api.route('/login/admin', methods=['POST'])
def loginAdmin():
    try:
        data = request.get_json()

        adminLogin = AdminLogin.from_json(data)
        adminRecord = get_admin_by_email(adminLogin.email)
        authenticated = adminLogin.validatePassword(adminRecord.password)
        if authenticated:
            return adminRecord.to_dict()
        else:
            return jsonify({"error": "Authentication Failed"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500
