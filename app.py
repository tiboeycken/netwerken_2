from flask import Flask, send_from_directory
import csv
import os

app = Flask(__name__)

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

@app.route('/api/counter', methods=['GET'])
def read_counter():
    return get_counter()

@app.route('/api/counter/increment', methods=['POST'])
def update_counter():
    return increment_counter()

@app.route('/webserver1/')
def server1_index():
    return send_from_directory(os.path.join('.', 'webserver1'), 'index.html')

@app.route('/webserver2/')
def server2_index():
    return send_from_directory(os.path.join('.', 'webserver2'), 'index.html')

@app.route('/webserver1/<path:filename>')
def webserver1_static(filename):
    return send_from_directory(os.path.join('.', 'webserver1'), filename)

@app.route('/webserver2/<path:filename>')
def webserver2_static(filename):
    return send_from_directory(os.path.join('.', 'webserver2'), filename)

if __name__ == '__main__':
    app.run(debug=True, port=5000)