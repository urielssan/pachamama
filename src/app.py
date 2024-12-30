from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from config import config
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import os
from datetime import datetime
from werkzeug.utils import secure_filename

# Models:
from models.ModelUser import ModelUser
from models.ModelPost import ModelPost
from models.ModelComment import ModelComment


# Entities:
from models.entities.User import User
from models.entities.Post import Post
from models.entities.Comment import Comment

app = Flask(__name__)
app.secret_key = 'your_secret_key'

csrf = CSRFProtect(app)
db = MySQL(app)
login_manager_app = LoginManager(app)
login_manager_app.login_view = 'login'

@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db, id)

app.config.from_object(config['development'])

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        fullname = request.form['fullname']
        user = User(0, username, password, fullname)
        if ModelUser.register(db, user):
            flash('Usuario registrado exitosamente')
            return redirect(url_for('login'))
        else:
            flash('Error al registrar el usuario')
    return render_template('auth/register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User(0, request.form['username'], request.form['password'])
        logged_user = ModelUser.login(db, user)
        if logged_user is not None:
            if logged_user.password:
                login_user(logged_user)
                flash(f'Bienvenido, {logged_user.fullname}')
                session['fullname'] = logged_user.fullname
                return redirect(url_for('home'))
            else:
                flash('Contraseña incorrecta')
                return render_template('auth/login.html')
        else:
            flash('Usuario no encontrado')
            return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/home')
@login_required
def home():
    return render_template('index.html')

@app.route('/protected')
@login_required
def protected():
    return "<h1>Protected</h1>"

def status_401(error):
    return redirect(url_for('login'))

def status_404(error):
    return "<h1>Página no encontrada</h1>", 404

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/create_post', methods=['POST'])
@login_required
def create_post():
    title = request.form['title']
    description = request.form['description']
    username = current_user.username
    photo = request.files['plant_photo']

    if photo:
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])

        filename = secure_filename(photo.filename)
        photo_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        photo.save(photo_path)

        post = Post(id,username, title, filename, description)
        try:
            ModelPost.create_post(db, post)
            flash('Publicación creada exitosamente.')
            return redirect(url_for('blog'))
        except Exception as ex:
            flash(f"Error al crear la publicación: {ex}")
            return redirect(url_for('blog'))

@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post(post_id):
    if request.method == 'POST':
        username = current_user.username
        comment_text = request.form['comment']
        comment = Comment(None, post_id, username, comment_text, None)
        try:
            ModelComment.add_comment(db, comment)
            flash('Comentario agregado exitosamente.')
        except Exception as ex:
            flash(f"Error al agregar el comentario: {ex}")
    
    try:
        cursor = db.connection.cursor()
        cursor.execute("SELECT id,username, title, photo_path, description, created_at FROM posts WHERE id = %s", (post_id,))
        post = cursor.fetchone()
        comments = ModelComment.get_comments_by_post_id(db, post_id)
        if post:
            return render_template('post.html', post=post, comments=comments)
        else:
            flash('Publicación no encontrada')
            return redirect(url_for('blog'))
    except Exception as ex:
        flash(f"Error al cargar la publicación: {ex}")
        return redirect(url_for('blog'))
    
@app.route('/principal')
def principal():
    return render_template('principal.html')

@app.route('/blog')
def blog():
    try:
        cursor = db.connection.cursor()
        cursor.execute("SELECT id,username, title, photo_path, description, created_at FROM posts ORDER BY created_at DESC LIMIT 3")
        posts = cursor.fetchall()
        return render_template('blog.html', posts=posts)
    except Exception as ex:
        flash(f"Error al cargar las publicaciones: {ex}")
        return render_template('blog.html', posts=[])

@app.route('/cuidados')
def cuidados():
    return render_template('cuidados.html')

@app.route('/galeria')
def galeria():
    return render_template('galeria.html')

@app.route('/registro')
def registro():
    return render_template('registro.html')

if __name__ == '__main__':
    app.config.from_object(config['development'])
    csrf.init_app(app)
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.run(debug=True)