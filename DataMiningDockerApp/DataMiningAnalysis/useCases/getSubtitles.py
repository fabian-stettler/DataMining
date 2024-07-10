from bs4 import BeautifulSoup


def extract_subtitles_from_html(file_path):
    """
    Ein Artikel enthält entweder 0, 1 oder mehrere subtitles.

    :param file_path
    :return: return eines arrays mit allen subtitles.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    soup = BeautifulSoup(html_content, 'html.parser')
    subtitles = soup.find_all('h2')

    extracted_subtitles = []
    for subtitle in subtitles:
        strong_tag = subtitle.find('strong')
        if strong_tag:
            extracted_subtitles.append(strong_tag.get_text(strip=True))

    return extracted_subtitles



subtitles = extract_subtitles_from_html('C:\\Users\\fabia\\Desktop\\htmlFiles\\htmlFiles\\2024-07-04\\output_19966881_vr-im-dienst-der-medizin-mit-dem-patienten-im-koerper-des-patienten.html')

print("Subtitles:")
print(subtitles)
