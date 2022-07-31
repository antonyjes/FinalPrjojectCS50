from flask import Flask, render_template, request, redirect, session, url_for, flash, jsonify
from flask_mysqldb import MySQL, MySQLdb
from werkzeug.security import generate_password_hash, check_password_hash
from helpers import login_required
import json

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
    if request.method == 'POST':
        if not request.form.get('email'):
            flash('Ingrese su correo electrónico', 'danger')
        elif not request.form.get('password'):
            flash('Ingrese su contraseña', 'danger')
        else:
            email = request.form.get('email')
            password = request.form.get('password')
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cur.fetchone()
            if user and check_password_hash(user['password'], password):
                session['user_id'] = user['id']
                session['user_name'] = user['username']
                session['user_email'] = user['email']
                return redirect(url_for('mainpage'))
            else:
                flash('Email o contraseña incorrectos', 'danger')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/mainpage')
@login_required
def mainpage():
    return render_template('mainpage.html')


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM users WHERE id = %s", (session['user_id'],))
    usuario = cur.fetchone()
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
            cur.execute("SELECT * FROM users WHERE email = %s AND id <> %s", (email, session['user_id'],))
            correos = cur.fetchall()
            if len(correos) >= 1:
                flash('Este correo ya existe', 'danger')
            else:
                cur.execute("UPDATE users SET username = %s, email = %s, password = %s WHERE id = %s", (username, email, generate_password_hash(password), session['user_id']))
                mysql.connection.commit()
                cur.close()
                session['user_name'] = username
                flash('Usuario actualizado correctamente', 'success')
                return redirect(url_for('account'))
    return render_template('account.html', usuario = usuario)


@app.route('/fetchtasks', methods=['GET', 'POST'])
@login_required
def fetchtasks():
    if request.method == 'POST':
        draw = request.form.get('draw')
        row = int(request.form.get('start'))
        rowerpage = int(request.form.get('length'))
        searchValue = request.form.get('search[value]')

        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT count(*) as total FROM tasks WHERE userid = %s", (session['user_id'],))
        rsallcount = cur.fetchone()
        totalRecord = rsallcount['total']

        like = '%' + searchValue + '%'
        cur.execute("SELECT count(*) as total FROM tasks WHERE userid = %s AND (name LIKE %s OR status LIKE %s)", (session['user_id'], like, like))
        rsall = cur.fetchone()
        totalRecordFilter = rsall['total']

        if searchValue == '':
            cur.execute("SELECT * FROM tasks WHERE userid = %s ORDER BY id DESC LIMIT %s, %s", (session['user_id'], row, rowerpage))
            tasklist = cur.fetchall()
        else:
            cur.execute("SELECT * FROM tasks WHERE userid = %s AND (name LIKE %s OR status LIKE %s) ORDER BY id DESC LIMIT %s, %s", (session['user_id'], like, like, row, rowerpage))
            tasklist = cur.fetchall()
        
        data = []

        for row in tasklist:
            data.append({
                'id': row['id'],
                'name': row['name'],
                'status': row['status'],
            })
        
        result = {
            'draw': draw,
            'recordsTotal': totalRecord,
            'recordsFiltered': totalRecordFilter,
            'data': data
        }

        return jsonify(result)


@app.route('/addtask', methods=['GET', 'POST'])
@login_required
def addtask():
    if request.method == 'POST':
        if not request.form.get('task'):
            flash('Nombre de la tarea es requerida', 'danger')
        else:
            name = request.form.get('task')
            status = 'En proceso'
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute("INSERT INTO tasks (name, status, userid) VALUES (%s, %s, %s)", (name, status, session['user_id']))
            mysql.connection.commit()
            cur.close()
            flash('Tarea creada correctamente', 'success')
        
        return redirect(url_for('mainpage'))


@app.route('/selecttask/<int:id>', methods=['GET', 'POST'])
@login_required
def selecttask(id):
    if request.method == 'POST':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM tasks WHERE id = %s AND userid= %s", (id, session['user_id']))
        task = cursor.fetchall()
        taskarray = []
        for result in task:
            task_dict = {
                'id': result['id'],
                'name': result['name'],
                'status': result['status'],
            }
            taskarray.append(task_dict)
        
        return json.dumps(taskarray)

@app.route('/edittask', methods=['GET', 'POST'])
@login_required
def edittask():
    if request.method == 'POST':
        name = request.form.get('task')
        status = request.form.get('status')
        id = request.form.get('id')

        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("UPDATE tasks SET name = %s, status = %s WHERE id = %s AND userid = %s", (name, status, id, session['user_id']))
        mysql.connection.commit()
        cur.close()
        flash('Tarea actualizada correctamente', 'success')
        return redirect(url_for('mainpage'))


@app.route('/deletetask/<int:id>', methods=['GET', 'POST'])
@login_required
def deletetask(id):
    if request.method == 'POST':
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("DELETE FROM tasks WHERE id = %s AND userid = %s", (id, session['user_id']))
        mysql.connection.commit()
        cur.close()
        flash('Tarea eliminada correctamente', 'success')
        return redirect(url_for('mainpage'))

if __name__ == '__main__':
    app.run(debug=True)