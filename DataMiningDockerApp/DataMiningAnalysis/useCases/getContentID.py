from bs4 import BeautifulSoup

def getContentID(soup):
    """
    :param file_path: Pfad zum relevanten HTML-Dokument
    :return: die Content ID des Artikels als Integer
    """
    content_tag = soup.find('meta', attrs={'name': "srf:content:id"})

    if content_tag:
        return int(content_tag['content'])
    else:
        return None
