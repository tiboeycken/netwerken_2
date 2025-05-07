from flask import Flask, send_from_directory
import csv
import os

app = Flask(__name__)

SERVER_ID = os.environ.get('SERVER_ID', 'default') # Get server ID from environment variable

COUNTER_FILE = 'shared_counter.csv'

# Initialize counter file (same as before)
if not os.path.exists(COUNTER_FILE):
    with open(COUNTER_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['0'])

# get_counter() and increment_counter() functions (same as before)
def get_counter():
    try:
        with open(COUNTER_FILE, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if row:
                    return row[0]
        return '0'
    except FileNotFoundError:
        return '0'
    except Exception as e:
        print(f"Error reading counter: {e}")
        return 'Error'

def increment_counter():
    try:
        current_value = int(get_counter())
        new_value = current_value + 1
        with open(COUNTER_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([str(new_value)])
        return str(new_value)
    except Exception as e:
        return f"Error incrementing counter: {e}"

@app.route('/')
def serve_root():
    if SERVER_ID == 'server1':
        return send_from_directory(os.path.join('.', 'webserver1'), 'index.html')
    elif SERVER_ID == 'server2':
        return send_from_directory(os.path.join('.', 'webserver2'), 'index.html')
    else:
        return "Welcome to the Load Balanced Application!" # Default if no ID

@app.route('/api/counter', methods=['GET'])
def read_counter():
    return get_counter()

@app.route('/api/counter/increment', methods=['POST'])
def update_counter():
    return increment_counter()

@app.route('/<path:filename>')
def serve_static(filename):
    if SERVER_ID == 'server1':
        return send_from_directory(os.path.join('.', 'webserver1'), filename)
    elif SERVER_ID == 'server2':
        return send_from_directory(os.path.join('.', 'webserver2'), filename)
    else:
        # Fallback to root if no ID
        return send_from_directory('.', filename)

if __name__ == '__main__':
    app.run(debug=True, port=5000)