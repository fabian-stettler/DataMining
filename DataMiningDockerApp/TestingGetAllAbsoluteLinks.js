const { getAllAbsoluteLinks } = require('./extractAllLinksFromWebpage.js');
const puppeteer = require('puppeteer');
const logToFile = require("./logging");
const fs = require('fs');


/**
 * @param url displays all sublinks
 * @returns {Promise<*>}
 */

async function main() {
    let array = await getAllAbsoluteLinks("https://www.srf.ch/wissen/", "https://www.srf.ch/wissen");
    console.log('Array:', array);  // Debugging output
    let string = "";

    if (Array.isArray(array)) {
        for (let element of array){
            string += element;
            string += "\n";
        }
        console.log(array.length);
    } else {
        console.error('Expected an array but got:', array);
    }

    logToFile(string, "C:\\Users\\fabia\\Desktop\\test.txt");
    fs.writeFileSync("C:\\Users\\fabia\\Desktop\\test.txt", string, 'utf8');
    console.log('Logged to file');  // Confirm that logging is attempted
}

main();
