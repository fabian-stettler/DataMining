from bs4 import BeautifulSoup

def getLinkedArticles(soup):
    """
    :param file_path: Pfad zum relevanten HTML-Dokument
    :return: Liste von Tupeln, die den Titel, href und die Content-ID jedes passenden <a>-Tags enthalten
    Artikel die in beiden Verlinkungskategorien "Passend zum Thema" und "Mehr zum Thema" enthalten sind, werden rausgefiltert.
    """
    list_tags = soup.find_all('ul', class_='related-items-list__list')

    if not list_tags:
        return []

    article_links = []
    seen_content_ids = set()
    for list_tag in list_tags:
        for a_tag in list_tag.find_all('a', href=True, attrs={'data-urn': True, 'data-title': True}):
            data_urn = a_tag['data-urn']
            if data_urn.startswith('urn:srf:article'):
                title = a_tag['data-title']
                href = a_tag['href']
                content_id = data_urn.split(':')[-1]
                if content_id not in seen_content_ids:
                    seen_content_ids.add(content_id)
                    article_links.append((title, href, content_id))

    return article_links

