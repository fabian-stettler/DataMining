const fs = require('fs');
const path = require('path');
const logToFile = require('./logging');
const {launch} = require("puppeteer");
const puppeteer = require("puppeteer");
var currentDate = new Date();
const constants = {
    FILE_PATH: '/media/supremeleader/Data/DataMiningProjekt/htmlFiles/logFile.log',
    OUTPUT_DIR:'/media/supremeleader/Data/DataMiningProjekt/htmlFiles/' + currentDate.toLocaleString(),
    SAVED_ARTICLES:'/media/supremeleader/Data/DataMiningProjekt/savedArticles.log',
};

/**
 * Docs
 * @param url link to the current site
 * @returns {Promise<boolean>} does save the html content of @param url if certain conditions are met.
 * conditions for saving the html file are that
 * 1. srfContentId must be equal or bigger than 8
 * when saving the article we save it to a file, to remember already saved articles.
 *
 */

async function saveWebpage(url) {
    const browser = await puppeteer.launch({
    executablePath: '/usr/bin/chromium-browser', // Adjust the path accordingly
    headless: true,
    });
    let page = await browser.newPage();
    let isArticle;
    try {
        // Navigate to the specified URL

        await page.goto(url, { waitUntil: 'networkidle2', timeout:15000});
        console.log('After navigating to the URL');

        // Get the HTML content of the page
        const htmlContent = await page.content();

        // Extract content from the "srf:content:id" meta tag
        const srfContentId = await page.$eval('meta[name="srf:content:id"]', meta => meta.getAttribute('content'));
        const lastSlashIndex = url.lastIndexOf('/');
        const titleOfArticle = url.slice(lastSlashIndex + 1);
        // Construct the output directory and filename (filename is the ContentId)
        const outputFile = path.join(constants.OUTPUT_DIR, `output_${srfContentId}_${titleOfArticle}.html`);

        // Ensure the output directory exists
        if (!fs.existsSync(constants.OUTPUT_DIR)) {
            fs.mkdirSync(constants.OUTPUT_DIR, { recursive: true });
            console.log("Output directory exists.");
        }

        // Check if the content is present and has a length greater than or equal to 8
        if (srfContentId && srfContentId.length >= 8) {
            // Save the HTML content to the dynamically created file
            fs.writeFileSync(outputFile, htmlContent);
            let logMessage = 'Webpage downloaded and saved!' + ' File withContentID ' + srfContentId + ' and title ' + titleOfArticle + ' was saved.';
            logToFile(logMessage, constants.FILE_PATH);
            logToFile(srfContentId + url, constants.SAVED_ARTICLES)
            isArticle = true;
	    console.log("article which will be saved was logged.");
        } else {
            let logMessage = 'Content does not meet criteria! File withContentID ' + srfContentId + ' and title ' + titleOfArticle + ' not saved.';
            logToFile(logMessage, constants.FILE_PATH);
            isArticle = false;
	    console.log("article which will not be saved was logged");
        }
    } catch (error) {
        logToFile('Error:' + error.message + "Die Seite hatte eventuell keine Content ID. Hier ist der Link dazu: " + url, constants.FILE_PATH);
        isArticle = false;
	    console.log("Fehler!!!!");
    }
    finally{
        await browser.close();
    }
    return isArticle;
}

// Replace 'https://example.com' with the URL of the webpage you want to download
saveWebpage('https://www.srf.ch/sport/fussball/super-league/22-runde-der-super-league-servette-jubelt-auch-gegen-stade-lausanne-ouchy');
module.exports = saveWebpage;
