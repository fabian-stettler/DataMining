from bs4 import BeautifulSoup

def extract_paragraphs_from_section(soup):
    """
    Diese Funktion gibt immer mindestens einen paragraph zurück.

   :param file_path des geöffneten files
   :return: return aller Paragraphen als array.
   """
    section = soup.find('section', class_='article-content', itemprop='articleBody')

    if not section:
        return []

    paragraphs = section.find_all('p')
    return [p.get_text(strip=True) for p in paragraphs]



"""
paragraphs = extract_paragraphs_from_section('C:\\Users\\fabia\\Desktop\\htmlFiles\\htmlFiles\\2024-07-04\\output_19966881_vr-im-dienst-der-medizin-mit-dem-patienten-im-koerper-des-patienten.html')

print(paragraphs)
"""