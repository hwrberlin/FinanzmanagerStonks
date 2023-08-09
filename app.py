import os
import os
from flask import Flask, render_template, redirect, url_for, request, flash, session
import db
 Datenbank
from werkzeug.security import generate_password_hash, check_password_hash

#mögliche Datenbankänderung

# ooof
 main
app = Flask(__name__)

app.config.from_mapping(
	SECRET_KEY='secret_key_just_for_dev_environment',
	DATABASE=os.path.join(app.instance_path, 'finance_manager.sqlite')
)
app.cli.add_command(db.init_db)
app.teardown_appcontext(db.close_db_con) # Test


@app.route('/')
def login():
    username = request.args.get('username')
    password = request.args.get('password')

    if username and password:
        db_con = db.get_db_con()
        user = db_con.execute('SELECT * FROM user WHERE username = ?', (username,)).fetchone()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
          #  return redirect(url_for('index'))
            flash('erfolgreicher login')

        else:
            flash('Incorrect username or password')

    return render_template('login.html') # HTML muss noch gecodet werden

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if not password == confirm_password:
            flash('Die Passwörter stimmen nicht überein!')
            return render_template('signup.html')

        if username and password:
            db_con = db.get_db_con()

            # Gibt es den Benutzer bereits?
            user = db_con.execute('SELECT id FROM user WHERE username = ?', (username,)).fetchone() 
            if user:
                flash('Benutzername schon vergeben!')
            else:
                db_con.execute(
                    'INSERT INTO user (username, password) VALUES (?, ?)',
                    (username, generate_password_hash(password))
                )
                db_con.commit()
                return redirect(url_for('login'))

    return render_template('signup.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

#@app.route('/')
#def index():
#    return render_template('login.html')






# app.run()











# Alt

@app.route('/lists/<int:list_id>')
def get_list_todos(list_id):
	sql_query_1 = f'SELECT name FROM list WHERE id={list_id}'
	sql_query_2 = (
		'SELECT id, complete, description FROM todo '
		f'JOIN todo_list ON todo_id=todo.id AND list_id={list_id} '
		'ORDER BY id;'
	)
	db_con = db.get_db_con()
	list = {}
	list['name'] = db_con.execute(sql_query_1).fetchone()['name']
	list['todos'] = db_con.execute(sql_query_2).fetchall()
	if request.args.get('json') is not None:
		list['todos'] = [dict(todo) for todo in list['todos']]
		return list
	else:
		return render_template('todos.html', list=list)

@app.route('/insert/sample')
def run_insert_sample():
	db.insert_sample()
	return 'Database flushed and populated with some sample data.'