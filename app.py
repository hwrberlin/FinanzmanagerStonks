import os
import os
from flask import Flask, render_template, redirect, url_for, request, flash, session
import db

from werkzeug.security import generate_password_hash, check_password_hash

#mögliche Datenbankänderung

# ooof
 
app = Flask(__name__)

app.config.from_mapping(
	SECRET_KEY='secret_key_just_for_dev_environment',
	DATABASE=os.path.join(app.instance_path, 'finance_manager.sqlite')
)
app.cli.add_command(db.init_db)
app.teardown_appcontext(db.close_db_con) # Test

"""
@app.route('/')
def login():
    username = request.args.get('username')
    password = request.args.get('password')

    if username and password:
        db_con = db.get_db_con()
        user = db_con.execute('SELECT * FROM user WHERE username = ?', (username,)).fetchone()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            return redirect(url_for('homepage'))
            flash('erfolgreicher login')

        else:
            flash('Incorrect username or password')

    return render_template('login_signup.html') # HTML muss noch gecodet werden
"""
@app.route('/', methods=['GET', 'POST'])
def login():
    session.clear() # ausloggungsfunktion, falls man sich nicht ausloggt per knopf
    if request.method == 'POST':
        action = request.form.get('action')

        username = request.form.get('username')
        password = request.form.get('password')
        db_con = db.get_db_con()

        if action == 'login':
            user = db_con.execute('SELECT * FROM user WHERE username = ?', (username,)).fetchone()
            
            if user and check_password_hash(user['password'], password):
                session['user_id'] = user['id']
                return redirect(url_for('homepage'))
            else:
                flash('Falscher Benutzername oder Passwort!')

        elif action == 'register':
            confirm_password = request.form.get('confirm_password')

            if not password == confirm_password:
                flash('Die Passwörter stimmen nicht überein!')
            else:
                # Überprüfen, ob der Benutzer bereits existiert
                existing_user = db_con.execute('SELECT id FROM user WHERE username = ?', (username,)).fetchone() 
                if existing_user:
                    flash('Benutzername schon vergeben!')
                else:
                    db_con.execute(
                        'INSERT INTO user (username, password) VALUES (?, ?)',
                        (username, generate_password_hash(password))
                    )
                    db_con.commit()
                    flash('Erfolgreich registriert. Bitte anmelden.')
                    return redirect(url_for('login'))

    return render_template('login_signup.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/get_users')
def get_users():
    db_con = db.get_db_con()
    users = db_con.execute('SELECT * FROM user').fetchall()

    output = []
    for user in users:
        user_data = {
            'id': user['id'],
            'username': user['username'],
            'password': user['password'],
            'role': user['role']
        }
        output.append(user_data)

    return {'users': output}

@app.route('/homepage')
def homepage():
    return render_template('homepage.html')

@app.route('/addTransaction', methods=['GET', 'POST'])
def addTransaction():

    user_id = session.get('user_id')
    print(f"Aktuelle Benutzer-ID aus der Session: {user_id}")

    if 'user_id' not in session:
        flash('Du musst eingeloggt sein, um Transaktionen hinzuzufügen.')
        return redirect(url_for('login'))   # funktioniert irgendwie NOCH nicht, statdessen wird die eingabe einfach nicht gespeichert
    
    if request.method == 'POST':
        user_id = session['user_id']
        amount = request.form.get('amount')
        description = request.form.get('description')

        db_con = db.get_db_con()
        db_con.execute(
            'INSERT INTO transactions (user_id, amount, description) VALUES (?, ?, ?)',
            (user_id, amount, description)
        )
        db_con.commit()
        flash('Transaktion erfolgreich hinzugefügt.')  
        return redirect(url_for('addTransaction')) 

    return render_template('addTransaction.html')


@app.route('/get_transactions')
def get_transactions():
    db_con = db.get_db_con()
    transactions = db_con.execute('SELECT * FROM transactions').fetchall()

    output = []
    for transaction in transactions:
        transaction_data = {
            'id': transaction['id'],
            'user_id': transaction['user_id'],
            'amount': transaction['amount'],
            'description': transaction['description']
        }
        output.append(transaction_data)

    return {'transactions': output} 

@app.route('/TransactionOverview')
def TransactionOverview():
    user_id = session.get('user_id')

    if user_id is None:
        flash('Du musst eingeloggt sein, um deine Transaktionen anzusehen.')
        return redirect(url_for('login'))

    db_con = db.get_db_con()
    transactions = db_con.execute(
        'SELECT * FROM transactions WHERE user_id = ? ORDER BY timestamp DESC',
        (user_id,)
    ).fetchall()

    return render_template('TransactionOverview.html', transactions=transactions)

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

@app.route('/budget', methods=['GET', 'POST'])
def budget():
    if 'user_id' not in session:
        flash('Du musst eingeloggt sein, um dein Budget zu verwalten.')
        return redirect(url_for('login'))

    user_id = session['user_id']
    db_con = db.get_db_con()
    budgets = db_con.execute('SELECT * FROM budget WHERE user_id = ?', (user_id,)).fetchall()

    if request.method == 'POST':
        name = request.form.get('budget_name')
        amount = request.form.get('budget_amount')
        end_date = request.form.get('budget_end_date')

        db_con.execute('INSERT INTO budget (user_id, name, amount, end_date) VALUES (?, ?, ?, ?)', (user_id, name, amount, end_date))
        db_con.commit()

        flash(f'Budget "{name}" erfolgreich erstellt.')
        return redirect(url_for('budget'))

    return render_template('budget.html', budgets=budgets)
