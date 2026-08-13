from datetime import date
from flask import Flask, jsonify, request, render_template
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


@app.get("/api/users/<int:user_id>")
def get_user_by_id(user_id):
    print(user_id)
    connection = sqlite3.connect(DB_NAME)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute('SELECT id, username FROM users WHERE id = ?', (user_id,))
    row = cursor.fetchone()
    user_information = dict(row)
  
    print(row)
    connection.close()
    return jsonify({
        'success': True,
        'message': 'User retrieved successfully',
        'data': user_information
    })





@app.get("/api/expenses/<int:user_id>")
def get_expenses_by_user_id(user_id):
    connection = sqlite3.connect(DB_NAME)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
   
    cursor.execute('SELECT * FROM budgets WHERE user_id = ?', (user_id,))
    rows = cursor.fetchall()
    
    if not rows:
        return jsonify({
            'success': False,
            'message': 'Expenses not found'
        }), 404
    
    expenses_information = [dict(row) for row in rows]
    connection.close()

    return jsonify({
        'success': True,
        'message': 'Expenses retrieved successfully',
        'data': expenses_information
    }), 200




# DELETE http://127.0.0.1:5000/api/expenses/<int:expense_id>
@app.delete("/api/expenses/<int:expense_id>")
def delete_expense(expense_id):
    connection = sqlite3.connect(DB_NAME)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute("SELECT id FROM budgets WHERE id = ?", (expense_id,))
    row = cursor.fetchone()

    if not row:
        connection.close()
        return jsonify({
            "success": False,
            "message": "Expense not found"
        }), 404

    cursor.execute("DELETE FROM budgets WHERE id = ?", (expense_id,))
    connection.commit()
    connection.close()

    return jsonify({
        "success": True,
        "message": "Expense deleted successfully"
    }), 200


# UPDATE http://127.0.0.1:5000/api/expenses/<int:expense_id>
@app.put("/api/expenses/<int:expense_id>")
def update_expense(expense_id):
   
    updated_expense = request.get_json()
    title = updated_expense["title"]
    description = updated_expense["description"]
    amount = updated_expense["amount"]
    category = updated_expense["category"]

    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

   
    cursor.execute("SELECT id FROM budgets WHERE id=?", (expense_id,))
    row = cursor.fetchone()

    if not row:
        connection.close()
        return jsonify({
            "success": False,
            "message": "Expense not found"
        }), 404

    cursor.execute(
        "UPDATE budgets SET title=?, description=?, amount=?, category=? WHERE id=?",
        (title, description, amount, category, expense_id)
    )
    connection.commit()
    connection.close()

    return jsonify({
        "success": True,
        "message": "Expense updated successfully"
    }), 200


@app.get("/")
@app.get("/index")
@app.get("/home")
def home():
    my_name= 'NICO'
  
    return render_template("home.html", name=my_name)

@app.get("/contact")
def contact():
    return render_template("contact.html")

@app.get("/about")
def about():
    return render_template("about.html")

@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404

init_db()
app.run(debug=True)