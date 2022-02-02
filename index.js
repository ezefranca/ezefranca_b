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
import DomParser from 'dom-parser';
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

		

async function generateReadMe() {

  const url = "https://ezequiel.app";

  const browser = await puppeteer.launch({
    defaultViewport: {width: 1300, height: 1200, deviceScaleFactor:5}
});
  const page = await browser.newPage();
  await page.goto(url);
  const delay = ms => new Promise(resolve => setTimeout(resolve, ms))
  await delay(5000)
  console.log('print')

 
  let bodyHTML = await page.evaluate(() =>  document.documentElement.outerHTML);
  var parser = new DomParser();
  var dom = parser.parseFromString(bodyHTML);
  var inner_html = dom.getElementById('social').innerHTML


  console.log(inner_html)

  await page.screenshot({ path: '_profile.png' })
  .then(screen => {
    fs.writeFileSync('profile.png', screen);
    fs.writeFileSync('README.md', inner_html);
  })
  
  const html = await page.content();
  const $ = cheerio.load(html);
  const span = $('.social');
  console.log(span.text());
  process.exit();
  //await browser.close();
}

var stringToHTML = function (str) {
	var parser = new DOMParser();
	var doc = parser.parseFromString(str, 'text/html');
	return doc.body;
};



async function action() {
  /**
   * Generate README
   */
  await generateReadMe();

}

action();

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