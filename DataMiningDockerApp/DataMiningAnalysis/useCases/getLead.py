from bs4 import BeautifulSoup
import requests

def extract_first_overline_title(soup):
    """
    :param file_path: Pfad zum relevanten Dokument
    :return: Der rote Lead oberhalb des Titels
    """
    # Find the first element with the class 'article-title__overline'
    overline_element = soup.find('span', class_='article-title__overline')

    # Extract and return the text content of this element
    if overline_element:
        return overline_element.get_text(strip=True)
    else:
        return None

