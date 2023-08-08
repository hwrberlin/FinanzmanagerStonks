import os
import os
from flask import Flask, render_template, redirect, url_for, request, flash, session
import db
from werkzeug.security import generate_password_hash, check_password_hash

#mögliche Datenbankänderung
app = Flask(__name__)

app.config.from_mapping(
	SECRET_KEY='secret_key_just_for_dev_environment',
	DATABASE=os.path.join(app.instance_path, 'finance_manager.sqlite')
)
app.cli.add_command(db.init_db)
app.teardown_appcontext(db.close_db_con) # Test

@app.route('/')
def index():
	return redirect(url_for('get_lists'))

@app.route('/login')
def login():
    username = request.args.get('username')
    password = request.args.get('password')

    if username and password:
        db_con = db.get_db_con()
        user = db_con.execute('SELECT * FROM user WHERE username = ?', (username,)).fetchone()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            return redirect(url_for('index'))
        else:
            flash('Incorrect username or password')

    return render_template('login.html')

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