import datetime
from flask import Flask, abort, flash, jsonify, render_template, request, redirect, url_for, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import mysql.connector

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'

login_manager = LoginManager()
login_manager.init_app(app)


class Usuario(UserMixin):
    def __init__(self, id:str, username:str, password:str, role:str):
        self.id = id
        self.username = username
        self.password = password
        self.role = role

    
class Producto:
    def __init__(self, id:str, nombre:str, precio:str, cantidad_disponible:int):
        self.codigo_barras = id
        self.nombre = nombre
        self.precio = precio
        self.existencia = cantidad_disponible


@login_manager.user_loader
def load_user(user_id):
    # Aquí deberías buscar y retornar el usuario desde tu base de datos utilizando el ID
    # Por ejemplo, puedes usar una consulta SQL para buscar el usuario en la base de datos
    conexion = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='appflask'
    )
    cursor = conexion.cursor()

    cursor.execute('SELECT * FROM login WHERE id = %s', (user_id,))
    usuario_data = cursor.fetchone()

    if usuario_data:
        usuario = Usuario(usuario_data[0], usuario_data[1], usuario_data[2], usuario_data[3])
        return usuario
    else:
        return None


@app.route('/', methods=['GET', 'POST'])
def inicio():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conexion = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
            database='appflask'
        )
        cursor = conexion.cursor()
        
        cursor.execute('SELECT * FROM login WHERE username = %s AND password = %s', (username, password))
        usuario_data = cursor.fetchone()
        if usuario_data:
            usuario = Usuario(usuario_data[0], usuario_data[1], usuario_data[2], usuario_data[3])
            login_user(usuario)
            cursor.close()
            conexion.close()
            
            # Verificar el rol del usuario y redirigir a la página correspondiente
            if usuario_data[3] == 'Administrador':
                return redirect(url_for('admin_page'))
            elif usuario_data[3] == 'Cajero':
                return redirect(url_for('cajero_page'))
            elif usuario_data[3] == 'Cliente':
                return redirect(url_for('cliente_page'))
        else:
            cursor.close()
            conexion.close()
            error = 'Usuario y/o contraseña incorrectos'
    return render_template('login.html', error=error)


@app.route('/admin')
@login_required
def admin_page():
    if current_user.is_authenticated and current_user.role == 'Administrador':
        return render_template('panelAdmin.html')
    else:
        return abort(401, description="No tienes permisos para acceder a esta página.")


@app.route('/cajero')
@login_required
def cajero_page():
    verificar_rol_cajero()
    return render_template('cajero.html')
    


@app.route('/cliente')
@login_required
def cliente_page():
    if current_user.is_authenticated and current_user.role == 'Cliente':
        return render_template('cliente.html')
    else:
        return abort(401, description="No tienes permisos para acceder a esta página.")


@app.route('/vender', methods=['GET', 'POST'])
@login_required
def vender():
    verificar_rol_cajero()
    error = None
    carrito = []
    total = 0.0
    if 'carrito' not in session:
        session['carrito'] = []
    if request.method == 'POST':
        
        # Aquí deberías procesar la venta y guardar la información en la base de datos
        # Por ejemplo, puedes obtener los datos del formulario y guardarlos en la base de datos
        # utilizando una consulta SQL
        codigo_barras = request.form['codigo-barras']
        cantidad = int(request.form['cantidad'])

        # buscar el producto en la base de datos
        conexion = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
            database='appflask'
        )

        cursor = conexion.cursor()
        
        cursor.execute('SELECT * FROM productos WHERE id = %s', (codigo_barras,))
        producto_data = cursor.fetchone()

        if producto_data:
            producto = Producto(producto_data[0], producto_data[1], producto_data[2], producto_data[3])
            cursor.close()
            conexion.close()
            carrito = session['carrito']
            # Verificar si el producto ya está en el carrito
            encontrado = False
            for item in carrito:
                if item['nombre'] == producto.nombre:
                    encontrado = True
                    cantidad_en_carrito = item['cantidad']
                    cantidad_total = cantidad_en_carrito + cantidad
                    if cantidad_total <= producto.existencia:
                        item['cantidad'] = cantidad_total
                        session['carrito'] = carrito
                    else:
                        error = 'No hay suficiente cantidad disponible, la cantidad máxima de ' + producto.nombre + ' es ' + str(producto.existencia)
                        total = sum(producto['precio'] * producto['cantidad'] for producto in carrito)
                        return render_template('vender.html', error=error, carrito=carrito, total=total, enumerate=enumerate)
                    # error = 'El producto ya está en el carrito'
                    total = sum(producto['precio'] * producto['cantidad'] for producto in carrito)
                    return render_template('vender.html', error=error, carrito=carrito, total=total, enumerate=enumerate)
            
            # verificar si hay suficiente cantidad disponible
            if producto.existencia >= cantidad:
                # Ejemplo de cómo agregar un producto al carrito con nombre y precio
                producto = {'nombre': producto.nombre, 'cantidad': cantidad, 'precio': producto.precio}
                carrito = session['carrito']
                carrito.append(producto)
                session['carrito'] = carrito
                total = sum(producto['precio'] * producto['cantidad'] for producto in carrito)
                total = round(total, 2)
                
            else:
                error = 'No hay suficiente cantidad disponible, la cantidad máxima de ' + producto.nombre + ' es ' + str(producto.existencia)
        else:
            cursor.close()
            conexion.close()
            carrito = session['carrito']
            total = sum(producto['precio'] * producto['cantidad'] for producto in carrito)
            total = round(total, 2)
            error = 'Producto no encontrado'
    carrito = session['carrito']
    total = sum(producto['precio'] * producto['cantidad'] for producto in carrito)
    return render_template('vender.html', error=error, carrito=carrito, total=total, enumerate=enumerate)


@app.route('/limpiar_carrito', methods=['GET'])
@login_required
def limpiar_carrito():
    verificar_rol_cajero()
    if 'carrito' in session:
        # Vaciar el carrito en la sesión del usuario
        session['carrito'] = []
    return redirect(url_for('vender'))  # Redirige de vuelta a la página de vender después de limpiar el carrito


@app.route('/delete/<int:index>', methods=['GET'])
@login_required
def delete_from_cart(index):
    verificar_rol_cajero()
    if 'carrito' in session:
        carrito = session['carrito']
        if 0 <= index < len(carrito):
            del carrito[index]  # Elimina el producto del carrito en el índice especificado
            session['carrito'] = carrito
    return redirect(url_for('vender'))  # Redirige de vuelta a la página de vender después de eliminar


@app.route('/update/<int:index>', methods=['GET', 'POST'])
@login_required
def update_from_cart(index):
    verificar_rol_cajero()
    if request.method == 'GET':
        if 'carrito' in session:
            carrito = session['carrito']
            if 0 <= index < len(carrito):
                producto = carrito[index]
                return render_template('update.html', producto=producto, index=index)
        # Si el producto no se encuentra en el carrito o la sesión del carrito no está disponible, redirecciona al usuario a otra página.
        return redirect(url_for('vender'))
    else:
        if 'carrito' in session:
            carrito = session['carrito']
            if 0 <= index < len(carrito):
                producto = carrito[index]
                cantidad = int(request.form['cantidad'])
                # # verificar si hay suficiente cantidad disponible
                conexion = mysql.connector.connect(
                    host='localhost',
                    user='root',
                    password='root',
                    database='appflask'
                )

                cursor = conexion.cursor()

                cursor.execute('SELECT * FROM productos WHERE nombre = %s', (producto['nombre'],))

                producto_data = cursor.fetchone()

                if producto_data:
                    producto = Producto(producto_data[0], producto_data[1], producto_data[2], producto_data[3])
                    cursor.close()
                    conexion.close()

                    if producto.existencia >= cantidad:
                        carrito[index]['cantidad'] = cantidad
                        session['carrito'] = carrito
                    else:
                        error = 'No hay suficiente cantidad disponible, la cantidad máxima de ' + producto.nombre + ' es ' + str(producto.existencia)
                        return render_template('update.html', producto=producto, index=index, error=error)
                else:
                    cursor.close()
                    conexion.close()
        return redirect(url_for('vender'))


@app.route('/finalizar_venta', methods=['GET'])
@login_required
def finalizar_venta():
    verificar_rol_cajero()
    carrito = session['carrito']
    if carrito == []:
        error = 'No hay productos en el carrito'
        return render_template('vender.html', error=error, carrito=carrito, total=0.0, enumerate=enumerate)
    total = sum(producto['precio'] * producto['cantidad'] for producto in carrito)
    total = round(total, 2)
    return render_template('cobrar.html', total=total, carrito=carrito, enumerate=enumerate, cambio = 0.0)


@app.route('/calcular_cambio', methods=['POST'])
@login_required
def calcular_cambio():
    verificar_rol_cajero()
    carrito = session['carrito']
    total = sum(producto['precio'] * producto['cantidad'] for producto in carrito)
    total = round(total, 2)
    efectivo = float(request.form['monto_recibido'])
    cambio = efectivo - total
    return render_template('cobrar.html', total=total, carrito=carrito, enumerate=enumerate, cambio=cambio)

@app.route('/fin_venta', methods=['GET'])
@login_required
def fin_venta():
    verificar_rol_cajero()
    carrito = session['carrito']
    total = sum(producto['precio'] * producto['cantidad'] for producto in carrito)
    total = round(total, 2)
    # Aquí deberías procesar la venta y guardar la información en la base de datos
    # Por ejemplo, puedes obtener los datos del formulario y guardarlos en la base de datos

    # Ejemplo de cómo guardar la venta en la base de datos
    conexion = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
            database='appflask'
        )
    
    cursor = conexion.cursor()
    fecha_actual = datetime.datetime.now()
    # Formatear la fecha y hora en el formato deseado
    fecha_formateada = fecha_actual.strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('INSERT INTO ventas (total, fecha) VALUES (%s, %s)', (total, fecha_formateada))
    venta_id = cursor.lastrowid
    for producto in carrito:
        cursor.execute('INSERT INTO ventas_productos (venta_id, producto_id, cantidad, fecha) VALUES (%s, %s, %s, %s)', (venta_id, producto['nombre'], producto['cantidad'], fecha_formateada))
        cursor.execute('UPDATE productos SET cantidad_disponible = cantidad_disponible - %s WHERE nombre = %s', (producto['cantidad'], producto['nombre']))
    conexion.commit()
    cursor.close()
    conexion.close()
    carrito = []
    session['carrito'] = []
    mensaje = 'Venta realizada con éxito'
    return render_template('vender.html', mensaje=mensaje, carrito=carrito, total=0.0, enumerate=enumerate)

@app.route('/gestion_usuario')
@login_required
def gestion_usuario():
    verificar_rol_admin()
    conexion = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='appflask'
    )
    cursor = conexion.cursor()
    cursor.execute('SELECT * FROM login')
    usuarios = cursor.fetchall()
    cursor.close()
    conexion.close()
    return render_template('gestion_usuario.html', usuarios=usuarios)

@app.route('/agregar_usuario', methods=['GET', 'POST'])
@login_required
def agregar_usuario():
    verificar_rol_admin()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        conexion = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
            database='appflask'
        )
        cursor = conexion.cursor()

        # Verificar si ya está registrado el usuario
        cursor.execute('SELECT * FROM login WHERE username = %s', (username,))
        usuario_data = cursor.fetchone()
        if usuario_data:
            flash('El nombre de usuario ya existe', 'warning')
            return render_template('agregar_usuario.html')
        cursor.execute('INSERT INTO login (username, password, role) VALUES (%s, %s, %s)', (username, password, role))
        conexion.commit()
        cursor.close()
        conexion.close()
        flash('Usuario agregado correctamente', 'success')
        return render_template('agregar_usuario.html')
    return render_template('agregar_usuario.html')


@app.route('/modificar_usuario', methods=['GET', 'POST'])
@login_required
def modificar_usuario():
    verificar_rol_admin()
    conexion = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='appflask'
    )
    cursor = conexion.cursor()
    cursor.execute('SELECT * FROM login')
    usuarios = cursor.fetchall()
    cursor.close()
    conexion.close()
    if request.method == 'POST':
        usuario_seleccionado = request.form['username']
        conexion = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='appflask'
        )
        cursor = conexion.cursor()
        opcion = request.form['opcion']
        if opcion == 'nombre':
            nuevo_nombre = request.form['new_username']
            cursor.execute('UPDATE login SET username = %s WHERE id = %s', (nuevo_nombre, usuario_seleccionado))
            conexion.commit()
            cursor.close()
            conexion.close()
            flash('Nombre de usuario modificado correctamente', 'success')
            return redirect(url_for('modificar_usuario'))
        elif opcion == 'contraseña':
            nueva_contraseña = request.form['new_password']
            cursor.execute('UPDATE login SET password = %s WHERE id = %s', (nueva_contraseña, usuario_seleccionado))
            conexion.commit()
            cursor.close()
            conexion.close()
            flash('Contraseña modificada correctamente', 'success')
            return redirect(url_for('modificar_usuario'))
    return render_template('modificar_usuario.html', usuarios=usuarios)


@app.route('/eliminar_usuario', methods=['GET', 'POST'])
@login_required
def eliminar_usuario():
    verificar_rol_admin()
    conexion = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='appflask'
    )
    cursor = conexion.cursor()
    cursor.execute('SELECT * FROM login')
    usuarios = cursor.fetchall()
    cursor.close()
    conexion.close()
    if request.method == 'POST':
        usuario_seleccionado = request.form['username']
        conexion = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='appflask'
        )
        cursor = conexion.cursor()
        cursor.execute('DELETE FROM login WHERE id = %s', (usuario_seleccionado,))
        conexion.commit()
        cursor.close()
        conexion.close()
        flash('Usuario eliminado correctamente', 'success')
        return redirect(url_for('eliminar_usuario'))
    return render_template('eliminar_usuario.html', usuarios=usuarios)


# Ruta para cerrar sesión
@app.route('/logout')
@login_required
def logout():
    session.pop('carrito', None)
    logout_user()
    return redirect(url_for('inicio'))


def verificar_rol_cajero():
    if not current_user.is_authenticated or current_user.role != 'Cajero':
        abort(401, description="No tienes permisos para acceder a esta página.")

def verificar_rol_admin():
    if not current_user.is_authenticated or current_user.role != 'Administrador':
        abort(401, description="No tienes permisos para acceder a esta página.")


# Manejador para errores 404
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', url=request.url), 404


# Manejador para errores 401
@app.errorhandler(401)
def page_not_found(error):
    logout_user()
    return render_template('401.html', url=request.url), 401


if __name__ == "__main__":
    app.run(debug=True, port=5000, host='0.0.0.0')