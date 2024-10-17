from flask import Blueprint, request, jsonify
from config import get_db_connection

albums_bp = Blueprint('albums', __name__)

@albums_bp.route('/', methods=['GET'])
def get_albums():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM Albums;')
    albums = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(albums)

@albums_bp.route('/', methods=['POST'])
def create_album():
    new_album = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO Albums (user_id, title)
        VALUES (%s, %s) RETURNING id;
    ''', (new_album['user_id'], new_album['title']))
    album_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'id': album_id}), 201

@albums_bp.route('/<int:id>', methods=['PUT'])
def update_album(id):
    updated_album = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        UPDATE Albums SET title = %s
        WHERE id = %s;
    ''', (updated_album['title'], id))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Album updated successfully'})

@albums_bp.route('/<int:id>', methods=['DELETE'])
def delete_album(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM Albums WHERE id = %s;', (id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Album deleted successfully'})