from bs4 import BeautifulSoup
import re

def getArticleLink(soup, articlePath):
    """
    Erhalten des Links von einem gespeicherten html files
    :param articlePath: Pfad zum gespeicherten Artikel
    :return: Weblink auf welchem der Artikel publiziert wurde
    """
    linkTag = soup.find('meta', property='og:url')

    if linkTag:
        return "return Value: " + linkTag['content']
    else:
        return ""


def getBaseKeywords(soup, articlePath):
    """
    :param articlePath: ist der Pfad auf welchem das html File gespeichert ist
    :return: Alle Keywords die aus dem Link zu entnehmen sind:
    1. portal
    2. rubrik
    3. alles was noch zusätzlich zwischen rubrik und dem title steht (Beispiel hier: output_168542942_wimbledon-tag-4-frauen-swiatek-humorlos-pegula-schon-in-der-2-runde-out.html ---> grand-slam-turniere)
    """
    articleLink = getArticleLink(soup, articlePath)

    # Use regex to extract the part of the URL between 'srf.ch' and the last part after the final '/'
    pattern = r'srf\.ch/(.*)/([^/]+)$'
    match = re.search(pattern, articleLink)

    if match:
        # Split the extracted part by '/'
        keywords = match.group(1).split('/')
        return keywords
    else:
        return []


