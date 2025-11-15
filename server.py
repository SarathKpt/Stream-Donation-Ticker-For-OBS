import json
import os
from flask import Flask, request, send_from_directory, jsonify, send_file, make_response

app = Flask(__name__)

# --- Configuration ---
HOST = '0.0.0.0'
PORT = 8000

# Get the absolute path to the directory where this script is running
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_FILE = os.path.join(BASE_DIR, 'donations.json')
HTML_FILE = 'obs-ticker.html'

# --- Routes ---

@app.route('/')
def index():
    """Serves the main HTML file."""
    return send_from_directory(BASE_DIR, HTML_FILE)

@app.route('/donations.json')
def get_donations():
    """Serves the donations.json file with headers to prevent caching."""
    try:
        response = make_response(send_file(JSON_FILE))
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response
    except Exception as e:
        print(f"Error serving /donations.json: {e}")
        return jsonify({'error': 'File not found'}), 404

@app.route('/add-donation', methods=['POST'])
def add_donation():
    """Receives a new donation and saves it to the file."""
    try:
        new_donation = request.json
        if not new_donation or 'name' not in new_donation or 'tip' not in new_donation or 'date' not in new_donation:
            return jsonify({'status': 'error', 'message': 'Invalid data'}), 400

        data = []
        if os.path.exists(JSON_FILE):
            try:
                with open(JSON_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if not isinstance(data, list): data = []
            except json.JSONDecodeError:
                data = [] 
        
        data.append(new_donation)

        with open(JSON_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

        return jsonify({'status': 'success', 'message': 'Donation added'}), 201

    except Exception as e:
        print(f"Error adding donation: {e}")
        return jsonify({'status': 'error', 'message': 'Internal server error'}), 500

# --- NEW DIAGNOSTIC ROUTE ---
@app.route('/test')
def test_file_read():
    """A test route to diagnose file reading issues."""
    print("\n--- Running /test diagnostics ---")
    print(f"Script base directory: {BASE_DIR}")
    print(f"Attempting to read file at path: {JSON_FILE}")
    
    if not os.path.exists(JSON_FILE):
        print("DIAGNOSIS: File does not exist at the path.")
        print("Please check for typos or hidden file extensions (like .json.txt)")
        return "TEST FAILED: File not found. Check terminal.", 500
    
    print("File was found. Attempting to open and read...")
    
    try:
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("DIAGNOSIS: File read successfully.")
        print(f"File content: {content}")
        return f"TEST SUCCESSFUL! File content: {content}", 200
        
    except Exception as e:
        print(f"DIAGNOSIS: File found but could not be read.")
        print(f"!!!!!!!! THE REAL ERROR IS: {e} !!!!!!!!")
        return f"TEST FAILED: File found but couldn't be read. Check terminal for the *real* error. {e}", 500

if __name__ == '__main__':
    print(f"--- OBS Donation Ticker Server ---")
    
    if not os.path.exists(JSON_FILE):
        print(f"Warning: '{JSON_FILE}' not found.")
        print(f"Creating empty '[]' file at: {JSON_FILE}")
        try:
            with open(JSON_FILE, 'w', encoding='utf-8') as f:
                json.dump([], f)
        except Exception as e:
            print(f"FATAL ERROR: Could not create {JSON_FILE}. Check permissions.")
            print(e)
            exit(1)
    else:
        print(f"Found '{JSON_FILE}' at: {JSON_FILE}")

    print(f"\nStarting server at http://{HOST}:{PORT}")
    print(f"Please open http://localhost:{PORT} in your browser.")
    print(f"Serving files from this directory: {BASE_DIR}")
    print("Press CTRL+C to stop the server.")
            
    app.run(host=HOST, port=PORT)