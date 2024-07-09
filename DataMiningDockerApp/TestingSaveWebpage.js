const { getAllAbsoluteLinks } = require('./extractAllLinksFromWebpage.js');
const saveWebpage = require('./saveFullWebpage');
const {launch} = require("puppeteer");
const createNewTargetDirectory = require('./createNewTargetDirectory');
const { readTitlesFromFile, overwriteSavedArticles } = require('./readWriteTitles');
const {sharedArray, newlySavedArticles} = require("./sharedArray");
const constants = require("./constants");
const logToFile = require("./logging");



let isArticle = saveWebpage("https://www.srf.ch/kultur/gesellschaft-religion");
console.log(isArticle);