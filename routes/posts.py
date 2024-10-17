from flask import Blueprint, request, jsonify
from config import get_db_connection

posts_bp = Blueprint('posts', __name__)

@posts_bp.route('/', methods=['GET'])
def get_posts():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM Posts;')
    posts = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(posts)

@posts_bp.route('/', methods=['POST'])
def create_post():
    new_post = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO Posts (user_id, title, body)
        VALUES (%s, %s, %s) RETURNING id;
    ''', (new_post['user_id'], new_post['title'], new_post['body']))
    post_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'id': post_id}), 201

@posts_bp.route('/<int:id>', methods=['PUT'])
def update_post(id):
    updated_post = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        UPDATE Posts SET title = %s, body = %s
        WHERE id = %s;
    ''', (updated_post['title'], updated_post['body'], id))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Post updated successfully'})

@posts_bp.route('/<int:id>', methods=['DELETE'])
def delete_post(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM Posts WHERE id = %s;', (id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Post deleted successfully'})