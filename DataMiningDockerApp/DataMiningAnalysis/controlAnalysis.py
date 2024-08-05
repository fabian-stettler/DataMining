import logging
import os
import sys
from time import sleep

from bs4 import BeautifulSoup
from pymongo import MongoClient
from transformers import AutoTokenizer, AutoModel
from datetime import datetime, timedelta

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


def controlAnalysis(directory):
    """
    :param directory: Directory, welches Artikel enthält die analysiert und gespeichert werden sollen.
    :controlAnalysis
     1.analysiert und extrahiert Informationen aus den html files
     2.erstellt ein neues Objekt und sichert es in MongoDB --> Datamining_Srf --> Articles
    :return: nothing
    """
    # Connect to the MongoDB server running on a container on the same "network" thanks to .yml file
    print(1, "MongoDB Connection initialization started")
    newlyInsertedDocuments = 0
    with MongoClient("mongodb://admin:secret@mongodb:27017/?authSource=admin", 27017) as client:
        db = client['Datamining_Srf']
        collection = db['Articles']
        print(1, "MongoDB Connection established")

        # Laden des deutschen BERT-Modells und des Tokenizers
        print(1, "Model Loading ....")
        model = AutoModel.from_pretrained("dbmdz/bert-base-german-cased")

        #read file and make soup object
        print(1, "Analysation logging has begun")
        print("Directory mit Pfaden ist: " + directory)
        all_absolute_paths = get_all_absolute_paths(directory)
        print("get_all_absolute_paths BEENDET")
        for ele in all_absolute_paths:
            print(ele)
        for file_path in all_absolute_paths:
            with open(file_path, 'r', encoding='utf8') as file:
                html_content = file.read()
            soup = BeautifulSoup(html_content, 'html.parser')

            #make Analysis of different parts
            author = extract_author_from_html(soup)
            paragraphs = extract_paragraphs_from_section(soup)
            publication_date, modification_date = find_dates(soup)
            rubrik = find_meta_content(soup)
            subtitles = extract_subtitles_from_html(soup)
            titles = extract_title_from_html(soup)
            baseKeyWords = getBaseKeywords(soup, directory)
            contentId = getContentID(soup)
            linkedArticles = getLinkedArticles(soup)
            commentsOn = getCommentsOn(soup)
            additionalKeywords = getBERTKeywords(extract_first_overline_title(soup), extract_title_from_html(soup), extract_subtitles_from_html(soup), extract_paragraphs_from_section(soup), model)

            #make object
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
            #save the Object in DB
            collection.insert_one(document)
            newlyInsertedDocuments = newlyInsertedDocuments + 1
            print("Entry corresponding to article with ContentID: " + str(contentId) + "and title: " + titles + "was saved")
    print(f"analyze_html_container has added {newlyInsertedDocuments} Documents to MongoDB Container")

today_date = datetime.now()
formatted_today_date = today_date.strftime('%Y-%m-%d')
print(formatted_today_date)
print(1, "Skript control analysis was triggered")
controlAnalysis("/usr/src/datamining/htmlFiles/" + formatted_today_date)
'''

# read the two provided command line arguments and exlcude the name of the script at position 0
all_dates = []
args = os.getenv("SCRIPT_ARGS", "").split()
for date in args:
    all_dates.append(date)
    print("appended date: " + date)

#if starting and ending date are equal, only make one function call.
if all_dates[0] == all_dates[1]:
    controlAnalysis("/usr/src/datamining/htmlFiles/" + all_dates[0])
else:
    current_date = datetime.strptime(all_dates[0], '%Y-%m-%d')
    end_date = datetime.strptime(all_dates[1], '%Y-%m-%d')
    while current_date <= end_date:
        controlAnalysis("/usr/src/datamining/htmlFiles/" + current_date.strftime('%Y-%m-%d'))
        current_date += timedelta(days=1)
'''