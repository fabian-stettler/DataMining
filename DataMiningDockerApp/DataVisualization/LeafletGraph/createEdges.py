from DataVisualization.LeafletGraph.countKeywords import countKeywords
from connectToMongoDBCollection import connectToMongoDBCollection
from constants import KEYWORDS_TO_IGNORE


def update_edges(key, edgesDictionary, allKeywords):
    '''

    :param key: is the keyword which serves as a key in the outer dictionary
    :param edgesDictionary:
    :param additional_keywords:
    :param base_keywords:
    dictConnectedKeywords is the dictionary within the edgesDictionary and holds the connected keywords and the weight of this edge.
    :return:
    '''

    #print(allKeywords)

    for ele in allKeywords:
        #print("This is an element" + ele)
        if key in ele:
            dictConnectedKeywords = edgesDictionary.get(key)
            if dictConnectedKeywords is None:
                #dict to this keyword does not exist
                edgesDictionary[key] = {}
                connectedKeywords = edgesDictionary[key]
                connectedKeywords[ele] = 1
            else:
                #dict to this keyword exists already
                connectedKeywords = dictConnectedKeywords.get(ele)
                if connectedKeywords is None:
                    #inner dict does not contain connected keywords
                    dictConnectedKeywords[ele] = 1
                else:
                    #inner dict does contain the connected keyword
                    dictConnectedKeywords[ele] = connectedKeywords + 1
    return edgesDictionary
def createEdges(sorted_keywords):
    '''
    This function creates the "edges" to all keywords in the top percent of keywords
    The function only consideres connections which are in the top percent of connectedKeywords and have a minimum of absolute counts.
    :return: Ein dictionary mit den key values, welche aus den Keywords besteht, von welchen die connections ausgehen.
    Die values dieses dictionary sind wiederum dictionaries mit keywords als keys und counts dieser keywords als values
    '''
    #print(sorted_keywords)
    global base_keywords
    global additional_keywords
    with connectToMongoDBCollection('Datamining_Srf', 'Articles') as collectionArticles:
        allArticlesWithKeywords = collectionArticles.find({
            'base_keywords':  { '$exists': True },
            'additional_keywords': { '$exists': True }
        })
        #print('Should now print articles')
        allKeywords = []
        for article in allArticlesWithKeywords:
            base_keywords = article['base_keywords']
            additional_keywords = article['additional_keywords']
            if additional_keywords not in KEYWORDS_TO_IGNORE:
                allKeywords.extend(additional_keywords)
            if base_keywords not in KEYWORDS_TO_IGNORE:
                allKeywords.extend(base_keywords)
        #print(allKeywords)
        lengthKeywords = len(sorted_keywords)
        #print(lengthKeywords)
        amountOfInnerNodes = int((lengthKeywords/100) * 20)

        edgesDictionary = {}
        keys = list(sorted_keywords.keys())
        #print(keys[1])
        topkeys = keys[:amountOfInnerNodes]
        #print(topkeys)
        #print(len(topkeys))

        for topkey in topkeys:
            edgesDictionary = update_edges(topkey, edgesDictionary, allKeywords)
        #print(edgesDictionary)
        #print(len(edgesDictionary.keys()))
        # filter out x percent of the connected keywords
        # Gegebene Parameter
        percentageAmountOfBorderNodes = 30
        minimalWeightOfConsideredConnection = 8

        # Neuen gefilterten Dictionary erstellen
        filtered_edgesDictionary = {}

        for keyword, connections in edgesDictionary.items():
            lengthOfCurrentConnectedKeywords = len(connections)
            amountOfConnectionsToBeConsidered = (lengthOfCurrentConnectedKeywords / 100) * percentageAmountOfBorderNodes
            currentAmountOfConnectionToBeConsidered = 0

            # Sortieren der Verbindungen nach Gewicht
            sorted_connections = dict(sorted(connections.items(), key=lambda item: item[1], reverse=True))
            # Initialisiere eine neue Liste für gefilterte Verbindungen
            filtered_connections = {}

            for connected_keyword, weight in sorted_connections.items():
                #print(connected_keyword, weight)
                if weight >= minimalWeightOfConsideredConnection and currentAmountOfConnectionToBeConsidered < amountOfConnectionsToBeConsidered and connected_keyword!=keyword:
                    filtered_connections[connected_keyword] = weight
                    currentAmountOfConnectionToBeConsidered += 1

            # Füge gefilterte Verbindungen zum gefilterten Dictionary hinzu, wenn sie vorhanden sind
            if filtered_connections:
                filtered_edgesDictionary[keyword] = filtered_connections

        #print(len(filtered_edgesDictionary))
        #print(filtered_edgesDictionary)
        return filtered_edgesDictionary
createEdges(countKeywords())