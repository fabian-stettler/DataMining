const fs = require('fs');
const path = require('path');
const logToFile = require('./logging');
const {launch} = require("puppeteer");
const puppeteer = require("puppeteer");
const { addElement, newlySavedArticles} = require('./sharedArray');

const constants = require("./constants");



/**
 * Docs
 * @param url link to the current site
 * @returns {Promise<boolean>} does save the html content of @param url if certain conditions are met.
 * conditions for saving the html file are that
 *   1.srfContentId ist vorhanden
 *   2.srfContentId must be equal or bigger than 8
 *   3.url darf nicht im urls to always expand sein (diese sind ein Sonderfall, weil trotz valider content ID kein Artikel
 *
 * @function addElement wird aufgerufen um die url hinzuzufügen, welche davor gesaved wurde.
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

        // Get the HTML content of the page
        const htmlContent = await page.content();

        // Extract content from the "srf:content:id" meta tag
        const srfContentId = await page.$eval('meta[name="srf:content:id"]', meta => meta.getAttribute('content'));
        const lastSlashIndex = url.lastIndexOf('/');
        const titleOfArticle = url.slice(lastSlashIndex + 1);
        // Construct the output directory and filename (filename is the ContentId)
        const outputFile = path.join(constants.TARGET_DIR, `output_${srfContentId}_${titleOfArticle}.html`);


        // Check if the content is present and has a length greater than or equal to 8
        if (srfContentId && srfContentId.length >= 8 && !constants.SITES_TO_ALWAYS_EXPAND.includes(url)) {
            // Save the HTML content to the dynamically created file
            console.log('\x1b[31m%s\x1b[0m', "Before saving file");
            fs.writeFileSync(outputFile, htmlContent);
            console.log('\x1b[31m%s\x1b[0m', "after saving file");
            addElement(url);
            let logMessage = 'Webpage downloaded and saved!' + ' File withContentID ' + srfContentId + ' and title ' + titleOfArticle + ' was saved.';
            logToFile(logMessage, String(constants.FILE_PATH_LOG_SUCCESSFULL));
            console.log('\x1b[31m%s\x1b[0m', logMessage);
            isArticle = true;
        } else {
            let logMessage = 'Content does not meet criteria! File withContentID ' + srfContentId + ' and title ' + titleOfArticle + ' not saved.';
            logToFile(logMessage, String(constants.FILE_PATH_LOG_NO_ARTICLE));
            console.log('\x1b[31m%s\x1b[0m', logMessage);
            isArticle = false;
        }
    } catch (error) {
        logToFile('Error:' + "Die Seite hatte keine Content ID. Es kann aber auch ein anderer Fehler sein siehe hier -->" + error.message + "Hier ist der Link dazu: " + url, String(constants.FILE_PATH_LOG_ERROR));
        logToFile("Diese Seite wurde nicht gespeichert error Message: " + error.message + "Link: " + url, String(constants.FILE_PATH_LOG_NO_ARTICLE));

        console.log('\x1b[31m%s\x1b[0m', "catch clause in saveFullWebpage" + error.message + "\n title of the article: " + url);
        isArticle = false;
    }
    finally{
        await browser.close();
    }
    return isArticle;
}

saveWebpage("https://www.srf.ch/kultur/gesellschaft-religion/brennpunkt-asien-china-vs-taiwan-springt-der-funke-ins-pulverfass")
module.exports = saveWebpage;