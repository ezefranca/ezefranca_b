import feedparser
import requests
import datetime
import os
import markdown
import json
from bs4 import BeautifulSoup
from steam_web_api import Steam
from tvtimewrapper import TVTimeWrapper
from scholarly_publications.fetcher import fetch_all_publications

# Obtain API keys from environment variables
GITHUB_API_KEY = os.getenv('GH_TOKEN')
LASTFM_API_KEY = os.getenv('LASTFM_API_KEY')
OPEN_WEATHER_API = os.getenv('OPEN_WEATHER_API')
STEAM_API_KEY = os.environ.get("STEAM_API_KEY")
TV_TIME_API_KEY = os.environ.get("TV_TIME_API_KEY")
TV_TIME_API_SECRET = os.environ.get("TV_TIME_API_SECRET")

def get_current_bio():
    
    intro_info = get_intro_info()
    working_info = get_work_info()
    education_info = get_education_info()
    last_song_info = get_last_song_info()
    last_book_info = get_last_book_info()
    day_info = get_day_info()
    weather_info = get_weather_and_pollution_info()
    last_game_info = get_last_game_played_info()
    last_games_ns_info = get_last_game_ns()
    last_episode_info = get_last_episode_info()
    linkedin_info = get_linkedin_info()
    
    bio_content = (
        f"- {day_info}\n"
        f"- {weather_info}\n"
        f"- {intro_info}\n"
        f"- {working_info}\n"
        f"- {education_info}\n"
        f"- {last_book_info}\n"
        f"- {last_game_info}\n"
        f"- {last_games_ns_info}\n"
        f"- {last_episode_info}\n"
        f"- {last_song_info}\n"
        f"- {linkedin_info}\n"
        f"\n\n"
    )

    return bio_content

def get_intro_info():
    return "🙋🏻‍♂️ I'm **Ezequiel** (Ezekiel), a passionate developer and creative technologist."

def get_work_info():
    return "💼 Role: **Mobile Developer** at [Miniclip](https://github.com/miniclip)."

def get_education_info():
    return "🎓 Pursuing a **PhD** in *Digital Games Development* at [IADE](https://www.iade.pt/en)."

def get_day_info():
    current_date = datetime.datetime.now()
    day_name = current_date.strftime('%A')
    date_str = current_date.strftime('%d of %B of %Y')
    return f"👋 **Hello!** Wishing you a wonderful *{day_name}* on this {date_str}."

def get_linkedin_info():
    linkedin_info = "⚡ Feel free to connect with me on [LinkedIn](https://www.linkedin.com/in/ezefranca)."
    return linkedin_info
    
def get_last_game_played_info():
    STEAM_ID = 76561198048997048
    steam = Steam(STEAM_API_KEY)
    if not STEAM_API_KEY:
        raise ValueError("STEAM_API_KEY is not set in environment variables")

    recent_games = steam.users.get_user_recently_played_games(STEAM_ID)
    if recent_games and recent_games.get('games'):
        last_game = recent_games['games'][0]
        game_name = last_game['name']
        last_played = datetime.datetime.fromtimestamp(last_game['last_play_time'])
        return f"🎮 Last played on [Steam](https://steamcommunity.com/id/ezequielapp) was {game_name} on {last_played.strftime('%d %b %Y')}."
    else:
        from time import strftime, localtime
        userDetails = steam.users.get_user_details(STEAM_ID)
        timestamp = userDetails['player']['lastlogoff']
        last_logoff = datetime.datetime.fromtimestamp(timestamp)
        return f"🎮 No recent games played on [Steam](https://steamcommunity.com/id/ezequielapp) since {last_logoff.strftime('%d %b %Y')} :("

def get_last_posts(limit=3):
    rss_url = "http://ezefranca.com/feed.rss"
    feed = feedparser.parse(rss_url)
    # Extract post titles and URLs
    posts = [{'title': entry.title, 'link': entry.link} for entry in feed.entries[:limit]]
    return posts

def get_last_song_info():
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
        song = {
            "name": song_name,
            "artist": artist,
            "album": album_name,
            "url": url,
            "image": image_url
        }
        last_song_info = f"🎧 Latest music: {song['name']} by [{song['artist']} - {song['album']}]({song['url']}) via [LastFM](https://www.last.fm/user/ezefranca)"
        return last_song_info
    else:
        return "🎧 ..."

def get_last_book_info():
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
        book = f"**{title}** by *{author}*"
        return f"📚 Reading: {book} via [GoodReads](https://www.goodreads.com/review/list/21512585-ezequiel-fran-a-dos-santos)"
    else:
        return "📚 Currently reading nothing :("

def get_weather_emoji(weather_condition):
    emojis = {
        'thunderstorm with light rain': '⛈',  # 200
        'thunderstorm with rain': '⛈',  # 201
        'thunderstorm with heavy rain': '⛈',  # 202
        'light thunderstorm': '⛈',  # 210
        'thunderstorm': '⛈',  # 211
        'heavy thunderstorm': '⛈',  # 212
        'ragged thunderstorm': '⛈',  # 221
        'thunderstorm with light drizzle': '⛈',  # 230
        'thunderstorm with drizzle': '⛈',  # 231
        'thunderstorm with heavy drizzle': '⛈',  # 232
        'light intensity drizzle': '💧',  # 300
        'drizzle': '💧',  # 301
        'heavy intensity drizzle': '💧',  # 302
        'light intensity drizzle rain': '💧',  # 310
        'drizzle rain': '💧',  # 311
        'heavy intensity drizzle rain': '💧',  # 312
        'shower rain and drizzle': '💧',  # 313
        'heavy shower rain and drizzle': '💧',  # 314
        'shower drizzle': '💧',  # 321
        'light rain': '☔️',  # 500
        'moderate rain': '☔️',  # 501
        'heavy intensity rain': '☔️',  # 502
        'very heavy rain': '☔️',  # 503
        'extreme rain': '☔️',  # 504
        'freezing rain': '❄️',  # 511
        'light intensity shower rain': '☔️',  # 520
        'shower rain': '☔️',  # 521
        'heavy intensity shower rain': '☔️',  # 522
        'ragged shower rain': '☔️',  # 531
        'light snow': '❄️',  # 600
        'snow': '❄️',  # 601
        'heavy snow': '❄️',  # 602
        'sleet': '❄️',  # 611
        'light shower sleet': '❄️',  # 612
        'shower sleet': '❄️',  # 613
        'light rain and snow': '❄️',  # 615
        'rain and snow': '❄️',  # 616
        'light shower snow': '❄️',  # 620
        'shower snow': '❄️',  # 621
        'heavy shower snow': '❄️',  # 622
        'mist': '🌫️',  # 701
        'smoke': '🌫️',  # 711
        'haze': '🌫️',  # 721
        'sand/dust whirls': '🌫️',  # 731
        'fog': '🌫️',  # 741
        'sand': '🌫️',  # 751
        'dust': '🌫️',  # 761
        'volcanic ash': '🌫️',  # 762
        'squalls': '🌬️',  # 771
        'tornado': '🌪️',  # 781
        'clear sky': '☀️',  # 800
        'few clouds': '⛅',  # 801
        'scattered clouds': '☁️',  # 802
        'broken clouds': '☁️',  # 803
        'overcast clouds': '☁️',  # 804
    }
    return emojis.get(weather_condition.lower(), '🌡')

def get_weather_and_pollution_info():
    LATITUDE = 38.736567139281746
    LONGITUDE = -9.303651246619502
    weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={LATITUDE}&lon={LONGITUDE}&appid={OPEN_WEATHER_API}&units=metric"
    weather_response = requests.get(weather_url)
    weather_data = weather_response.json() if weather_response.status_code == 200 else {}

    if 'weather' in weather_data and weather_data['weather']:
        main_weather = weather_data['weather'][0]['main']
        description = weather_data['weather'][0]['description']
        temp = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        icon_code = weather_data['weather'][0]['icon']
        icon_url = f"https://openweathermap.org/img/wn/{icon_code}@2x.png"
        emoji = get_weather_emoji(description)


        rounded_temp_c = round(float(temp))
        temp_fahrenheit = (float(temp) * 9/5) + 32
        rounded_temp_f = round(temp_fahrenheit)

        weather = {
            'emoji': emoji,
            'description': description,
            'temperature': rounded_temp_c,
            'humidity': humidity,
            'icon_url': icon_url
        }
        weather_info = (
            f"{weather.get('emoji', '')} The weather here is {weather.get('description', '')}, "
            f"{weather.get('temperature', 'N/A')}°C ({rounded_temp_f}°F) and humidity {weather.get('humidity', 'N/A')}%."
        )
        return weather_info
    return {}

def get_last_episode_info():
    tvtime = TVTimeWrapper(TV_TIME_API_KEY, TV_TIME_API_SECRET)
    
    episodes = tvtime.episode.watched(limit=1)
    if episodes:
        episode_data = episodes[0]
        date_object = datetime.datetime.strptime(episode_data['seen_date'], '%Y-%m-%d %H:%M:%S')
        formatted_date = date_object.strftime('%d %b %Y') 
        
        # Extract details about the episode
        show_name = episode_data['show']['name']
        show_id = episode_data['show']['id']
        season_number = episode_data['season_number']
        episode_number = episode_data['number']
        episode_name = episode_data['name']
        show_url = f"https://www.tvtime.com/show/{show_id}"
        show_link = f"[{show_name}]({show_url})"
        
        last_episode_info = (
            f"📺 Recently watched {show_link} S{season_number}E{episode_number} \"{episode_name}\" on {formatted_date} via [TVTime](https://www.tvtime.com/user/4784821)."
        )
        return last_episode_info
    else:
        return "📺 No recent episodes watched, via [TVTime](https://www.tvtime.com/user/4784821)."

def update_readme():
    posts = get_last_posts()
    bio = get_current_bio()
    with open('README.md', 'w') as file:
        if bio:
            file.write(f"{bio}\n")
        # Writing the blog posts section
        file.write("> [!NOTE]\n")
        file.write("> Last personal updates:\n")
        for post in posts:
            file.write(f">  - [{post['title']}]({post['link']})\n")
        file.write("\n")

def update_html():
  with open('README.md', 'r', encoding='utf-8') as f:
      markdown_content = f.read()
      html_content = markdown.markdown(markdown_content)
      with open('index.html', 'w', encoding='utf-8') as f:
          f.write(html_content)

def update_publications_json():
    author_id = '6nOPl94AAAAJ'
    publications = fetch_all_publications(author_id, sortby='pubdate')
    with open('publications.json', 'w', encoding='utf-8') as f:
        json.dump(publications, f, ensure_ascii=False, indent=4)

def get_last_game_ns():
    if not GITHUB_API_KEY:
        print("GitHub token not found in environment variables.")
        return

    issues_url = f"https://api.github.com/repos/ezefranca/ns/issues"
    response = requests.get(issues_url, headers={'Authorization': f'token {GITHUB_API_KEY}'})

    if response.status_code != 200:
        print(f"Failed to fetch issues. Status code: {response.status_code}")
        return

    issues = response.json()

    if not issues:
        print("No issues found.")
        return

    last_issue = issues[-1]
    text_file_link = last_issue['body']
    response = requests.get(text_file_link)

    if response.status_code != 200:
        print(f"Failed to fetch text file. Status code: {response.status_code}")
        return

    text_file_data = json.loads(response.text)
    latest_game = ''
    latest_date = ''

    # Check all records to find the most recent game played
    for record in text_file_data['items']:
        if record['playedApps'] and 'date' in record:
            record_date = datetime.strptime(record['date'], "%Y-%m-%d")
            if record_date > latest_date:
                for app in record['playedApps']:
                    latest_game = app
                    latest_date = record_date

    if latest_game:
        game_name = latest_game['title']
        play_date = latest_date
        shop_uri = latest_game['shopUri']  
        return f"🕹️ Last played on [Nintendo Switch](https://nin.codes/ezefranca) was [{game_name}]({shop_uri}) on {play_date.strftime('%d %b %Y')}."
    
    return f"🕹️ No recent game played on [Nintendo Switch](https://nin.codes/ezefranca)"

update_readme()
update_html()
update_publications_json()

