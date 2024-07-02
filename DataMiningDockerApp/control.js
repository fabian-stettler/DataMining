const { getAllAbsoluteLinks } = require('./extractAllLinksFromWebpage.js');
const saveWebpage = require('./saveFullWebpage');
const logToFile = require("./logging");
const {launch} = require("puppeteer");
const createNewTargetDirectory = require('./createNewTargetDirectory');
const { readTitlesFromFile, appendTitlesToFile } = require('./readWriteTitles');
const constants = require("./constants");


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
        throw new Error("Error while creating new daily directory");
    }
    else{
        logToFile("Error while creating new daily directory", constants.FILE_PATH_LOG_SUCCESSFULL);
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
        logToFile("Error reading all 'saved articles' from file alreadySavedArticles", constants.FILE_PATH_LOG_ERROR);
        console.log("Error reading all 'saved articles' from file alreadySavedArticles");
        throw new Error("Error reading all 'saved articles' from file alreadySavedArticles");
    }

    //console.log(articlesAlreadySaved);
    while (extractedLinks.length > 0) {

        let firstLink = extractedLinks.shift();
        if (!articlesAlreadySaved.includes(firstLink) || !constants.URLS_TO_IGNORE.includes(firstLink)) {
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
        isArticle = false;
        console.log(extractedLinks.length);
        logToFile(extractedLinks.length, constants.FILE_PATH_LOG_TEMP);
    }

    //save all articles to savedArticles file
    appendTitlesToFile(constants.FILE_PATH_ALREADY_SAVED_ARTICLES, constants.NEW_ARTICLES, (err) => {
        if (err) {
            logToFile("Error when saving new 'Saved articles' to alreadySavedArticles", constants.FILE_PATH_LOG_ERROR)
        } else {
            logToFile("Successfully saved new 'Saved articles' to alreadySavedArticles", constants.FILE_PATH_LOG_SUCCESSFULL)
        }
    });

    //logging
    logToFile("Summary of execution at " + new Date().toISOString().slice(0, 10) + "\n", constants.FILE_PATH_SUMMARY );
    logToFile("________________________________________________________________________________________________", constants.FILE_PATH_SUMMARY);
    logToFile("Amount of newly saved articles: " + constants.NEW_ARTICLES.length + "\n", constants.FILE_PATH_SUMMARY);
    logToFile("Total amount of saved articles: " + (articlesAlreadySaved.length + constants.NEW_ARTICLES.length) + "\n", constants.FILE_PATH_SUMMARY);

}

module.exports = constants;
control();

