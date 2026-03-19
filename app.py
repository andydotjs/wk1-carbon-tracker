from flask import Flask, render_template
import requests
import os

app = Flask(__name__)

@app.route('/')
def index():
    # 1. Fetch live data from the UK Carbon Intensity API
    url = "https://api.carbonintensity.org.uk/intensity"
    try:
        response = requests.get(url)
        data = response.json()['data'][0]
        
        # 2. Extract the bits we want
        stats = {
            "index": data['intensity']['index'],  # e.g., "low"
            "actual": data['intensity']['actual'], # e.g., 145
            "period": data['from']                # Timeframe
        }
    except Exception as e:
        stats = {"index": "Error", "actual": "N/A", "period": str(e)}

    return render_template('index.html', stats=stats)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)