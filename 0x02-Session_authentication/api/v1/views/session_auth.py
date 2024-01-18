#!/usr/bin/env python3
"""
Handles all Session Authentication routes.
"""
from api.v1.views import app_views
from flask import request, jsonify, abort
from models.user import User
import os

@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def auth_session_login():
    """
    Handles user authentication 
    """
    user_email = request.form.get('email')
    user_pwd = request.form.get('password')
    if not user_email:
        return jsonify({"error": "email missing"}), 400
    if not user_pwd:
        return jsonify({"error": "password missing"}), 400
    users = User.search({"email": user_email})
    if not users:
        return jsonify({"error": "no user found for this email"}), 404
    for user in users:
        if user.is_valid_password(user_pwd):
            from api.v1.app import auth
            session_id = auth.create_session(user.id)
            response = jsonify(user.to_json())
            session_name = os.getenv("SESSION_NAME")
            response.set_cookie(session_name, session_id)
            return response
        return jsonify({"error": "wrong password"}), 401
