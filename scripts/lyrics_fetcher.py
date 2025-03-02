import requests
import re
from typing import Dict, Optional, Tuple
from urllib.parse import urlparse
from .config import Config

def fetch_lyrics(artist: str, title: str) -> Dict[str, str]:
    """Fetch lyrics using Genius API"""
    headers = {'Authorization': f'Bearer {Config.GENIUS_API_KEY}'}
    
    # First search for the song
    search_url = f"https://api.genius.com/search?q={artist} {title}"
    try:
        response = requests.get(search_url, headers=headers, timeout=10)
        if response.status_code == 200:
            hits = response.json()['response']['hits']
            if hits:
                # Get the first match
                song_url = hits[0]['result']['url']
                # Now fetch lyrics using lyrics.ovh as fallback
                return fetch_lyrics_from_ovh(artist, title)
        return {
            'status': 'error',
            'message': 'Song not found on Genius'
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Error: {str(e)}'
        }

# Rename existing fetch_lyrics to fetch_lyrics_from_ovh
def fetch_lyrics_from_ovh(artist: str, title: str) -> Dict[str, str]:
    """
    Fetch lyrics for a given song from lyrics.ovh API
    
    Args:
        artist (str): Name of the artist
        title (str): Title of the song
    
    Returns:
        Dict[str, str]: Dictionary containing status and either lyrics or error message
    """
    # Clean up artist and title (remove extra spaces, etc)
    artist = artist.strip()
    title = title.strip()
    
    # Construct the API URL
    url = f"https://api.lyrics.ovh/v1/{artist}/{title}"
    
    try:
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            lyrics = response.json().get('lyrics', '')
            if lyrics:
                return {
                    'status': 'success',
                    'lyrics': lyrics
                }
            else:
                return {
                    'status': 'error',
                    'message': 'No lyrics found for this song'
                }
        else:
            return {
                'status': 'error',
                'message': f'Failed to fetch lyrics (Status code: {response.status_code})'
            }
            
    except requests.exceptions.Timeout:
        return {
            'status': 'error',
            'message': 'Request timed out. Please try again.'
        }
    except requests.exceptions.RequestException as e:
        return {
            'status': 'error',
            'message': f'An error occurred: {str(e)}'
        }

def is_youtube_url(url: str) -> bool:
    """Check if the URL is a valid YouTube URL"""
    youtube_regex = r'^(https?://)?(www\.)?(youtube\.com/watch\?v=|youtu\.be/)[A-Za-z0-9_-]+.*$'
    return bool(re.match(youtube_regex, url))

def is_spotify_url(url: str) -> bool:
    """Check if the URL is a valid Spotify URL"""
    spotify_regex = r'^(https?://)?(open\.)?spotify\.com/track/[A-Za-z0-9]+.*$'
    return bool(re.match(spotify_regex, url))

def extract_from_youtube(url: str) -> Optional[Tuple[str, str]]:
    """Extract artist and title from YouTube video using oEmbed"""
    oembed_url = f"https://www.youtube.com/oembed?url={url}&format=json"
    try:
        response = requests.get(oembed_url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            title = data.get('title', '')
            # Attempt to split title into artist and song (common YouTube format: "Artist - Song")
            parts = title.split(' - ', 1)
            if len(parts) == 2:
                return parts[0], parts[1]
            return None, title
        return None, None
    except:
        return None, None

def extract_from_spotify(url: str) -> Optional[Tuple[str, str]]:
    """Extract artist and title from Spotify track using oEmbed"""
    oembed_url = f"https://open.spotify.com/oembed?url={url}"
    try:
        response = requests.get(oembed_url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            title = data.get('title', '')
            artist = data.get('author_name', '')
            return artist, title
        return None, None
    except:
        return None, None

def get_lyrics_from_url_or_title(input_text: str) -> Dict[str, str]:
    """Main function to handle both URLs and direct title input"""
    input_text = input_text.strip()
    
    if input_text.startswith(('http://', 'https://', 'www.')):
        if is_youtube_url(input_text):
            artist, title = extract_from_youtube(input_text)
        elif is_spotify_url(input_text):
            artist, title = extract_from_spotify(input_text)
        else:
            return {
                'status': 'error',
                'message': 'Unsupported URL format. Please use YouTube or Spotify links.'
            }
            
        if not title:
            return {
                'status': 'error',
                'message': 'Could not extract song information from the URL.'
            }
            
        # If we couldn't get the artist, try fetching lyrics with just the title
        if not artist:
            # Try to split title if it contains a hyphen
            parts = title.split(' - ', 1)
            if len(parts) == 2:
                artist, title = parts
            else:
                # Search without artist name
                artist = ""
    else:
        # Handle direct input (assuming format: "Artist - Title" or just "Title")
        parts = input_text.split(' - ', 1)
        if len(parts) == 2:
            artist, title = parts
        else:
            artist = ""
            title = input_text
    
    return fetch_lyrics(artist, title)

# Example usage
if __name__ == "__main__":
    # Test with different input types
    test_inputs = [
        "Rick Astley - Never Gonna Give You Up",
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "https://open.spotify.com/track/4cOdK2wGLETKBW3PvgPWqT"
    ]
    
    for input_text in test_inputs:
        print(f"\nTesting with input: {input_text}")
        result = get_lyrics_from_url_or_title(input_text)
        if result['status'] == 'success':
            print("Lyrics found!")
            print(result['lyrics'][:100] + "...")  # Print first 100 chars
        else:
            print(result['message'])
