import os

from bs4 import BeautifulSoup

from DataMiningAnalysis.Keyword_Generator.getBERTKeywords import getBERTKeywords
from DataMiningAnalysis.Keyword_Generator.getBaseKeywords import getBaseKeywords
from DataMiningAnalysis.useCases.getAuthor import extract_author_from_html
from DataMiningAnalysis.useCases.getCommentsOn import getCommentsOn
from DataMiningAnalysis.useCases.getContentID import getContentID
from DataMiningAnalysis.useCases.getLead import extract_first_overline_title
from DataMiningAnalysis.useCases.getLinkedArticles import getLinkedArticles
from DataMiningAnalysis.useCases.getParagraphes import extract_paragraphs_from_section
from DataMiningAnalysis.useCases.getPublicationAndModificationDate import find_dates
from DataMiningAnalysis.useCases.getRubric import find_meta_content
from DataMiningAnalysis.useCases.getSubtitles import extract_subtitles_from_html
from DataMiningAnalysis.useCases.getTitle import extract_title_from_html
from DataMiningAnalysis.useCases.get_all_absolute_paths import get_all_absolute_paths
from Keyword_Generator import *



# Beispielnutzung
#directory = 'C:/Users/fabia/Desktop/htmlFiles/htmlFiles/2024-07-07/'
#all_absolute_paths = get_all_absolute_paths(directory)

counter = 0
for file_path in all_absolute_paths:
    if counter == 4:
        break
    with open(file_path, 'r', encoding='utf8') as file:
        html_content = file.read()
    soup = BeautifulSoup(html_content, 'html.parser')
    # Hier kannst du mit soup weiterarbeiten
    counter += 1
"""

    print("Information about the article")
    print("-----------------------------")
    print("Author: " + str(extract_author_from_html(soup)))
    print("Paragraphs:" + str(extract_paragraphs_from_section(soup)))
    print("Publication and modification date: " + str(find_dates(soup)))
    print("Rubrik: " + str(find_meta_content(soup)))
    print("Subtitles: " + str(extract_subtitles_from_html(soup)))
    print("Titles: " + str(extract_title_from_html(soup)))
    print("Base Keywords" + str(getBaseKeywords(soup, directory)))
    print("ContentID " + str(getContentID(soup)))
    print("Linked Articles and Information: " + str(getLinkedArticles(soup)))
    print("Comments on: " + str(getCommentsOn(soup)))
    print("Additional Keywords" + str(getBERTKeywords(extract_first_overline_title(soup), extract_title_from_html(soup), extract_subtitles_from_html(soup), extract_paragraphs_from_section(soup))))
"""