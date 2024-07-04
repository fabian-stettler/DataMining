const fs = require('fs');
const path = require('path');
const sendEmail = require('./emailSender');
const constants = require("./constants");
const logToFile = require("./logging");


// Pfad zur Log-Datei
const logFilePath = constants.FILE_PATH_LOG_ABORT_ERROR;
// Funktion zum Lesen der letzten Zeile der Log-Datei
const getLastLogEntry = (filePath) => {
    return new Promise((resolve, reject) => {
        fs.readFile(filePath, 'utf8', (err, data) => {
            if (err) {
                return reject(err);
            }
            const lines = data.trim().split('\n');
            resolve(lines.slice(-1)[0]);
        });
    });
};

// Funktion zum Lesen des letzten gespeicherten Standes
const getLastSavedState = (filePath) => {
    return new Promise((resolve, reject) => {
        fs.readFile(filePath, 'utf8', (err, data) => {
            if (err) {
                return resolve(null); // Wenn die Datei nicht existiert, ist das der erste Lauf
            }
            resolve(data.trim());
        });
    });
};

// Funktion zum Speichern des aktuellen Standes
const saveCurrentState = (filePath, state) => {
    return new Promise((resolve, reject) => {
        fs.writeFile(filePath, state, 'utf8', (err) => {
            if (err) {
                return reject(err);
            }
            resolve();
        });
    });
};

// Hauptfunktion zur Überwachung der Log-Datei
const monitorLogFile = async () => {

    try {
        //Testfall fürs Schreiben eines Mails diese zwei Zeilen
        //const testMessage = `Test message at ${new Date().toISOString()}`;
        //await saveCurrentState(constants.FILE_PATH_LOG_ABORT_ERROR, testMessage);

        const lastLogEntry = await getLastLogEntry(constants.FILE_PATH_LOG_ABORT_ERROR);
        const lastSavedState = await getLastSavedState(constants.FILE_PATH_LAST_STATE);

        if (lastLogEntry !== lastSavedState) {
            let emailText = "New log entry detected: check the abort log file" + lastLogEntry;
            sendEmail('Problem beim Scrapping', emailText);
            await saveCurrentState(constants.FILE_PATH_LAST_STATE, lastLogEntry);
        } else {
            logToFile("Durchlauf ohne Abort --> keine Mail versandt.", constants.FILE_PATH_SUMMARY);
        }
    } catch (error) {
        console.log(`Error during log file monitoring: ${error.message}`)
        console.error(`Error during log file monitoring: ${error.message}`);
        logToFile('Error during monitoring of Log File AbortLog', constants.FILE_PATH_LOG_ABORT_ERROR);
    }
};

monitorLogFile();
