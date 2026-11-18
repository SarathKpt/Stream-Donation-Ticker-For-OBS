import json
import os
import re
import shutil
import threading
import uuid
from flask import Flask, request, send_from_directory, jsonify, send_file, make_response, render_template, abort
from werkzeug.serving import make_server

app = Flask(__name__)

# --- Configuration ---
HOST = '0.0.0.0'
PORT = 8127

# Keep application code, local data, and settings in predictable locations.
APP_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(APP_DIR)
TEMPLATE_DIR = os.path.join(APP_DIR, 'templates')
IS_VERCEL = bool(os.environ.get('VERCEL'))
DATA_DIR = os.environ.get('STREAM_DONATION_DATA_DIR') or (os.path.join('/tmp', 'stream-donation-ticker') if IS_VERCEL else os.path.join(PROJECT_DIR, 'data'))
JSON_FILE = os.path.join(DATA_DIR, 'donations.json')
CONFIG_FILE = os.environ.get('STREAM_DONATION_CONFIG_FILE') or (os.path.join(DATA_DIR, 'config.json') if IS_VERCEL else os.path.join(PROJECT_DIR, 'config.json'))
ADMIN_FILE = 'admin.html'

DEFAULT_TICKER_CONFIG = {
    "page": "#0f172a", "ticker": "#111827", "opacity": "95",
    "text": "#ffffff", "accent": "#7c3aed",
    "filterType": "lifetime", "customStart": "", "customEnd": "",
    "currency": "₹", "speed": "120", "font": "Inter", "fontSize": "1.35",
    "code": {"html": "", "css": "", "js": ""}
}
DEFAULT_TOP_DONATION_CONFIG = {
    "page": "#0f172a", "text": "#ffffff", "accent": "#7c3aed",
    "filterType": "lifetime", "customStart": "", "customEnd": "",
    "currency": "₹", "font": "Inter", "fontSize": "1.35",
    "code": {"html": "", "css": "", "js": ""}
}
DEFAULT_CONFIG = {
    "donation-ticker": DEFAULT_TICKER_CONFIG,
    "top-donation": DEFAULT_TOP_DONATION_CONFIG
}


def normalize_config(raw):
    """Return customization grouped by widget slug, migrating the old flat file."""
    raw = raw if isinstance(raw, dict) else {}
    nested = isinstance(raw.get('donation-ticker'), dict) or isinstance(raw.get('top-donation'), dict)

    ticker = dict(DEFAULT_TICKER_CONFIG)
    top_donation = dict(DEFAULT_TOP_DONATION_CONFIG)
    if nested:
        ticker.update(raw.get('donation-ticker') or {})
        top_donation.update(raw.get('top-donation') or {})
    else:
        ticker.update({key: value for key, value in raw.items() if key in DEFAULT_TICKER_CONFIG})
        old_css = raw.get('customCSS', '')
        ticker['code'] = {"html": "", "css": old_css, "js": ""}

    for widget in (ticker, top_donation):
        code = widget.get('code') if isinstance(widget.get('code'), dict) else {}
        widget['code'] = {key: str(code.get(key, '') or '') for key in ('html', 'css', 'js')}
    return {"donation-ticker": ticker, "top-donation": top_donation}


def load_config():
    """Load the one config file and migrate legacy flat settings if needed."""
    ensure_data_files()
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            stored = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        stored = {}
    normalized = normalize_config(stored)
    if normalized != stored:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(normalized, f, indent=2)
    return normalized


def render_widget(slug, title):
    """Build a complete browser-source document from one widget's config code."""
    code = load_config().get(slug, {}).get('code', {})
    html = code.get('html', '')
    css = code.get('css', '').replace('</style', '<\\/style')
    js = code.get('js', '').replace('</script', '<\\/script')
    style_tag = f'<style>{css}</style>' if css else ''
    script_tag = f'<script>{js}</script>' if js else ''

    if re.search(r'<html\b', html, re.IGNORECASE):
        document = html
        if style_tag:
            if re.search(r'</head\s*>', document, re.IGNORECASE):
                document = re.sub(r'</head\s*>', style_tag + '</head>', document, count=1, flags=re.IGNORECASE)
            else:
                document = re.sub(r'<html\b[^>]*>', lambda match: match.group(0) + '<head>' + style_tag + '</head>', document, count=1, flags=re.IGNORECASE)
        if script_tag:
            if re.search(r'</body\s*>', document, re.IGNORECASE):
                document = re.sub(r'</body\s*>', script_tag + '</body>', document, count=1, flags=re.IGNORECASE)
            else:
                document += script_tag
    else:
        document = (
            '<!doctype html><html lang="en"><head>'
            '<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{title}</title>{style_tag}</head>'
            f'<body>{html}{script_tag}</body></html>'
        )
    return make_response(document, 200, {'Content-Type': 'text/html; charset=utf-8',
                                         'Cache-Control': 'no-cache, no-store, must-revalidate'})


def ensure_data_files():
    """Ensures writable data files exist for local and serverless runtimes."""
    os.makedirs(DATA_DIR, exist_ok=True)

    if not os.path.exists(JSON_FILE):
        source_json = os.path.join(PROJECT_DIR, 'data', 'donations.json')
        if source_json != JSON_FILE and os.path.exists(source_json):
            shutil.copyfile(source_json, JSON_FILE)
        else:
            with open(JSON_FILE, 'w', encoding='utf-8') as f:
                json.dump([], f)

    if not os.path.exists(CONFIG_FILE):
        source_config = os.path.join(PROJECT_DIR, 'config.json')
        if source_config != CONFIG_FILE and os.path.exists(source_config):
            shutil.copyfile(source_config, CONFIG_FILE)
        else:
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(DEFAULT_CONFIG, f, indent=2)


def load_donations():
    """Load donations and assign stable IDs to legacy records once."""
    try:
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        data = []
    if not isinstance(data, list):
        data = []

    changed = False
    for donation in data:
        if isinstance(donation, dict) and not donation.get('id'):
            donation['id'] = uuid.uuid4().hex
            changed = True
    if changed:
        with open(JSON_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
    return data

# --- Routes ---

@app.route('/')
def index():
    """Serves the dashboard as the application home page."""
    return send_from_directory(TEMPLATE_DIR, ADMIN_FILE)


@app.route('/customize/<slug>')
def customize_widget(slug):
    widget_names = {'donation-ticker': 'Donation Ticker', 'top-donation': 'Top Donation'}
    if slug not in widget_names:
        abort(404)
    return render_template('customize.html', widget_slug=slug, widget_name=widget_names[slug])

@app.route('/widgets/donation-ticker')
@app.route('/ticker')
def donation_ticker():
    """Serves the donation ticker composed from config.json."""
    return render_widget('donation-ticker', 'OBS Donation Ticker')

@app.route('/widgets/top-donation')
def top_donation_widget():
    """Serves the top donation widget composed from config.json."""
    return render_widget('top-donation', 'OBS Top Donation')

@app.route('/donations.json')
def get_donations():
    """Serves the donations.json file with headers to prevent caching."""
    try:
        ensure_data_files()
        load_donations()
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
    ensure_data_files()
    if request.method == 'GET':
        try:
            response = make_response(jsonify(load_config()))
            response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            return response
        except Exception:
            return jsonify(DEFAULT_CONFIG)
    
    elif request.method == 'POST':
        try:
            new_config = normalize_config(request.get_json(silent=True))
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(new_config, f, indent=2)
            return jsonify({'status': 'success', 'message': 'Config saved'}), 200
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/add-donation', methods=['POST'])
def add_donation():
    """Receives a new donation and saves it to the file."""
    try:
        ensure_data_files()
        new_donation = request.json
        if not new_donation or 'name' not in new_donation or 'tip' not in new_donation or 'date' not in new_donation:
            return jsonify({'status': 'error', 'message': 'Invalid data'}), 400

        data = load_donations()
        new_donation['id'] = uuid.uuid4().hex
        
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
        ensure_data_files()
        payload = request.json
        target_id = payload.get('id')
        if not target_id: return jsonify({'status': 'error'}), 400
        
        data = []
        if os.path.exists(JSON_FILE):
            data = load_donations()
        
        new_data = [d for d in data if d.get('id') != target_id]
        if len(new_data) == len(data):
            return jsonify({'status': 'error', 'message': 'Not found'}), 404
        
        with open(JSON_FILE, 'w', encoding='utf-8') as f:
            json.dump(new_data, f, indent=2)
            
        return jsonify({'status': 'success'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/edit-donation', methods=['POST'])
def edit_donation():
    """Edits an existing donation."""
    try:
        ensure_data_files()
        payload = request.json
        target_id = payload.get('id')
        updates = payload.get('data')
        if not target_id or not isinstance(updates, dict): return jsonify({'status': 'error'}), 400
        
        data = []
        if os.path.exists(JSON_FILE):
            data = load_donations()

        found = False
        for d in data:
            if d.get('id') == target_id:
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
    ensure_data_files()
    if not os.path.exists(JSON_FILE):
        return "TEST FAILED: File not found.", 500
    try:
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
        return f"TEST SUCCESSFUL! File content: {content}", 200
    except Exception as e:
        return f"TEST FAILED: {e}", 500

def main():
    print(f"--- OBS Donation Ticker Server ---")
    ensure_data_files()

    print(f"\n> Dashboard:  http://localhost:{PORT}")
    print(f"> Ticker URL: http://localhost:{PORT}/widgets/donation-ticker")
    print(f"> Top donor:  http://localhost:{PORT}/widgets/top-donation")

    def start_server():
        server = make_server(HOST, PORT, app, threaded=True)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        return server, thread

    server, server_thread = start_server()
    if not os.isatty(0):
        try:
            server_thread.join()
        except KeyboardInterrupt:
            pass
        finally:
            server.shutdown()
            server.server_close()
    else:
        print("Press Ctrl+R to restart or Ctrl+C to stop.")
        try:
            if os.name == 'nt':
                import msvcrt
                idle = threading.Event()
                while True:
                    if msvcrt.kbhit() and msvcrt.getwch() == '\x12':
                        print("\nCtrl+R pressed. Restarting server...")
                        server.shutdown()
                        server_thread.join()
                        server.server_close()
                        server, server_thread = start_server()
                        print("Server restarted.")
                    else:
                        idle.wait(0.05)
            else:
                import select
                import sys
                import termios
                import tty
                fd = sys.stdin.fileno()
                previous = termios.tcgetattr(fd)
                try:
                    tty.setcbreak(fd)
                    while True:
                        readable, _, _ = select.select([sys.stdin], [], [], 0.1)
                        if readable and sys.stdin.read(1) == '\x12':
                            print("\nCtrl+R pressed. Restarting server...")
                            server.shutdown()
                            server_thread.join()
                            server.server_close()
                            server, server_thread = start_server()
                            print("Server restarted.")
                finally:
                    termios.tcsetattr(fd, termios.TCSADRAIN, previous)
        except KeyboardInterrupt:
            print("\nStopping server...")
        finally:
            server.shutdown()
            server_thread.join()
            server.server_close()


if __name__ == '__main__':
    main()


