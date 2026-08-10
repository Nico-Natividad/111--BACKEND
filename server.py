from datetime import date
from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

DB_NAME = 'budget_manager.db'

def init_db():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS budgets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            amount INTEGER NOT NULL,
            date TEXT NOT NULL,
            category TEXT NOT NULL,
            user_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    connection.commit()
    connection.close()

@app.post('/api/users')
def register():
    new_user = request.get_json()

    username = new_user['username']
    password = new_user['password']

    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
    connection.commit()
    connection.close()
    
    return jsonify({
        'success': True,
        'message': 'User created successfully'
    }), 201

@app.get('/api/health')
def health_check():
    return jsonify({
        'status': 'OK'
    }), 200

@app.get('/api/users')
def get_users():
    connection = sqlite3.connect(DB_NAME)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute('SELECT id, username FROM users')
    rows = cursor.fetchall()
    connection.close()

    users = []
    for row in rows:
        print(row)
        users.append(dict(row))

    return jsonify({
        'success': True,
        'message': 'Users retrieved successfully',
        'data': users
    }), 200

@app.post('/api/expenses')
def create_expense():
    new_expense = request.get_json()

    title = new_expense['title']
    description = new_expense['description']
    amount = new_expense['amount']
    date_expense = str(date.today())
    category = new_expense['category']
    user_id = new_expense['user_id']

    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute('''
        INSERT INTO budgets (title, description, amount, date, category, user_id)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (title, description, amount, date_expense, category, user_id))

    connection.commit()
    connection.close()
    
    return jsonify({
        'success': True,
        'message': 'Expense created successfully'
    }), 201

init_db()
app.run(debug=True)