import feedparser
import requests
import datetime
import os

# Obtain API keys from environment variables
LASTFM_API_KEY = os.getenv('LASTFM_API_KEY')

def get_current_bio():
    current_date = datetime.datetime.now()
    day_name = current_date.strftime('%A')
    date_str = current_date.strftime('%d of %B of %Y')

    # Create a bio content with context and emojis
    bio_content = (
        f"👋 Hello, nice {day_name}, on {date_str}. I am working as a Mobile Developer "
        f"🙋🏻‍♂️ I'm Ezequiel (Ezekiel), a developer and creative technologist. I enjoy creating software tools and making basil pesto.\n"
        f"💼📱 [@miniclip](https://github.com/miniclip) and advancing my PhD studies in Technology 👨🏻‍💻🎓 [@iade-pt](https://github.com/iade-pt). "
        f"👾 Passionate about game development and leveraging tech for creative solutions!"
    )

    return bio_content

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

def update_readme(posts, song, bio):
    day_name = datetime.datetime.now().strftime('%A')
    with open('README.md', 'w') as file:
        # Writing the greeting with the day name
        if bio:
            file.write(f"{bio}\n")

        # Writing the tip section
        file.write("> [!TIP]\n")
        file.write("> Most of the stuff on here is storage space.\n")

        # Writing the blog posts section
        file.write("> [!NOTE]\n")
        file.write("> Last personal updates:\n")
        for post in posts:
            file.write(f"  - [{post['title']}]({post['link']})\n")

        # Writing the last song listened section
        if song:
            file.write("> [!IMPORTANT]\n")
            file.write("> Last song listened.\n\n")
            file.write(f"| ![Cover Image]({song['image']}) | [{song['name']} by {song['artist']} - {song['album']}]({song['url']}) |\n")
            file.write("|---------------|:---------------------------------------------|\n\n")

# Main execution
posts = get_last_posts()
song = get_last_song()
bio = get_current_bio()
update_readme(posts, song)
