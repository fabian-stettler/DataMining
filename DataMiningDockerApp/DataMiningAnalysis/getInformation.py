from DataMiningAnalysis.useCases.getAuthor import extract_author_from_html
from DataMiningAnalysis.useCases.getParagraphes import extract_paragraphs_from_section
from DataMiningAnalysis.useCases.getPublicationAndModificationDate import find_dates
from DataMiningAnalysis.useCases.getRubric import find_meta_content
from DataMiningAnalysis.useCases.getSubtitles import extract_subtitles_from_html
from DataMiningAnalysis.useCases.getTitle import extract_title_from_html

from Keyword_Generator import *

file_path = 'C:\\Users\\fabia\\Desktop\\htmlFiles\\htmlFiles\\2024-07-07\\output_20065304_oekobilanz-von-haustieren-luna-und-rocky-als-klimakiller.html'

print("Information about the article")
print("-----------------------------")
print("Author: " + str(extract_author_from_html(file_path)))
print("Paragraphs:" + str(extract_paragraphs_from_section(file_path)))
print("Publication and modification date: " + str(find_dates(file_path)))
print("Rubrik: " + str(find_meta_content(file_path)))
print("Subtitles: " + str(extract_subtitles_from_html(file_path)))
print("Titles: " + str(extract_title_from_html(file_path)))


