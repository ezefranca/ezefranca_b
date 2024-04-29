import feedparser
import requests
import datetime
import os

# Obtain API keys from environment variables
LASTFM_API_KEY = os.getenv('LASTFM_API_KEY')

def get_last_posts(limit=3):
    rss_url = "http://ezefranca.com/feed.rss"
    feed = feedparser.parse(rss_url)
    return [entry.title for entry in feed.entries[:limit]]

def get_last_song():
    url = f"http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user=ezefranca&api_key={LASTFM_API_KEY}&format=json"
    response = requests.get(url)
    data = response.json()
    # Parse the first track from the recent tracks
    if data['recenttracks']['track']:
        track = data['recenttracks']['track'][0]  # Get the latest track
        artist = track['artist']['#text']
        song_name = track['name']
        album_name = track['album']['#text']
        url = track['url']
        # Extract the medium size image
        image_url = next((img['#text'] for img in track['image'] if img['size'] == 'medium'), None)
        return {
            "name": song_name,
            "artist": artist,
            "album": album_name,
            "url": url,
            "image": image_url
        }
    else:
        return None

def update_readme(posts, song):
    day_name = datetime.datetime.now().strftime('%A')
    with open('README.md', 'r+') as file:
        content = file.read()
        content = content.replace('{$day_name}', day_name)
        if song:
            new_content = f"Last song listened: [{song['name']} by {song['artist']} - {song['album']}]({song['url']})\n![Cover Image]({song['image']})"
            content += "\n\n" + new_content
        # Insert posts into the content
        if posts:
            content += "\n\nLast blog posts:\n"
            for post in posts:
                content += f"- {post}\n"
        file.seek(0)
        file.write(content)
        file.truncate()

# Main execution
posts = get_last_posts()
song = get_last_song()
update_readme(posts, song)
