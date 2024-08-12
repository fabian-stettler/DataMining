from DataVisualization.LeafletGraph.countKeywords import countKeywords, getMongoDBEntries
from connectToMongoDBCollection import connectToMongoDBCollection
from constants import KEYWORDS_TO_IGNORE

#constants
PERCENTAGE_OF_INNER_NODES = 20
PERCENTAGE_OF_OUTER_NODES = 30
MINIMAL_WEIGHT_OF_CONSIDERED_CONNECTION = 20




def update_edges(key, edgesDictionary, allKeywords):
    '''

    :param key: is the current key to analyze and update the outer dict
    :param edgesDictionary: current version of the final dictionary
    :param allKeywords: Matrix mit Artikeln und ihren Keywords
    :return: eine neu version mit einem updgedateten inner dict für key.
    :keyword ist ein einziges keyword in einem Artikel
    die Funktion schaut nach ob sich key in einem der Artikel befindet, wenn ja macht key in seinem innerdict updates zu allen keywords,
    welche sich in diesem Artikel befinden.
    Es wird ein break gemacht, wenn ein Artikel berücksichtigt worden ist.
    '''

    for keywordsOfArticle in allKeywords:
        for keyword in keywordsOfArticle:
            #print(f"This is a keyword: {keyword}")
            if key == keyword:
                dictConnectedKeywords = edgesDictionary.get(key)
                if dictConnectedKeywords is None:
                    #dict to this keyword does not exist
                    edgesDictionary[key] = {}
                    connectedKeywords = edgesDictionary[key]
                    for currentKeyword in keywordsOfArticle:
                        connectedKeywords[currentKeyword] = 1
                    break
                else:
                    #dict to this keyword exists already
                    for currentKeyword in keywordsOfArticle:
                        if currentKeyword not in dictConnectedKeywords:
                            dictConnectedKeywords[currentKeyword] = 1
                        else:
                            count = dictConnectedKeywords.get(currentKeyword)
                            dictConnectedKeywords[currentKeyword] = count + 1
                    break

    return edgesDictionary
def createEdges(sorted_keywords):
    '''
    :param sorted_keywords: Ist ein Dictionary mit allen Keywords als items und die Anzahl wie oft sie in allen Artikel vorkommen als value.
    :return: eine dict Matrix mit den topkeys und allen connected keywords mit ihrer Anzahl
    '''
    #constants to manipulate amount of nodes and structure of the graph

    #remove all keywords which are in our exlude List
    articlesWithKeywords = getMongoDBEntries()
    for article in articlesWithKeywords:
        for keyword in article:
            if keyword in KEYWORDS_TO_IGNORE:
                article.remove(keyword)
    #getLength of our sorted_keywords
    lengthKeywords = len(sorted_keywords)

    #define the amount of inner nodes
    amountOfInnerNodes = int((lengthKeywords/100) * PERCENTAGE_OF_INNER_NODES)

    #extract the all keys of our sorted_keywords
    keys = list(sorted_keywords.keys())

    #filter the inner Nodes
    topkeys = keys[:amountOfInnerNodes]

    #update the edges of our Dictionary
    edgesDictionary = {}
    for topkey in topkeys:
        edgesDictionary = update_edges(topkey, edgesDictionary, articlesWithKeywords)

    #filter the outer Nodes

    filtered_edgesDictionary = filterOuterNodes(edgesDictionary, MINIMAL_WEIGHT_OF_CONSIDERED_CONNECTION,
                                                PERCENTAGE_OF_OUTER_NODES)
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