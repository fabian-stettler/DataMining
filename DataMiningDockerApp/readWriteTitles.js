const fs = require('fs');
const path = require('path');
const logToFile = require("./logging");
const constants = require("./constants");

/**
 * Utility function to read titles from file
 * @param filePath is the path from which to read FROM and TO
 * @param callback
 * @returns {Promise<unknown>}
 */
//
function readTitlesFromFile(filePath, callback) {
    return new Promise((resolve, reject) => {
        fs.readFile(filePath, 'utf8', (err, data) => {
            if (err) {
                if (err.code === 'ENOENT') {
                    // File does not exist, return an empty array
                    return resolve([]);
                }
                logToFile("Error occured in readTitlesFromFile" + err.message, constants.FILE_PATH_LOG_ERROR);
                return reject(err);
            }
            const titles = data.trim().split('\n').filter(Boolean);
            resolve(titles);
        });
    });
}

/**
 *
 * @param filePath ist der Pfad in welches der neue String geschrieben werden soll
 * @param newArticles sind die Artikel die am heutigen Tag gesaved wurden
 * @param callback
 * @returns {*}
 * @function overwriteSavedArticles schreibt alle übergebenen Artikel in das file savedArticles und ÜBERSCHREIBT Daten die dort standen.
 *
 */
function overwriteSavedArticles(filePath, newArticles, callback) {

    //newArticles not array
    if (!Array.isArray(newArticles)) {
        const error = new TypeError('titles should be an array');
        logToFile('Error: titles should be an array' + error.message, constants.FILE_PATH_LOG_ERROR);
        return callback(error);
    }

    //new Articles is empty
    if (newArticles.length === 0) {
        const message = 'No titles to append';
        logToFile(message, constants.FILE_PATH_LOG_ERROR);
        return callback(null, message);
    }

    //construct a string
    let temp = "";
    for (let i = 0; i < newArticles.length; i++) {
        temp += newArticles[i] + '\n';
    }

    //apend to file
    fs.writeFile(filePath, temp, 'utf8', (err) => {
        if (err) {
            logToFile("Error in writeFile() when writing new articles to file", constants.FILE_PATH_LOG_ERROR);
            return callback(err);
        } else {
            logToFile("Successfully overwritten saved articles!", constants.FILE_PATH_LOG_SUCCESSFULL);
            return callback(null, true);
        }
    });
}

module.exports = {
    readTitlesFromFile,
    overwriteSavedArticles
};