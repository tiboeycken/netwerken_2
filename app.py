from flask import Flask, send_from_directory
import csv
import subprocess
import os

app = Flask(__name__)

REMOTE_HOST = 'webserver2@192.168.100.12'
REMOTE_PATH = '/home/webserver2/netwerken2isb/'
SERVER_ID = os.environ.get('SERVER_ID', 'default')  # Get server ID from environment variable

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


def sync_counter():
    try:
        # Gebruik het absolute pad naar rsync
        subprocess.run(['/usr/bin/rsync', '-avz', COUNTER_FILE, f'{REMOTE_HOST}:{REMOTE_PATH}'], check=True)
        print("Counter gesynchroniseerd.")
    except subprocess.CalledProcessError as e:
        print(f"Fout tijdens synchronisatie: {e}")
    except FileNotFoundError:
        print(f"Bestand niet gevonden: {COUNTER_FILE}")


@app.route('/')
def serve_root():
    folder = 'webserver1' if SERVER_ID == 'server1' else 'webserver2'
    return send_from_directory(folder, 'index.html')


@app.route('/<path:filename>')
def serve_static(filename):
    folder = 'webserver1' if SERVER_ID == 'server1' else 'webserver2'
    return send_from_directory(folder, filename)


@app.route('/api/counter', methods=['GET'])
def read_counter():
    return get_counter()


@app.route('/api/counter/increment', methods=['POST'])
def update_counter():
    new_value = increment_counter()
    if not new_value.startswith("Error"):  # Controleer of het incrementeren succesvol was
        sync_counter()
        return new_value
    else:
        return new_value

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
