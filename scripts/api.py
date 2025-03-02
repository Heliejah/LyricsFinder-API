import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from .lyrics_fetcher import get_lyrics_from_url_or_title

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Get config from environment variables
port = int(os.environ.get('PORT', 10000))
flask_env = os.environ.get('FLASK_ENV', 'production')

@app.route('/')
def hello():
    return {"status": "success", "message": "API is running"}

@app.route('/favicon.ico')
def favicon():
    return '', 204  # Return No Content response for favicon requests

@app.route('/get_lyrics', methods=['GET'])
def get_lyrics():
    """
    Endpoint to fetch lyrics. Accepts either:
    - query parameter: song title/URL
    - query parameters: artist and title separately
    """
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
            'message': 'Missing required parameters. Provide either "query" or both "artist" and "title"'
        }), 400

@app.errorhandler(Exception)
def handle_error(error):
    """Handle any unhandled exceptions"""
    return jsonify({
        'status': 'error',
        'message': str(error)
    }), 500

@app.errorhandler(500)
def internal_error(error):
    return {
        "status": "error",
        "message": "Internal server error occurred"
    }, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', 
            port=port,
            debug=flask_env == 'development')