from DataVisualization.LeafletGraph.countKeywords import countKeywords, getMongoDBEntries
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

    for keywordsOfArticle in allKeywords:
        for keyword in keywordsOfArticle:
            #print("This is an element" + keywordsOfArticle)
            if key in keyword:
                dictConnectedKeywords = edgesDictionary.get(key)
                if dictConnectedKeywords is None:
                    #dict to this keyword does not exist
                    edgesDictionary[key] = {}
                    connectedKeywords = edgesDictionary[key]
                    connectedKeywords[keyword] = 1
                else:
                    #dict to this keyword exists already
                    connectedKeywords = dictConnectedKeywords.get(keyword)
                    if connectedKeywords is None:
                        #inner dict does not contain connected keywords
                        dictConnectedKeywords[keyword] = 1
                    else:
                        #inner dict does contain the connected keyword
                        dictConnectedKeywords[keyword] = connectedKeywords + 1
    return edgesDictionary
def createEdges(sorted_keywords):
    '''
    :param sorted_keywords: Ist ein Dictionary mit allen Keywords als items und die Anzahl wie oft sie in allen Artikel vorkommen als value.
    :return: eine dict Matrix mit den topkeys und allen connected keywords mit ihrer Anzahl
    '''
    #constants to manipulate amount of nodes and structure of the graph
    percentageOfInnerNodes = 20
    percentageAmountOfOuterNodes = 30
    minimalWeightOfConsideredConnection = 8

    #remove all keywords which are in our exlude List
    articlesWithKeywords = getMongoDBEntries()
    for article in articlesWithKeywords:
        for keyword in article:
            if keyword in KEYWORDS_TO_IGNORE:
                article.remove(keyword)
    #getLength of our sorted_keywords
    lengthKeywords = len(sorted_keywords)

    #define the amount of inner nodes
    amountOfInnerNodes = int((lengthKeywords/100) * percentageOfInnerNodes)

    #extract the all keys of our sorted_keywords
    keys = list(sorted_keywords.keys())

    #filter the inner Nodes
    topkeys = keys[:amountOfInnerNodes]

    #update the edges of our Dictionary
    edgesDictionary = {}
    for topkey in topkeys:
        edgesDictionary = update_edges(topkey, edgesDictionary, articlesWithKeywords)

    #filter the outer Nodes

    filtered_edgesDictionary = filterOuterNodes(edgesDictionary, minimalWeightOfConsideredConnection,
                                                percentageAmountOfOuterNodes)
    return filtered_edgesDictionary



def filterOuterNodes(edgesDictionary, minimalWeightOfConsideredConnection,
                     percentageAmountOfBorderNodes):
    '''
    :param edgesDictionary: Ausgangs Dictionary mit allen äusseren nodes
    :param minimalWeightOfConsideredConnection: minimale Connection, welche ein node braucht um abgebildet zu werden
    :param percentageAmountOfBorderNodes: Der Prozentsatz an connections zu äusseren Nodes(aller connections des momentanen nodes).
    :return: Ein dictionary, welches weniger äussere Nodes berücksichtigt, als vorher
    '''
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
            # print(connected_keyword, weight)
            if weight >= minimalWeightOfConsideredConnection and currentAmountOfConnectionToBeConsidered < amountOfConnectionsToBeConsidered and connected_keyword != keyword:
                filtered_connections[connected_keyword] = weight
                currentAmountOfConnectionToBeConsidered += 1

        # Füge gefilterte Verbindungen zum gefilterten Dictionary hinzu, wenn sie vorhanden sind
        if filtered_connections:
            filtered_edgesDictionary[keyword] = filtered_connections
    return filtered_edgesDictionary

createEdges(countKeywords())