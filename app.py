from flask import Flask
from routes import users, posts, comments, albums, photos, todos

app = Flask(__name__)

# Register blueprints
app.register_blueprint(users.users_bp, url_prefix='/users')
app.register_blueprint(posts.posts_bp, url_prefix='/posts')
app.register_blueprint(photos.photos_bp, url_prefix='/photos')
app.register_blueprint(todos.todos_bp, url_prefix='/todos')
app.register_blueprint(comments.comments_bp, url_prefix='/comments')
app.register_blueprint(albums.albums_bp, url_prefix='/albums')

if __name__ == '__main__':
    app.run(debug=True)