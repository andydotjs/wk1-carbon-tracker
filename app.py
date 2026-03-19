import sys
print("DEBUG: Script started", file=sys.stderr)
sys.stderr.flush()

from flask import Flask, render_template
import requests
import os

print("DEBUG: Imports completed", file=sys.stderr)
sys.stderr.flush()

# Explicitly specify template folder
template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
print(f"DEBUG: Template dir: {template_dir}", file=sys.stderr)
sys.stderr.flush()

app = Flask(__name__, template_folder=template_dir)
print("DEBUG: Flask app created", file=sys.stderr)
sys.stderr.flush()

@app.route('/')
def index():
    print("DEBUG: Route handler called", file=sys.stderr)
    sys.stderr.flush()
    
    # 1. Fetch live data from the UK Carbon Intensity API
    url = "https://api.carbonintensity.org.uk/intensity"
    stats = {"index": "Loading...", "actual": "N/A", "period": "N/A"}
    
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()['data'][0]
        
        # 2. Extract the bits we want
        stats = {
            "index": data['intensity']['index'],  # e.g., "low"
            "actual": data['intensity']['actual'], # e.g., 145
            "period": data['from']                # Timeframe
        }
        print(f"DEBUG: API Response: {stats}", file=sys.stderr)
        sys.stderr.flush()
    except Exception as e:
        error_msg = f"API Error: {str(e)}"
        print(f"DEBUG: {error_msg}", file=sys.stderr)
        sys.stderr.flush()
        stats = {"index": "Error", "actual": "N/A", "period": error_msg}

    # For now, return HTML directly instead of using render_template
    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>UK Grid Status</title>
    <style>
        body {{ font-family: sans-serif; display: flex; justify-content: center; padding: 50px; background: #f4f4f9; }}
        .card {{ background: white; padding: 2rem; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); text-align: center; }}
        .status {{ font-size: 2rem; font-weight: bold; text-transform: uppercase; color: #2ecc71; }}
        .{stats['index']} {{ color: #e74c3c; }}
    </style>
</head>
<body>
    <div class="card">
        <h1>UK Grid Carbon Status</h1>
        <p class="status {stats['index']}">{stats['index']}</p>
        <p>Current Intensity: <strong>{stats['actual']} gCO2/kWh</strong></p>
        <small>Updated: {stats['period']}</small>
    </div>
</body>
</html>"""
    
    print(f"DEBUG: Returning HTML of length {len(html)}", file=sys.stderr)
    sys.stderr.flush()
    return html

if __name__ == "__main__":
    print("--- Starting Flask Server ---") # This will prove the script is running
    sys.stdout.flush()
    port = int(os.environ.get("PORT", 5050))  # Use 5050 instead of 5000
    app.run(host='127.0.0.1', port=port, debug=False)