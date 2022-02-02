// index.js
console.log(process.env.COORDINATES_TOKEN)
// const aqicolors = ['#fff', '#00e400', '#ffff00', '#ff7e00', '#ff0000', '#8f3f97', '#7e0023']
// import dotenv from 'dotenv';
// import 'dotenv/config'
// //require('dotenv').config();
// //const Mustache = require('mustache');
// import mustache from "mustache";
// import fetch from "node-fetch";
// import fs from 'fs';
// const MUSTACHE_MAIN_DIR = './main.mustache';
// /**
//   * DATA is the object that contains all
//   * the data to be provided to Mustache
//   * Notice the "name" and "date" property.
// */
// var DATA = {
//   name: 'Ezequiel',
//   date: new Date().toLocaleDateString('en-US', {
//     weekday: 'long',
//     month: 'long',
//     day: 'numeric',
//     hour: 'numeric',
//     minute: 'numeric',
//     timeZoneName: 'short',
//     timeZone: 'Europe/Madrid',
//   }),
// };

		
// /**
//   * A - We open 'main.mustache'
//   * B - We ask Mustache to render our file with the data
//   * C - We create a README.md file with the generated output
//   */
// function generateReadMe() {
//   fs.readFile(MUSTACHE_MAIN_DIR, (err, data) =>  {
//     if (err) throw err;
//     const output = mustache.render(data.toString(), DATA);
//     fs.writeFileSync('README.md', output);
//   });
// }

// async function setWeatherInformation() {

//   var headers = {'Authorization': process.env.COORDINATES_TOKEN, 'Accept': '*/*', }
//   var options = { method: 'GET', headers: headers }

//   // var headers = {
//   //   'Authorization': 'token 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',
//   //   'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:96.0) Gecko/20100101 Firefox/96.0',
//   //   'Accept': 'application/vnd.github.v3+json'
//   // };

//   // var options = {
//   //   url: 'https://api.github.com/repos/ezefranca/poumonapp/issues',
//   //   headers: headers
//   // };
//   await fetch(process.env.COORDINATES_URL, options)
//   .then(response => response.text())
//   .then(body => {

//     let coordinates = JSON.parse(body)[0].body.split(":")
//     let url = `https://api.openweathermap.org/data/2.5/weather?lat=${coordinates[0]}&lon=${coordinates[1]}&appid=${process.env.OPEN_WEATHER_MAP_KEY}&units=metric`
//     fetch(
//     url
//   )
//     .then(r => r.json())
//     .then(r => {
//       let weather = { 'main': r.main, 'wind': r.wind, 'clouds': r.clouds, 'weather': r.weather[0], 'sys': r.sys }
 
//       DATA.sun_rise = new Date(weather.sys.sunrise * 1000).toLocaleString('en-GB', {
//         hour: '2-digit',
//         minute: '2-digit',
//         timeZone: 'Europe/Madrid',
//       });
//       DATA.sun_set = new Date(weather.sys.sunset * 1000).toLocaleString('en-GB', {
//         hour: '2-digit',
//         minute: '2-digit',
//         timeZone: 'Europe/Madrid',
//       });

//       var date = Date.parse(r.dt)
//       if (!date) {
//           date = new Date(Number(r.dt) * 1000)
//       }
//       let differDate = timeDiffCalc(Date.now(), date)
//       DATA.weather = `Weather is ${getWeatherEMoji(weather.weather.main)} ${weather.weather.description}, feels like <var> ${weather.main.feels_like}°C</var>, but in real <var> ${Math.round(Number(weather.main.temp))}°C </var>, 🌬 wind speed is <var> ${mps_to_kmph(Math.round(Number(weather.wind.speed)))} km/h</var>. ${differDate}`
      
//       let aqiURL = `https://api.openweathermap.org/data/2.5/air_pollution?lat=${coordinates[0]}&lon=${coordinates[1]}&appid=${process.env.OPEN_WEATHER_MAP_KEY}&units=metric`
//       fetch(aqiURL).then(s => s.json()).then(s => {
//           console.log(s.list[0])

//           date = Date.parse(s.list[0].dt)
//           if (!date) {
//               date = new Date(Number(s.list[0].dt) * 1000)
//           }
//           let aqi = Number(s.list[0].main.aqi)
//           DATA.airquality = `Air Quality index is ${aqi} (${getMessageAQI(aqi, aqicolors[aqi])}) ${timeDiffCalc(Date.now(), date)}`
        
//           generateReadMe();
//         });
      
      
      
//       //let airquelity =` Air Quality index is <var>${aqi}}</var> {{aqi_color}} {{differDate_airquality}}</p>`
    
     
//     });
//   })

// }


// function setAirQualityInformation() {


// }



// async function action() {
//   /**
//    * Fetch Weather
//    */
//   await setWeatherInformation();

//   /**
//    * Get pictures
//    */
//   //await setAirQualityInformation();

//   /**
//    * Generate README
//    */
//   // await generateReadMe();

//   /**
//    * Fermeture de la boutique 👋
//    */
//   //await puppeteerService.close();
// }

// action();

// function mps_to_kmph(mps) {
//   return (3.6 * mps);
// }

// function getWeatherEMoji(text) {

//   switch (text) {
//   case `thunderstorm`:
//       return `⛈`
//   case `drizzle`:
//       return `💧`
//   case `rain`:
//       return `☔️`
//   case `snowflake`:
//       return `❄️`
//   case `snowman`:
//       return `⛄`
//   case `atmosphere`:
//       return `🌁`
//   case `clearSky`:
//       return `☀️`
//   case `fewClouds`:
//       return `⛅`
//   case `clouds`:
//       return `☁️`
//   case `hot`:
//       return `🔥`
//   case `broken clouds`:
//     return `☁️`
//   default:
//       return `🌀`
//   }
// }


// function getMessageAQI(aqi, color) {
//   const moods = [`<span >😁</span>`, `<span >😄</span>`, `<span >😐</span>`, `<span >😟</span>`, `<span >😰</span>`]
//   switch (Number(aqi)) {
//   case 1:
//       return `<span style="color: transparent; text-shadow: 0 0 0${color}">${moods[0]}</span> Good`
//   case 2:
//       return `<span style="color: transparent; text-shadow: 0 0 0${color}">${moods[1]}</span> Fair`
//   case 3:
//       return `<span style="color: transparent; text-shadow: 0 0 0${color}">${moods[2]}</span> Moderate`
//   case 4:
//       return `<span style="color: transparent; text-shadow: 0 0 0${color}">${moods[3]}</span> Poor`
//   case 5:
//       return `<span style="color: transparent; text-shadow: 0 0 0${color}">${moods[4]}</span> Very Poor `
//   }
// }

// function timeDiffCalc(df, dn) {

//   var dateFuture = df
//   var dateNow = dn

//   if (!df) {
//       dateFuture = Date.now()
//   }

//   ////${differDate}(`future`)
//   ////${differDate}(dateFuture)

//   ////${differDate}(`now`)
//   ////${differDate}(dateNow)
//   let diffInMilliSeconds = Math.abs(dateFuture - dateNow) / 1000;

//   // calculate days
//   const days = Math.floor(diffInMilliSeconds / 86400);
//   diffInMilliSeconds -= days * 86400;
//   //////${differDate}('calculated days', days);

//   // calculate hours
//   const hours = Math.floor(diffInMilliSeconds / 3600) % 24;
//   diffInMilliSeconds -= hours * 3600;
//   //////${differDate}('calculated hours', hours);

//   // calculate minutes
//   const minutes = Math.floor(diffInMilliSeconds / 60) % 60;
//   diffInMilliSeconds -= minutes * 60;
//   //////${differDate}('minutes', minutes);

//   let difference = '';
//   if (days >= 365) {
//       difference += (days / 365 === 1) ? `${days} year` : `${days} years`;
//       return `<small class="text-muted">${difference} ago </small>`;
//   }
//   if (days >= 30) {
//       difference += (days / 30 === 1) ? `${days} month` : `${days} months`;
//       return `<small class="text-muted">${difference} ago </small>`;
//   }
//   if (days > 0) {
//       difference += (days === 1) ? `${days} day` : `${days} days`;
//   } else if (hours == 0 && minutes > 0) {
//       difference += (minutes === 0 || hours === 1) ? `${minutes} minutes` :
//           `${minutes} minutes`;
//   } else if (hours === 0) {
//       difference += `right now`
//       return `<small class="text-muted">${difference} </small>`;
//   } else {
//       difference += (hours === 0 || hours === 1) ? `${hours} hour and ` :
//           `${hours} hours and `;
//       difference += (minutes === 0 || hours === 1) ? `${minutes} minutes` :
//           `${minutes} minutes `;
//   }

//   return `<small class="text-muted">${difference} ago </small>`;
// }
