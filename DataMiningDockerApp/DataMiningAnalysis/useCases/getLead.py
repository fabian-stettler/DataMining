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


'''


test
file_path = "C:/Users/fabia/Desktop/htmlFiles/htmlFiles/outputHeader.html"



with open(file_path, 'r', encoding='utf8') as file:
    html_content = file.read()
soup = BeautifulSoup(html_content, 'html.parser')

print(extract_first_overline_title(soup))
'''
