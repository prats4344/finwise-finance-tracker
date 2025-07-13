from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from collections import defaultdict
import os

app = Flask(__name__)
app.secret_key = 'secret123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ----------------- Models --------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    type = db.Column(db.String(20))  # 'investment' or 'expense'
    category = db.Column(db.String(100))
    amount = db.Column(db.Float)
    date = db.Column(db.Date)

# ----------------- Routes --------------------
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        if User.query.filter_by(username=username).first():
            return 'Username already exists!'
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        session['user_id'] = user.id
        return redirect('/dashboard')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['user_id'] = user.id
            return redirect('/dashboard')
        else:
            return 'Invalid credentials!'
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')

    user_id = session['user_id']

    if request.method == 'POST':
        type_ = request.form['type']
        category = request.form['category'].strip()
        amount = float(request.form['amount'])
        date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
        transaction = Transaction(user_id=user_id, type=type_, category=category, amount=amount, date=date)
        db.session.add(transaction)
        db.session.commit()

    transactions = Transaction.query.filter_by(user_id=user_id).order_by(Transaction.date.asc()).all()

    # Separate investments and expenses
    investments = [t for t in transactions if t.type == 'investment']
    expenses = [t for t in transactions if t.type == 'expense']

    # Group by category for summary
    def group_sum(items):
        summary = {}
        for i in items:
            summary[i.category] = summary.get(i.category, 0) + i.amount
        return summary

    investment_summary = group_sum(investments)
    expense_summary = group_sum(expenses)

    # Calculate total investments and expenses
    total_investments = sum(t.amount for t in investments)
    total_expenses = sum(t.amount for t in expenses)
    total_savings = total_investments - total_expenses

    # Line chart data
    date_labels = sorted(list(set([t.date.strftime('%Y-%m-%d') for t in transactions])))
    investment_by_date = {d: 0 for d in date_labels}
    expense_by_date = {d: 0 for d in date_labels}

    for t in investments:
        investment_by_date[t.date.strftime('%Y-%m-%d')] += t.amount
    for t in expenses:
        expense_by_date[t.date.strftime('%Y-%m-%d')] += t.amount

    # Calculate savings by date (investment - expense)
    savings_by_date = []
    for d in date_labels:
        savings_by_date.append(investment_by_date[d] - expense_by_date[d])

    # Prepare date-wise summary dict for template
    date_summary = defaultdict(lambda: {'investment': 0, 'expense': 0, 'savings': 0})
    for d in date_labels:
        inv_amt = investment_by_date.get(d, 0)
        exp_amt = expense_by_date.get(d, 0)
        sav_amt = inv_amt - exp_amt
        date_summary[d]['investment'] = inv_amt
        date_summary[d]['expense'] = exp_amt
        date_summary[d]['savings'] = sav_amt

    return render_template('dashboard.html',
                           investments=investments,
                           expenses=expenses,
                           investment_summary=investment_summary,
                           expense_summary=expense_summary,
                           total_investments=total_investments,
                           total_expenses=total_expenses,
                           total_savings=total_savings,
                           date_labels=date_labels,
                           investment_data=list(investment_by_date.values()),
                           expense_data=list(expense_by_date.values()),
                           savings_data=savings_by_date,
                           date_summary=date_summary)

# Create database tables if they don't exist yet
if __name__ == '__main__':
    if not os.path.exists('data.db'):
        with app.app_context():
            db.create_all()
    app.run(debug=True)


















