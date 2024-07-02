var assert = require('assert');
const { run, getAllAbsoluteLinks } = require('../src/main/extractAllLinksFromWebpage.js');
const { describe } = require("mocha");
const {launch} = require("puppeteer");  // Correct import statement
let websiteTestUrl = 'https://www.srf.ch/news/international/ukraine-friedensgipfel-cassis-verlaesst-peking-mit-leeren-haenden';

// get the links on the given site
describe('This function is used as a wrapper for the other ones', function () {
    let allLinks;

    // Set a higher timeout for the entire suite
    this.timeout(10000); // Set timeout to 10 seconds

    // This function will run before each test case in this describe block
    beforeEach(async function () {
        const browser = await launch();
        // Common setup or initialization code goes here
        allLinks = await getAllAbsoluteLinks(websiteTestUrl, websiteTestUrl);
        this.timeout(10000); // Set timeout to 10 seconds
        // Ensure allLinks is an array
        if (!Array.isArray(allLinks)) {
            throw new Error('The result from getAllAbsoluteLinks is not an array.');
        }
    });

    describe('Extract Links: no Hashtags included', function () {
        it('should return an array with strings which do not include #', function () {
            allLinks.forEach(function (currentElement) {
                assert.equal(currentElement.includes('_'), false);
            });
        });
    });

    // case 2
    describe('Extract Links: no Duplicates', function () {
        it('should return an array with strings which does not contain duplicates', function () {
            allLinks.forEach(function (currentElement) {
                assert.equal(currentElement.includes('#'), false);
            });
        });
    });

    //case 3
    describe('Exclude website which do not have the site structure https://www.srf.ch/', function () {
        it('should return an array with strings which does not contain duplicates', function () {
            allLinks.forEach(function (currentElement) {
                assert.equal(currentElement.startsWith('https://www.srf.ch'), true);
            });
        });
    });

});
