const fs = require('fs');
const path = require('path');
const logToFile = require('./logging');
const {launch} = require("puppeteer");
const puppeteer = require("puppeteer");
const constants = require("./constants");



/**
 * Docs
 * @param url link to the current site
 * @returns {Promise<boolean>} does save the html content of @param url if certain conditions are met.
 * conditions for saving the html file are that
 * 1. srfContentId must be equal or bigger than 8
 * 2.
 *
 */

async function saveWebpage(url) {
    const browser = await puppeteer.launch({
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    let page = await browser.newPage();
    let isArticle;
    try {
        // Navigate to the specified URL

        await page.goto(url, { waitUntil: 'networkidle2', timeout:6000});
        console.log('After navigating to the URL');

        // Wait for the page to load completely
        await page.waitForTimeout(2000); // Adjust as needed based on the webpage

        // Get the HTML content of the page
        const htmlContent = await page.content();

        // Extract content from the "srf:content:id" meta tag
        const srfContentId = await page.$eval('meta[name="srf:content:id"]', meta => meta.getAttribute('content'));
        const lastSlashIndex = url.lastIndexOf('/');
        const titleOfArticle = url.slice(lastSlashIndex + 1);
        // Construct the output directory and filename (filename is the ContentId)
        const outputFile = path.join(constants.TARGET_DIR, `output_${srfContentId}_${titleOfArticle}.html`);

        // Ensure the output directory exists
        if (!fs.existsSync(constants.TARGET_DIR)) {
            fs.mkdirSync(constants.TARGET_DIR, { recursive: true });
        }

        // Check if the content is present and has a length greater than or equal to 8
        if (srfContentId && srfContentId.length >= 8) {
            // Save the HTML content to the dynamically created file
            fs.writeFileSync(outputFile, htmlContent);
            constants.NEW_ARTICLES.add(url);
            let logMessage = 'Webpage downloaded and saved!' + ' File withContentID ' + srfContentId + ' and title ' + titleOfArticle + ' was saved.';
            logToFile(logMessage, String(constants.FILE_PATH_LOG_SUCCESSFULL));
            isArticle = true;
        } else {
            let logMessage = 'Content does not meet criteria! File withContentID ' + srfContentId + ' and title ' + titleOfArticle + ' not saved.';
            logToFile(logMessage, String(constants.FILE_PATH_LOG_NO_ARTICLE));
            isArticle = false;
        }
    } catch (error) {
        logToFile('Error:' + error.message + "Die Seite hatte keine Content ID. Hier ist der Link dazu: " + url, String(constants.FILE_PATH_LOG_ERROR));
        isArticle = false;
    }
    finally{
        await browser.close();
    }
    return isArticle;
}

//saveWebpage('https://www.srf.ch/sport/fussball/super-league/22-runde-der-super-league-servette-jubelt-auch-gegen-stade-lausanne-ouchy');
module.exports = saveWebpage;