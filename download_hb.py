#!/usr/bin/env python
# A script that parses HumbleBundle book download page and downloads books that
# are there.
# The script expects the final html file, that is generated after javascript has
# fetched download links, to be in HTML_FILE file. It downloads the books into
# TARGET_DIR.

from bs4 import BeautifulSoup
import os
import os.path
import urllib.request

HTML_FILE='book.html'
TARGET_DIR='HB books'

def extract_book_links(page):
    '''Returns a dictionary from book name to a dictionary to book links.'''
    soup = BeautifulSoup(page, 'html.parser')
    dl_divs = soup.find_all('div', {'class': 'js-all-downloads-holder'})
    found_books = {}
    assert(len(dl_divs) == 1)
    for dl_div in dl_divs[0]:
        link = dl_div.find('div', {'class': 'title'}).find('a')
        assert(link is not None)
        book_title = link.string.strip()

        links = dl_div.find('div', {'class': 'ebook'}).find(
                'div', {'class': 'download-buttons'}).find_all(
                'a', {'class': 'a'})
        found_books[book_title] = {l.string.strip(): l['href'] for l in links}
    return found_books

if __name__ == '__main__':
    with open(HTML_FILE, 'r') as f:
        page = f.read()
    found_books = extract_book_links(page)
    os.makedirs(TARGET_DIR, exist_ok=True)
    for book in found_books:
        os.makedirs(os.path.join(TARGET_DIR, book), exist_ok=True)
        targets = found_books[book]
        for target in targets:
            print("Downloading {0} for {1}".format(target, book))
            urllib.request.urlretrieve(targets[target],
                    os.path.join(TARGET_DIR, book,
                        book + '.' + target.lower()))
