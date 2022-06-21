from flask import Flask, render_template, request, redirect, url_for, Blueprint, flash
from flask_login import login_required, logout_user, login_user, current_user, UserMixin

from application.forms import formulario, form_crea_articulos, Form_Comentarios, Form_Login, Form_Signup, Tags
from application.db import get_db, close_db

from .models import User

from werkzeug.security import check_password_hash, generate_password_hash


blog_bp = Blueprint('blog_bp', __name__)
auth_bp = Blueprint('auth_bp', __name__)


# Routes

@auth_bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('blog_bp.index')) 


@auth_bp.route("/login", methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('blog_bp.index'))
    form = Form_Login()

    if request.method == 'POST':
        print('Solicitud POST')
        if form.validate_on_submit():
            print('Formulario validado')
            conn = get_db()
            curs = conn.cursor()
            curs.execute("SELECT * FROM login_usuario WHERE usuario = (?)", [form.usuario.data])
            if curs.fetchone() == None:
                flash('No existe usuario')
                return render_template('login_form.html', form=form)

            else:
                curs.execute("SELECT * FROM login_usuario WHERE usuario = (?)", [form.usuario.data])
                user = curs.fetchone()
                print(f"ID de usuario: {user[0]}")
                # Us = load_user(user[0]) // deprecated
                # print(f"US: {Us}") // deprecated

                if form.usuario.data == user[1] and check_password_hash(user[2], form.password.data):
                    print('email y password correctos')
                    mixed_user = User(user[0], user[1], user[2], user[3])
                    login_user(mixed_user, remember = form.remember.data)
                    Umail = list({form.usuario.data})[0].split('@')[0]
                    print('Logged in successfully ' + Umail)
                    return redirect(url_for('blog_bp.index'))
                
                else:
                    flash('Contraseña incorrecta')
    
    return render_template("login_form.html", form=form)


@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    form = Form_Signup(request.form)
    if request.method == "POST":
        usuario= form.usuario.data
        password= form.password.data
        pass_crypt = generate_password_hash(password, 'sha256')

        conn = get_db()
        conn.execute('INSERT INTO login_usuario (usuario, password) VALUES (?,?)', (usuario, pass_crypt))
        conn.commit()
        close_db()

        return redirect(url_for('blog_bp.index'))
    
    else:
        return render_template("signup_form.html", form=form)


##########################################


@blog_bp.route('/', methods=["GET", "POST"])
def index():
    form_tags = Tags(request.form)

    if request.method == "POST":
        nivel = form_tags.nivel.data
        conn = get_db()
        id_articulos = conn.execute('SELECT * FROM articulos INNER JOIN tags ON articulos.id = tags.articuloId WHERE nivel=?', (nivel)).fetchall()
        ##articulos_id = dict(id_articulos)
        for articuloid in id_articulos:
            # Imprime el id de cada articulo
            print(articuloid[0])
        return render_template("index.html", form_tags=form_tags)


    return render_template("index.html", form_tags=form_tags)



@blog_bp.route("/contacto", methods=["GET", "POST"])
def contacto():
    form = formulario(request.form)
    if request.method == "POST":
        nombre = form.name.data
        email = form.email.data
        text =  form.text.data
        print(nombre + email + text)

        conn = get_db()
        conn.execute('INSERT INTO contacto (nombre, email, mensaje) VALUES (?,?,?)',
            (nombre, email, text))
        conn.commit()
        close_db()

        return redirect(url_for('blog_bp.index'))
    
    else:
        return render_template("contacto.html", form=form)


@blog_bp.route("/mensajes")
def mensajes():
    conn = get_db()
    mensajes = conn.execute('SELECT * FROM contacto').fetchall()
    close_db()
    return render_template('mensajes.html', mensajes=mensajes)


@blog_bp.route("/crear_articulos", methods=["GET", "POST"])
@login_required
def crea_articulos():
    form = form_crea_articulos(request.form)
    form_tags = Tags(request.form)
    if request.method == "POST":
        titulo= form.titulo.data
        articulo = form.articulo.data
        nivel = form_tags.nivel.data

        conn = get_db()
        conn.execute('INSERT INTO articulos (titulo, articulo) VALUES (?,?)',
            (titulo, articulo))
        conn.commit()


        articuloId = conn.execute('SELECT id FROM articulos WHERE titulo=?', (titulo,)).fetchone()
        print(articuloId)
        print(articuloId[0])
        conn.execute('INSERT INTO tags (nivel, articuloId) VALUES (?,?)',
            (nivel, articuloId[0]))

        conn.commit()
        close_db()

        return redirect(url_for('blog_bp.index'))
        # A modificar después 
    
    else:
        return render_template("crea_articulos.html", form=form, form_tags=form_tags)


@blog_bp.route("/articulos")
def articulos():
    conn = get_db()
    articulos = conn.execute('SELECT * FROM articulos ORDER BY fecha DESC').fetchall()
    close_db()
    return render_template('articulos.html', articulos=articulos)


@blog_bp.route("/<int:id>/articulo")
def ver_articulo(id):

    form = Form_Comentarios(request.form)

    conn = get_db()
    articulo = conn.execute('SELECT * FROM articulos WHERE id=?', (id,)).fetchone()
    conn.commit()
    close_db()

    if request.method == "POST":
        autor = form.autor.data
        comentario = form.comentario.data

    return render_template("ver_articulo.html", articulo=articulo, form=form)


@blog_bp.route("/articulos_admin")
@login_required
def articulos_admin():
    conn = get_db()
    articulos = conn.execute('SELECT * FROM articulos ORDER BY fecha DESC').fetchall()
    close_db()
    return render_template('articulos_admin.html', articulos=articulos)


@blog_bp.route("/<int:id>/edit", methods=["GET", "POST"])
@login_required
def edit_post(id):
    conn = get_db()
    articulo = conn.execute('SELECT * FROM articulos WHERE id=?', (id,)).fetchone()
    close_db()
    if articulo is None:
        abort(404)

    form = form_crea_articulos(request.form)

    if request.method == "POST":
        titulo= form.titulo.data
        articulo = form.articulo.data

        conn = get_db()
        conn.execute('UPDATE articulos SET titulo = ?, articulo= ? WHERE id=?', (titulo, articulo, id))

        conn.commit()
        close_db()

        return redirect(url_for('blog_bp.articulos'))

    form.titulo.data = articulo["titulo"]
    form.articulo.data = articulo["articulo"]


    return render_template('edit_post.html', form=form)


@blog_bp.route("/<int:id>/borrar", methods=["GET", "POST"])
@login_required
def borrar_articulo(id):
    conn = get_db()
    articulo = conn.execute('SELECT * FROM articulos WHERE id=?', (id,)).fetchone()
    conn.commit()
    close_db()
    
    if request.method == "POST":
        conn = get_db()
        articulo = conn.execute('DELETE FROM articulos WHERE id=?', (id,))
        conn.commit()
        conn.close()


    return redirect(url_for('blog_bp.articulos'))
