import feedparser
import requests
import datetime
import os

# Obtain API keys from environment variables
LASTFM_API_KEY = os.getenv('LASTFM_API_KEY')

def get_last_posts(limit=3):
    rss_url = "http://ezefranca.com/feed.rss"
    feed = feedparser.parse(rss_url)
    # Extract post titles and URLs
    posts = [{'title': entry.title, 'link': entry.link} for entry in feed.entries[:limit]]
    return posts

def get_last_song():
    url = f"http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user=ezefranca&api_key={LASTFM_API_KEY}&format=json"
    response = requests.get(url)
    data = response.json()
    if data['recenttracks']['track']:
        track = data['recenttracks']['track'][0]
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
    with open('README.md', 'w') as file:
        # Writing the greeting with the day name
        file.write(f"> Happy {day_name}! 👋🏻\n\n")

        # Writing the tip section
        file.write("> [!TIP]\n")
        file.write("> Hey, 👋🏻, I'm Ezequiel (Ezekiel), an iOS developer and Creative Technologist with experience in various areas of technology such as mobile software development, game development, project design, software engineering, electronics, and the Internet of Things. I also enjoy creating software tools and making basil pesto. </blockquote>\n\n")
        file.write("> Most of the stuff on here is storage space.\n\n")

        # Writing the last song listened section
        if song:
            file.write("> [!IMPORTANT]\n")
            file.write("> Last song listened.\n\n")
            file.write(f"| ![Cover Image]({song['image']}) | [{song['name']} by {song['artist']} - {song['album']}]({song['url']}) |\n")
            file.write("|---------------|:---------------------------------------------|\n\n")

        # Writing the blog posts section
        file.write("> [!NOTE]\n")
        file.write("> Last personal updates:\n")
        for post in posts:
            file.write(f"  - [{post['title']}]({post['link']})\n")

# Main execution
posts = get_last_posts()
song = get_last_song()
update_readme(posts, song)
