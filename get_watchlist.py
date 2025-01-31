import urllib.request
import ssl
from bs4 import BeautifulSoup

def get_page_count(username):
    """Fetches the total number of pages in the user's watchlist."""
    url = f"https://letterboxd.com/{username}/watchlist"
    req = urllib.request.Request(url, headers={'User-Agent': "Magic Browser"})
    try:
        with urllib.request.urlopen(req) as response:
            soup = BeautifulSoup(response.read().decode("utf8"), 'html.parser')
    except urllib.error.URLError:
        print(f"Invalid URl or no internet: {url}")
        exit()
    count_element = soup.find('span', {'class': 'js-watchlist-count'})
    if count_element:
        page_count = int(count_element.text.replace('\xa0films', ''))
        return (page_count // (7 * 4)) + 1
    return 1

def fetch_watchlist_page(username, page):
    """Fetches and returns the HTML content of a given watchlist page."""
    url = f"https://letterboxd.com/{username}/watchlist/by/popular/page/{page}"
    req = urllib.request.Request(url, headers={'User-Agent': "Magic Browser"})
    with urllib.request.urlopen(req) as response:
        return response.read().decode("utf8")

def extract_watchlist_titles(html):
    """Extracts movie titles from the watchlist page's HTML."""
    soup = BeautifulSoup(html, 'html.parser')
    watchlist_titles = []
    
    for html_object in soup.findAll('li', {'class': 'poster-container'}):
        img_tag = html_object.find('img', alt=True)
        if img_tag:
            watchlist_titles.append(img_tag['alt'])
    
    return watchlist_titles

def get_watchlist(username):
    """Fetches the full watchlist titles for a given username."""
    ssl._create_default_https_context = ssl._create_unverified_context
    watchlist_titles = []
    page_count = get_page_count(username)
    
    for i in range(1, page_count + 1):
        html = fetch_watchlist_page(username, i)
        watchlist_titles.extend(extract_watchlist_titles(html))
    
    return watchlist_titles

def main():
    username = 'aldinsmajlovic'
    watchlist = get_watchlist(username)
    print(f"{username}'s watchlist: {watchlist}")

if __name__ == "__main__":
    main()
