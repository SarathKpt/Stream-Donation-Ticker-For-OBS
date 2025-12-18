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
CONFIG_FILE = os.path.join(BASE_DIR, 'config.json') 
HTML_FILE = 'obs-ticker.html'
ADMIN_FILE = 'admin.html'

# --- Routes ---

@app.route('/')
def index():
    """Serves the main ticker for OBS."""
    return send_from_directory(BASE_DIR, HTML_FILE)

@app.route('/admin')
def admin():
    """Serves the Admin/Settings page."""
    return send_from_directory(BASE_DIR, ADMIN_FILE)

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
        return jsonify([]), 200 

@app.route('/config', methods=['GET', 'POST'])
def handle_config():
    """Reads or updates the configuration file."""
    if request.method == 'GET':
        if os.path.exists(CONFIG_FILE):
            try:
                response = make_response(send_file(CONFIG_FILE))
                response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
                return response
            except:
                return jsonify({})
        return jsonify({}) 
    
    elif request.method == 'POST':
        try:
            new_config = request.json
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(new_config, f, indent=2)
            return jsonify({'status': 'success', 'message': 'Config saved'}), 200
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500

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

@app.route('/delete-donation', methods=['POST'])
def delete_donation():
    """Deletes a donation by its date timestamp."""
    try:
        payload = request.json
        target_date = payload.get('date')
        if not target_date: return jsonify({'status': 'error'}), 400
        
        data = []
        if os.path.exists(JSON_FILE):
            with open(JSON_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
        
        new_data = [d for d in data if d.get('date') != target_date]
        
        with open(JSON_FILE, 'w', encoding='utf-8') as f:
            json.dump(new_data, f, indent=2)
            
        return jsonify({'status': 'success'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/edit-donation', methods=['POST'])
def edit_donation():
    """Edits an existing donation."""
    try:
        payload = request.json
        target_date = payload.get('original_date')
        updates = payload.get('data')
        if not target_date or not updates: return jsonify({'status': 'error'}), 400
        
        data = []
        if os.path.exists(JSON_FILE):
            with open(JSON_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)

        found = False
        for d in data:
            if d.get('date') == target_date:
                d['name'] = updates.get('name', d['name'])
                try:
                    d['tip'] = float(updates.get('tip', d['tip']))
                except: pass
                found = True
                break
        
        if found:
            with open(JSON_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            return jsonify({'status': 'success'}), 200
        else:
            return jsonify({'status': 'error', 'message': 'Not found'}), 404
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/test')
def test_file_read():
    """A test route to diagnose file reading issues."""
    print("\n--- Running /test diagnostics ---")
    if not os.path.exists(JSON_FILE):
        return "TEST FAILED: File not found.", 500
    try:
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
        return f"TEST SUCCESSFUL! File content: {content}", 200
    except Exception as e:
        return f"TEST FAILED: {e}", 500

if __name__ == '__main__':
    print(f"--- OBS Donation Ticker Server ---")
    
    if not os.path.exists(JSON_FILE):
        with open(JSON_FILE, 'w', encoding='utf-8') as f: json.dump([], f)
    
    # Ensure config.json exists with expanded defaults
    if not os.path.exists(CONFIG_FILE):
        default_conf = {
            "page": "#0f172a", "ticker": "#111827", "opacity": "95", 
            "text": "#ffffff", "accent": "#7c3aed",
            "filterType": "lifetime", "customStart": "", "customEnd": "",
            "currency": "₹", "speed": "120", "font": "Inter", "fontSize": "1.35",
            "customCSS": ""
        }
        with open(CONFIG_FILE, 'w') as f: json.dump(default_conf, f)

    print(f"\n> Ticker URL: http://{HOST}:{PORT}")
    print(f"> Admin URL:  http://{HOST}:{PORT}/admin")
    
    app.run(host=HOST, port=PORT)