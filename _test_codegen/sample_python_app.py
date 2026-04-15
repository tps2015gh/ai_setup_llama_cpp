"""
Sample Python Flask Controller for AI Coder testing
"""

from flask import Flask, request, jsonify
from typing import Dict, List, Optional

app = Flask(__name__)

# Sample data store
users: List[Dict] = []


@app.route('/users', methods=['GET'])
def get_users() -> jsonify:
    """Get all users"""
    return jsonify({'users': users, 'count': len(users)})


@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id: int) -> jsonify:
    """Get a specific user by ID"""
    user = next((u for u in users if u.get('id') == user_id), None)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify(user)


@app.route('/users', methods=['POST'])
def create_user() -> jsonify:
    """Create a new user"""
    data = request.get_json()
    
    if not data or 'name' not in data:
        return jsonify({'error': 'Name is required'}), 400
    
    new_user = {
        'id': len(users) + 1,
        'name': data['name'],
        'email': data.get('email', '')
    }
    
    users.append(new_user)
    return jsonify(new_user), 201


@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id: int) -> jsonify:
    """Delete a user"""
    global users
    initial_len = len(users)
    users = [u for u in users if u.get('id') != user_id]
    
    if len(users) == initial_len:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({'message': 'User deleted'}), 200


if __name__ == '__main__':
    app.run(debug=True, port=5000)
