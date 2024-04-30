import feedparser
import requests
import datetime
import os
from bs4 import BeautifulSoup
from steam_web_api import Steam

# Obtain API keys from environment variables
LASTFM_API_KEY = os.getenv('LASTFM_API_KEY')
OPEN_WEATHER_API = os.getenv('OPEN_WEATHER_API')
STEAM_API_KEY = os.environ.get("STEAM_API_KEY")

LATITUDE = 38.736567139281746
LONGITUDE = -9.303651246619502

steam = Steam(STEAM_API_KEY)

def get_current_bio(book="..."):
    
    current_date = datetime.datetime.now()
    day_name = current_date.strftime('%A')
    date_str = current_date.strftime('%d of %B of %Y')

    weather = fetch_weather_and_pollution(LATITUDE, LONGITUDE)
    weather_info = f"{weather.get('emoji', '')} The weather where I am is {weather.get('description', 'clear')}, {weather.get('temperature', 'N/A')}°C, humidity {weather.get('humidity', 'N/A')}%."

    last_game_info = get_last_game_played("76561198048997048")
    
    bio_content = (
        f"> [!TIP]\n"
        f"> - 👋 **Hello!** Wishing you a wonderful {day_name} on this {date_str}.\n"
        f"> - {weather_info}\n"
        f"> - 🙋🏻‍♂️ I'm **Ezequiel** (Ezekiel), a passionate developer and creative technologist.\n"
        f"> - 💼 Currently, I'm a **Mobile Developer** at [Miniclip](https://www.miniclip.com).\n"
        f"> - 🎓 I'm also pursuing a **PhD** in Digital Games Development at [IADE](https://www.iade.pt/en).\n"
        f"> - 📚 Currently reading the book '{book}'.\n"
        f"> - 🎮 {last_game_info}\n"
        f"> - ⚡ Feel free to connect with me on [LinkedIn](https://www.linkedin.com/in/ezefranca).\n"
        f"> > Most of the stuff on here is storage space.\n\n"
    )

    return bio_content

def get_last_game_played(steam_id):
    # Fetches the recently played games for the given Steam ID
    if not STEAM_API_KEY:
        raise ValueError("STEAM_API_KEY is not set in environment variables")

    recent_games = steam.users.get_user_recently_played_games(steam_id)
    if recent_games and recent_games.get('games'):
        last_game = recent_games['games'][0]
        game_name = last_game['name']
        last_played = datetime.datetime.fromtimestamp(last_game['last_play_time'])
        return f"Last played {game_name} on {last_played.strftime('%d %b %Y')} on Steam"
    return "No recent games played."

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

def get_last_book():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:96.0) Gecko/20100101 Firefox/96.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'If-None-Match': 'W/"f79b14fd1aab2bac76e8cddd3e691641"',
        'Cache-Control': 'max-age=0'
    }

    response = requests.get('https://www.goodreads.com/review/list/21512585-ezequiel-fran-a-dos-santos?shelf=currently-reading', headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    book_elements = soup.select('tr.bookalike')
    if book_elements:
        title = book_elements[0].select_one('td.title a').text.strip()
        author = book_elements[0].select_one('td.author a').text.strip()
        return f"{title} by {author}"
  
    else:
        return None

def get_weather_emoji(weather_condition):
    emojis = {
        'thunderstorm': '⛈',
        'drizzle': '💧',
        'rain': '☔️',
        'snow': '❄️',
        'mist': '🌫️',
        'smoke': '🌫️',
        'haze': '🌫️',
        'dust': '🌫️',
        'hot': '🔥',
        'fog': '🌁',
        'sand': '🌫️',
        'ash': '🌫️',
        'squall': '🌬️',
        'tornado': '🌪️',
        'clear': '☀️',
        'clearSky': '☀️',
        'clouds': '☁️',
        'fewClouds': '⛅',
        'atmosphere': '🌁',
        'clouds': '☁️'
    }
    return emojis.get(weather_condition.lower(), '🌡')

def fetch_weather_and_pollution(lat, lon):
    weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPEN_WEATHER_API}&units=metric"
    pollution_url = f"https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={OPEN_WEATHER_API}"
    # Fetch weather data
    weather_response = requests.get(weather_url)
    weather_data = weather_response.json() if weather_response.status_code == 200 else {}

    # Fetch pollution data
    pollution_response = requests.get(pollution_url)
    pollution_data = pollution_response.json() if pollution_response.status_code == 200 else {}

        # Prepare to extract main weather, temperature, and humidity
    if 'weather' in weather_data and weather_data['weather']:
        main_weather = weather_data['weather'][0]['main']
        description = weather_data['weather'][0]['description']
        temp = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        emoji = get_weather_emoji(description)

        # You can fetch pollution data similarly if needed here
        return {
            'emoji': emoji,
            'description': description,
            'temperature': temp,
            'humidity': humidity
        }
    return {}

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
        file.write("\n")
        
        # Writing the last song listened section
        if song:
            file.write("> [!IMPORTANT]\n")
            file.write("> Last song listened.\n")
            file.write(
                f"> | ![Cover Image]({song['image']}) | [{song['name']} by {song['artist']} - {song['album']}]({song['url']}) |\n"
                " > |---------------|:---------------------------------------------|\n"
            )

# Main execution
book = get_last_book()
song = get_last_song()
posts = get_last_posts()
bio = get_current_bio(book)
update_readme(posts, song, bio)
