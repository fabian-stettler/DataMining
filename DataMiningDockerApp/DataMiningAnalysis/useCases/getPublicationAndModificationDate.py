from bs4 import BeautifulSoup

def find_dates(file_path):
    """
    Gibt das publication und modification date in einem array der länge 2 zurück.

    :param file_path: path des momentanen files
    :return: publication und last modification date return als Array
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    soup = BeautifulSoup(html_content, 'html.parser')
    tag = soup.find('p', class_='article-author__date js-dateline')

    publication_date = None
    modification_date = None

    if tag:
        if 'data-publicationdate' in tag.attrs:
            publication_date = tag['data-publicationdate']
        if 'data-modificationdate' in tag.attrs:
            modification_date = tag['data-modificationdate']

    return publication_date, modification_date



"""
publication_date, modification_date = find_dates('C:\\Users\\fabia\\Desktop\\htmlFiles\\htmlFiles\\2024-07-07\\output_145604398_hochwasser-im-wallis-welche-zukunft-hat-die-industrie-in-siders-und-chippis.html')

if publication_date:
    print(f"Publication Date: {publication_date}")
else:
    print("Publication Date not found")

if modification_date:
    print(f"Modification Date: {modification_date}")
else:
    print("Modification Date not found")
"""