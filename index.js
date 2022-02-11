
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
    defaultViewport: {width: 1300, height: 1700, deviceScaleFactor:5}
});
  const page = await browser.newPage();
  await page.goto(url);
  const delay = ms => new Promise(resolve => setTimeout(resolve, ms))
  await delay(10000)
  
  let bodyHTML = await page.evaluate(() =>  document.documentElement.outerHTML);
  var parser = new DomParser();
  var dom = parser.parseFromString(bodyHTML);
  var inner_html = dom.getElementById('social').innerHTML
  var items = inner_html.replaceAll('<p>', '<li>')
  items = items.replaceAll('</p>', '</li>')
  items = items.replaceAll('<hr/>', '')
  

  await page.screenshot({ path: 'profile.png' })
  .then(screen => {
    fs.writeFileSync(`img_history/${Date.now()}.png`, screen);
    fs.writeFileSync(`data_history/${Date.now()}.MD`, inner_html)
    let finalReadMe = `<h2><img height="30px" width="30px" src="https://camo.githubusercontent.com/e8e7b06ecf583bc040eb60e44eb5b8e0ecc5421320a92929ce21522dbc34c891/68747470733a2f2f6d656469612e67697068792e636f6d2f6d656469612f6876524a434c467a6361737252346961377a2f67697068792e676966"></img>Hi, my name is Ezequiel</h2> <blockquote> I'm a software developer who enjoys who loves building creative things. </blockquote><ul> ${items}  <li>:octocat: This README is updated every ~60 minutes </li><li> :shipit: last update <code>${Date()}</code></li></ul><br>` 
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
