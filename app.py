from flask import Flask, request, jsonify
from flask_cors import CORS
from scripts.lyrics_fetcher import get_lyrics_from_url_or_title

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return 'Lyrics API is running'

@app.route('/get_lyrics')
def get_lyrics():
    query = request.args.get('query')
    artist = request.args.get('artist')
    title = request.args.get('title')

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
    app.run(debug=True)
