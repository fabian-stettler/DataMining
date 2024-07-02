const fs = require('fs');
const constants = require("./constants");


/**
 *
 * @param message does define the content which gets logged to the logFile
 * @param filePath has tobe provided when calling
 * @returns {boolean} if the log was successfull it returns true, else false
 * writes error in the logging process to the console.
 * Might want to extend that error logging to a special error log file.
 */
function logToFile(message, filePath) {
    const timestamp = new Date().toISOString();
    const logMessage = `[${timestamp}] ${message}\n`;

    // Append the log message to the file
    fs.appendFile(filePath, logMessage, (err) => {
        if (err) {
            console.error('Error writing to log file:', err);
            return false;
        }
    });
    return true;
}

module.exports = logToFile;
// Example usage
//logToFile('This is a log message.');
