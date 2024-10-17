from flask import Blueprint, jsonify, request
import json
from config import get_db_connection

users_bp = Blueprint('users', __name__)

@users_bp.route('/', methods=['GET'])
def get_users():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM Users;')
    users = cur.fetchall()
    cur.close()
    conn.close()
    user_list = []
    for user in users:
        user_data = {
            'id': user[0],
            'name': user[1],
            'username': user[2],
            'email': user[3],
            'address': user[4],
            'geo': user[5],
            'phone': user[6],
            'website': user[7],
            'company_name': user[8],
            'company_catchphrase': user[9],
            'company_bs': user[10]
        }
        user_list.append(user_data)
    return jsonify(user_list)

@users_bp.route('/', methods=['POST'])
def create_user():
    new_user = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    address_json = json.dumps(new_user['address'])
    geo_json = json.dumps(new_user['geo'])
    cur.execute('''
        INSERT INTO Users (name, username, email, address, geo, phone, website, company_name, company_catchphrase, company_bs)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;
    ''', (
        new_user['name'], new_user['username'], new_user['email'], address_json, geo_json,
        new_user['phone'], new_user['website'], new_user['company_name'], new_user['company_catchphrase'],
        new_user['company_bs']
    ))
    user_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'id': user_id}), 201

@users_bp.route('/<int:id>', methods=['PUT'])
def update_user(id):
    updated_user = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    address_json = json.dumps(updated_user['address'])
    geo_json = json.dumps(updated_user['geo'])
    cur.execute('''
        UPDATE Users SET name = %s, username = %s, email = %s, address = %s, geo = %s, phone = %s, website = %s, company_name = %s, company_catchphrase = %s, company_bs = %s
        WHERE id = %s;
    ''', (
        updated_user['name'], updated_user['username'], updated_user['email'], address_json, geo_json,
        updated_user['phone'], updated_user['website'], updated_user['company_name'], updated_user['company_catchphrase'],
        updated_user['company_bs'], id
    ))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'User updated successfully'})

@users_bp.route('/<int:id>', methods=['DELETE'])
def delete_user(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM Users WHERE id = %s;', (id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'User deleted successfully'})