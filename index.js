// index.js

// const aqicolors = ['#fff', '#00e400', '#ffff00', '#ff7e00', '#ff0000', '#8f3f97', '#7e0023']
import dotenv from 'dotenv';
import puppeteer from 'puppeteer'
import 'dotenv/config'
import * as cheerio from 'cheerio';
// //require('dotenv').config();
// //const Mustache = require('mustache');
import mustache from "mustache";
import fetch from "node-fetch";
import fs from 'fs';
const MUSTACHE_MAIN_DIR = './main.mustache';

const puppeteerService = NaN;
// import { puppeteerService } from './services/puppeteer.service'
// /**
//   * DATA is the object that contains all
//   * the data to be provided to Mustache
//   * Notice the "name" and "date" property.
// */
var DATA = {
  name: 'Ezequiel',
  date: new Date().toLocaleDateString('en-US', {
    weekday: 'long',
    month: 'long',
    day: 'numeric',
    hour: 'numeric',
    minute: 'numeric',
    timeZoneName: 'short',
    timeZone: 'Europe/Madrid',
  }),
};

		
// /**
//   * A - We open 'main.mustache'
//   * B - We ask Mustache to render our file with the data
//   * C - We create a README.md file with the generated output
//   */
async function setInstagramPosts() {
  // images = await getProfileWidget();
  // DATA.img1 = images[0];

  const url = "https://ezequiel.app";

  // async function getPage(url) {
  //   const browser = await puppeteer.launch({headless: true});
  //   const page = await browser.newPage();
  //   await page.goto(url, {waitUntil: 'networkidle0'});

  //   const html = await page.content(); // serialized HTML of page DOM.
  //   await browser.close();
  //   return html;
  // }

  // const html = await getPage(url);
  // const $ = cheerio.load(html);
  // const span = $('.social');
  // console.log(span.text());

  const browser = await puppeteer.launch({
    defaultViewport: {width: 1500, height: 1200}
});
  const page = await browser.newPage();
  await page.goto(url);
  const delay = ms => new Promise(resolve => setTimeout(resolve, ms))
  await delay(5000)
  console.log('print')
  await page.screenshot({ path: '_profile.png' })
  .then(screen => {
    fs.writeFileSync('profile.png', screen);
    fs.writeFileSync('README.md', '<p><img width="750" src="profile.png" /></p>');
  })
  
  const html = await page.content();
  const $ = cheerio.load(html);
  const span = $('.social');
  console.log(span.text());
  process.exit();
  //await browser.close();
}

function generateReadMe() {
  fs.readFile(MUSTACHE_MAIN_DIR, (err, data) =>  {
    if (err) throw err;
    const output = mustache.render(data.toString(), DATA);
    fs.writeFileSync('README.md', output);
  });
}

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



async function action() {
  /**
   * Fetch Weather
   */
  //await setWeatherInformation();

  /**
   * Get pictures
   */
  //await setAirQualityInformation();

  /**
   * Generate README
   */
  await setInstagramPosts();
  await generateReadMe();

  /**
   * Fermeture de la boutique 👋
   */
  //await puppeteerService.close();
}

action();

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

/*

Currently:

📍&nbsp;{{location}}<br>
🌡&nbsp;{{weather}}<br>
💨&nbsp;{{airquality}}<br>
🧠&nbsp;{{mood}}<br>
🎧&nbsp;{{lastfm}}<br>
💻&nbsp;{{github}}<br>
🚲&nbsp;{{strava}}<br>
🎮&nbsp;{{steam}}<br>
🐦&nbsp;{{twitter}}<br>
*/
var page;
var browser = await puppeteer.launch({
  args: [
    '--no-sandbox',
    '--disable-setuid-sandbox',
    '--disable-infobars',
    '--window-position=0,0',
    '--ignore-certifcate-errors',
    '--ignore-certifcate-errors-spki-list',
    '--incognito',
    '--proxy-server=http=194.67.37.90:3128',
    // '--user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3312.0 Safari/537.36"', //
  ],
  // headless: false,
});



  /**
   *
   * @param {string} url
   */
  async function goToPage(url) {
    if (!browser) {
        return
    }
    page = await browser.newPage();

    await page.setExtraHTTPHeaders({
      'Accept-Language': 'en-US',
    });

    await page.goto(url, {
      waitUntil: `networkidle0`,
    });
  }

  async function close() {
    await page.close();
    await browser.close();
  }
  
  /**
   *
   * @param {string} acc Account to crawl
   * @param {number} n Qty of image to fetch
   */
  async function getProfileWidget() {
    try {
      const page = `https://ezequiel.app`//`https://dumpor.com/v/${acc}`;
      await goToPage(page);
      let previousHeight;

      //previousHeight = await this.page.evaluate(`document.body.scrollHeight`);
      //await this.page.evaluate(`window.scrollTo(0, document.body.scrollHeight)`);
      // 🔽 Doesn't seem to be needed
      // await this.page.waitForFunction(`document.body.scrollHeight > ${previousHeight}`);
      await waitFor(1000);

      const nodes = await page.evaluate(() => {
        const images = document.querySelectorAll(`.social`);
        return [].map.call(images, img => img.src);
      });

      return nodes;//nodes.slice(0, 3);
    } catch (error) {
      console.log('Error', error);
      process.exit();
    }
  }

  // async getLatestMediumPublications(acc, n) {
  //   const page = `https://medium.com/${acc}`;

  //   await this.goToPage(page);

  //   console.log('PP', page);
  //   let previousHeight;

  //   try {
  //     previousHeight = await this.page.evaluate(`document.body.scrollHeight`);
  //     console.log('MED1');
  //     await this.page.evaluate(`window.scrollTo(0, document.body.scrollHeight)`);
  //     console.log('MED2', previousHeight);
  //     await this.page.waitForFunction(`document.body.scrollHeight > ${previousHeight}`);
  //     console.log('MED3');
  //     await this.page.waitFor(1000);
  //     console.log('MED4');

  //     const nodes = await this.page.evaluate(() => {
  //       const posts = document.querySelectorAll('.fs.ft.fu.fv.fw.z.c');
  //       return [].map.call(posts);
  //     });
  //     console.log('POSTS', nodes);
  //     return;
  //   } catch (error) {
  //     console.log('Error', error);
  //     process.exit();
  //   }
  // }


