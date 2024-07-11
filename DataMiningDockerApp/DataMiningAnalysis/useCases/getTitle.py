from bs4 import BeautifulSoup

def extract_title_from_html(file_path):
    """
    Diese Funktion muss immer genau einen Titel zurückgeben.

    :param html_content: html des geöffneten files
    :return: return des Artikel Titels als String
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    soup = BeautifulSoup(html_content, 'html.parser')
    meta_tag = soup.find('meta', attrs={'name': 'headline'})

    if meta_tag and 'content' in meta_tag.attrs:
        return meta_tag['content']

    return "Title not found"



"""
title = extract_title_from_html('C:\\Users\\fabia\\Desktop\\htmlFiles\\htmlFiles\\2024-07-04\\output_19966881_vr-im-dienst-der-medizin-mit-dem-patienten-im-koerper-des-patienten.html')

print(f"Title: {title}")
"""