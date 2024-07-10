from bs4 import BeautifulSoup

def extract_author_from_html(file_path):
    """

    :param file_path: Pfad zum entsprechenden html file
    :return:
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser')

    # Try to find the author in the first pattern
    author_tag = soup.find('p', class_='article-reference')
    if author_tag:
        author_name = author_tag.find('span', itemprop='name')
        if author_name:
            return author_name.get_text(strip=True)

    # Try to find the author in the second pattern
    author_div = soup.find('div', class_='article-author')
    if author_div:
        author_name = author_div.find('span', itemprop='name')
        if author_name:
            return author_name.get_text(strip=True)

    return "Author not found"

# Example usage
author = extract_author_from_html("C:\\Users\\fabia\\Desktop\\htmlFiles\\htmlFiles\\2024-07-04\\output_19966881_vr-im-dienst-der-medizin-mit-dem-patienten-im-koerper-des-patienten.html")
print(f"Author's name: {author}")
