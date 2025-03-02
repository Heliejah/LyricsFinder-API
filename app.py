import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from scripts.lyrics_fetcher import get_lyrics_from_url_or_title
from scripts.config import Config

app = Flask(__name__)
CORS(app)

GENIUS_API_KEY = Config.GENIUS_API_KEY

@app.route('/')
def home():
    return 'Lyrics API is running'

@app.route('/get_lyrics')
def get_lyrics():
    query = request.args.get('query')
    artist = request.args.get('artist')
    title = request.args.get('title')

    # If we have both artist and title, try Genius API first
    if artist and title:
        print(f"Fetching lyrics for: {artist} - {title}")  # Debugging
        
        # Fetch from Genius API
        base_url = "https://api.genius.com/search"
        headers = {"Authorization": f"Bearer {GENIUS_API_KEY}"}
        params = {"q": f"{artist} {title}"}

        try:
            response = requests.get(base_url, headers=headers, params=params)
            print("Genius API Response:", response.status_code)  # Debugging

            if response.status_code == 200:
                json_data = response.json()
                if json_data["response"]["hits"]:
                    song_url = json_data["response"]["hits"][0]["result"]["url"]
                    return jsonify({
                        "status": "success",
                        "lyrics_url": song_url
                    })
        except Exception as e:
            print(f"Genius API error: {str(e)}")
            # Fall through to lyrics.ovh if Genius fails
    
    # Fallback to lyrics.ovh
    if query:
        result = get_lyrics_from_url_or_title(query)
        return jsonify(result)
    elif artist and title:
        result = get_lyrics_from_url_or_title(f"{artist} - {title}")
        return jsonify(result)
    else:
        return jsonify({
            'status': 'error',
            'message': 'Missing parameters'
        }), 400

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
