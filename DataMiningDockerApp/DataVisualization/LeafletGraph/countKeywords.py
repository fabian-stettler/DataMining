from connectToMongoDBCollection import connectToMongoDBCollection
from constants import KEYWORDS_TO_IGNORE


def countKeywords():
    '''
    counts all keywords from all articles and sorts the keywordsCounter by the amount of occurences
    :return: keywords with an occurence count in all articles sorted by the count in form of a dictionary
    '''
    with connectToMongoDBCollection('Datamining_Srf', 'Articles') as collectionArticles:
        allArticlesWithKeywords = collectionArticles.find({
            'base_keywords':  { '$exists': True },
            'additional_keywords': { '$exists': True }
        })
        keywordsCounter = {}
        #print('Should now print articles')
        for article in allArticlesWithKeywords:
            base_keywords = article['base_keywords']
            additional_keywords = article['additional_keywords']
            #print(article['base_keywords'])
            #print(article['additional_keywords'])
            for base_keyword in base_keywords:
                if base_keyword not in KEYWORDS_TO_IGNORE:
                    if keywordsCounter.get(base_keyword) is None:
                        keywordsCounter[base_keyword] = 1
                    else:
                        countKeyword = keywordsCounter[base_keyword]
                        countKeyword += 1
                        keywordsCounter[base_keyword] = countKeyword
            for additional_keyword in additional_keywords:
                if additional_keyword not in KEYWORDS_TO_IGNORE:
                    if keywordsCounter.get(additional_keyword) is None:
                        keywordsCounter[additional_keyword] = 1
                    else:
                        countKeyword = keywordsCounter[additional_keyword]
                        countKeyword += 1
                        keywordsCounter[additional_keyword] = countKeyword
        sorted_keywords = dict(sorted(keywordsCounter.items(), key=lambda item: item[1], reverse=True))
        for key, value in sorted_keywords.items():
            #print(key, value)
            pass
    return sorted_keywords
countKeywords()