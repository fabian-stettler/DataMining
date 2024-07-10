from bs4 import BeautifulSoup

# Function to find and print the content of the specific meta tag
def find_meta_content(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    meta_tag = soup.find('meta', attrs={'name': 'srf.rubric1'})
    if meta_tag and 'content' in meta_tag.attrs:
        print(meta_tag['content'])
    else:
        print("Meta tag not found or does not have content.")

# Load HTML content from a file
with open('C:\\Users\\fabia\\Desktop\\htmlFiles\\htmlFiles\\2024-07-07\\output_145604398_hochwasser-im-wallis-welche-zukunft-hat-die-industrie-in-siders-und-chippis.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

find_meta_content(html_content)

