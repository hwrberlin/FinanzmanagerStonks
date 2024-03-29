import os
from flask import Flask, render_template, redirect, url_for, request, flash, session, jsonify
import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


 
app = Flask(__name__)

app.config.from_mapping(
	SECRET_KEY='secret_key_just_for_dev_environment',
	DATABASE=os.path.join(app.instance_path, 'finance_manager.sqlite')
)
app.cli.add_command(db.init_db)
app.cli.add_command(db.insert_sample)
app.teardown_appcontext(db.close_db_con) 

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
                session['user_role'] = user['role']
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

"wir hatten hier eine get users route, um immer wieder beim testen alle Nutzer auszugeben"

@app.route('/homepage')
def homepage():
   

    user_id = session.get('user_id')
    user_role = session.get('user_role')  

    if user_id is None:
        flash('Du musst eingeloggt sein, um die Homepage zu sehen.')
        return redirect(url_for('login'))

    db_con = db.get_db_con()
    transactions = db_con.execute(
        'SELECT id, user_id, amount, description, DATE(timestamp) as date, transaction_type, category, kontostand FROM transactions WHERE user_id = ? ORDER BY timestamp DESC LIMIT 5',
        (user_id,)
    ).fetchall()
    
    budgets = db_con.execute('SELECT * FROM budget WHERE user_id = ?', (user_id,)).fetchall()


    current_balance = db_con.execute(
    'SELECT kontostand FROM transactions WHERE user_id = ? ORDER BY id DESC LIMIT 1',
    (user_id,)
    ).fetchone()
    
    if current_balance is None:
        current_balance = 0
    else:
        current_balance = current_balance['kontostand']

    account_balance_data = db_con.execute(
        'SELECT kontostand, timestamp FROM transactions WHERE user_id = ? ORDER BY timestamp ASC',
        (user_id,)
    ).fetchall()
    dates = [entry['timestamp'] for entry in account_balance_data]
    
    balances = [entry['kontostand'] for entry in account_balance_data]

    return render_template('homepage.html', transactions=transactions, user_role = user_role, budgets = budgets, current_balance=current_balance, dates=dates, balances=balances)


@app.route('/addTransaction', methods=['GET', 'POST'])
def addTransaction():
    user_id = session.get('user_id')
    print(f"Aktuelle Benutzer-ID aus der Session: {user_id}")

    if 'user_id' not in session:
        flash('Du musst eingeloggt sein, um Transaktionen hinzuzufügen.')
        return redirect(url_for('login'))   
    
    if request.method == 'POST':
        user_id = session['user_id']
        amount = float(request.form.get('amount'))
        description = request.form.get('description')
        transaction_type = request.form.get('transaction_type')
        category = request.form.get('category')  #toggle button (Finanzkategorie)

        db_con = db.get_db_con()

        # aktuellen Kontostand des Benutzers abrufen
        current_balance = db_con.execute(
            'SELECT kontostand FROM transactions WHERE user_id = ? ORDER BY id DESC LIMIT 1',
            (user_id,)
        ).fetchone()
        
        if current_balance is None:
            current_balance = 0
        else:
            current_balance = current_balance['kontostand']

        # Kontostand basierend auf der Transaktion aktualisieren
        if transaction_type == 'einnahme':
            new_balance = current_balance + amount
        elif transaction_type == 'ausgabe':
            new_balance = current_balance - amount
        else:
            flash('Ungültiger Transaktionstyp.')
            return redirect(url_for('addTransaction'))

        # Überprüfen, ob ein Budget für diese Kategorie existiert
        budget = db_con.execute('SELECT * FROM budget WHERE user_id = ? AND category = ?', (user_id, category)).fetchone()
        if budget and transaction_type == 'ausgabe':
            remaining_budget = float(budget['amount']) - amount
            db_con.execute('UPDATE budget SET amount = ? WHERE user_id = ? AND category = ?', (remaining_budget, user_id, category))
            db_con.commit()

        db_con.execute(
            'INSERT INTO transactions (user_id, amount, description, transaction_type, category, kontostand) VALUES (?, ?, ?, ?, ?, ?)',
            (user_id, amount, description, transaction_type, category, new_balance)  
        )
        db_con.commit()
        flash('Transaktion erfolgreich hinzugefügt.')  
        return redirect(url_for('homepage')) 
        
        

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
            'description': transaction['description'],
            'transaction_type': transaction['transaction_type'],
            'category': transaction['category'],
            'kontostand': transaction['kontostand']
        }
        output.append(transaction_data)

    return {'transactions': output} 

"wir hatten hier eine get transaction route, um immer wieder beim testen alle Transactionen auszugeben"


@app.route('/TransactionOverview')
def TransactionOverview():
    user_id = session.get('user_id')

    if user_id is None:
        flash('Du musst eingeloggt sein, um deine Transaktionen anzusehen.')
        return redirect(url_for('login'))

    db_con = db.get_db_con()
    transactions = db_con.execute(
        'SELECT id, user_id, amount, description, DATE(timestamp) as date, transaction_type, category, kontostand FROM transactions WHERE user_id = ? ORDER BY timestamp DESC',
        (user_id,)
    ).fetchall()

    return render_template('TransactionOverview.html', transactions=transactions)

@app.route('/delete_transaction/<int:id>', methods=['POST'])
def delete_transaction(id):
    next_url = request.form.get('next_url')
    user_id = session.get('user_id')
    if user_id is None:
        flash('Du musst eingeloggt sein, um Transaktionen zu löschen.')
        return redirect(url_for('login'))

    db_con = db.get_db_con()
    
    transaction_to_delete = db_con.execute(
        'SELECT * FROM transactions WHERE id = ? AND user_id = ?',
        (id, user_id)
    ).fetchone()

    if transaction_to_delete is None:
        flash('Transaktion nicht gefunden oder du hast nicht die Berechtigung, sie zu löschen.')
        return redirect(url_for('TransactionOverview'))
    
    # Kontostand
    current_balance = transaction_to_delete['Kontostand']

    # Aktualisieren des Kontostandes
    if transaction_to_delete['transaction_type'] == 'einnahme':
        new_balance = current_balance - transaction_to_delete['amount']
    else:
        new_balance = current_balance + transaction_to_delete['amount']

    if new_balance is None:
        new_balance = 0
        
    # Aktualisieren des Kontostandes in der Datenbank
    db_con.execute(
        'UPDATE transactions SET Kontostand = ? WHERE id = ?', (new_balance, id)
    )

    # Löschen
    db_con.execute('DELETE FROM transactions WHERE id = ?', (id,))
    db_con.commit()

    # Aktualisieren des Kontostandes für alle nachfolgenden Transaktionen
    subsequent_transactions = db_con.execute(
        'SELECT * FROM transactions WHERE user_id = ? AND timestamp > ? ORDER BY timestamp ASC',
        (user_id, transaction_to_delete['timestamp'])
    ).fetchall()

    for transaction in subsequent_transactions:
        if transaction['transaction_type'] == 'einnahme':
            new_balance += transaction['amount']
        else:
            new_balance -= transaction['amount']

        db_con.execute(
            'UPDATE transactions SET Kontostand = ? WHERE id = ?', (new_balance, transaction['id'])
        )
    
    from datetime import datetime

    from datetime import datetime

    # Anpassen des Budgets
    budget = db_con.execute(
        'SELECT * FROM budget WHERE user_id = ? AND category = ?',
        (user_id, transaction_to_delete['category'])
    ).fetchone()

    if budget and transaction_to_delete['transaction_type'] == 'ausgabe':
        budget_creation_timestamp = datetime.strptime(budget['created_at'], '%Y-%m-%d %H:%M:%S')
        transaction_timestamp = datetime.strptime(transaction_to_delete['timestamp'], '%Y-%m-%d %H:%M:%S')

        # Debug-Informationen
        print(f"Budget-Erstellungszeitstempel: {budget_creation_timestamp}")
        print(f"Transaktionszeitstempel: {transaction_timestamp}")

        if transaction_timestamp >= budget_creation_timestamp:
            adjusted_budget = float(budget['amount']) + transaction_to_delete['amount']
            db_con.execute(
                'UPDATE budget SET amount = ? WHERE user_id = ? AND category = ?',
                (adjusted_budget, user_id, transaction_to_delete['category'])
            )
            db_con.commit()
            flash('Budget erfolgreich angepasst.')
        else:
            flash('Transaktion beeinflusst nicht das Budget.')




    
    db_con.commit()
    flash('Transaktion erfolgreich gelöscht!')

    if next_url:
        return redirect(next_url)
    else:
        return redirect(url_for('TransactionOverview'))




@app.route('/Steuerung')
def Steuerung():
    # Admin ja oder nein
    current_user_role = session.get('user_role')
    if current_user_role != 'admin':
        flash('Nur Administratoren dürfen Benutzer verwalten.')
        return redirect(url_for('homepage'))

    db_con = db.get_db_con()
    users = db_con.execute('SELECT * FROM user').fetchall()
    # hier werden alle user gespeichert, um es dann html anzeigen zu lassen
    return render_template('Steuerung.html', users=users)

@app.route('/deleteUser/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    # Prüfe, ob der Benutzer in der Session ein Admin ist
    current_user_id = session.get('user_id')
    current_user_role = session.get('user_role')
    if current_user_role != 'admin':
        flash('Nur Administratoren dürfen Benutzer löschen.')
        return redirect(url_for('Steuerung'))

    db_con = db.get_db_con()
        
    user_to_delete = db_con.execute('SELECT * FROM user WHERE id = ?', (user_id,)).fetchone()

    if current_user_id == user_id:
        flash('Du kannst dich selbst nicht löschen.')
        return redirect(url_for('Steuerung'))
    elif user_to_delete['role'] == 'admin':
        flash('Admins können andere Admins nicht löschen.')
        return redirect(url_for('Steuerung'))
    
    db_con.execute('DELETE FROM transactions WHERE user_id = ?', (user_id,))
    db_con.execute('DELETE FROM budget WHERE user_id = ?', (user_id,))
    db_con.execute('DELETE FROM user WHERE id = ?', (user_id,))
    db_con.commit()

    flash('Benutzer erfolgreich gelöscht.')
    return redirect(url_for('Steuerung')) 


@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if 'user_id' not in session:
        flash('Du musst eingeloggt sein, um dein Profil zu bearbeiten.')
        return redirect(url_for('login'))

    user_id = session['user_id']    
    db_con = db.get_db_con()
    user = db_con.execute('SELECT * FROM user WHERE id = ?', (user_id,)).fetchone()

    # Überprüfen, ob der Benutzer sein Konto löschen möchte
    if request.form.get('delete_request'):
        # Überprüfen, ob der Benutzer ein Administrator ist
        if user['role'] == 'admin':
            flash('Admin-Konten können nicht gelöscht werden.')
            return redirect(url_for('edit_profile'))

        db_con.execute('DELETE FROM transactions WHERE user_id = ?', (user_id,))
        db_con.execute('DELETE FROM budget WHERE user_id = ?', (user_id,))
        db_con.execute('DELETE FROM user WHERE id = ?', (user_id,))
        db_con.commit()
        session.clear()  
        flash('Benutzerkonto erfolgreich gelöscht.')
        return redirect(url_for('login'))

    if request.method == 'POST':
        new_username = request.form.get('new_username')
        password = request.form.get('password')

        # doppelt gesichert (html required und hier)
        if not new_username: 
            flash('Neuer Benutzername muss eingegeben werden.')
            return render_template('edit_profile.html', user=user)

        if not check_password_hash(user['password'], password):
            flash('Falsches Passwort!')
            return render_template('edit_profile.html', user=user)

        # Überprüfen, ob der neue Benutzername bereits existiert
        existing_user = db_con.execute('SELECT id FROM user WHERE username = ?', (new_username,)).fetchone() 
        if existing_user:
            flash('Benutzername schon vergeben!')
        else:
            db_con.execute(
                'UPDATE user SET username = ? WHERE id = ?',
                (new_username, user_id)
            )
            db_con.commit()
            flash('Benutzername erfolgreich aktualisiert!')
            return redirect(url_for('homepage'))
    
    return render_template('edit_profile.html', user=user)



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
        category = request.form.get('budget_category')
        amount = request.form.get('budget_amount')
        end_date = request.form.get('budget_end_date')

        existing_budget = db_con.execute('SELECT * FROM budget WHERE user_id = ? AND category = ?', (user_id, category)).fetchone()

        if existing_budget:
            flash(f'Es gibt bereits ein Budget für die Kategorie "{category}".')
        else:
            db_con.execute('INSERT INTO budget (user_id, category, amount, end_date) VALUES (?, ?, ?, ?)', (user_id, category, amount, end_date))
            db_con.commit()

            flash(f'Budget für Kategorie "{category}" erfolgreich erstellt.')

        return redirect(url_for('homepage'))

    return render_template('budget.html', budgets=budgets)

@app.route('/delete_budget/<int:id>', methods=['POST'])
def delete_budget(id):
    if 'user_id' not in session:
        flash('Du musst eingeloggt sein, um ein Budget zu löschen.')
        return redirect(url_for('login'))

    user_id = session['user_id']
    db_con = db.get_db_con()

    # Make sure that the budget exists and belongs to the logged-in user
    budget = db_con.execute('SELECT * FROM budget WHERE id = ? AND user_id = ?', (id, user_id)).fetchone()

    if not budget:
        flash('Budget nicht gefunden oder gehört nicht zum eingeloggten Benutzer.')
    else:
        # Delete the budget from the database
        db_con.execute('DELETE FROM budget WHERE id = ?', (id,))
        db_con.commit()

        flash(f'Budget für Kategorie "{budget["category"]}" erfolgreich gelöscht.')

    return redirect(url_for('homepage'))



@app.route('/getChartData', methods=['POST'])
def get_chart_data():
    category = request.form.get('category')
    db_con = db.get_db_con()
    user_id = session['user_id']

    if category == 'kontostand':
        transactions = db_con.execute('SELECT timestamp, kontostand FROM transactions WHERE user_id = ? ORDER BY timestamp ASC', (user_id,)).fetchall()
        labels = [str(t[0]) for t in transactions]
        data_values = [t[1] for t in transactions]
    else:
        transactions = db_con.execute('SELECT timestamp, amount FROM transactions WHERE user_id = ? AND category = ? ORDER BY timestamp ASC', (user_id, category)).fetchall()
        labels = [str(t[0]) for t in transactions]
        
        # Berechnen der Summe der Transaktionsbeträge
        cumulative_sum = 0
        cumulative_sums = []
        for t in transactions:
            cumulative_sum += t[1]
            cumulative_sums.append(cumulative_sum)
        data_values = cumulative_sums

    data = {
        'labels': labels,
        'datasets': [
            {
                'label': category,
                'data': data_values,
                'borderColor': 'rgba(75, 192, 192, 1)',
                'fill': False,
            }
        ]
    }

    return jsonify(data)


