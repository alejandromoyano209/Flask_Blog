from wtforms import Form, StringField, EmailField, TextAreaField, SubmitField, DateTimeField, validators, PasswordField, BooleanField, RadioField
from flask_wtf import FlaskForm

class formulario(Form):
    name = StringField("name", [validators.Length(min=3, max=25)])
    email = EmailField("email", [validators.Length(min=3, max=25)])
    text = TextAreaField("Mensaje", [validators.Length(min=3, max=200)])

class form_crea_articulos(Form):
    titulo = StringField("titulo", [validators.Length(min=3, max=25)])
    autor = StringField("autor", [validators.Length(min=3, max=25)])
    articulo = TextAreaField("articulo")
    button = SubmitField("Enviar artículo")

class Form_Comentarios(Form):
    autor = StringField("Autor")
    comentario = TextAreaField("Comentario")
    boton = SubmitField("Enviar comentario")

class Form_Login(FlaskForm):
    usuario = StringField("usuario")
    password = PasswordField("contraseña")
    remember = BooleanField("Recordarme")
    boton = SubmitField("Enviar")

class Form_Signup(Form):
    usuario = StringField("usuario")
    password = PasswordField("contraseña")
    boton = SubmitField("Enviar")

class Tags(Form):
    nivel = RadioField('nivel', choices=[(1, 'principante'), (2, 'medio'), (3, 'avanzado')])