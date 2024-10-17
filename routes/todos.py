from flask import Blueprint, request, jsonify
from config import get_db_connection

todos_bp = Blueprint('todos', __name__)

@todos_bp.route('/', methods=['GET'])
def get_todos():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM Todos;')
    todos = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(todos)

@todos_bp.route('/', methods=['POST'])
def create_todo():
    new_todo = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO Todos (user_id, title, completed)
        VALUES (%s, %s, %s) RETURNING id;
    ''', (new_todo['user_id'], new_todo['title'], new_todo['completed']))
    todo_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'id': todo_id}), 201

@todos_bp.route('/<int:id>', methods=['PUT'])
def update_todo(id):
    updated_todo = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        UPDATE Todos SET title = %s, completed = %s
        WHERE id = %s;
    ''', (updated_todo['title'], updated_todo['completed'], id))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Todo updated successfully'})

@todos_bp.route('/<int:id>', methods=['DELETE'])
def delete_todo(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM Todos WHERE id = %s;', (id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Todo deleted successfully'})