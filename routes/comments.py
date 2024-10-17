from flask import Blueprint, request, jsonify
from config import get_db_connection

comments_bp = Blueprint('comments', __name__)

@comments_bp.route('/', methods=['GET'])
def get_comments():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM Comments;')
    comments = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(comments)

@comments_bp.route('/', methods=['POST'])
def create_comment():
    new_comment = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO Comments (post_id, name, email, body)
        VALUES (%s, %s, %s, %s) RETURNING id;
    ''', (new_comment['post_id'], new_comment['name'], new_comment['email'], new_comment['body']))
    comment_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'id': comment_id}), 201

@comments_bp.route('/<int:id>', methods=['PUT'])
def update_comment(id):
    updated_comment = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        UPDATE Comments SET name = %s, email = %s, body = %s
        WHERE id = %s;
    ''', (updated_comment['name'], updated_comment['email'], updated_comment['body'], id))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Comment updated successfully'})

@comments_bp.route('/<int:id>', methods=['DELETE'])
def delete_comment(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM Comments WHERE id = %s;', (id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Comment deleted successfully'})