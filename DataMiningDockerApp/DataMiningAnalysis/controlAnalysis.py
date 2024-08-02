import logging
from time import sleep

from bs4 import BeautifulSoup
from pymongo import MongoClient
from transformers import AutoTokenizer, AutoModel
from datetime import datetime

from Keyword_Generator.getBERTKeywords import getBERTKeywords
from Keyword_Generator.getBaseKeywords import getBaseKeywords
from useCases.get_all_absolute_paths import get_all_absolute_paths
from useCases.getAuthor import extract_author_from_html
from useCases.getCommentsOn import getCommentsOn
from useCases.getContentID import getContentID
from useCases.getLead import extract_first_overline_title
from useCases.getLinkedArticles import getLinkedArticles
from useCases.getParagraphes import extract_paragraphs_from_section
from useCases.getPublicationAndModificationDate import find_dates
from useCases.getRubric import find_meta_content
from useCases.getSubtitles import extract_subtitles_from_html
from useCases.getTitle import extract_title_from_html


def controlHtmlExtraction(directory):
    """
    This specific version of this script only works for this system here
    :param directory: Directory, welcher Artikel enthält die analysiert und gespeichert werden sollen.
    :controlAnalysis
     1.analysiert und extrahiert Informationen aus den html files
     2.erstellt ein neues Objekt und sichert es in MongoDB --> Datamining_Srf --> Articles
    :return: nothing
    """

    # Connect to the MongoDB server running on a container on the same "network" thanks to .yml file
    print(1, "MongoDB Connection initialization started")
    client = MongoClient("mongodb://admin:secret@mongodb:27017/?authSource=admin", 27017)
    db = client['Datamining_Srf']
    collection = db['Articles']
    print(1, "MongoDB Connection established")


    # Laden des deutschen BERT-Modells und des Tokenizers
    print(1, "Model Loading ....")
    model = AutoModel.from_pretrained("dbmdz/bert-base-german-cased")

    #read file and make soup object
    print(1, "Analysation logging has begun")
    print("Directory mit Pfaden ist: " + directory)

    #temp all dir
    alldir = [
        "/usr/src/datamining/htmlFiles/2024-07-04", "/usr/src/datamining/htmlFiles/2024-07-07", "/usr/src/datamining/htmlFiles/2024-07-09", "/usr/src/datamining/htmlFiles/2024-07-10", "/usr/src/datamining/htmlFiles/2024-07-11",
        "/usr/src/datamining/htmlFiles/2024-07-12", "/usr/src/datamining/htmlFiles/2024-07-13", "/usr/src/datamining/htmlFiles/2024-07-14", "/usr/src/datamining/htmlFiles/2024-07-15", "/usr/src/datamining/htmlFiles/2024-07-16",
        "/usr/src/datamining/htmlFiles/2024-07-17", "/usr/src/datamining/htmlFiles/2024-07-18", "/usr/src/datamining/htmlFiles/2024-07-19", "/usr/src/datamining/htmlFiles/2024-07-20", "/usr/src/datamining/htmlFiles/2024-07-21",
        "/usr/src/datamining/htmlFiles/2024-07-22", "/usr/src/datamining/htmlFiles/2024-07-23", "/usr/src/datamining/htmlFiles/2024-07-24"
    ]


    #temp loop
    for currentdirectory in alldir:
        try:
            all_absolute_paths = get_all_absolute_paths(currentdirectory)
            print(f"Processing directory: {currentdirectory}, found {len(all_absolute_paths)} files.")
            for file_path in all_absolute_paths:
                print(f"Processing file: {file_path}")
                try:
                    with open(file_path, 'r', encoding='utf8') as file:
                        html_content = file.read()
                    soup = BeautifulSoup(html_content, 'html.parser')

                    # Extrahiere Informationen aus dem HTML-Inhalt
                    author = extract_author_from_html(soup)
                    paragraphs = extract_paragraphs_from_section(soup)
                    publication_date, modification_date = find_dates(soup)
                    rubrik = find_meta_content(soup)
                    subtitles = extract_subtitles_from_html(soup)
                    titles = extract_title_from_html(soup)
                    baseKeyWords = getBaseKeywords(soup, currentdirectory)
                    contentId = getContentID(soup)
                    linkedArticles = getLinkedArticles(soup)
                    commentsOn = getCommentsOn(soup)
                    additionalKeywords = getBERTKeywords(
                        extract_first_overline_title(soup),
                        extract_title_from_html(soup),
                        extract_subtitles_from_html(soup),
                        extract_paragraphs_from_section(soup),
                        model
                    )

                    # Erstelle das Dokument und speichere es in der Datenbank
                    document = {
                        "author": author,
                        "paragraphs": paragraphs,
                        "publication_date": publication_date,
                        "modification_date": modification_date,
                        "rubrik": rubrik,
                        "subtitles": subtitles,
                        "titles": titles,
                        "base_keywords": baseKeyWords,
                        "additional_keywords": additionalKeywords,
                        "content_id": contentId,
                        "linked_articles": linkedArticles,
                        "commentsOn": commentsOn
                    }
                    collection.insert_one(document)
                    print(f"Entry saved: {contentId}, {titles}")

                except Exception as e:
                    print(f"Error processing file {file_path}: {e}")
        except Exception as e:
            print(f"Error processing directory {currentdirectory}: {e}")



today_date = datetime.now()
formatted_today_date = today_date.strftime('%Y-%m-%d')
print(formatted_today_date)

print(1, "Skript control analysis was triggered")
controlHtmlExtraction("/usr/src/datamining/htmlFiles/" + formatted_today_date)
