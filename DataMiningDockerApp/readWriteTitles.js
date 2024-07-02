const fs = require('fs');
const path = require('path');
const logToFile = require("./logging");
const constants = require("./constants");

// Utility function to read titles from file
function readTitlesFromFile(filePath, callback) {
    return new Promise((resolve, reject) => {
        fs.readFile(filePath, 'utf8', (err, data) => {
            if (err) {
                if (err.code === 'ENOENT') {
                    // File does not exist, return an empty array
                    return resolve([]);
                }
                return reject(err);
            }
            const titles = data.trim().split('\n').filter(Boolean);
            resolve(titles);
        });
    });
}

// Utility function to write titles to file
function appendTitlesToFile(filePath, newArticles, callback) {

    //newArticles not array
    if (!Array.isArray(newArticles)) {
        const error = new TypeError('titles should be an array');
        logToFile('Error: titles should be an array', constants.FILE_PATH_LOG_ERROR);
        return callback(error);
    }

    //new Articles is empty
    if (newArticles.length === 0) {
        const message = 'No titles to append';
        logToFile(message, constants.FILE_PATH_LOG_ERROR);
        return callback(null, message);
    }

    //construct a string
    let temp = '\n NEW DATE:' + new Date().toISOString().slice(0, 10) + "\n";
    for (let i = 0; i < newArticles.length; i++) {
        temp += newArticles[i] + '\n';
    }

    //apend to file
    fs.appendFile(filePath, temp, 'utf8', (err) => {
        if (err) {
            logToFile("Error in appendFile() when writing new articles to file", constants.FILE_PATH_LOG_ERROR);
            return callback(err);
        } else {
            logToFile("Successfully writing new articles to file in appendFile()", constants.FILE_PATH_LOG_SUCCESSFULL);
            return callback(true);
        }
    });
}

module.exports = {
    readTitlesFromFile,
    appendTitlesToFile
};