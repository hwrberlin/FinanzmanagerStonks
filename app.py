import os
from flask import Flask, render_template, redirect, url_for, request
import db
#MOIN Kekw 123
app = Flask(__name__)

app.config.from_mapping(
	SECRET_KEY='secret_key_just_for_dev_environment',
	DATABASE=os.path.join(app.instance_path, 'todos.sqlite')
)
app.cli.add_command(db.init_db)
app.teardown_appcontext(db.close_db_con) #TEST

@app.route('/')
def index():
	return redirect(url_for('get_lists'))

@app.route('/lists/')
def get_lists():
	sql_query = 'SELECT * from list ORDER BY name'
	db_con = db.get_db_con()
	lists_temp = db_con.execute(sql_query).fetchall()
	lists = []
	for list_temp in lists_temp:
		list = dict(list_temp)
		sql_query = (
			'SELECT COUNT(complete) = SUM(complete) '
			'AS complete FROM todo '
			f'JOIN todo_list ON list_id={list["id"]} '
				'AND todo_id=todo.id; '
		)
		complete = db_con.execute(sql_query).fetchone()['complete']
		list['complete'] = complete
		lists.append(list)
	if request.args.get('json') is not None:
		return lists
	else:
		return render_template('lists.html', lists=lists)

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