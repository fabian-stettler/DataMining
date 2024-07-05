const puppeteer = require('puppeteer');
const logToFile = require('./logging');
const constants = require("./constants");



/**
 *Docs
 * @param url Is the site which we want to extract the sublinks from.
 * @param websiteUrl Is the site which we want to extract the sublinks from.
 *
 *
 * @returns {Promise<*>} all filtered absolute links to all pages which are linked from the current page.
 * filtering does filter out all links with '_' and '#' and duplicate links.
 *
* @exception page.goto wird direkt gehandelt und führt nicht zu Abbruch des Skriptes sondern nur zu einem Error Log.
 * @exception page.eval wird direkt gehandelt und führt nicht zu Abbruch des Skriptes sondern nur zu einem Error Log.
 * @exception error (andere exceptions im try Block) führen zu einem abort über catch.
 */

async function getAllAbsoluteLinks(url, websiteUrl) {
    let links = [];
    let finalfilteredLinks = [];
    const browser = await puppeteer.launch({
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    const page = await browser.newPage();

    try{
        await page.goto(url, { waitUntil: 'networkidle2', timeout:15000}).catch(error => logToFile('Error during page.goto:' + error, constants.FILE_PATH_LOG_ERROR));
        links = await page.$$eval('a', anchors => anchors.map(anchor => anchor.href)).catch(error => logToFile('Error during page.eval:' + error, constants.FILE_PATH_LOG_ERROR));
        console.log('Links before filtering:', links);

        //filter all links which do not match the websiteUrl (which are not in the same scope)
        //delete duplicates and delete the websiteUrl itself (links to itself)
        const filteredLinks = links.filter(link => link.startsWith(websiteUrl));
        let filteredLinksReflexive = filteredLinks.filter(item => item !== websiteUrl.toString());
        let filteredLinksDuplicates = filteredLinksReflexive.filter((value, index, self) => {
            return self.indexOf(value) === index;
        });
        let filteredLinksHashtagLess = filteredLinksDuplicates.filter( item => !item.includes('#') && !item.includes('_'));
        finalfilteredLinks = filteredLinksHashtagLess.filter(item => item.startsWith(websiteUrl));
        console.log('Length of filtered Links: ', finalfilteredLinks.length);
        console.log('Filtered Links:', finalfilteredLinks);
    }
    catch(error){
        logToFile("Error in extractAllLinksFromWebpage " + error.message , constants.FILE_PATH_LOG_ERROR);
        logToFile("Abort error occured in <extractAllLinksFromWebpage,js>, siehe letzter Eintrag im File: FILE_PATH_LOG_ERROR", constants.FILE_PATH_LOG_ABORT_ERROR);
        return;
    }
    finally {
        await browser.close();
    }
    return finalfilteredLinks;
}

module.exports = { getAllAbsoluteLinks }; // Export both the run function and getAllAbsoluteLinks function
