# Full-featured POS System - Flask App for Render.com
from flask import Flask, render_template_string, request, session, redirect, url_for, jsonify
import datetime
import random

app = Flask(__name__)
app.secret_key = 'pos-secret-key-2024'

# Login credentials
VALID_USERNAME = 'Admin'
VALID_PASSWORD = 'admin112233'

# Sample Data
inventory_data = [
    {'id': '1', 'nama': 'GULA PASIR 1KG', 'jumlah': '50', 'satuan': 'pcs', 'harga_borong': '2.50', 'harga_jual': '3.00', 'expired': '2026-12-31', 'status': 'Active'},
    {'id': '2', 'nama': 'MINYAK MASAK 2KG', 'jumlah': '30', 'satuan': 'botol', 'harga_borong': '8.00', 'harga_jual': '10.00', 'expired': '2026-08-15', 'status': 'Active'},
    {'id': '3', 'nama': 'MINYAK MASAK 5KG', 'jumlah': '20', 'satuan': 'botol', 'harga_borong': '18.00', 'harga_jual': '22.00', 'expired': '2026-08-15', 'status': 'Active'},
    {'id': '4', 'nama': 'TELUR AYAM GRED A', 'jumlah': '100', 'satuan': 'biji', 'harga_borong': '0.40', 'harga_jual': '0.50', 'expired': '2026-05-01', 'status': 'Active'},
    {'id': '5', 'nama': 'TELUR AYAM GRED B', 'jumlah': '100', 'satuan': 'biji', 'harga_borong': '0.35', 'harga_jual': '0.45', 'expired': '2026-05-01', 'status': 'Active'},
    {'id': '6', 'nama': 'MINYAK OLIVE 1L', 'jumlah': '15', 'satuan': 'botol', 'harga_borong': '12.00', 'harga_jual': '15.00', 'expired': '2027-01-01', 'status': 'Active'},
    {'id': '7', 'nama': 'TEPUNG BERSERAGAM 1KG', 'jumlah': '5', 'satuan': 'bungkus', 'harga_borong': '2.00', 'harga_jual': '2.80', 'expired': '2026-06-30', 'status': 'Active'},
]

supplier_data = [
    {'id': '1', 'nama': 'Kedai Runcit ABC', 'alamat': 'No 123, Jalan Maju', 'tel': '012-1234567', 'email': 'abc@supplier.com'},
    {'id': '2', 'nama': 'Pembekal XYZ', 'alamat': 'No 456, Jalan Baru', 'tel': '012-7654321', 'email': 'xyz@supplier.com'},
    {'id': '3', 'nama': 'Grossario Sdn Bhd', 'alamat': 'No 789, Jalan Besi', 'tel': '013-9876543', 'email': 'gros@sb.com'},
]

customer_data = [
    {'id': '1', 'nama': 'Ahmad Bin Abu', 'tel': '019-1111111', 'alamat': 'Kampung Sentosa', 'point': '150', 'status': 'Active'},
    {'id': '2', 'nama': 'Siti Binti Saleha', 'tel': '019-2222222', 'alamat': 'Kampung Bahagia', 'point': '85', 'status': 'Active'},
    {'id': '3', 'nama': 'Muhammad Ali', 'tel': '019-3333333', 'alamat': 'Taman Mewah', 'point': '220', 'status': 'Active'},
]

selling_data = [
    {'no': '1', 'tarikh': '25-04-2026', 'no_invois': 'INV-001', 'jumlah': 'RM 150.00', 'bayar': 'RM 150.00', 'status': 'Lunas'},
    {'no': '2', 'tarikh': '24-04-2026', 'no_invois': 'INV-002', 'jumlah': 'RM 85.50', 'bayar': 'RM 85.50', 'status': 'Lunas'},
    {'no': '3', 'tarikh': '23-04-2026', 'no_invois': 'INV-003', 'jumlah': 'RM 210.00', 'bayar': 'RM 180.00', 'status': 'Belum Lunas'},
]

payment_data = [
    {'no': '1', 'invois': 'INV-001', 'tarikh': '25-04-2026', 'jumlah': 'RM 200.00', 'bayar': 'RM 200.00', 'baki': 'RM 0.00', 'status': 'Lunas'},
    {'no': '2', 'invois': 'INV-002', 'tarikh': '24-04-2026', 'jumlah': 'RM 150.00', 'bayar': 'RM 100.00', 'baki': 'RM 50.00', 'status': 'Belum Lunas'},
    {'no': '3', 'invois': 'INV-003', 'tarikh': '23-04-2026', 'jumlah': 'RM 300.00', 'bayar': 'RM 300.00', 'baki': 'RM 0.00', 'status': 'Lunas'},
]

user_data = [
    {'nama': 'Admin User', 'username': 'Admin', 'level': 'Admin', 'status': 'Active'},
    {'nama': 'Kasir One', 'username': 'kasir1', 'level': 'Kasir', 'status': 'Active'},
    {'nama': 'Kasir Two', 'username': 'kasir2', 'level': 'Kasir', 'status': 'Active'},
]

cheque_data = [
    {'no': '1', 'no_cheque': 'CH001', 'bank': 'CIMB', 'jumlah': 'RM 500.00', 'tarikh': '20-04-2026', 'status': 'Belum'},
    {'no': '2', 'no_cheque': 'CH002', 'bank': 'Maybank', 'jumlah': 'RM 350.00', 'tarikh': '22-04-2026', 'status': 'Cleared'},
]

return_data = [
    {'no': '1', 'no_return': 'RTN-001', 'tarikh': '24-04-2026', 'item': 'GULA PASIR 1KG', 'jumlah': 'RM 5.00', 'sebab': 'Rosak'},
    {'no': '2', 'no_return': 'RTN-002', 'tarikh': '23-04-2026', 'item': 'TELUR AYAM', 'jumlah': 'RM 3.00', 'sebab': 'Tukar barang'},
]

stats = {
    'total_payment': 'RM 158,120.17',
    'total_selling': 'RM 165,305.38',
    'total_profit': 'RM 7,185.21',
    'total_inventory': len(inventory_data),
    'total_user': len(user_data),
    'total_suplier': len(supplier_data),
    'total_customer': len(customer_data),
    'total_invoice': len(payment_data),
    'total_cheque': len(cheque_data),
    'total_return': len(return_data),
    'total_redeem': 0,
    'total_expired': len(inventory_data),
    'total_low': 5,
}

# Base HTML Template
BASE_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>POS APP - {{ page_title }}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Arial, sans-serif; background: #f4f6f9; }
        .sidebar { width: 250px; background: #2c3e50; color: white; min-height: 100vh; position: fixed; }
        .sidebar h2 { padding: 20px; background: #1a252f; text-align: center; font-size: 18px; }
        .menu-section { padding: 10px 20px 5px; font-size: 11px; color: #95a5a6; text-transform: uppercase; font-weight: bold; }
        .menu a { display: flex; align-items: center; padding: 12px 20px; color: #ecf0f1; text-decoration: none; transition: 0.3s; }
        .menu a:hover { background: #34495e; }
        .menu a i { margin-right: 10px; width: 20px; }
        .menu .badge { margin-left: auto; background: #e74c3c; padding: 2px 8px; border-radius: 10px; font-size: 11px; }
        .main { margin-left: 250px; padding: 20px; }
        .topbar { background: white; padding: 15px 25px; border-radius: 5px; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        .topbar h2 { color: #2c3e50; }
        .topbar .user-info { display: flex; align-items: center; gap: 15px; }
        .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 30px; }
        .stat-card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        .stat-card h3 { font-size: 13px; color: #7f8c8d; margin-bottom: 10px; }
        .stat-card .value { font-size: 24px; font-weight: bold; color: #2c3e50; }
        .stat-card .value.profit { color: #27ae60; }
        .stat-card.payment .value { color: #3498db; }
        .stat-card.selling .value { color: #9b59b6; }
        table { width: 100%; background: white; border-collapse: collapse; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        th, td { padding: 12px 15px; text-align: left; border-bottom: 1px solid #ecf0f1; }
        th { background: #3498db; color: white; font-weight: 600; }
        tr:hover { background: #f8f9fa; }
        .status-lunas { color: #27ae60; font-weight: bold; }
        .status-belum { color: #e74c3c; font-weight: bold; }
        .btn { padding: 8px 15px; background: #3498db; color: white; border: none; border-radius: 5px; cursor: pointer; text-decoration: none; display: inline-block; }
        .btn:hover { background: #2980b9; }
        .btn-success { background: #27ae60; }
        .btn-danger { background: #e74c3c; }
        .form-group { margin-bottom: 15px; }
        .form-group label { display: block; margin-bottom: 5px; font-weight: 600; }
        .form-group input, .form-group select { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px; }
        .card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); margin-bottom: 20px; }
    </style>
</head>
<body>
    <div class="sidebar">
        <h2><i class="fas fa-cash-register"></i> POS APP</h2>
        <div class="menu">
            <div class="menu-section">Main</div>
            <a href="/public/admin"><i class="fas fa-tachometer-alt"></i> Dashboard</a>
            <div class="menu-section">Selling App</div>
            <a href="/public/selling/cart"><i class="fas fa-shopping-cart"></i> POS <span class="badge">0</span></a>
            <a href="/public/quote"><i class="fas fa-file-alt"></i> Quotation</a>
            <a href="/public/selling"><i class="fas fa-chart-line"></i> Selling <span class="badge">''' + str(stats['total_invoice']) + '''</span></a>
            <a href="/public/selling/indexMinyak"><i class="fas fa-oil-can"></i> Minyake <span class="badge" style="background:#f39c12">New</span></a>
            <div class="menu-section">Data App</div>
            <a href="/public/suplier"><i class="fas fa-truck"></i> Suplier <span class="badge">''' + str(stats['total_suplier']) + '''</span></a>
            <a href="/public/customer"><i class="fas fa-users"></i> Customer <span class="badge">''' + str(stats['total_customer']) + '''</span></a>
            <a href="/public/redeempoint"><i class="fas fa-gift"></i> Redeem Point <span class="badge">''' + str(stats['total_redeem']) + '''</span></a>
            <a href="/public/inventory"><i class="fas fa-box"></i> Inventory <span class="badge">''' + str(stats['total_inventory']) + '''</span></a>
            <a href="/public/cheque"><i class="fas fa-money-check"></i> Cheque <span class="badge">''' + str(stats['total_cheque']) + '''</span></a>
            <a href="/public/payment"><i class="fas fa-file-invoice-dollar"></i> Invoice & Payment <span class="badge">''' + str(stats['total_invoice']) + '''</span></a>
            <a href="/public/returns"><i class="fas fa-undo"></i> Return <span class="badge">''' + str(stats['total_return']) + '''</span></a>
            <div class="menu-section">Monitoring</div>
            <a href="/public/inventory/experied"><i class="fas fa-exclamation-triangle"></i> Expired Stock <span class="badge">''' + str(stats['total_expired']) + '''</span></a>
            <a href="/public/lowstock"><i class="fas fa-exclamation-circle"></i> Low Stock <span class="badge">''' + str(stats['total_low']) + '''</span></a>
            <div class="menu-section">Version</div>
            <a href="/public/admin/versiapp"><i class="fas fa-info-circle"></i> Versi Aplikasi</a>
            <div class="menu-section">User</div>
            <a href="/public/user"><i class="fas fa-user-cog"></i> User <span class="badge">''' + str(stats['total_user']) + '''</span></a>
            <a href="/public/admin/qr"><i class="fas fa-qrcode"></i> QR Inventory</a>
        </div>
    </div>
    <div class="main">
        <div class="topbar">
            <h2><i class="fas fa-{{ icon }}"></i> {{ page_title }}</h2>
            <div class="user-info">
                <span>{{ session.username }}</span>
                <a href="/logout" class="btn btn-danger"><i class="fas fa-sign-out-alt"></i> Logout</a>
            </div>
        </div>
        {% block content %}{% endblock %}
    </div>
</body>
</html>
'''

def render_page(content, page_title, icon='cube'):
    return render_template_string(BASE_HTML.replace('{{ page_title }}', page_title).replace('{{ icon }}', icon) + '{% block content %}' + content + '{% endblock %}', stats=stats, session=session)

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
    
    LOGIN_HTML = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>POS - Login</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <style>
            body { font-family: Arial, sans-serif; background: linear-gradient(135deg, #667eea, #764ba2); min-height: 100vh; display: flex; align-items: center; justify-content: center; }
            .login-box { background: white; padding: 40px; border-radius: 10px; width: 350px; box-shadow: 0 10px 40px rgba(0,0,0,0.2); }
            h2 { text-align: center; color: #333; margin-bottom: 20px; }
            .error { color: red; margin-bottom: 15px; text-align: center; }
            input { width: 100%; padding: 12px; margin-bottom: 15px; border: 1px solid #ddd; border-radius: 5px; box-sizing: border-box; }
            button { width: 100%; padding: 12px; background: #27ae60; color: white; border: none; border-radius: 5px; font-size: 16px; cursor: pointer; font-weight: bold; }
            button:hover { background: #219a52; }
        </style>
    </head>
    <body>
        <div class="login-box">
            <h2><i class="fas fa-cash-register"></i> POS Login</h2>
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
    return render_template_string(LOGIN_HTML, error=error)

# Dashboard
@app.route('/public/admin')
def dashboard():
    if not session.get('logged_in'):
        return redirect('/public/home')
    
    content = '''
    <div class="stats">
        <div class="stat-card payment">
            <h3>Payment</h3>
            <div class="value">{{ stats.total_payment }}</div>
        </div>
        <div class="stat-card selling">
            <h3>Selling</h3>
            <div class="value">{{ stats.total_selling }}</div>
        </div>
        <div class="stat-card">
            <h3>Profit</h3>
            <div class="value profit">{{ stats.total_profit }}</div>
        </div>
    </div>
    <div class="stats">
        <div class="stat-card"><h3>Total Inventory</h3><div class="value">{{ stats.total_inventory }}</div></div>
        <div class="stat-card"><h3>Total Invoice</h3><div class="value">{{ stats.total_invoice }}</div></div>
        <div class="stat-card"><h3>Total Suplier</h3><div class="value">{{ stats.total_suplier }}</div></div>
        <div class="stat-card"><h3>Total Customer</h3><div class="value">{{ stats.total_customer }}</div></div>
    </div>
    <div class="card">
        <h3 style="margin-bottom:15px;"><i class="fas fa-box"></i> Inventory List</h3>
        <table>
            <tr><th>No</th><th>Nama Barangan</th><th>Qty</th><th>Satuan</th><th>Harga Jual</th><th>Status</th></tr>
            {% for item in inventory %}
            <tr><td>{{ loop.index }}</td><td>{{ item.nama }}</td><td>{{ item.jumlah }}</td><td>{{ item.satuan }}</td><td>RM {{ item.harga_jual }}</td><td>{{ item.status }}</td></tr>
            {% endfor %}
        </table>
    </div>
    '''
    return render_page(content, 'Dashboard', 'tachometer-alt').replace('{% for item in inventory %}', '{% for item in inventory_data %}')

# Inventory
@app.route('/public/inventory')
def inventory():
    if not session.get('logged_in'):
        return redirect('/public/home')
    content = '''
    <div class="card">
        <div style="margin-bottom:15px;">
            <a href="#" class="btn btn-success"><i class="fas fa-plus"></i> Tambah</a>
            <a href="#" class="btn"><i class="fas fa-print"></i> Print</a>
            <a href="#" class="btn"><i class="fas fa-file-excel"></i> Excel</a>
        </div>
        <table>
            <tr><th>No</th><th>Nama Barangan</th><th>Qty</th><th>Satuan</th><th>Harga Borong</th><th>Harga Jual</th><th>Expired</th><th>Status</th><th>Action</th></tr>
            {% for item in items %}
            <tr>
                <td>{{ loop.index }}</td>
                <td>{{ item.nama }}</td>
                <td>{{ item.jumlah }}</td>
                <td>{{ item.satuan }}</td>
                <td>RM {{ item.harga_borong }}</td>
                <td>RM {{ item.harga_jual }}</td>
                <td>{{ item.expired }}</td>
                <td>{{ item.status }}</td>
                <td>
                    <a href="#" class="btn"><i class="fas fa-edit"></i></a>
                    <a href="#" class="btn btn-danger"><i class="fas fa-trash"></i></a>
                </td>
            </tr>
            {% endfor %}
        </table>
    </div>
    '''
    return render_page(content, 'Inventory', 'box').replace('{% for item in items %}', '{% for item in inventory_data %}')

# Supplier
@app.route('/public/suplier')
def suplier():
    if not session.get('logged_in'):
        return redirect('/public/home')
    content = '''
    <div class="card">
        <div style="margin-bottom:15px;">
            <a href="#" class="btn btn-success"><i class="fas fa-plus"></i> Tambah</a>
        </div>
        <table>
            <tr><th>No</th><th>Nama Supplier</th><th>Alamat</th><th>No. Tel</th><th>Email</th><th>Action</th></tr>
            {% for s in suppliers %}
            <tr>
                <td>{{ loop.index }}</td>
                <td>{{ s.nama }}</td>
                <td>{{ s.alamat }}</td>
                <td>{{ s.tel }}</td>
                <td>{{ s.email }}</td>
                <td>
                    <a href="#" class="btn"><i class="fas fa-edit"></i></a>
                    <a href="#" class="btn btn-danger"><i class="fas fa-trash"></i></a>
                </td>
            </tr>
            {% endfor %}
        </table>
    </div>
    '''
    return render_page(content, 'Supplier', 'truck').replace('{% for s in suppliers %}', '{% for s in supplier_data %}')

# Customer
@app.route('/public/customer')
def customer():
    if not session.get('logged_in'):
        return redirect('/public/home')
    content = '''
    <div class="card">
        <div style="margin-bottom:15px;">
            <a href="#" class="btn btn-success"><i class="fas fa-plus"></i> Tambah</a>
        </div>
        <table>
            <tr><th>No</th><th>Nama Customer</th><th>No. Tel</th><th>Alamat</th><th>Point</th><th>Status</th><th>Action</th></tr>
            {% for c in customers %}
            <tr>
                <td>{{ loop.index }}</td>
                <td>{{ c.nama }}</td>
                <td>{{ c.tel }}</td>
                <td>{{ c.alamat }}</td>
                <td><i class="fas fa-star" style="color:#f39c12"></i> {{ c.point }}</td>
                <td>{{ c.status }}</td>
                <td>
                    <a href="#" class="btn"><i class="fas fa-edit"></i></a>
                    <a href="#" class="btn btn-danger"><i class="fas fa-trash"></i></a>
                </td>
            </tr>
            {% endfor %}
        </table>
    </div>
    '''
    return render_page(content, 'Customer', 'users').replace('{% for c in customers %}', '{% for c in customer_data %}')

# Selling
@app.route('/public/selling')
def selling():
    if not session.get('logged_in'):
        return redirect('/public/home')
    content = '''
    <div class="card">
        <table>
            <tr><th>No</th><th>Tarikh</th><th>No. Invois</th><th>Jumlah</th><th>Bayar</th><th>Status</th></tr>
            {% for s in selling %}
            <tr>
                <td>{{ s.no }}</td>
                <td>{{ s.tarikh }}</td>
                <td>{{ s.no_invois }}</td>
                <td>{{ s.jumlah }}</td>
                <td>{{ s.bayar }}</td>
                <td class="{{ 'status-lunas' if s.status == 'Lunas' else 'status-belum' }}">{{ s.status }}</td>
            </tr>
            {% endfor %}
        </table>
    </div>
    '''
    return render_page(content, 'Selling', 'chart-line').replace('{% for s in selling %}', '{% for s in selling_data %}')

# POS/Cart
@app.route('/public/selling/cart')
def selling_cart():
    if not session.get('logged_in'):
        return redirect('/public/home')
    content = '''
    <div class="card">
        <h3 style="margin-bottom:20px;"><i class="fas fa-shopping-cart"></i> Point of Sale (POS)</h3>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px;">
            <div>
                <h4>Carian Produk</h4>
                <div class="form-group">
                    <input type="text" placeholder="Nama produk atau barcode...">
                </div>
                <div class="form-group">
                    <select>
                        <option>Semua Kategori</option>
                        <option>Makanan</option>
                        <option>Minuman</option>
                        <option>Barangan Rumah</option>
                    </select>
                </div>
                <table>
                    <tr><th>Produk</th><th>Harga</th><th>Action</th></tr>
                    {% for item in items %}
                    <tr>
                        <td>{{ item.nama }}</td>
                        <td>RM {{ item.harga_jual }}</td>
                        <td><button class="btn"><i class="fas fa-plus"></i></button></td>
                    </tr>
                    {% endfor %}
                </table>
            </div>
            <div>
                <h4>Cart</h4>
                <table>
                    <tr><th>Produk</th><th>Qty</th><th>Harga</th><th>Total</th></tr>
                    <tr><td colspan="4" style="text-align:center;color:#999;">Tiada produk lagi</td></tr>
                </table>
                <div style="margin-top:20px;text-align:right;">
                    <h3>Jumlah: RM 0.00</h3>
                    <button class="btn btn-success" style="margin-top:10px;"><i class="fas fa-save"></i> Bayar</button>
                </div>
            </div>
        </div>
    </div>
    '''
    return render_page(content, 'POS', 'shopping-cart').replace('{% for item in items %}', '{% for item in inventory_data %}')

# Quotation
@app.route('/public/quote')
def quote():
    if not session.get('logged_in'):
        return redirect('/public/home')
    content = '''
    <div class="card">
        <h3><i class="fas fa-file-alt"></i> Quotation</h3>
        <p style="color:#666;margin-top:10px;">Coming soon...</p>
    </div>
    '''
    return render_page(content, 'Quotation', 'file-alt')

# Minyake
@app.route('/public/selling/indexMinyak')
def minyak():
    if not session.get('logged_in'):
        return redirect('/public/home')
    content = '''
    <div class="card">
        <h3><i class="fas fa-oil-can"></i> Minyake (Oil)</h3>
        <table>
            <tr><th>No</th><th>Produk</th><th>Harga Borong</th><th>Harga Jual</th><th>Stok</th></tr>
            <tr><td>1</td><td>MINYAK MASAK 2KG</td><td>RM 8.00</td><td>RM 10.00</td><td>30</td></tr>
            <tr><td>2</td><td>MINYAK MASAK 5KG</td><td>RM 18.00</td><td>RM 22.00</td><td>20</td></tr>
            <tr><td>3</td><td>MINYAK OLIVE 1L</td><td>RM 12.00</td><td>RM 15.00</td><td>15</td></tr>
        </table>
    </div>
    '''
    return render_page(content, 'Minyake', 'oil-can')

# Redeem Point
@app.route('/public/redeempoint')
def redeempoint():
    if not session.get('logged_in'):
        return redirect('/public/home')
    content = '''
    <div class="card">
        <h3><i class="fas fa-gift"></i> Redeem Point</h3>
        <p style="color:#666;margin-top:10px;">Coming soon...</p>
    </div>
    '''
    return render_page(content, 'Redeem Point', 'gift')

# Cheque
@app.route('/public/cheque')
def cheque():
    if not session.get('logged_in'):
        return redirect('/public/home')
    content = '''
    <div class="card">
        <table>
            <tr><th>No</th><th>No. Cheque</th><th>Bank</th><th>Jumlah</th><th>Tarikh</th><th>Status</th></tr>
            {% for c in cheque %}
            <tr>
                <td>{{ c.no }}</td>
                <td>{{ c.no_cheque }}</td>
                <td>{{ c.bank }}</td>
                <td>{{ c.jumlah }}</td>
                <td>{{ c.tarikh }}</td>
                <td class="{{ 'status-lunas' if c.status == 'Cleared' else 'status-belum' }}">{{ c.status }}</td>
            </tr>
            {% endfor %}
        </table>
    </div>
    '''
    return render_page(content, 'Cheque', 'money-check').replace('{% for c in cheque %}', '{% for c in cheque_data %}')

# Invoice & Payment
@app.route('/public/payment')
def payment():
    if not session.get('logged_in'):
        return redirect('/public/home')
    content = '''
    <div class="card">
        <table>
            <tr><th>No</th><th>No. Invois</th><th>Tarikh</th><th>Jumlah</th><th>Bayar</th><th>Baki</th><th>Status</th></tr>
            {% for p in payment %}
            <tr>
                <td>{{ p.no }}</td>
                <td>{{ p.invois }}</td>
                <td>{{ p.tarikh }}</td>
                <td>{{ p.jumlah }}</td>
                <td>{{ p.bayar }}</td>
                <td>{{ p.baki }}</td>
                <td class="{{ 'status-lunas' if p.status == 'Lunas' else 'status-belum' }}">{{ p.status }}</td>
            </tr>
            {% endfor %}
        </table>
    </div>
    '''
    return render_page(content, 'Invoice & Payment', 'file-invoice-dollar').replace('{% for p in payment %}', '{% for p in payment_data %}')

# Return
@app.route('/public/returns')
def returns():
    if not session.get('logged_in'):
        return redirect('/public/home')
    content = '''
    <div class="card">
        <table>
            <tr><th>No</th><th>No. Return</th><th>Tarikh</th><th>Item</th><th>Jumlah</th><th>Sebab</th></tr>
            {% for r in returns %}
            <tr>
                <td>{{ r.no }}</td>
                <td>{{ r.no_return }}</td>
                <td>{{ r.tarikh }}</td>
                <td>{{ r.item }}</td>
                <td>{{ r.jumlah }}</td>
                <td>{{ r.sebab }}</td>
            </tr>
            {% endfor %}
        </table>
    </div>
    '''
    return render_page(content, 'Return', 'undo').replace('{% for r in returns %}', '{% for r in return_data %}')

# Expired Stock
@app.route('/public/inventory/experied')
def experied():
    if not session.get('logged_in'):
        return redirect('/public/home')
    content = '''
    <div class="card">
        <h3><i class="fas fa-exclamation-triangle"></i> Expired Stock</h3>
        <table>
            <tr><th>No</th><th>Nama Barangan</th><th>Qty</th><th>Expired Date</th><th>Status</th></tr>
            {% for item in items %}
            <tr>
                <td>{{ loop.index }}</td>
                <td>{{ item.nama }}</td>
                <td>{{ item.jumlah }}</td>
                <td>{{ item.expired }}</td>
                <td style="color:#e74c3c">Expired</td>
            </tr>
            {% endfor %}
        </table>
    </div>
    '''
    return render_page(content, 'Expired Stock', 'exclamation-triangle').replace('{% for item in items %}', '{% for item in inventory_data %}')

# Low Stock
@app.route('/public/lowstock')
def lowstock():
    if not session.get('logged_in'):
        return redirect('/public/home')
    low_items = [item for item in inventory_data if int(item['jumlah']) < 10]
    content = '''
    <div class="card">
        <h3><i class="fas fa-exclamation-circle"></i> Low Stock Items</h3>
        <table>
            <tr><th>No</th><th>Nama Barangan</th><th>Qty</th><th>Satuan</th><th>Status</th></tr>
            {% for item in items %}
            <tr>
                <td>{{ loop.index }}</td>
                <td>{{ item.nama }}</td>
                <td style="color:#e74c3c;font-weight:bold;">{{ item.jumlah }}</td>
                <td>{{ item.satuan }}</td>
                <td style="color:#e74c3c">Low Stock</td>
            </tr>
            {% endfor %}
        </table>
    </div>
    '''
    return render_page(content, 'Low Stock', 'exclamation-circle').replace('{% for item in items %}', '{% for item in low_items %}')

# Version
@app.route('/public/admin/versiapp')
def versiapp():
    if not session.get('logged_in'):
        return redirect('/public/home')
    content = '''
    <div class="card">
        <h3><i class="fas fa-info-circle"></i> Versi Aplikasi</h3>
        <div style="padding:20px;text-align:center;">
            <h2>POS APP Version 3.1.0</h2>
            <p style="color:#666;margin-top:10px;">Copyright © 2026 Kaymedia Digital.</p>
            <p style="color:#666;">All rights reserved.</p>
        </div>
    </div>
    '''
    return render_page(content, 'Versi Aplikasi', 'info-circle')

# User Management
@app.route('/public/user')
def users():
    if not session.get('logged_in'):
        return redirect('/public/home')
    content = '''
    <div class="card">
        <div style="margin-bottom:15px;">
            <a href="#" class="btn btn-success"><i class="fas fa-plus"></i> Tambah User</a>
        </div>
        <table>
            <tr><th>No</th><th>Nama</th><th>Username</th><th>Level</th><th>Status</th><th>Action</th></tr>
            {% for u in users_list %}
            <tr>
                <td>{{ loop.index }}</td>
                <td>{{ u.nama }}</td>
                <td>{{ u.username }}</td>
                <td>{{ u.level }}</td>
                <td>{{ u.status }}</td>
                <td>
                    <a href="#" class="btn"><i class="fas fa-edit"></i></a>
                    <a href="#" class="btn btn-danger"><i class="fas fa-trash"></i></a>
                </td>
            </tr>
            {% endfor %}
        </table>
    </div>
    '''
    return render_page(content, 'User Management', 'user-cog').replace('{% for u in users_list %}', '{% for u in user_data %}')

# QR Inventory
@app.route('/public/admin/qr')
def qr_inventory():
    if not session.get('logged_in'):
        return redirect('/public/home')
    content = '''
    <div class="card">
        <h3><i class="fas fa-qrcode"></i> QR Inventory</h3>
        <div class="form-group">
            <input type="text" placeholder="Scan atau masukkan invoice number...">
        </div>
        <div style="padding:40px;text-align:center;background:#f8f9fa;border-radius:8px;margin-top:20px;">
            <i class="fas fa-qrcode" style="font-size:100px;color:#95a5a6;"></i>
            <p style="color:#666;margin-top:20px;">Scan QR Code untuk lihat maklumat inventory</p>
        </div>
    </div>
    '''
    return render_page(content, 'QR Inventory', 'qrcode')

# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/public/home')

# Export for Gunicorn
if __name__ == '__main__':
    application = app
    app = application