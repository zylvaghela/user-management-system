from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/user_management_db'
mongo = PyMongo(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = mongo.db.users.find_one({'username': username, 'password': password})
        if user:
            return f'Welcome, {username}! You are logged in.'
        else:
            return 'Invalid username or password'
    else:
        return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if password != confirm_password:
            return 'Passwords do not match'
        existing_user = mongo.db.users.find_one({'username': username})
        if existing_user:
            return 'Username already exists'
        mongo.db.users.insert_one({'name': name, 'username': username, 'password': password})
        return redirect(url_for('login'))
    else:
        return render_template('signup.html')

if __name__ == '__main__':
    app.run(debug=True)







   
