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

def get_current_bio(lat, long):
    
    intro_info = get_intro_info()
    working_info = get_work_info()
    education_info = get_education_info()
    last_song_info = get_last_song_info()
    last_book_info = get_last_book_info()
    day_info = get_day_info()
    weather_info = get_weather_info(lat, long)
    air_quality_info = get_air_pollution(lat, long)
    last_game_info = get_last_game_played_info()
    last_games_ns_info = get_last_game_ns()
    last_episode_info = get_last_episode_info()
    linkedin_info = get_linkedin_info()
    presentation_info = get_last_presentation()
    
    bio_content = (
        f"- {day_info}\n"
        f"- {intro_info}\n"
        f"- {weather_info}\n"
        f"- {air_quality_info}\n"
        f"- {working_info}\n"
        f"- {education_info}\n"
        f"- {presentation_info}\n"
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
    headers = {'Authorization': f'token {GITHUB_API_KEY}'}
    github_user_endpoint = "https://api.github.com/users/ezefranca"  # Adjust username as needed

    response = requests.get(github_user_endpoint, headers=headers)
    if response.status_code == 200:
        data = response.json()
        name = data.get('name')
        bio = data.get('bio')
        if not name or not bio:
            return "🚫 GitHub profile information is incomplete."
        return f"🙋🏻‍♂️ I'm **{name}**, {bio}"
    else:
        return "🚫 Failed to fetch data from GitHub."

def get_work_info():
    headers = {'Authorization': f'token {GITHUB_API_KEY}'}
    github_user_endpoint = "https://api.github.com/users/ezefranca"  # GitHub user's endpoint

    response = requests.get(github_user_endpoint, headers=headers)
    if response.status_code == 200:
        data = response.json()
        company = data.get('company')
        if not company:
            return "🚫 No current company information available on GitHub."
        company_handle = company.lstrip('@')
        org_url = f"https://api.github.com/orgs/{company_handle}"
        org_response = requests.get(org_url, headers=headers)
        if org_response.status_code == 200:
            org_data = org_response.json()
            name = org_data.get('name', company_handle)
            description = org_data.get('description', "No description available.")
            blog_url = org_data.get('blog', 'No website provided.')

            return f"💼 Role: **Mobile Developer** at [{name}]({blog_url}) - {description}"
        else:
            return "🚫 Failed to fetch organization details from GitHub."
    else:
        return "🚫 Failed to fetch data from GitHub."

def get_education_info():
    orcid_id = '0000-0001-9321-8444'
    url = f'https://orcid.org/{orcid_id}/affiliationGroups.json'
    
    response = requests.get(url)
    data = response.json()

    if len(data['affiliationGroups']['EDUCATION']) >= 1:
        affiliations = data['affiliationGroups']['EDUCATION']
        affiliation = affiliations[-1]['affiliations'][0] 
        affiliation_roleTitle = affiliation['roleTitle']['value']
        affiliation_departmentName = affiliation['departmentName']['value']
        affiliation_url = affiliation['url']['value']
        affiliation_region = affiliation['region']['value']
        output = f"🎓I'm pursuing a {affiliation_roleTitle} at [{affiliation_departmentName}]({affiliation_url}) in {affiliation_region}."
        return output
    else:
        return f"🎓 ..."

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

def get_weather_info(lat, long):
    LATITUDE = lat
    LONGITUDE = long
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

def get_air_pollution(lat, long):
    LATITUDE = lat
    LONGITUDE = long
    pollution_url = f"https://api.openweathermap.org/data/2.5/air_pollution?lat={LATITUDE}&lon={LONGITUDE}&appid={OPEN_WEATHER_API}"
    response = requests.get(pollution_url)
    if response.status_code == 200:
        data = response.json()['list'][0]
        aqi = data['main']['aqi']
        components = data['components']

        pollution_markdown = f"🔬 Air Quality here, **AQI Level**: {aqi}"
        return pollution_markdown
    else:
        return "Failed to retrieve air pollution data."


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

def update_readme(lat, long):
    posts = get_last_posts()
    bio = get_current_bio(lat, long)
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

def parse_date(date_str):
    try:
        return datetime.datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError as e:
        print(f"Error parsing date: {e}")
        return None

def parse_timestamp(ts):
    try:
        return datetime.datetime.fromtimestamp(ts)
    except Exception as e:
        print(f"Error parsing timestamp: {e}")
        return None

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

    json_data = json.loads(response.text)

    latest_time = None
    last_played_game = None

    for item in json_data['items']:
        if 'playedApps' in item:
            for game in item['playedApps']:
                last_played_at = item.get('lastPlayedAt')
                if last_played_at:
                    last_played_at_datetime = datetime.datetime.fromtimestamp(last_played_at)
                    print(f"Checking game {game['title']} with date: {last_played_at_datetime}")  # Debug print
                    if not latest_time or last_played_at_datetime > latest_time:
                        print(f"Updating latest game: {game['title']}")  # Debug print
                        latest_time = last_played_at_datetime
                        last_played_game = game

    if last_played_game:
        game_name = last_played_game['title']
        shop_uri = last_played_game['shopUri']
        play_date = latest_time.strftime('%-d of %B of %Y')
        return f"🕹️ Last played on [Nintendo Switch](https://lounge.nintendo.com/friendcode/5071-0358-7137/DKDfpY5MsZ) was [{game_name}]({shop_uri}) on {play_date}."
    else:
        return "🕹️ No recent game played on [Nintendo Switch](https://lounge.nintendo.com/friendcode/5071-0358-7137/DKDfpY5MsZ)."


def get_last_presentation():
    url = "https://speakerdeck.com/ezefranca"
    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to retrieve the page")
        return None
    soup = BeautifulSoup(response.text, 'html.parser')
    cards = soup.find_all('div', class_='card deck-preview')

    if cards:
        last_presentation = cards[0]
        presentation_link = last_presentation.find('a', class_='deck-preview-link')['href']
        presentation_title = last_presentation.find('div', class_='deck-title').text.strip()
        last_presentation = {
            'title': presentation_title,
            'link': f"https://speakerdeck.com{presentation_link}"
        }
        if last_presentation:
            title = last_presentation['title']
            link = last_presentation['link']
            return f"💻 Last uploaded deck was [{title}]({link})"
        else:
            return "💻 No recent presentations found on [Speakerdeck](https://speakerdeck.com/ezefranca)"
    else:
        return "💻 No recent presentations found on [Speakerdeck](https://speakerdeck.com/ezefranca)"

def get_location():
    if not GITHUB_API_KEY:
        print("GitHub token not found in environment variables.")
        return

    issues_url = f"https://api.github.com/repos/ezefranca/location/issues"
    response = requests.get(issues_url, headers={'Authorization': f'token {GITHUB_API_KEY}'})

    if response.status_code != 200:
        print(f"Failed to fetch issues. Status code: {response.status_code}")
        return

    issues = response.json()

    if not issues:
        print("No issues found.")
        return

    last_issue = issues[-1]
    location_data = last_issue['body']
    lat_str, long_str = location_data.split(',')
    latitude = float(lat_str.strip())
    longitude = float(long_str.strip())
    return latitude, longitude


lat, long = get_location()
update_readme(lat, long)
update_html()
update_publications_json()

