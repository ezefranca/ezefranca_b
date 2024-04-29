import feedparser
import requests
import datetime

def get_last_posts(limit=3):
    rss_url = "http://ezefranca.com/feed.rss"
    feed = feedparser.parse(rss_url)
    return [entry.title for entry in feed.entries[:limit]]

def get_last_song():
    url = f"http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user=yourusername&api_key={LASTFM_API_KEY}&api_sig={LASTFM_API_SECRET}&format=json"
    response = requests.get(url)
    data = response.json()
    track = data['recenttracks']['track'][0]
    return {
        "name": track['name'],
        "artist": track['artist']['#text'],
        "cover": track['image'][2]['#text']  # middle size image
    }

def update_readme(posts, song):
    with open('README.md', 'r+') as file:
        content = file.read()
        content = content.replace('{$day_name}', datetime.datetime.now().strftime('%A'))
        # Insert posts and song into the content
        print(content)
        file.seek(0)
        file.write(content)
        file.truncate()

# Main execution
posts = get_last_posts()
song = get_last_song()
update_readme(posts, song)
