from connectToMongoDBCollection import connectToMongoDBCollection
from constants import KEYWORDS_TO_IGNORE

def getMongoDBEntries():
    allArticlesWithKeywordsMatrix = []
    with connectToMongoDBCollection('Datamining_Srf', 'Articles') as collectionArticles:
        allArticlesWithKeywords = collectionArticles.find({
            'base_keywords':  { '$exists': True },
            'additional_keywords': { '$exists': True }
        })
        for article in allArticlesWithKeywords:
            oneArticleKeywords = []
            base_keywords = article['base_keywords']
            additional_keywords = article['additional_keywords']
            oneArticleKeywords.extend(base_keywords)
            oneArticleKeywords.extend(additional_keywords)
            allArticlesWithKeywordsMatrix.append(oneArticleKeywords)
    return allArticlesWithKeywordsMatrix


def countKeywords():
    '''
    counts all keywords from all articles and sorts the keywordsCounter by the amount of occurences
    :return: keywords with an occurence count in all articles sorted by the count in form of a dictionary
    '''
    allArticlesWithKeywords = getMongoDBEntries()
    keywordsCounter = {}
    for article in allArticlesWithKeywords:
        for keyword in article:
            if keyword not in KEYWORDS_TO_IGNORE:
                if keywordsCounter.get(keyword) is None:
                    keywordsCounter[keyword] = 1
                else:
                    countKeyword = keywordsCounter[keyword]
                    countKeyword += 1
                    keywordsCounter[keyword] = countKeyword
    sorted_keywords = dict(sorted(keywordsCounter.items(), key=lambda item: item[1], reverse=True))
    return sorted_keywords
countKeywords()