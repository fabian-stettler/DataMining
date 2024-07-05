// sharedArray.js
const sharedArray = [];
let newlySavedArticles = 0;

/**
 *
 * @param element ist eine url, welche gesaved ist, weil sie in der Vergangenheit besucht worden ist oder jetzt besucht wurde.
 */
function addElement(element) {
    sharedArray.push(element);
    newlySavedArticles++;
    console.log(`Element ${element} hinzugefügt`);
}


module.exports = {
    addElement,
    sharedArray,
    newlySavedArticles
};
