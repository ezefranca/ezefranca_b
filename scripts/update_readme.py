import feedparser
import requests
import datetime
import os

# > [!TIP]
# > - 👋 **Hello!** Wishing you a wonderful Monday on this 29 of April of 2024.
# > - 🙋🏻‍♂️ I'm **Ezequiel** (Ezekiel), a passionate developer and creative technologist.
# > - 💼 Currently, I'm a **Mobile Developer** at [Miniclip](https://www.miniclip.com).
# > - 🎓 I'm also pursuing a **PhD** in Digital Games Development at [IADE](https://www.iade.pt/en).
# > - ⚡ Feel free to connect with me on [LinkedIn](https://www.linkedin.com/in/ezefranca).
# >> Most of the stuff on here is storage space.

# > [!NOTE]
# > Last personal updates:
#   > - [📃 Presenting at MobileSoft'24](https://ezefranca.com/news/presenting-mobilesoft-2024)
#   > - [🎖️ Internal Hackathon Miniclip 2024](https://ezefranca.com/news/hackathon-miniclip-2024)
#   > - [🥈 Tech for Good IADE 2024](https://ezefranca.com/news/tech-for-good-iade-2024)
    
# > [!IMPORTANT]
# > > Last song listened.
# > > | ![Cover Image](https://lastfm.freetls.fastly.net/i/u/64s/7b11b155153b825a3dbd6e4a600345ac.jpg) | [Mary Jane by Alanis Morissette - Jagged Little Pill (2015 Remaster)](https://www.last.fm/music/Alanis+Morissette/_/Mary+Jane) |
# > >|---------------|:---------------------------------------------|


# Obtain API keys from environment variables
LASTFM_API_KEY = os.getenv('LASTFM_API_KEY')

def get_current_bio():
    current_date = datetime.datetime.now()
    day_name = current_date.strftime('%A')
    date_str = current_date.strftime('%d of %B of %Y')

    # Create an enriched bio content with context, emojis, and Markdown, each on a new line
    bio_content = (
        f"> [!TIP]\n"
        f"> - 👋 **Hello!** Wishing you a wonderful {day_name} on this {date_str}.\n"
        f"> - 🙋🏻‍♂️ I'm **Ezequiel** (Ezekiel), a passionate developer and creative technologist.\n"
        f"> - 💼 Currently, I'm a **Mobile Developer** at [Miniclip](https://www.miniclip.com).\n"
        f"> - 🎓 I'm also pursuing a **PhD** in Digital Games Development at [IADE](https://www.iade.pt/en).\n"
        f"> - ⚡ Feel free to connect with me on [LinkedIn](https://www.linkedin.com/in/ezefranca).\n"
        f"> > Most of the stuff on here is storage space.\n\n"
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

        # Writing the blog posts section
        file.write("> [!NOTE]\n")
        file.write("> Last personal updates:\n")
        for post in posts:
            file.write(f">  - [{post['title']}]({post['link']})\n")

        # Writing the last song listened section
        if song:
            file.write("> [!IMPORTANT]\n")
            file.write("> > Last song listened.\n\n")
            file.write(f"> > | ![Cover Image]({song['image']}) | [{song['name']} by {song['artist']} - {song['album']}]({song['url']}) |\n")
            file.write("> > |---------------|:---------------------------------------------|\n\n")

# Main execution
posts = get_last_posts()
song = get_last_song()
bio = get_current_bio()
update_readme(posts, song, bio)
