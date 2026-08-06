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
    connection.commit()
    connection.close()


@app.post('/api/users')
def register():
    new_user = request.get_json()
    print(new_user)

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

init_db()
app.run(debug=True)