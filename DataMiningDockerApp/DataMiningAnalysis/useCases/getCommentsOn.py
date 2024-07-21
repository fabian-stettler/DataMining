import bs4

def getCommentsOn(soup):
    """
    :param soup: BeautifulSoup object of the HTML content
    :return: Boolean indicating whether the comments are on or not
    """
    link_tag = soup.find('link', attrs={'rel': 'stylesheet', 'type': 'text/css'})
    if link_tag and 'href' in link_tag.attrs:
        return link_tag['href'].endswith('srf-comments-react.e37400d9.css')
    return False