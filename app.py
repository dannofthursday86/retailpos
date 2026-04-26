from flask import Flask, render_template_string, request, session, redirect
app = Flask(__name__)
app.secret_key = 'key123'

@app.route('/')
@app.route('/public/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if request.form.get('username') == 'Admin' and request.form.get('password') == 'admin112233':
            session['logged_in'] = True
            session['username'] = 'Admin'
            return redirect('/public/admin')
        return '<h1>Wrong password</h1><a href="/public/home">Back</a>'
    return '''<h1>POS Login</h1>
    <form method="post">
    <input name="username" placeholder="Username" required>
    <input name="password" type="password" placeholder="Password" required>
    <button type="submit">Login</button>
    </form>'''

@app.route('/public/admin')
def admin():
    if not session.get('logged_in'):
        return redirect('/public/home')
    return '''<h1>POS Dashboard</h1>
    <p>Welcome, ''' + session.get('username', '') + '''</p>
    <ul>
    <li><a href="/public/inventory">Inventory</a></li>
    <li><a href="/public/suplier">Supplier</a></li>
    <li><a href="/public/customer">Customer</a></li>
    <li><a href="/public/selling/cart">POS</a></li>
    <li><a href="/public/selling">Selling</a></li>
    <li><a href="/public/cheque">Cheque</a></li>
    <li><a href="/public/payment">Payment</a></li>
    <li><a href="/public/returns">Return</a></li>
    <li><a href="/public/user">User</a></li>
    </ul>
    <a href="/logout">Logout</a>'''

@app.route('/public/inventory')
def inventory():
    if not session.get('logged_in'): return redirect('/public/home')
    return '<h1>Inventory</h1><a href="/public/admin">Back</a>'

@app.route('/public/suplier')  
def suplier():
    if not session.get('logged_in'): return redirect('/public/home')
    return '<h1>Supplier</h1><a href="/public/admin">Back</a>'

@app.route('/public/customer')
def customer():
    if not session.get('logged_in'): return redirect('/public/home')
    return '<h1>Customer</h1><a href="/public/admin">Back</a>'

@app.route('/public/selling/cart')
def cart():
    if not session.get('logged_in'): return redirect('/public/home')
    return '<h1>POS Cart</h1><a href="/public/admin">Back</a>'

@app.route('/public/selling')
def selling():
    if not session.get('logged_in'): return redirect('/public/home')
    return '<h1>Selling</h1><a href="/public/admin">Back</a>'

@app.route('/public/cheque')
def cheque():
    if not session.get('logged_in'): return redirect('/public/home')
    return '<h1>Cheque</h1><a href="/public/admin">Back</a>'

@app.route('/public/payment')
def payment():
    if not session.get('logged_in'): return redirect('/public/home')
    return '<h1>Payment</h1><a href="/public/admin">Back</a>'

@app.route('/public/returns')
def returns():
    if not session.get('logged_in'): return redirect('/public/home')
    return '<h1>Returns</h1><a href="/public/admin">Back</a>'

@app.route('/public/user')
def user():
    if not session.get('logged_in'): return redirect('/public/home')
    return '<h1>User</h1><a href="/public/admin">Back</a>'

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/public/home')

if __name__ == '__main__':
    app.run(debug=True)
