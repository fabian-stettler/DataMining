from bs4 import BeautifulSoup

def extract_title_from_html(soup):
    """
    Diese Funktion muss immer genau einen Titel zurückgeben.
    Achtung dieser Titel ist nicht immer derjenige der displayed wird, sondern
    der titel im header aber mit Berücksichtigung der Gross Klein Schreibung

    :param html_content: html des geöffneten files
    :return: return des Artikel Titels als String
    """
    meta_tag = soup.find('meta', attrs={'name': 'headline'})

    if meta_tag and 'content' in meta_tag.attrs:
        return meta_tag['content']

    return "Title not found"



"""
title = extract_title_from_html('C:\\Users\\fabia\\Desktop\\htmlFiles\\htmlFiles\\2024-07-04\\output_19966881_vr-im-dienst-der-medizin-mit-dem-patienten-im-koerper-des-patienten.html')

print(f"Title: {title}")
"""