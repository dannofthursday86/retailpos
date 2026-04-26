from flask import Flask, render_template_string, request, session, redirect, url_for
import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Sample inventory data similar to original
inventory_data = [
    {'id_inventory': '4434', 'nama_barangan': 'GULA PASIR PRAI 1KG', 'jumlah': '20', 'satuan': 'pcs'},
    {'id_inventory': '6039', 'nama_barangan': 'MINYAK MASAK 2KG', 'jumlah': '15', 'satuan': 'BOTOL'},
    {'id_inventory': '6040', 'nama_barangan': 'MINYAK MASAK 5KG', 'jumlah': '8', 'satuan': 'BOTOL'},
    {'id_inventory': '6389', 'nama_barangan': 'MINYAK MASAK PAKET', 'jumlah': '150', 'satuan': 'PAKET'},
    {'id_inventory': '6390', 'nama_barangan': 'TELUR AYAM GRED A', 'jumlah': '600', 'satuan': 'BIJI'},
    {'id_inventory': '6391', 'nama_barangan': 'TELUR AYAM GRED B', 'jumlah': '600', 'satuan': 'BIJI'},
    {'id_inventory': '6392', 'nama_barangan': 'TELUR AYAM GRED C', 'jumlah': '0', 'satuan': 'BIJI'},
    {'id_inventory': '6393', 'nama_barangan': 'TELUR AYAM GRED D', 'jumlah': '600', 'satuan': 'BIJI'},
    {'id_inventory': '6395', 'nama_barangan': 'MINYAK MASAK BOTOL 1KG', 'jumlah': '28', 'satuan': 'BOTOL'},
]

# Login credentials
VALID_USERNAME = 'Admin'
VALID_PASSWORD = 'admin112233'

# HTML templates
LOGIN_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>lhtsystem.com/public/home</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            font-family: Arial, sans-serif;
            background-image: url('https://lhtsystem.com/public/assets/images/bg1.jpg');
            background-size: cover;
            background-position: center;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }
        .login-container {
            background: rgba(255, 255, 255, 0.95);
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.2);
            width: 350px;
            text-align: center;
        }
        .logo {
            margin-bottom: 20px;
        }
        .logo img {
            max-width: 150px;
        }
        h2 {
            color: #333;
            margin-bottom: 30px;
        }
        .form-group {
            margin-bottom: 20px;
            text-align: left;
        }
        label {
            display: block;
            margin-bottom: 5px;
            color: #555;
            font-weight: bold;
        }
        input[type="text"],
        input[type="password"] {
            width: 100%;
            padding: 12px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 14px;
            box-sizing: border-box;
        }
        .checkbox-group {
            display: flex;
            align-items: center;
            margin-bottom: 20px;
        }
        .checkbox-group input {
            margin-right: 10px;
        }
        .btn-login {
            width: 100%;
            padding: 12px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            cursor: pointer;
            font-weight: bold;
        }
        .btn-login:hover {
            background-color: #45a049;
        }
        .nav-links {
            margin-top: 20px;
            padding-top: 20px;
            border-top: 1px solid #eee;
        }
        .nav-links a {
            color: #666;
            text-decoration: none;
            margin: 0 10px;
        }
        .nav-links a:hover {
            color: #333;
        }
        .footer {
            margin-top: 30px;
            font-size: 12px;
            color: #888;
        }
        .error {
            color: red;
            margin-bottom: 10px;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <div class="logo">
            <img src="https://lhtsystem.com/public/assets/images/logo.png" alt="POS">
        </div>
        <h2>POS</h2>
        <h3>Login v1.0.0</h3>
        
        {% if error %}
            <p class="error">{{ error }}</p>
        {% endif %}
        
        <form method="POST" action="{{ url_for('login') }}">
            <div class="form-group">
                <label for="username">Username</label>
                <input type="text" id="username" name="username" placeholder="Username" required>
            </div>
            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" id="password" name="password" placeholder="Password" required>
            </div>
            <div class="checkbox-group">
                <input type="checkbox" id="remember" name="remember">
                <label for="remember" style="display:inline; font-weight:normal;">Ingat saya</label>
            </div>
            <button type="submit" class="btn-login">Masuk</button>
        </form>
        
        <div class="nav-links">
            <a href="{{ url_for('list') }}">List Inventory</a>
        </div>
        
        <div class="footer">
            <p>Made with  by <a href="http://kaymedia.net">Kay Media Digital</a></p>
            <p>Copyright 2026</p>
        </div>
    </div>
</body>
</html>
'''

LIST_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>lhtsystem.com/public/home/list</title>
    <style>
        body {
            margin: 0;
            padding: 20px;
            font-family: Arial, sans-serif;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        h1 {
            text-align: center;
            color: #333;
            margin-bottom: 10px;
        }
        .date {
            text-align: center;
            color: #666;
            margin-bottom: 30px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            background-color: #4CAF50;
            color: white;
        }
        tr:hover {
            background-color: #f5f5f5;
        }
        .nav-links {
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #eee;
            text-align: center;
        }
        .nav-links a {
            color: #666;
            text-decoration: none;
            margin: 0 10px;
            padding: 10px 20px;
            display: inline-block;
        }
        .nav-links a:hover {
            color: #333;
            background-color: #e0e0e0;
            border-radius: 5px;
        }
        .footer {
            margin-top: 30px;
            text-align: center;
            font-size: 12px;
            color: #888;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>LEPAR HILIR TRADING</h1>
        <div class="date">Date {{ current_date }}</div>
        
        <table>
            <thead>
                <tr>
                    <th>No</th>
                    <th>Nama Barangan</th>
                    <th>Qty</th>
                </tr>
            </thead>
            <tbody>
                {% for item in inventory %}
                <tr>
                    <td>{{ loop.index }}</td>
                    <td>{{ item.nama_barangan }}</td>
                    <td>{{ item.jumlah }} {{ item.satuan }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
        
        <div class="nav-links">
            <a href="{{ url_for('login') }}">Login</a>
        </div>
        
        <div class="footer">
            <p>Made with  by <a href="http://kaymedia.net">Kay Media Digital</a></p>
            <p>Copyright 2026</p>
        </div>
    </div>
</body>
</html>
'''


@app.route('/')
def index():
    if session.get('logged_in'):
        return redirect(url_for('list'), code=302)
    return render_template_string(LOGIN_TEMPLATE)


@app.route('/public/home', methods=['GET', 'POST'])
def login():
    if session.get('logged_in'):
        return redirect(url_for('list'), code=302)
    
    error = None
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        
        if username == VALID_USERNAME and password == VALID_PASSWORD:
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('list'), code=302)
        else:
            error = 'Invalid username or password'
    
    return render_template_string(LOGIN_TEMPLATE, error=error)


@app.route('/home/act_login', methods=['POST'])
def act_login():
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    
    if username == VALID_USERNAME and password == VALID_PASSWORD:
        session['logged_in'] = True
        session['username'] = username
        return redirect(url_for('list'), code=302)
    else:
        return render_template_string(LOGIN_TEMPLATE, error='Invalid username or password')


@app.route('/public/home/list')
def list():
    if not session.get('logged_in'):
        return redirect(url_for('login'), code=302)
    
    current_date = datetime.datetime.now().strftime('%d-%m-%Y')
    return render_template_string(LIST_TEMPLATE, inventory=inventory_data, current_date=current_date)


@app.route('/home/list')
def list_alt():
    return list()


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'), code=302)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)