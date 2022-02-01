class MainStringService {
  
    init() {
      this.service = service
    }

    get(object) {
        const now = Date.now()
        var date = Date.parse(object.ts)
        if (!date) {
            date = new Date(Number(object.ts) * 1000)
        }
        var differDate = timeDiffCalc(now, date)
        var string = ""
        switch (object.type) {
        case "strava":
            return `Last activity: ${object.elements[1]}: <a class="darkmode-ignore" href=${object.elements[2]}> ${object.elements[3]} </a>, distance <var>${Number(object[4]) / 1000}</var> km, duration ${object[5]} on <a class="darkmode-ignore" href=${object[6]}> Strava ${differDate}`
        case 'weather':
            sunrise = object.sys.sunrise
            sunset = object.sys.sunset
            return `Weather is ${this.getWeatherEMoji(object.text.toLowerCase())} ${object.description}, feels like <var>${object.feels_like}°C</var>, real <var>${object.temp}°C</var>, <span class="darkmode-ignore">🌬</span> wind speed is <var> ${mps_to_kmph(object.wind.speed).toFixed(2)} km/h</var> ${differDate}`
        case 'airquality':
            return `Air Quality index is <var>${object.main.aqi}</var> (${getMessageAQI(object.main.aqi, object.color)}) ${differDate}`
        case 'location':
            var json = object
            var emojiDayState = ""
                var nowLocal = new Date(json.datetime)
                if (sunset && sunrise) {
                    var sunsetDate = new Date(sunset * 1000);
                    var sunriseDate = new Date(sunrise * 1000)
                    emojiDayState = `<span class="darkmode-ignore">☀️`
                    if (nowLocal < sunsetDate && nowLocal < sunriseDate) {
                        emojiDayState = `<span class="darkmode-ignore">🌙`
                    } else if (nowLocal < sunsetDate && nowLocal >
                        sunriseDate) {
                        emojiDayState = `<span class="darkmode-ignore">☀️`
                    } else if (nowLocal > sunsetDate && nowLocal >
                        sunriseDate) {
                        emojiDayState = `<span class="darkmode-ignore">🌙`
                    }
                }
                return `${valuesLocal.location.city}, ${valuesLocal.location.country} ${emojiDayState}  <small class="text-muted"> current time, ${nowLocal.getHours().pad()}:${nowLocal.getMinutes().pad()} </small>`
                
        case "lastfm":
            string = ``
            if (object.elements[4].value == 'true') {
                string = `<span class="wave">🎶 </span>`
                string +=
                    `playing now on <a class="darkmode-ignore" href="https://music.apple.com/profile/ezequielapp">Apple Music</a>`
            } else {
                string +=
                    `played <small>on <a class="darkmode-ignore" href="https://music.apple.com/profile/ezequielapp">Apple Music</a></small> ${differDate}`
            }
            return `${object.elements[0].value} from <a class="darkmode-ignore" href=${object.elements[3].value}> ${object.elements[2].value[[`#text`]]} </a> (${object.elements[1].value}) ${string}`
    
        case `github`:
            return `<code>${object.elements[0].value}</code> on <a class="darkmode-ignore" href=${object.elements[1].value}> ${object.elements[3].value}</a> repo on <a class="darkmode-ignore" href=${object.elements[1].value}> Github </a> ${differDate}`
        case `vaccine`:
            string = ``
        case `work`:
            string = ``
        case `mood`:
            return `I'm feeling ${getMoodEmoji(object.elements[3].value)} <mark><strong>${object.elements[3].value}</strong></mark> ${moodActivities(object)}, registered on <a class="darkmode-ignore" href="https://daylio.net/"><small>Daylio</small></a> ${differDate} `
        case `steam`:
            return `Last game played <a class="darkmode-ignore" href="https://store.steampowered.com/app/${object.elements[2].value} "> ${object.elements[0].value} </a> on <a class="darkmode-ignore" href="${object.elements[3].value} ">Steam</a> ${differDate}`
        case `twitter`:
            return `Last activity <q class='markquote'>${object.elements[0].value.replace(/(?:https?|ftp):\/\/[\n\S]+/g, '')}</q> on <small><a class="darkmode-ignore" href="${object.elements[4].value}"> ${object.elements[1].value} </a></small> ${differDate}`
        default:
            break
        }
    
        return string
    }

    getWeatherEMoji(text) {

        switch (text) {
        case `thunderstorm`:
            return `<span class="darkmode-ignore">⛈</span>`
        case `drizzle`:
            return `<span class="darkmode-ignore">💧</span>`
        case `rain`:
            return `<span class="darkmode-ignore">☔️</span>`
        case `snowflake`:
            return `<span class="darkmode-ignore">❄️</span>`
        case `snowman`:
            return `<span class="darkmode-ignore">⛄</span>`
        case `atmosphere`:
            return `<span class="darkmode-ignore">🌁</span>`
        case `clearSky`:
            return `<span class="darkmode-ignore">☀️</span>`
        case `fewClouds`:
            return `<span class="darkmode-ignore">⛅</span>`
        case `clouds`:
            return `<span class="darkmode-ignore">☁️</span>`
        case `hot`:
            return `<span class="darkmode-ignore">🔥</span>`
        default:
            return `<span class="darkmode-ignore">🌀</span>`
        }
    }
  

  }
  
  const puppeteerService = new PuppeteerService();
  
  module.exports = puppeteerService;
  