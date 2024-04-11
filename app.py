from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu_clave_secreta'  # Cambia esto por una clave segura en un entorno de producción
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/appflask'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Modelo de usuario
class Login(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # Agregamos el campo 'role'

# Definimos el formulario de inicio de sesión
class LoginForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Iniciar sesión')

# Configuramos el manejador de inicio de sesión
@login_manager.user_loader
def load_user(user_id):
    return Login.query.get(int(user_id))

# Rutas de la aplicación
@app.route('/')
@login_required
def index():
    if current_user.role == 'Administrador':
        return redirect(url_for('admin_dashboard'))
    elif current_user.role == 'Cajero':
        return redirect(url_for('cajero_dashboard'))
    elif current_user.role == 'Cliente':
        return redirect(url_for('cliente_dashboard'))

@app.route('/admin_dashboard')
@login_required
def admin_dashboard():
    if current_user.role != 'Administrador':
        flash('Acceso denegado: no eres un administrador', 'error')
        return redirect(url_for('index'))  # Redireccionar si el usuario no es administrador
    return 'Panel de administrador'

@app.route('/cajero_dashboard')
@login_required
def cajero_dashboard():
    if current_user.role != 'Cajero':
        flash('Acceso denegado: no eres un cajero', 'error')
        return redirect(url_for('index'))  # Redireccionar si el usuario no es cajero
    return 'Panel de cajero'

@app.route('/cliente_dashboard')
@login_required
def cliente_dashboard():
    if current_user.role != 'Cliente':
        flash('Acceso denegado: no eres un cliente', 'error')
        return redirect(url_for('index'))  # Redireccionar si el usuario no es cliente
    return 'Panel de cliente'

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Login.query.filter_by(username=form.username.data, password=form.password.data).first()
        if user:
            login_user(user)
            flash('Has iniciado sesión correctamente', 'success')
            return redirect(url_for('index'))
        else:
            flash('Usuario o contraseña incorrectos', 'error')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión correctamente', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)