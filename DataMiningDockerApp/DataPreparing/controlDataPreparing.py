from DataPreparing.convertPublicationDateToDatetime import convertPublicationDateToDatetime
from DataPreparing.sentimentExtraction import controlSentimentExtraction
from DataVisualization.sentimentAnalysis import sentimentAnalysis

from connectToMongoDBCollection import connectToMongoDBCollection
from constants import ASPECT_POOL


def deleteDuplicates():
    '''
    Deletes duplicates in DB Datamining_Srf
    :return:
    '''
    pipeline = [
        {"$group": {
            "_id": {
                "titles": '$titles',
                "content_id": "$content_id",
            },
            "uniqueIds": {"$addToSet": "$_id"},
            "count": {"$sum": 1}
        }},
        {"$match": {
            "count": {"$gt": 1}
        }}
    ]
    with connectToMongoDBCollection('Datamining_Srf', 'Articles') as collection:
        # Find duplicates
        duplicates = list(collection.aggregate(pipeline))
        print("Current amount of duplicates: " + str(len(duplicates)))

        total_deleted = 0  # Initialize counter for deleted documents

        # Delete duplicates, keeping one instance of each
        for record in duplicates:
            ids = record["uniqueIds"]
            # Remove the first ID from the list to retain it
            ids.pop(0)
            # Delete all other duplicates
            if ids:  # Ensure there are IDs to delete
                result = collection.delete_many({"_id": {"$in": ids}})
                total_deleted += result.deleted_count  # Accumulate deleted count

        print(f"Duplicate entries deleted: {total_deleted}")


def deleteArticlesWithFalseTitles():
    '''
    deletes articles with broken titles.
    :return:
    '''
    with connectToMongoDBCollection('Datamining_Srf', 'Articles') as collection:
        query = {
            '$or': [
                {'titles': 'Title not found'},
                {'titles': None},
                {'titles': {'$exists': False}},
            ]
        }

        # Lösche alle Dokumente, die der Abfrage entsprechen
        result = collection.delete_many(query)
        print(f"Deleted {result.deleted_count} documents with broken titles.")

def getCurrentDocumentCount():
    '''
    provides current amount of documents in DB Datamining_Srf und collections Articles
    :return:
    '''
    with connectToMongoDBCollection('Datamining_Srf', 'Articles') as collection:
        result = collection.count_documents({})
        print("Current amount of articles" + str(result))
        return result

def prepareMongoDBData(dateToGenerateSentimentsFrom):
    '''
    Skript should clean the data in following ways
    1. Remove Duplicates
    2. create datatypes on publication date
    3. Artikel mit einem leeren title oder mit einem title not found direkt löschen
    4. Generiert fehlende sentiments für die neuen Daten für Aspekte aus dem Sentiment Pool
    :return:
    '''
    getCurrentDocumentCount()
    convertPublicationDateToDatetime('publication_date')
    convertPublicationDateToDatetime('modification_date')
    deleteDuplicates()
    deleteArticlesWithFalseTitles()
    getCurrentDocumentCount()
    for aspect in ASPECT_POOL:
        controlSentimentExtraction(aspect, dateToGenerateSentimentsFrom)

#date format yyyy-mm-dd
#letztes Datum, an welchem die DB geladen wurde 04.08.2024
prepareMongoDBData("2024-08-02T00:00:00.000+00:00")