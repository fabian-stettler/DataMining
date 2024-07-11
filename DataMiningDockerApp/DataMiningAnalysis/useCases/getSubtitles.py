from bs4 import BeautifulSoup


def extract_subtitles_from_html(file_path):
    """
    Ein Artikel enthält entweder 0, 1 oder mehrere subtitles.

    :param file_path: Pfad zur entsprechenden HTML-Datei
    :return: Array mit allen subtitles.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser')
    section = soup.find('section', class_='article-content', itemprop='articleBody')

    if not section:
        return []

    extracted_subtitles = section.find_all('h2', class_=False)
    return [h2.get_text(strip=True) for h2 in extracted_subtitles]


"""
# Beispielanwendung
file_path = 'C:\\Users\\fabia\\Desktop\\htmlFiles\\htmlFiles\\2024-07-04\\output_19966881_vr-im-dienst-der-medizin-mit-dem-patienten-im-koerper-des-patienten.html'
subtitles = extract_subtitles_from_html(file_path)

print("Subtitles:")
print(subtitles)
"""