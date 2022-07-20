from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_mysqldb import MySQL, MySQLdb
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.secret_key = "projectfinalCS50"

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'todoapp'
mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if not request.form.get('username'):
            flash('Nombre de usuario es requerido', 'danger')
        elif not request.form.get('email'):
            flash('Correo electrónico es requerido', 'danger')
        elif not request.form.get('password'):
            flash('Contraseña es requerida', 'danger')        
        elif not request.form.get('confirm_password'):
            flash('Confirma tu contraseña', 'danger')
        elif request.form.get('password') != request.form.get('confirm_password'):
            flash('Las contraseñas no coinciden', 'danger')
        else:
            email = request.form.get('email')
            username = request.form.get('username')
            password = request.form.get('password')
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute("SELECT * FROM users WHERE email = %s", (email,))
            correos = cur.fetchall()
            if len(correos) >= 1:
                flash('Este correo ya existe', 'danger')
            else:
                cur.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, generate_password_hash(password)))
                mysql.connection.commit()
                cur.close()
                flash('Usuario creado correctamente', 'success')
                return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)