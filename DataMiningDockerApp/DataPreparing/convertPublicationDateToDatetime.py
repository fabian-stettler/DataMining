from pymongo import MongoClient
from dateutil import parser
from pymongo import UpdateOne

from connectToMongoDBCollection import connectToMongoDBCollection


def convertPublicationDateToDatetime(date_field):
    '''
    Converts a certain provided field in Articles collection, which is formatted as string, to datetime datatype
    :return:
    '''
    # Verbindung zur MongoDB
    with connectToMongoDBCollection('Datamining_Srf', 'Articles') as collection:
        # Liste zum Speichern der Update-Operationen
        updates = []

        # Durchsuchen aller Dokumente in der Sammlung
        for document in collection.find({}):
            date_str = document.get(date_field)
            if date_str and isinstance(date_str, str):
                try:
                    # Umwandlung des Datumsstrings in ein datetime-Objekt
                    date_obj = parser.parse(date_str)
                    # Erstellen einer Update-Operation
                    updates.append(UpdateOne(
                        {'_id': document['_id']},
                        {'$set': {date_field: date_obj}}
                    ))
                except Exception as e:
                    print(f"Fehler bei der Verarbeitung von Dokument ID {document['_id']}: {e}")

        # Batch-Update in der Datenbank
        if updates:
            result = collection.bulk_write(updates)
            print(f'{result.modified_count} Dokument(e) aktualisiert.')
        else:
            print('Keine zu aktualisierenden Dokumente gefunden.')

#convertPublicationDateToDatetime('publication_date')