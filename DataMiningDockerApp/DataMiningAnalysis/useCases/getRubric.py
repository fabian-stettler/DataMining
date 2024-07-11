from bs4 import BeautifulSoup

# Function to find and print the content of the specific meta tag
def find_meta_content(file_path):
    """

    :param file_path: file des aktuellen Files
    :return: die Rubrik (also nicht das Portal) als String
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    soup = BeautifulSoup(html_content, 'html.parser')
    meta_tag = soup.find('meta', attrs={'name': 'srf.rubric1'})
    if meta_tag and 'content' in meta_tag.attrs:
        return meta_tag['content']
    else:
        print("Meta tag not found or does not have content.")


"""
find_meta_content('C:\\Users\\fabia\\Desktop\\htmlFiles\\htmlFiles\\2024-07-07\\output_145604398_hochwasser-im-wallis-welche-zukunft-hat-die-industrie-in-siders-und-chippis.html')

"""