// sharedArray.js
const sharedArray = [];
let newlySavedArticles = 0;

/**
 *
 * @param element ist eine url, welche gesaved ist, weil sie in der Vergangenheit besucht worden ist oder jetzt besucht wurde.
 */
function addElement(element) {
    sharedArray.push(element);
    newlySavedArticles = newlySavedArticles + 1;
    console.log(`Element ${element} hinzugefügt`);
}


module.exports = {
    addElement,
    sharedArray,
    newlySavedArticles
};
