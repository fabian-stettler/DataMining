import time
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, OperationFailure

def wait_for_mongodb():
    time.sleep(3)
    client = MongoClient("mongodb://admin:secret@mongodb:27017/Datamining_Srf?authSource=admin")
    timeout = 30  # in Sekunden
    start_time = time.time()

    while time.time() - start_time < timeout:
        try:
            # Versuche, eine Verbindung herzustellen und eine Liste der Datenbanken abzurufen
            client.list_database_names()
            print("MongoDB ist bereit!")
            return
        except ServerSelectionTimeoutError:
            print("Warten auf MongoDB...")
            time.sleep(2)
        except OperationFailure as e:
            print(f"Authentifizierungsfehler: {e}")
            raise e
    raise Exception("Konnte keine Verbindung zu MongoDB herstellen")

