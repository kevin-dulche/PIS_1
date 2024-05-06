from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, HiddenField
from wtforms.validators import DataRequired
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu_clave_secreta'  # Cambia esto por una clave segura en un entorno de producción
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/appflask'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Modelo de usuario
class Login(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # Agregamos el campo 'role'

# Definimos el formulario de inicio de sesión
class LoginForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Iniciar sesión')

class NuevoUsuarioForm(FlaskForm):
    username = StringField('Nombre de Usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    role = StringField('Rol', validators=[DataRequired()])
    submit = SubmitField('Guardar Usuario')

class ModificarUsuarioForm(FlaskForm):
    username = SelectField('Seleccionar usuario:', coerce=int, validators=[DataRequired()])
    new_username = StringField('Nuevo nombre de usuario', validators=[DataRequired()])
    password = PasswordField('Nueva contraseña', validators=[DataRequired()])
    submit = SubmitField('Guardar Cambios')

class EliminarUsuarioForm(FlaskForm):
    username = SelectField('Selecciona el usuario a eliminar:', coerce=int, validators=[DataRequired()])
    role = HiddenField('Rol del usuario')
    submit = SubmitField('Eliminar Usuario')

# Configuramos el manejador de inicio de sesión
@login_manager.user_loader
def load_user(user_id):
    return Login.query.get(int(user_id))

# Rutas de la aplicación
@app.route('/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:  # Si el usuario ya está autenticado, redirige a la página correspondiente
        if current_user.role == 'Administrador':
            return redirect(url_for('admin_dashboard'))
        elif current_user.role == 'Cajero':
            return redirect(url_for('cajero_dashboard'))
        elif current_user.role == 'Cliente':
            return redirect(url_for('cliente_dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        user = Login.query.filter_by(username=form.username.data, password=form.password.data).first()
        if user:
            login_user(user)
            return redirect(url_for('login'))  # Redirecciona a la página correspondiente después del login
        else:
            flash('Usuario y/o contraseña incorrectos', 'error')
    return render_template('login.html', form=form)


@app.route('/admin_dashboard')
@login_required
def admin_dashboard():
    if current_user.role != 'Administrador':
        flash('Acceso denegado: no eres un administrador', 'error')
        return redirect(url_for('login'))  # Redireccionar si el usuario no es administrador
    return render_template('panelAdmin.html')

@app.route('/cajero_dashboard')
@login_required
def cajero_dashboard():
    if current_user.role != 'Cajero':
        flash('Acceso denegado: no eres un cajero', 'error')
        return redirect(url_for('login'))  # Redireccionar si el usuario no es cajero
    return render_template('panelCajero.html')

@app.route('/cliente_dashboard')
@login_required
def cliente_dashboard():
    if current_user.role != 'Cliente':
        flash('Acceso denegado: no eres un cliente', 'error')
        return redirect(url_for('login'))  # Redireccionar si el usuario no es cliente
    return 'Panel de cliente'

@app.route('/gestion_usuario')
def gestion_usuarios():
    usuarios = Login.query.all()
    return render_template('gestion_usuario.html', usuarios=usuarios)

# Ruta para registrar un nuevo usuario
@app.route('/agregar_usuario', methods=['GET', 'POST'])
def agregar_usuario():
    form = NuevoUsuarioForm()
    if form.validate_on_submit():
        try:
            nuevo_usuario = Login(username=form.username.data, password=form.password.data, role=form.role.data)
            db.session.add(nuevo_usuario)
            db.session.commit()
            flash('Usuario agregado correctamente', 'success')
            return redirect(url_for('gestion_usuarios'))
        except IntegrityError:
            flash('El nombre de usuario ya existe', 'error')
            return redirect(url_for('agregar_usuario'))
    return render_template('agregar_usuario.html', form=form)

# Ruta para modificar un usuario
@app.route('/modificar_usuario', methods=['GET', 'POST'])
@login_required
def modificar_usuario():
    form = ModificarUsuarioForm()
    usuarios = Login.query.all()
    form.username.choices = [(user.id, f"{user.username} ({user.role})") for user in usuarios]
    
    print("Entrando al método modificar_usuario")  # Imprimir mensaje de entrada al método

    if form.validate_on_submit():
        print("Formulario válido")  # Imprimir mensaje de formulario válido
        usuario_id = form.username.data
        usuario = Login.query.get(usuario_id)
        if usuario:
            if form.opcion.data == 'nombre':
                print("Modificando nombre de usuario")  # Imprimir mensaje de modificación de nombre de usuario
                # Modificar el nombre de usuario
                usuario.username = form.new_username.data
            elif form.opcion.data == 'contraseña':
                print("Modificando contraseña de usuario")  # Imprimir mensaje de modificación de contraseña
                # Modificar la contraseña del usuario
                usuario.password = form.password.data
            db.session.commit()
            flash('Usuario modificado correctamente', 'success')
            return redirect(url_for('gestion_usuarios'))
        else:
            flash('No se encontró al usuario seleccionado', 'error')
    else:
        print("Formulario no válido")  # Imprimir mensaje de formulario no válido
    
    return render_template('modificar_usuario.html', form=form, usuarios=usuarios)



#Ruta para elimanr a un usuario
@app.route('/eliminar_usuario', methods=['GET', 'POST'])
@login_required
def eliminar_usuario():
    form = EliminarUsuarioForm()
    usuarios = Login.query.all()
    form.username.choices = [(user.id, f"{user.username} ({user.role})") for user in usuarios]
    
    if form.validate_on_submit():
        usuario_id = form.username.data
        usuario = Login.query.get(usuario_id)
        if usuario:
            db.session.delete(usuario)
            db.session.commit()
            flash('Usuario eliminado correctamente', 'success')
        else:
            flash('No se encontró al usuario seleccionado', 'error')
        return redirect(url_for('gestion_usuarios'))
    
    return render_template('eliminar_usuario.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión correctamente', 'success')
    return redirect(url_for('login'))

# Manejador para errores 404
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', url=request.url), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')