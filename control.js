const { run, getAllAbsoluteLinks } = require('./extractAllLinksFromWebpage.js');
const saveWebpage = require('./saveFullWebpage');
const logToFile = require("./logging");
const {launch} = require("puppeteer");
const { exec } = require('child_process');
constants = {
    LOG_FILE_PATH: '/media/supremeleader/Data/DataMiningProjekt/htmlFiles/logFile.log',
}
//this is my test comment for testing github on linux maschine

async function control() {

	//call IP Rotating Script;
	const shellScriptPath = './rotateIPAdress.sh';
	exec(`bash ${shellScriptPath}`, (error, stdout, stderr) => {
	  if (error) {
	    console.error(`Error executing the script: ${error.message}`);
	    return;
	  }

	  if (stderr) {	
	    console.error(`Script stderr: ${stderr}`);
	    return;
	  }
	  
	   if (stdout) {
		   
	    console.error(`Script stderr: ${stderr}`);
	    return;
	  }

	  
	  console.log(`Script output: ${stdout}`);
	});


    let alreadyExpandedSites = [];
    let alreadyVisitedSites = [];
    let originSite = "https://www.srf.ch";
    let extractedLinks = await getAllAbsoluteLinks(originSite, originSite);
    let isArticle = false;
    console.log(extractedLinks);


    while (extractedLinks.length > 0) {
        let firstLink = extractedLinks.shift();
        if (!alreadyVisitedSites.includes(firstLink)) {
            isArticle = await saveWebpage(firstLink);
	    console.log("All Loggings from saveWebpage should be logged at this point.");
            alreadyVisitedSites.push(firstLink);
        }

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
        isArticle = false;
        console.log(extractedLinks.length);
        logToFile(extractedLinks.length, constants.LOG_FILE_PATH);
	console.log("Length of extracted Links should have been logged by now.");
    }
    logToFile(alreadyExpandedSites.join(', '), constants.LOG_FILE_PATH);
    logToFile(alreadyVisitedSites.join(', '), constants.LOG_FILE_PATH);
    logToFile(extractedLinks.join(', '), constants.LOG_FILE_PATH);
}

control();
