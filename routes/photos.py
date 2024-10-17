from flask import Blueprint, request, jsonify
from config import get_db_connection

photos_bp = Blueprint('photos', __name__)

@photos_bp.route('/', methods=['GET'])
def get_photos():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM Photos;')
    photos = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(photos)

@photos_bp.route('/', methods=['POST'])
def create_photo():
    new_photo = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO Photos (album_id, title, url, thumbnail_url)
        VALUES (%s, %s, %s, %s) RETURNING id;
    ''', (new_photo['album_id'], new_photo['title'], new_photo['url'], new_photo['thumbnail_url']))
    photo_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'id': photo_id}), 201

@photos_bp.route('/<int:id>', methods=['PUT'])
def update_photo(id):
    updated_photo = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        UPDATE Photos SET title = %s, url = %s, thumbnail_url = %s
        WHERE id = %s;
    ''', (updated_photo['title'], updated_photo['url'], updated_photo['thumbnail_url'], id))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Photo updated successfully'})

@photos_bp.route('/<int:id>', methods=['DELETE'])
def delete_photo(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM Photos WHERE id = %s;', (id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Photo deleted successfully'})