import re
from bs4 import BeautifulSoup



def extract_author_from_html(soup):
    """
    Extrahiert die Autoren aus einer HTML-Datei und gibt sie als Liste zurück.
    Entweder ein Kürzel oder ein voller Name. Meine Vermutung:
    1. Eigene Artikel --> voller Name
    2. Fremde Artikel --> Kürzel

    :param soup: BeautifulSoup-Objekt der HTML-Datei
    :return: Liste der Autoren
    """

    keyword_to_exclude = ["sda"]

    # Try to find the author in the first pattern
    author_tag = soup.find('p', class_='article-reference')
    if author_tag:
        author_name = author_tag.find('span', itemprop='name')
        if author_name:
            author_text = author_name.get_text(strip=True)
            authors = [author.strip() for author in re.split(r'[\/,;]', author_text)]
            return authors

    # Try to find the author in the second pattern
    author_div = soup.find('div', class_='article-author')
    if author_div:
        author_name = author_div.find('span', itemprop='name')
        if author_name:
            author_text = author_name.get_text(strip=True)
            authors = [author.strip() for author in re.split(r'[\/,;]', author_text)]
            return authors

    return ["Author not found"]

""" Example usage

directory = "C:\\Users\\fabia\\Desktop\\htmlFiles\\htmlFiles\\2024-07-07"
for file_path in get_all_absolute_paths(directory):
    with open(file_path, 'r', encoding='utf8') as file:
        html_content = file.read()
    soup = BeautifulSoup(html_content, 'html.parser')
    authors = extract_author_from_html(soup)
    print(f"Authors: {authors} for article {file_path}")
"""