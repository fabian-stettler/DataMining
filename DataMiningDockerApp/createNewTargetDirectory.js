const fs = require('fs');
const path = require('path');
const logToFile = require('./logging');
const constants = require("./constants");

/**
 *
 * @param inputDirectory ist das directory in welchem das täglich neue directory (Ordner mit Datum) erstellt werden soll
 * @returns {string} wenn empty string returned wird an control.js weis control.js das Fehler passiert ist.
 * Diese Funktion erstellt täglich ein neues Output Directory
 */
function createNewTargetDirectory(inputDirectory) {
    // Get the current date in YYYY-MM-DD format
    const currentDate = new Date().toISOString().slice(0, 10);
    let currentDate2 = currentDate + "/";
    const newDirectory = path.join(inputDirectory, currentDate2);

    //flag
    let flag;

    // Create the new directory
    fs.mkdir(newDirectory, { recursive: true }, (err) => {
        if (err) {
            console.log(`An error occurred: ${err.message}`);
            logToFile("An error occurred when creating new targetDirectory", String(constants.FILE_PATH_LOG_ERROR))
            flag = false;
        } else {
            console.log(`Directory '${newDirectory}' created successfully.`);
            logToFile(`Directory: '${newDirectory}' created successfully.`, constants.FILE_PATH_LOG_SUCCESSFULL)
            flag = true;
        }
    });
    if (flag === false){
        return "";
    }
    else{
        return newDirectory;
    }
}

// Example usage
//const inputDirectory = '/path/to/input_directory';
//createDirectoryBasedOnCurrentDay(inputDirectory);

module.exports = createNewTargetDirectory;