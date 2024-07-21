from bs4 import BeautifulSoup
import re
def extract_author_from_html(soup):
    """
    Extrahiert die Autoren aus einer HTML-Datei und gibt sie als Array zurück.
    Entweder ein Kürzel oder ein voller Name. Meine Vermutung:
    1. Eigene Artikel --> voller Name
    2. Fremde Artikel --> Kürzel

    :param file_path: Pfad zur entsprechenden HTML-Datei
    :return: Liste der Autoren
    """

    keyword_to_exclude = ["sda"]

    # Try to find the author in the first pattern
    author_tag = soup.find('p', class_='article-reference')
    if author_tag:
        author_name = author_tag.find('span', itemprop='name')
        if author_name:
            authors = author_name.get_text(strip=True).split(';')
            return [author.strip() for author in authors]

    # Try to find the author in the second pattern
    author_div = soup.find('div', class_='article-author')
    if author_div:
        author_name = author_div.find('span', itemprop='name')
        if author_name:
            author_text = author_name.get_text(strip=True)
            authors = [author.strip() for author in re.split(r'[\,;]', author_text)]
            return authors

    return ["Author not found"]

""" Example usage
file_path = "C:\\Users\\fabia\\Desktop\\htmlFiles\\htmlFiles\\2024-07-04\\output_19955553_artensterben-in-den-alpen-fuer-bergvoegel-wird-die-luft-duenn.html"
authors = extract_author_from_html(file_path)
print(f"Authors: {authors}")
"""