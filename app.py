from flask import Flask, render_template, redirect, url_for, flash, request
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
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # Agregamos el campo 'role'

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
    return 'Panel de administrador'

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