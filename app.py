import sqlite3
from flask import Flask, request, jsonify, render_template
from datetime import datetime

app = Flask(__name__)
DB_NAME = 'expenses.db'

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            note TEXT
        )''')
        
init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/expenses', methods=['GET', 'POST'])
def handle_expenses():
    if request.method == 'POST':
        data = request.json
        
        # THIS IS THE FIXED LINE: 
        # Using .get('title', '').strip() prevents users from submitting "   " as a title
        if not data.get('title', '').strip() or not data.get('amount') or not data.get('category'):
            return jsonify({'error': 'Missing required fields or blank title'}), 400
            
        try:
            amount = float(data['amount'])
            if amount <= 0: return jsonify({'error': 'Amount must be positive'}), 400
        except ValueError:
            return jsonify({'error': 'Invalid amount'}), 400
            
        date = data.get('date') or datetime.today().strftime('%Y-%m-%d')
        
        with get_db() as conn:
            cur = conn.cursor()
            cur.execute('INSERT INTO expenses (title, amount, category, date, note) VALUES (?, ?, ?, ?, ?)',
                        (data['title'].strip(), amount, data['category'], date, data.get('note', '')))
            conn.commit()
            return jsonify({'id': cur.lastrowid}), 201

    # GET Method with Filtering
    query = "SELECT * FROM expenses WHERE 1=1"
    params = []
    
    category = request.args.get('category')
    if category:
        query += " AND category = ?"
        params.append(category)
        
    start_date = request.args.get('start_date')
    if start_date:
        query += " AND date >= ?"
        params.append(start_date)
        
    end_date = request.args.get('end_date')
    if end_date:
        query += " AND date <= ?"
        params.append(end_date)
        
    search = request.args.get('search')
    if search:
        query += " AND title LIKE ?"
        params.append(f"%{search}%")
        
    query += " ORDER BY date DESC, id DESC"
    
    with get_db() as conn:
        expenses = conn.execute(query, params).fetchall()
        return jsonify([dict(row) for row in expenses])

@app.route('/api/expenses/<int:id>', methods=['PUT', 'DELETE'])
def handle_expense(id):
    if request.method == 'DELETE':
        with get_db() as conn:
            conn.execute('DELETE FROM expenses WHERE id = ?', (id,))
            conn.commit()
        return '', 204
        
    if request.method == 'PUT':
        data = request.json
        with get_db() as conn:
            conn.execute('UPDATE expenses SET title=?, amount=?, category=?, date=?, note=? WHERE id=?',
                         (data['title'], float(data['amount']), data['category'], data['date'], data.get('note', ''), id))
            conn.commit()
        return '', 204

@app.route('/api/summary')
def summary():
    current_month = datetime.today().strftime('%Y-%m')
    with get_db() as conn:
        total = conn.execute("SELECT SUM(amount) FROM expenses WHERE date LIKE ?", (f"{current_month}%",)).fetchone()[0] or 0
        breakdown = conn.execute("SELECT category, SUM(amount) as total FROM expenses WHERE date LIKE ? GROUP BY category", (f"{current_month}%",)).fetchall()
        
    return jsonify({
        'total': total,
        'breakdown': [dict(row) for row in breakdown]
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)