
import dotenv from 'dotenv';
import puppeteer from 'puppeteer'
import 'dotenv/config'
import * as cheerio from 'cheerio';

import mustache from "mustache";
import fetch from "node-fetch";
import fs from 'fs';
import DomParser from 'dom-parser';
const MUSTACHE_MAIN_DIR = './main.mustache';

const puppeteerService = NaN;
		
async function generateReadMe() {

  const url = "https://ezequiel.app/about.html";

  const browser = await puppeteer.launch({
    defaultViewport: {width: 1300, height: 1500, deviceScaleFactor:5}
});
  const page = await browser.newPage();
  await page.goto(url);
  const delay = ms => new Promise(resolve => setTimeout(resolve, ms))
  await delay(10000)
  
  let bodyHTML = await page.evaluate(() =>  document.documentElement.outerHTML);
  var parser = new DomParser();
  var dom = parser.parseFromString(bodyHTML);
  var inner_html = dom.getElementById('social').innerHTML

  await page.screenshot({ path: 'profile.png' })
  .then(screen => {
    fs.writeFileSync(`img_history/${Date.now()}.png`, screen);
    fs.writeFileSync(`data_history/${Date.now()}.MD`, inner_html)
    let finalReadMe = `## Hi, I am Ezequiel<br> >I enjoy building creative things. ${inner_html} <br> (:octocat: This README is updated every ~60 minutes) last update :shipit: <code>${Date()}</code>` 
    fs.writeFileSync('README.md', finalReadMe);
  })
  
  process.exit();
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
