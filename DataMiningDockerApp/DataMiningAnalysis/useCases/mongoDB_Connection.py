from pymongo import MongoClient

# Connect to the MongoDB server running on localhost at port 27017
client = MongoClient('localhost', 27017)

# List all databases
databases = client.list_database_names()
print("Databases:", databases)

# Access a specific database
db = client['Datamining_Srf']

# List all collections in the database
collections = db.list_collection_names()
print("Collections:", collections)


# Access a specific collection
collection = db['Articles']

# Example: Find one document in the collection
document = collection.find_one()
print("Document:", document)


#insert one example document
document = {
    "author": ["agenturen/grej", "harm"],
    "paragraphs": [
        "«Die mauretanische Küstenwache hat die Leichen von 89 Personen an Bord eines grossen traditionellen Fischerbootes gefunden, das am Montag, 1. Juli an der Küste des Atlantischen Ozeans gekentert ist», vier Kilometer von der Stadt Ndiago (im Südwesten Mauretaniens) entfernt, wie die mauretanische Nachrichtenagentur berichtete.",
        "Die Küstenwache rettete neun Menschen, darunter ein fünfjähriges Mädchen, wie sie berichtete. Die Agentur zitierte Aussagen von Überlebenden, denen zufolge das Boot mit 170 Passagieren an Bord von der Grenze zwischen Senegal und Gambia aus gestartet war. Das Boot soll demnach die senegalesische Küste in nördlicher Richtung hinaufgefahren sein und hatte gerade die mauretanischen Gewässer passiert, als es sank. Sie beziffern die Zahl der Vermissten auf 72.",
        "Ein hochrangiger Beamter der örtlichen Verwaltung gab der AFP unter Wahrung seiner Anonymität ähnliche Informationen. In anderen Meldungen werden 184 Menschen an Boot, 87 Tote und 36 Gerettete genannt.",
        "Dies ist das jüngste Drama auf der Migrationsroute über den Atlantik, deren erstes Ziel die Kanarischen Inseln sind, eine spanische Inselgruppe und das Tor zu Europa. Eine Vielzahl von afrikanischen Menschen, die vor Armut, Arbeitslosigkeit oder fehlenden Zukunftsperspektiven fliehen, nehmen diese gefährliche Route. Gegen Geld schiffen sie sich illegal auf Pirogen oder unsicheren Booten ein, die Dutzende von Passagieren befördern."
    ],
    "publication_date": "2024-07-05T09:56:00+02:00",
    "modification_date": "2024-07-05T09:56:00+02:00",
    "rubrik": "International",
    "subtitles": ["Menschen nehmen weiterhin die gefährliche Route"],
    "titles": "Flüchtlinge: Tote bei Bootsunglück vor Mauretanien befürchtet",
    "base_keywords": ["news", "international"],
    "content_id": 104728980,
    "linked_articles": [
        {
            "title": "Behörden rechnen mit über 500 Toten bei Griechenland-Bootsunglück",
            "url": "/news/international/panik-auf-fluechtlingsboot-behoerden-rechnen-mit-ueber-500-toten-bei-griechenland-bootsunglueck",
            "content_id": "20325181"
        },
        {
            "title": "Reform des EU-Asylsystems: das Wichtigste in Kürze",
            "url": "/news/international/treffen-der-innenminister-reform-des-eu-asylsystems-das-wichtigste-in-kuerze",
            "content_id": "20322556"
        }
    ],
    "comments_on": False
}

# Insert the document into the collection
collection.insert_one(document)