# Minimal Flask app for Vercel
from flask import Flask, render_template_string, request, session, redirect, url_for
import datetime

app = Flask(__name__)
app.secret_key = 'vercel-secret-key'

VALID_USERNAME = 'Admin'
VALID_PASSWORD = 'admin112233'

# Sample data
inventory_data = [
    {'id': '1', 'nama': 'GULA PASIR 1KG', 'jumlah': '50', 'satuan': 'pcs'},
    {'id': '2', 'nama': 'MINYAK MASAK 2KG', 'jumlah': '30', 'satuan': 'botol'},
    {'id': '3', 'nama': 'MINYAK MASAK 5KG', 'jumlah': '20', 'satuan': 'botol'},
    {'id': '4', 'nama': 'TELUR AYAM GRED A', 'jumlah': '100', 'satuan': 'biji'},
    {'id': '5', 'nama': 'TELUR AYAM GRED B', 'jumlah': '100', 'satuan': 'biji'},
]

stats = {
    'total_inventory': len(inventory_data),
    'total_user': 3,
    'total_suplier': 3,
    'total_customer': 3,
    'total_invoice': 3,
}

# Simple login template
LOGIN_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>POS - Login</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Arial, sans-serif; background: linear-gradient(135deg, #667eea, #764ba2); min-height: 100vh; display: flex; align-items: center; justify-content: center; }
        .login-box { background: white; padding: 40px; border-radius: 10px; width: 350px; box-shadow: 0 10px 40px rgba(0,0,0,0.2); }
        h2 { text-align: center; color: #333; margin-bottom: 20px; }
        .error { color: red; margin-bottom: 15px; text-align: center; }
        input { width: 100%; padding: 12px; margin-bottom: 15px; border: 1px solid #ddd; border-radius: 5px; }
        button { width: 100%; padding: 12px; background: #27ae60; color: white; border: none; border-radius: 5px; font-size: 16px; cursor: pointer; font-weight: bold; }
        button:hover { background: #219a52; }
    </style>
</head>
<body>
    <div class="login-box">
        <h2>POS Login</h2>
        {% if error %}<p class="error">{{ error }}</p>{% endif %}
        <form method="POST" action="/public/home">
            <input type="text" name="username" placeholder="Username" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">Masuk</button>
        </form>
    </div>
</body>
</html>
'''

# Admin template
ADMIN_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>POS Admin</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Arial, sans-serif; background: #f4f6f9; }
        .sidebar { width: 250px; background: #2c3e50; color: white; min-height: 100vh; position: fixed; }
        .sidebar h2 { padding: 20px; background: #1a252f; text-align: center; font-size: 18px; }
        .menu a { display: block; padding: 12px 20px; color: #ecf0f1; text-decoration: none; }
        .menu a:hover { background: #34495e; }
        .menu-section { padding: 10px 20px; font-size: 11px; color: #7f8c8d; text-transform: uppercase; }
        .main { margin-left: 250px; padding: 20px; }
        .topbar { background: white; padding: 15px 20px; border-radius: 5px; margin-bottom: 20px; display: flex; justify-content: space-between; }
        .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; }
        .stat-card { background: white; padding: 20px; border-radius: 8px; }
        .stat-card h3 { font-size: 14px; color: #7f8c8d; }
        .stat-card .value { font-size: 24px; font-weight: bold; color: #2c3e50; }
        table { width: 100%; background: white; border-collapse: collapse; }
        th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ecf0f1; }
        th { background: #f8f9fa; }
    </style>
</head>
<body>
    <div class="sidebar">
        <h2>POS APP</h2>
        <div class="menu">
            <div class="menu-section">Main</div>
            <a href="/public/admin">Dashboard</a>
            <div class="menu-section">Selling</div>
            <a href="/public/selling/cart">POS</a>
            <a href="/public/selling">Selling</a>
            <div class="menu-section">Data</div>
            <a href="/public/inventory">Inventory</a>
            <a href="/public/suplier">Supplier</a>
            <a href="/public/customer">Customer</a>
            <a href="/public/payment">Invoice</a>
            <div class="menu-section">Settings</div>
            <a href="/public/user">User</a>
            <a href="/logout">Logout</a>
        </div>
    </div>
    <div class="main">
        <div class="topbar">
            <h2>Dashboard</h2>
            <span>Welcome, {{ session.username }}</span>
        </div>
        <div class="stats">
            <div class="stat-card"><h3>Total Inventory</h3><div class="value">{{ stats.total_inventory }}</div></div>
            <div class="stat-card"><h3>Total User</h3><div class="value">{{ stats.total_user }}</div></div>
            <div class="stat-card"><h3>Total Supplier</h3><div class="value">{{ stats.total_suplier }}</div></div>
            <div class="stat-card"><h3>Total Customer</h3><div class="value">{{ stats.total_customer }}</div></div>
        </div>
        <h3 style="margin: 30px 0 15px;">Inventory List</h3>
        <table>
            <tr><th>No</th><th>Nama Barangan</th><th>Qty</th><th>Satuan</th></tr>
            {% for item in inventory %}
            <tr><td>{{ loop.index }}</td><td>{{ item.nama }}</td><td>{{ item.jumlah }}</td><td>{{ item.satuan }}</td></tr>
            {% endfor %}
        </table>
    </div>
</body>
</html>
'''

@app.route('/')
def index():
    if session.get('logged_in'):
        return redirect('/public/admin')
    return redirect('/public/home')

@app.route('/public/home', methods=['GET', 'POST'])
def login():
    if session.get('logged_in'):
        return redirect('/public/admin')
    error = None
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        if username == VALID_USERNAME and password == VALID_PASSWORD:
            session['logged_in'] = True
            session['username'] = username
            return redirect('/public/admin')
        error = 'Invalid credentials'
    return render_template_string(LOGIN_HTML, error=error)

@app.route('/public/admin')
def admin():
    if not session.get('logged_in'):
        return redirect('/public/home')
    return render_template_string(ADMIN_HTML, inventory=inventory_data, stats=stats)

@app.route('/public/inventory')
def inventory():
    if not session.get('logged_in'):
        return redirect('/public/home')
    html = ADMIN_HTML.replace('Dashboard', 'Inventory').replace('<th>No</th><th>Nama Barangan</th><th>Qty</th><th>Satuan</th>', '<th>No</th><th>Nama Barangan</th><th>Qty</th><th>Satuan</th>')
    return render_template_string(html, inventory=inventory_data, stats=stats)

@app.route('/public/suplier')
def suplier():
    if not session.get('logged_in'):
        return redirect('/public/home')
    suppliers = [{'nama': 'Supplier A', 'tel': '012-1234567'}, {'nama': 'Supplier B', 'tel': '012-7654321'}]
    html = ADMIN_HTML.replace('Dashboard', 'Supplier').replace('<th>No</th><th>Nama Barangan</th><th>Qty</th><th>Satuan</th>', '<th>No</th><th>Nama Supplier</th><th>No. Tel</th>').replace('{% for item in inventory %}', '{% for s in suppliers %}').replace('<td>{{ loop.index }}</td><td>{{ item.nama }}</td><td>{{ item.jumlah }}</td><td>{{ item.satuan }}</td>', '<td>{{ loop.index }}</td><td>{{ s.nama }}</td><td>{{ s.tel }}</td><td>-</td>')
    return render_template_string(html, inventory=suppliers, stats=stats)

@app.route('/public/customer')
def customer():
    if not session.get('logged_in'):
        return redirect('/public/home')
    customers = [{'nama': 'Customer A', 'tel': '019-1234567', 'point': '100'}]
    html = ADMIN_HTML.replace('Dashboard', 'Customer').replace('<th>No</th><th>Nama Barangan</th><th>Qty</th><th>Satuan</th>', '<th>No</th><th>Nama Customer</th><th>No. Tel</th><th>Point</th>').replace('{% for item in inventory %}', '{% for c in customers %}').replace('<td>{{ loop.index }}</td><td>{{ item.nama }}</td><td>{{ item.jumlah }}</td><td>{{ item.satuan }}</td>', '<td>{{ loop.index }}</td><td>{{ c.nama }}</td><td>{{ c.tel }}</td><td>{{ c.point }}</td>')
    return render_template_string(html, inventory=customers, stats=stats)

@app.route('/public/user')
def users():
    if not session.get('logged_in'):
        return redirect('/public/home')
    users_list = [{'nama': 'Admin', 'username': 'Admin', 'level': 'Admin'}, {'nama': 'Kasir', 'username': 'kasir', 'level': 'Kasir'}]
    html = ADMIN_HTML.replace('Dashboard', 'User').replace('<th>No</th><th>Nama Barangan</th><th>Qty</th><th>Satuan</th>', '<th>No</th><th>Nama</th><th>Username</th><th>Level</th>').replace('{% for item in inventory %}', '{% for u in users_list %}').replace('<td>{{ loop.index }}</td><td>{{ item.nama }}</td><td>{{ item.jumlah }}</td><td>{{ item.satuan }}</td>', '<td>{{ loop.index }}</td><td>{{ u.nama }}</td><td>{{ u.username }}</td><td>{{ u.level }}</td>')
    return render_template_string(html, inventory=users_list, stats=stats)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/public/home')

# Vercel and Gunicorn exports
app = application = app