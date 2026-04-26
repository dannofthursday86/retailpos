from flask import Flask, render_template_string, request, session, redirect, url_for, jsonify
import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Login credentials
VALID_USERNAME = 'Admin'
VALID_PASSWORD = 'admin112233'

# Sample inventory data
inventory_data = [
    {'id_inventory': '4434', 'nama_barangan': 'GULA PASIR PRAI 1KG', 'jumlah': '20', 'satuan': 'pcs', 'harga_borong': '3.00', 'harga_jual': '3.00', 'barcode': '9556058000031', 'status': 'Active', 'is_minyak': '1'},
    {'id_inventory': '6039', 'nama_barangan': 'MINYAK MASAK 2KG', 'jumlah': '15', 'satuan': 'BOTOL', 'harga_borong': '11.00', 'harga_jual': '13.50', 'barcode': '9557561100447', 'status': 'Active', 'is_minyak': '1'},
    {'id_inventory': '6040', 'nama_barangan': 'MINYAK MASAK 5KG', 'jumlah': '8', 'satuan': 'BOTOL', 'harga_borong': '24.00', 'harga_jual': '30.90', 'barcode': '9557561100461', 'status': 'Active', 'is_minyak': '1'},
    {'id_inventory': '6389', 'nama_barangan': 'MINYAK MASAK PAKET', 'jumlah': '150', 'satuan': 'PAKET', 'harga_borong': '2.80', 'harga_jual': '3.00', 'barcode': '', 'status': 'Active', 'is_minyak': '1'},
    {'id_inventory': '6390', 'nama_barangan': 'TELUR AYAM GRED A', 'jumlah': '600', 'satuan': 'BIJI', 'harga_borong': '0.43', 'harga_jual': '0.45', 'barcode': '', 'status': 'Active', 'is_minyak': '1'},
    {'id_inventory': '6391', 'nama_barangan': 'TELUR AYAM GRED B', 'jumlah': '600', 'satuan': 'BIJI', 'harga_borong': '0.42', 'harga_jual': '0.43', 'barcode': '', 'status': 'Active', 'is_minyak': '1'},
    {'id_inventory': '6392', 'nama_barangan': 'TELUR AYAM GRED C', 'jumlah': '0', 'satuan': 'BIJI', 'harga_borong': '0.40', 'harga_jual': '0.41', 'barcode': '', 'status': 'Active', 'is_minyak': '1'},
    {'id_inventory': '6393', 'nama_barangan': 'TELUR AYAM GRED D', 'jumlah': '600', 'satuan': 'BIJI', 'harga_borong': '0.38', 'harga_jual': '0.39', 'barcode': '', 'status': 'Active', 'is_minyak': '1'},
    {'id_inventory': '6395', 'nama_barangan': 'MINYAK MASAK BOTOL 1KG', 'jumlah': '28', 'satuan': 'BOTOL', 'harga_borong': '6.50', 'harga_jual': '6.90', 'barcode': '', 'status': 'Active', 'is_minyak': '1'},
]

# Add more sample inventory
for i in range(10, 100):
    inventory_data.append({
        'id_inventory': str(6000 + i),
        'nama_barangan': f'PRODUK ITEM {i}',
        'jumlah': str(50 + i * 5),
        'satuan': 'BIJI',
        'harga_borong': f'{(i % 10) + 1}.00',
        'harga_jual': f'{(i % 10) + 2}.00',
        'barcode': f'12345678{i:05d}',
        'status': 'Active',
        'is_minyak': '0'
    })

# Sample data
supplier_data = [
    {'id_suplier': '1', 'nama_suplier': 'SYARIKAT MINYAK MALAYSIA', 'no_tel': '03-12345678', 'alamat': 'Kuala Lumpur'},
    {'id_suplier': '2', 'nama_suplier': 'PERTANIAN SELANGOR', 'no_tel': '03-87654321', 'alamat': 'Selangor'},
    {'id_suplier': '3', 'nama_suplier': 'PT NUSANTARA', 'no_tel': '021-1234567', 'alamat': 'Indonesia'},
]

customer_data = [
    {'id_customer': '1', 'nama_customer': 'AHMAD BIN ABU', 'no_tel': '012-3456789', 'alamat': 'Kuala Lumpur', 'point': '150'},
    {'id_customer': '2', 'nama_customer': 'SITI BINTI HAWA', 'no_tel': '019-9876543', 'alamat': 'Selangor', 'point': '80'},
    {'id_customer': '3', 'nama_customer': 'MUHAMMAD ALI', 'no_tel': '011-12345678', 'alamat': 'Perak', 'point': '200'},
]

invoice_data = [
    {'id_payment': 'INV001', 'tanggal': '2026-04-26', 'nama_customer': 'AHMAD BIN ABU', 'total': '250.00', 'bayaran': '250.00', 'status': 'Lunas'},
    {'id_payment': 'INV002', 'tanggal': '2026-04-25', 'nama_customer': 'SITI BINTI HAWA', 'total': '180.00', 'bayaran': '100.00', 'status': 'Belum Lunas'},
    {'id_payment': 'INV003', 'tanggal': '2026-04-24', 'nama_customer': 'MUHAMMAD ALI', 'total': '320.00', 'bayaran': '320.00', 'status': 'Lunas'},
]

selling_data = [
    {'id_sell': 'S001', 'tanggal': '2026-04-26', 'total': '150.00', 'bayaran': '200.00', 'baki': '50.00', 'status': 'Lunas'},
    {'id_sell': 'S002', 'tanggal': '2026-04-26', 'total': '75.50', 'bayaran': '100.00', 'baki': '24.50', 'status': 'Lunas'},
]

user_data = [
    {'id_user': '1', 'nama': 'Admin', 'username': 'Admin', 'level': 'Admin', 'status': 'Active'},
    {'id_user': '2', 'nama': 'Kasir 1', 'username': 'kasir1', 'level': 'Kasir', 'status': 'Active'},
    {'id_user': '3', 'nama': 'Gudang', 'username': 'gudang', 'level': 'Gudang', 'status': 'Active'},
]

stats = {
    'payment_total': '158,120.17',
    'selling_total': '165,305.38',
    'profit': '7,185.21',
    'total_user': '3',
    'total_inventory': len(inventory_data),
    'total_invoice': len(invoice_data),
    'total_suplier': len(supplier_data),
    'total_customer': len(customer_data),
    'expired_stock': len(inventory_data),
    'low_stock': sum(1 for item in inventory_data if int(item['jumlah']) < 10)
}

# Base Template with Sidebar
BASE = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}POS APP{% endblock %}</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, sans-serif; background: #f4f6f9; }
        .wrapper { display: flex; }
        .sidebar { width: 250px; background: #2c3e50; color: white; min-height: 100vh; position: fixed; }
        .sidebar-header { padding: 20px; background: #1a252f; text-align: center; }
        .sidebar-header h2 { font-size: 18px; margin-bottom: 5px; }
        .sidebar-header span { font-size: 12px; color: #95a5a6; }
        .sidebar-menu { padding: 10px 0; }
        .menu-section { padding: 10px 20px; font-size: 11px; text-transform: uppercase; color: #7f8c8d; font-weight: bold; }
        .sidebar a { display: block; padding: 12px 20px; color: #ecf0f1; text-decoration: none; transition: 0.3s; }
        .sidebar a:hover, .sidebar a.active { background: #34495e; border-left: 3px solid #3498db; }
        .sidebar a i { margin-right: 10px; width: 20px; }
        .badge { float: right; background: #e74c3c; padding: 2px 8px; border-radius: 10px; font-size: 11px; }
        .main-content { margin-left: 250px; flex: 1; padding: 20px; }
        .top-bar { background: white; padding: 15px 20px; border-radius: 5px; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        .user-info { display: flex; align-items: center; gap: 10px; }
        .user-avatar { width: 35px; height: 35px; border-radius: 50%; background: #3498db; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; }
        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 30px; }
        .stat-card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .stat-card h3 { font-size: 14px; color: #7f8c8d; margin-bottom: 10px; }
        .stat-card .value { font-size: 24px; font-weight: bold; color: #2c3e50; }
        .stat-card.green { border-left: 4px solid #27ae60; }
        .stat-card.blue { border-left: 4px solid #3498db; }
        .stat-card.orange { border-left: 4px solid #f39c12; }
        .table-container { background: white; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); overflow: hidden; }
        .table-header { padding: 15px 20px; border-bottom: 1px solid #ecf0f1; display: flex; justify-content: space-between; align-items: center; }
        .table-header h3 { color: #2c3e50; }
        table { width: 100%; border-collapse: collapse; }
        th, td { padding: 12px 15px; text-align: left; border-bottom: 1px solid #ecf0f1; }
        th { background: #f8f9fa; font-weight: 600; color: #2c3e50; }
        tr:hover { background: #f8f9fa; }
        .btn { padding: 8px 15px; border: none; border-radius: 4px; cursor: pointer; text-decoration: none; display: inline-block; font-size: 13px; }
        .btn-primary { background: #3498db; color: white; }
        .btn-success { background: #27ae60; color: white; }
        .btn-danger { background: #e74c3c; color: white; }
        .search-box { padding: 8px 15px; border: 1px solid #ddd; border-radius: 4px; width: 250px; }
        .footer { text-align: center; padding: 20px; color: #7f8c8d; font-size: 12px; margin-top: 30px; }
    </style>
</head>
<body>
    {% if session.get('logged_in') %}
    <div class="wrapper">
        <div class="sidebar">
            <div class="sidebar-header">
                <h2><i class="fas fa-cash-register"></i> POS APP</h2>
                <span>LEPAR HILIR TRADING</span>
            </div>
            <div class="sidebar-menu">
                <div class="menu-section">Main</div>
                <a href="/public/admin"><i class="fas fa-tachometer-alt"></i> Dashboard</a>
                <div class="menu-section">Selling App</div>
                <a href="/public/selling/cart"><i class="fas fa-shopping-cart"></i> POS <span class="badge">0</span></a>
                <a href="/public/quote"><i class="fas fa-file-alt"></i> Quotation</a>
                <a href="/public/selling"><i class="fas fa-shopping-bag"></i> Selling</a>
                <a href="/public/selling/indexMinyak"><i class="fas fa-oil-can"></i> Minyake</a>
                <div class="menu-section">Data App</div>
                <a href="/public/suplier"><i class="fas fa-truck"></i> Suplier</a>
                <a href="/public/customer"><i class="fas fa-users"></i> Customer</a>
                <a href="/public/redeempoint"><i class="fas fa-gift"></i> Redeem Point</a>
                <a href="/public/inventory"><i class="fas fa-boxes"></i> Inventory</a>
                <a href="/public/cheque"><i class="fas fa-money-check"></i> Cheque</a>
                <a href="/public/payment"><i class="fas fa-file-invoice-dollar"></i> Invoice</a>
                <a href="/public/returns"><i class="fas fa-undo"></i> Return</a>
                <div class="menu-section">Monitoring</div>
                <a href="/public/inventory/experied"><i class="fas fa-exclamation-triangle"></i> Expired Stock</a>
                <a href="/public/inventory/stok"><i class="fas fa-level-down-alt"></i> Low Stock</a>
                <div class="menu-section">Settings</div>
                <a href="/public/admin/versiapp"><i class="fas fa-info-circle"></i> Versi Aplikasi</a>
                <a href="/public/user"><i class="fas fa-user-cog"></i> User</a>
                <a href="/public/admin/qr"><i class="fas fa-qrcode"></i> QR Inventory</a>
                <a href="/logout"><i class="fas fa-sign-out-alt"></i> Log Out</a>
            </div>
        </div>
        <div class="main-content">
            <div class="top-bar">
                <h2>{% block page_title %}<i class="fas fa-tachometer-alt"></i> Dashboard{% endblock %}</h2>
                <div class="user-info">
                    <span>Welcome, <strong>{{ session.get('username') }}</strong></span>
                    <div class="user-avatar">A</div>
                </div>
            </div>
            {% block content %}{% endblock %}
            <div class="footer">
                <p>Copyright 2026 <a href="https://kaymedia.net">Kaymedia Digital</a>. All rights reserved.</p>
                <p>Version 3.1.0</p>
            </div>
        </div>
    </div>
    {% else %}
        {% block login_content %}{% endblock %}
    {% endif %}
</body>
</html>
'''

# Login Template
LOGIN_PAGE = BASE.replace('{% block login_content %}{% endblock %}', '''
<div style="display:flex;justify-content:center;align-items:center;min-height:100vh;background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
    <div style="background:white;padding:40px;border-radius:10px;box-shadow:0 10px 40px rgba(0,0,0,0.2);width:350px;">
        <div style="text-align:center;margin-bottom:30px;">
            <img src="https://lhtsystem.com/public/assets/images/logo.png" alt="POS" style="max-width:120px;">
            <h2 style="color:#333;margin-top:15px;">POS</h2>
            <p style="color:#666;">Login v1.0.0</p>
        </div>
        {% if error %}<p style="color:red;margin-bottom:15px;">{{ error }}</p>{% endif %}
        <form method="POST" action="/public/home">
            <div style="margin-bottom:15px;">
                <label style="display:block;margin-bottom:5px;color:#555;font-weight:bold;">Username</label>
                <input type="text" name="username" placeholder="Username" required style="width:100%;padding:12px;border:1px solid #ddd;border-radius:5px;">
            </div>
            <div style="margin-bottom:15px;">
                <label style="display:block;margin-bottom:5px;color:#555;font-weight:bold;">Password</label>
                <input type="password" name="password" placeholder="Password" required style="width:100%;padding:12px;border:1px solid #ddd;border-radius:5px;">
            </div>
            <button type="submit" style="width:100%;padding:12px;background:#27ae60;color:white;border:none;border-radius:5px;font-size:16px;cursor:pointer;font-weight:bold;">Masuk</button>
        </form>
        <div style="margin-top:20px;text-align:center;">
            <a href="/public/home/list" style="color:#666;text-decoration:none;">List Inventory</a>
        </div>
        <div style="margin-top:30px;text-align:center;font-size:12px;color:#888;">
            <p>Made with <i class="fas fa-heart" style="color:#e74c3c;"></i> by Kay Media Digital</p>
        </div>
    </div>
</div>
''').replace('{% if session.get', '{% if False and session.get')

# Dashboard
DASHBOARD = BASE.replace('{% block content %}{% endblock %}', '''
<div class="stats-grid">
    <div class="stat-card green"><h3><i class="fas fa-file-invoice-dollar"></i> Payment</h3><div class="value">RM {{ stats.payment_total }}</div></div>
    <div class="stat-card blue"><h3><i class="fas fa-shopping-bag"></i> Selling</h3><div class="value">RM {{ stats.selling_total }}</div></div>
    <div class="stat-card orange"><h3><i class="fas fa-chart-line"></i> Profit</h3><div class="value">RM {{ stats.profit }}</div></div>
    <div class="stat-card"><h3><i class="fas fa-calendar"></i> Tanggal Hari ini</h3><div class="value" style="font-size:18px;">{{ current_date }}</div></div>
</div>
<div class="stats-grid">
    <div class="stat-card"><h3><i class="fas fa-user-cog"></i> Total Admin</h3><div class="value">{{ stats.total_user }}</div></div>
    <div class="stat-card"><h3><i class="fas fa-boxes"></i> Total Inventory</h3><div class="value">{{ stats.total_inventory }}</div></div>
    <div class="stat-card"><h3><i class="fas fa-file-invoice"></i> Total Invoice</h3><div class="value">{{ stats.total_invoice }}</div></div>
    <div class="stat-card"><h3><i class="fas fa-truck"></i> Total Suplier</h3><div class="value">{{ stats.total_suplier }}</div></div>
    <div class="stat-card"><h3><i class="fas fa-users"></i> Total Customer</h3><div class="value">{{ stats.total_customer }}</div></div>
</div>
''').replace('{% block page_title %}', '<i class="fas fa-tachometer-alt"></i> Dashboard - ').replace('{% endblock %}', '')

# Inventory List
INVENTORY_PAGE = BASE.replace('{% block content %}{% endblock %}', '''
<div class="table-container">
    <div class="table-header">
        <h3><i class="fas fa-boxes"></i> Inventory List</h3>
        <div><input type="text" class="search-box" placeholder="Search..."></div>
    </div>
    <table>
        <thead><tr><th>No</th><th>Nama Barangan</th><th>Barcode</th><th>Qty</th><th>Satuan</th><th>Harga Borong</th><th>Harga Jual</th><th>Status</th></tr></thead>
        <tbody>
            {% for item in inventory %}
            <tr>
                <td>{{ loop.index }}</td>
                <td>{{ item.nama_barangan }}</td>
                <td>{{ item.barcode or '-' }}</td>
                <td>{{ item.jumlah }}</td>
                <td>{{ item.satuan }}</td>
                <td>RM {{ item.harga_borong }}</td>
                <td>RM {{ item.harga_jual }}</td>
                <td><span style="color:green;">{{ item.status }}</span></td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
''').replace('{% block page_title %}', '<i class="fas fa-boxes"></i> Inventory - ').replace('{% endblock %}', '')

# Supplier
SUPPLIER_PAGE = BASE.replace('{% block content %}{% endblock %}', '''
<div class="table-container">
    <div class="table-header"><h3><i class="fas fa-truck"></i> Supplier List</h3></div>
    <table>
        <thead><tr><th>No</th><th>Nama Suplier</th><th>No. Tel</th><th>Alamat</th></tr></thead>
        <tbody>
            {% for s in suppliers %}
            <tr><td>{{ loop.index }}</td><td>{{ s.nama_suplier }}</td><td>{{ s.no_tel }}</td><td>{{ s.alamat }}</td></tr>
            {% endfor %}
        </tbody>
    </table>
</div>
''').replace('{% block page_title %}', '<i class="fas fa-truck"></i> Supplier - ').replace('{% endblock %}', '')

# Customer
CUSTOMER_PAGE = BASE.replace('{% block content %}{% endblock %}', '''
<div class="table-container">
    <div class="table-header"><h3><i class="fas fa-users"></i> Customer List</h3></div>
    <table>
        <thead><tr><th>No</th><th>Nama Customer</th><th>No. Tel</th><th>Alamat</th><th>Point</th></tr></thead>
        <tbody>
            {% for c in customers %}
            <tr><td>{{ loop.index }}</td><td>{{ c.nama_customer }}</td><td>{{ c.no_tel }}</td><td>{{ c.alamat }}</td><td style="color:#f39c12;font-weight:bold;">{{ c.point }}</td></tr>
            {% endfor %}
        </tbody>
    </table>
</div>
''').replace('{% block page_title %}', '<i class="fas fa-users"></i> Customer - ').replace('{% endblock %}', '')

# Invoices
INVOICE_PAGE = BASE.replace('{% block content %}{% endblock %}', '''
<div class="table-container">
    <div class="table-header"><h3><i class="fas fa-file-invoice-dollar"></i> Invoice & Payment</h3></div>
    <table>
        <thead><tr><th>No</th><th>Invoice No</th><th>Tanggal</th><th>Customer</th><th>Total</th><th>Bayaran</th><th>Status</th></tr></thead>
        <tbody>
            {% for inv in invoices %}
            <tr>
                <td>{{ loop.index }}</td>
                <td>{{ inv.id_payment }}</td>
                <td>{{ inv.tanggal }}</td>
                <td>{{ inv.nama_customer }}</td>
                <td>RM {{ inv.total }}</td>
                <td>RM {{ inv.bayaran }}</td>
                <td>{% if inv.status == 'Lunas' %}<span style="color:green;font-weight:bold;">{{ inv.status }}</span>{% else %}<span style="color:red;font-weight:bold;">{{ inv.status }}</span>{% endif %}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
''').replace('{% block page_title %}', '<i class="fas fa-file-invoice-dollar"></i> Invoice - ').replace('{% endblock %}', '')

# Selling
SELLING_PAGE = BASE.replace('{% block content %}{% endblock %}', '''
<div class="table-container">
    <div class="table-header"><h3><i class="fas fa-shopping-bag"></i> Selling List</h3></div>
    <table>
        <thead><tr><th>No</th><th>Sell ID</th><th>Tanggal</th><th>Total</th><th>Bayaran</th><th>Baki</th><th>Status</th></tr></thead>
        <tbody>
            {% for s in sales %}
            <tr><td>{{ loop.index }}</td><td>{{ s.id_sell }}</td><td>{{ s.tanggal }}</td><td>RM {{ s.total }}</td><td>RM {{ s.bayaran }}</td><td>RM {{ s.baki }}</td><td><span style="color:green;">{{ s.status }}</span></td></tr>
            {% endfor %}
        </tbody>
    </table>
</div>
''').replace('{% block page_title %}', '<i class="fas fa-shopping-bag"></i> Selling - ').replace('{% endblock %}', '')

# User
USER_PAGE = BASE.replace('{% block content %}{% endblock %}', '''
<div class="table-container">
    <div class="table-header"><h3><i class="fas fa-user-cog"></i> User List</h3></div>
    <table>
        <thead><tr><th>No</th><th>Nama</th><th>Username</th><th>Level</th><th>Status</th></tr></thead>
        <tbody>
            {% for u in users %}
            <tr><td>{{ loop.index }}</td><td>{{ u.nama }}</td><td>{{ u.username }}</td><td>{{ u.level }}</td><td><span style="color:green;">{{ u.status }}</span></td></tr>
            {% endfor %}
        </tbody>
    </table>
</div>
''').replace('{% block page_title %}', '<i class="fas fa-user-cog"></i> User - ').replace('{% endblock %}', '')

# Low Stock
LOWSTOCK_PAGE = BASE.replace('{% block content %}{% endblock %}', '''
<div class="table-container">
    <div class="table-header"><h3><i class="fas fa-level-down-alt"></i> Low Stock Items</h3></div>
    <table>
        <thead><tr><th>No</th><th>Nama Barangan</th><th>Barcode</th><th>Qty</th><th>Status</th></tr></thead>
        <tbody>
            {% for item in low_items %}
            <tr><td>{{ loop.index }}</td><td>{{ item.nama_barangan }}</td><td>{{ item.barcode or '-' }}</td><td style="color:red;font-weight:bold;">{{ item.jumlah }}</td><td style="color:red;">Low Stock</td></tr>
            {% endfor %}
        </tbody>
    </table>
</div>
''').replace('{% block page_title %}', '<i class="fas fa-level-down-alt"></i> Low Stock - ').replace('{% endblock %}', '')

# Routes
@app.route('/')
def index():
    if session.get('logged_in'): return redirect(url_for('admin'))
    return render_template_string(LOGIN_PAGE)

@app.route('/public/home', methods=['GET', 'POST'])
def login():
    if session.get('logged_in'): return redirect(url_for('admin'))
    error = None
    if request.method == 'POST':
        if request.form.get('username') == VALID_USERNAME and request.form.get('password') == VALID_PASSWORD:
            session['logged_in'] = True
            session['username'] = VALID_USERNAME
            return redirect(url_for('admin'), code=302)
        error = 'Invalid username or password'
    return render_template_string(LOGIN_PAGE, error=error)

@app.route('/home/act_login', methods=['POST'])
def act_login():
    return login()

@app.route('/public/admin')
def admin():
    if not session.get('logged_in'): return redirect(url_for('login'), code=302)
    return render_template_string(DASHBOARD, stats=stats, current_date=datetime.datetime.now().strftime('%d-%m-%Y'))

@app.route('/public/inventory')
def inventory():
    if not session.get('logged_in'): return redirect(url_for('login'), code=302)
    return render_template_string(INVENTORY_PAGE, inventory=inventory_data, stats=stats)

@app.route('/public/suplier')
def suplier():
    if not session.get('logged_in'): return redirect(url_for('login'), code=302)
    return render_template_string(SUPPLIER_PAGE, suppliers=supplier_data, stats=stats)

@app.route('/public/customer')
def customer():
    if not session.get('logged_in'): return redirect(url_for('login'), code=302)
    return render_template_string(CUSTOMER_PAGE, customers=customer_data, stats=stats)

@app.route('/public/payment')
def payment():
    if not session.get('logged_in'): return redirect(url_for('login'), code=302)
    return render_template_string(INVOICE_PAGE, invoices=invoice_data, stats=stats)

@app.route('/public/selling')
def selling():
    if not session.get('logged_in'): return redirect(url_for('login'), code=302)
    return render_template_string(SELLING_PAGE, sales=selling_data, stats=stats)

@app.route('/public/user')
def user():
    if not session.get('logged_in'): return redirect(url_for('login'), code=302)
    return render_template_string(USER_PAGE, users=user_data, stats=stats)

@app.route('/public/inventory/stok')
def low_stock():
    if not session.get('logged_in'): return redirect(url_for('login'), code=302)
    low_items = [i for i in inventory_data if int(i['jumlah']) < 10]
    return render_template_string(LOWSTOCK_PAGE, low_items=low_items, stats=stats)

@app.route('/public/home/list')
def home_list():
    if not session.get('logged_in'): return redirect(url_for('login'), code=302)
    from flask import render_template_string
    html = '<html><head><title>Inventory List</title><style>body{font-family:Arial;padding:20px;background:#f5f5f5;}.c{max-width:800px;margin:0 auto;background:white;padding:30px;border-radius:10px;}table{width:100%;border-collapse:collapse;}th,td{padding:12px;border:1px solid #ddd;text-align:left;}th{background:#4CAF50;color:white;}</style></head><body><div class="c"><h1>LEPAR HILIR TRADING</h1><p>Date: ' + datetime.datetime.now().strftime('%d-%m-%Y') + '</p><table><tr><th>No</th><th>Nama Barangan</th><th>Qty</th></tr>'
    for i, item in enumerate(inventory_data, 1): html += f'<tr><td>{i}</td><td>{item["nama_barangan"]}</td><td>{item["jumlah"]} {item["satuan"]}</td></tr>'
    html += '</table></div></body></html>'
    return html

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'), code=302)

# Dummy routes
for r in ['/public/selling/cart', '/public/quote', '/public/selling/indexMinyak', '/public/redeempoint', '/public/cheque', '/public/returns', '/public/inventory/experied', '/public/admin/versiapp', '/public/admin/qr']:
    @app.route(r)
    def dummy(r=r):
        if not session.get('logged_in'): return redirect(url_for('login'), code=302)
        return render_template_string(BASE.replace('{% block content %}{% endblock %}', '<div class="table-container"><div class="table-header"><h3><i class="fas fa-cube"></i> ' + r + '</h3></div><p style="padding:20px;">Coming soon...</p></div>').replace('{% block page_title %}', '<i class="fas fa-cube"></i> ' + r.replace('/public/','').title() + ' - ').replace('{% endblock %}', ''), stats=stats, current_date=datetime.datetime.now().strftime('%d-%m-%Y'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)