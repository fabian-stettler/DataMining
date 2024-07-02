const {launch} = require("puppeteer");
var assert = require('assert');
const { expect } = import('chai');
const { describe, it, beforeEach } = require("mocha"); // Import Mocha functions directly
const fs = require('fs');
const readline = require('readline');
const saveWebpage = require('../src/main/saveFullWebpage');

let websiteTestUrl = 'https://www.srf.ch/news/international/krieg-in-der-ukraine-cassis-laedt-china-zu-friedenskonferenz-ein-antwort-steht-aus';
let isArticleWhichShouldBeSaved = true;
const htmlFileRepository = 'C:\\Users\\fabia\\Desktop\\htmlFiles\\';
const logFilePath = 'C:\\Users\\fabia\\Desktop\\htmlFiles\\logfile.txt';
let srfContentId = 21104244;

//create title
const lastSlashIndex = websiteTestUrl.lastIndexOf('/');
const titleOfArticle = websiteTestUrl.slice(lastSlashIndex + 1);


describe('This function is used as a wrapper for the other ones', function () {
    //defines the time this test case is able to run without time out.
    this.timeout(3000);
    beforeEach(async function () {

    });

    it('should detect a logging entry in the log file in either case of storing the article or not storing', async function () {
        // Trigger savingWebpage Function, await makes sure to wait for response of saveWebpage
        this.timeout(10000); // Adjust the timeout as needed

        let answer = await saveWebpage(websiteTestUrl);
        //read the log file
        // Create a readable stream from a file
        const readableStream = fs.createReadStream(logFilePath, { encoding: 'utf8' });
        // Create a readline interface
        const rl = readline.createInterface({
            input: readableStream,
            crlfDelay: Infinity,
        });

        // Variable to store the last line
        let lastLine = '';

        // Event listener for each line
        rl.on('line', (line) => {
            lastLine = line;
        });

        // Wait for the 'close' event before making assertions
        await new Promise((resolve) => {
            rl.on('close', () => {
                // The 'close' event is triggered when the readline interface reaches the end of the file
                // Now, 'lastLine' contains the last line of the file
                console.log('Last Entry:', lastLine);
                resolve();
            });
        });
        this.timeout(8000); // Adjust the timeout as needed
        console.log(lastLine);

        if (isArticleWhichShouldBeSaved) {
            let expectedLoggingEntry = ' Webpage downloaded and saved! File withContentID ' + srfContentId + ' and title ' + titleOfArticle + ' was saved.';
            assert.equal(lastLine.includes(expectedLoggingEntry), true);
        } else {
            let expectedLoggingEntry = 'Content does not meet criteria! File withContentID ' + srfContentId + ' and title ' + titleOfArticle + ' not saved.';
            assert.equal(lastLine.includes(expectedLoggingEntry), true);
        }
    });

    it('should detect the file inside the html storage repository', async function () {
        //the function in testCase 1 above should have triggered the creation of a new html file
        this.timeout(5000); // Adjust the timeout as needed
        const fullPath = htmlFileRepository + 'output_' + srfContentId + '_' + titleOfArticle + '.html';
        console.log(fullPath);

        // Use fs.existsSync to check if the file exists
        const fileExists = fs.existsSync(fullPath);

        // Assert that the file exists using Chai's expect
        assert.equal(fileExists, true);
        });
});
