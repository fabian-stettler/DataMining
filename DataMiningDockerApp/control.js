const { getAllAbsoluteLinks } = require('./extractAllLinksFromWebpage.js');
const saveWebpage = require('./saveFullWebpage');
const {launch} = require("puppeteer");
const createNewTargetDirectory = require('./createNewTargetDirectory');
const { readTitlesFromFile, overwriteSavedArticles } = require('./readWriteTitles');
const {sharedArray, newlySavedArticles} = require("./sharedArray");
const constants = require("./constants");
const logToFile = require("./logging");

/**
 * controls the execution of the web scrapping task on srf.ch
 * @returns nothing
 */


async function control() {
    let alreadyExpandedSites = [];
    let alreadyVisitedSites = [];
    let originSite = "https://www.srf.ch";
    let isArticle = false;

    let extractedLinks = await getAllAbsoluteLinks(originSite, originSite);
    console.log(extractedLinks);


    //creation of daily new directory
    let out = createNewTargetDirectory(constants.OUTPUT_DIR);
    if (out === ""){
        logToFile("Error while creating new daily directory", constants.FILE_PATH_LOG_ERROR);
        logToFile("Aborting error ist in control.js>createNewDirectory.js aufgetreten siehe letzter Eintrag FILE_PATH_LOG_ERROR", constants.FILE_PATH_LOG_ABORT_ERROR)
        return;
    }
    else{
        logToFile("Succesfuly created new daily directory", constants.FILE_PATH_LOG_SUCCESSFULL);
        constants.TARGET_DIR = out;
    }

    //read all articles of already downloaded articles and save them into an array
    let articlesAlreadySaved = [];
    try{
        articlesAlreadySaved = await readTitlesFromFile(constants.FILE_PATH_ALREADY_SAVED_ARTICLES);
        logToFile('Articles read correctly', constants.FILE_PATH_LOG_SUCCESSFULL);
        console.log('Articles read correctly');
    }
    catch (err) {
        logToFile("Error reading all 'saved articles' from file alreadySavedArticles " + err.message, constants.FILE_PATH_LOG_ERROR);
        console.log("Error reading all 'saved articles' from file alreadySavedArticles");
        logToFile("Aborting error ist beim Lesen von articlesAlreadySaved aufgetreten siehe letzter Eintrag FILE_PATH_LOG_ERROR", constants.FILE_PATH_LOG_ABORT_ERROR)
        return;
    }

    console.log("Aus dem file gelesene, bereits gedownloadete Links: ");
    articlesAlreadySaved.forEach(element => {
        console.log(element);
    })

    //console.log(articlesAlreadySaved);
    while (extractedLinks.length > 0) {
        let firstLink = extractedLinks.shift();
        if (!articlesAlreadySaved.includes(firstLink) && !constants.URLS_TO_IGNORE.includes(firstLink) && firstLink.startsWith('https://www.srf.ch')) {
            if (!alreadyExpandedSites.includes(firstLink) && isArticle === false) {
                let newSubLinks = await getAllAbsoluteLinks(firstLink, firstLink);
                for (let currentLink of newSubLinks) {
                    if (alreadyVisitedSites.includes(currentLink)) {
                        continue;
                    }
                    if (!extractedLinks.includes(currentLink)) {
                        extractedLinks.push(currentLink);
                    }
                }
                alreadyExpandedSites.push(firstLink);
            }
            if (!alreadyVisitedSites.includes(firstLink)) {
                isArticle = await saveWebpage(firstLink);
                alreadyVisitedSites.push(firstLink);
            }
        }
        else {
            console.log('\x1b[33m%s\x1b[0m', "Artikel wurde bereits gesaved und wieder auf der Website gefunden --> wurde dem sharedArray hinzugefügt.");
            logToFile("Artikel wurde bereits gesaved und wieder auf der Website gefunden --> wurde dem sharedArray hinzugefügt", constants.FILE_PATH_LOG_SUCCESSFULL);
            sharedArray.push(firstLink);
        }

        isArticle = false;
        console.log("Number of links still to visit: ", extractedLinks.length);
        logToFile(extractedLinks.length, constants.FILE_PATH_LOG_TEMP);
    }

    //save all articles to savedArticles file
    overwriteSavedArticles(constants.FILE_PATH_ALREADY_SAVED_ARTICLES, sharedArray, (err) => {
        if (err) {
            logToFile("Error when saving new 'Saved articles' to alreadySavedArticles siehe constants.FILE_PATH_LOG_ERROR", constants.FILE_PATH_LOG_ABORT_ERROR);
            console.log("Error occured on line 93!!!");
            //throw new Error();
        } else {
            logToFile("Successfully saved new 'Saved articles' to alreadySavedArticles", constants.FILE_PATH_LOG_SUCCESSFULL)
        }
    });


    logToFile("Summary of execution at " + new Date().toISOString().slice(0, 10) + "\n", constants.FILE_PATH_SUMMARY );
    logToFile("________________________________________________________________________________________________", constants.FILE_PATH_SUMMARY);
    logToFile("Amount of newly saved articles: " + newlySavedArticles + "\n", constants.FILE_PATH_SUMMARY);
    logToFile("Total amount of current articles stil on SRF (length of saved Articles): " + (sharedArray.length) + "\n", constants.FILE_PATH_SUMMARY);

}

module.exports = constants;
control();

