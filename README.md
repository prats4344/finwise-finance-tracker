# 💰 Finwise – Personal Finance Tracker

**Finwise** is a mobile-friendly personal finance tracking web app built with Flask. It allows users to manage their investments and expenses, view financial summaries, and visualize financial trends through interactive charts — all in a clean, responsive interface.

---

## 🚀 Features

- 👤 User registration and login system
- ➕ Add transactions with:
  - Type: Investment or Expense
  - Category, Amount, Date
- 📊 Dashboard with:
  - Total Investments, Expenses, and Net Savings
  - Category-wise and Date-wise summaries
  - Interactive line chart (Green: Investments, Red: Expenses, Blue: Net Savings)
- 📱 Fully responsive design (mobile + desktop)
- 🔐 Built with Flask, SQLite, SQLAlchemy, Chart.js

---


## 📦 Tech Stack

| Layer         | Technology            |
|---------------|------------------------|
| Frontend      | HTML, CSS, Chart.js    |
| Backend       | Python (Flask)         |
| Database      | SQLite + SQLAlchemy    |
| Authentication| Flask Sessions         |

---

## 🛠️ How to Run Locally

```bash
# Clone the repository
git clone https://github.com/prats4344/finwise-finance-tracker.git
cd finwise-finance-tracker

# (Optional) Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the Flask app
python app.py

