const puppeteer = require('puppeteer');
const logToFile = require('./logging');


/**
 *Docs
 * @param url Is the site which we want to extract the sublinks from.
 * @param websiteUrl Is the site which we want to extract the sublinks from.
 *
 *
 * @returns {Promise<*>} all filtered absolute links to all pages which are linked from the current page.
 * filtering does filter out all links with '_' and '#' and duplicate links.
 *
 */

async function getAllAbsoluteLinks(url, websiteUrl) {
    let links = [];
    let finalfilteredLinks = [];
    const browser = await puppeteer.launch({
    executablePath: '/usr/bin/chromium-browser', // Adjust the path accordingly
    headless: true,
    });
    const page = await browser.newPage();

    try{
        await page.goto(url, { waitUntil: 'networkidle2', timeout:15000}).catch(error => console.error('Error during page.goto:', error));
        links = await page.$$eval('a', anchors => anchors.map(anchor => anchor.href)).catch(error => console.error('Error during page.goto:', error));
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
        console.log(finalfilteredLinks.length);
        console.log('Filtered Links:', finalfilteredLinks);
    }
    catch(error){
        throw error;
    }
    finally {
        await browser.close();
    }
    return finalfilteredLinks;
}

async function run() {
    const websiteUrl = 'https://www.srf.ch/sport';
}

module.exports = { run, getAllAbsoluteLinks }; // Export both the run function and getAllAbsoluteLinks function

// In another file where you use this function
