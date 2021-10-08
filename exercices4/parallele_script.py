import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool

# This script was added because the multiprocessing pool doesn't work on Jupyter notebook.
# Its purpose is to have a functional answer to the final question of the projet

# We create a custom Exception class to return an exception in case of a bad status code returned by the website
class BadStatusCode(Exception):
     def __init__(self, code):
         super().__init__('Unable to connect, received status code: {}'.format(code))

def extract_beer_infos(url):
    # we request the url
    r = requests.get(url)

    # we raise an Exception if the status code is not 200
    if r.status_code != 200:
        raise BadStatusCode(r.status_code)
    
    # we get our soup from the downloaded content
    soup = BeautifulSoup(r.content, features="lxml")
    
    infos = {
        'name': soup.find('div', {'class': 'product-detail-info-title'}).find('h1').text,
        'note': int(soup.find('div', {'class': 'stars'}).attrs['data-percent']),
        'price': float(soup.find('span', {'class': 'price'}).text[:-2].replace(',', '.')),
        'volume': int(soup.find('dd', {'class': 'js-beer-volume'}).attrs['data-volume'][:-3]),
    }
    return infos

def extract_beer_list_infos_parallele(url):
    # Collecter les pages de bières à partir du JSON
    # we request the url
    r = requests.get(url)

    # we raise an Exception if the status code is not 200
    if r.status_code != 200:
        raise BadStatusCode(r.status_code)
    
    # we read our json data
    data = r.json()
    base_url = 'https://www.beerwulf.com'

    beers_urls = [base_url+item['contentReference'] for item in data['items']]
    # Parallel version (faster):
    with Pool() as p:
        beers = p.map(extract_beer_infos, beers_urls)
    
    return beers

def main():
    URL_BEERLIST_FRANCE = "https://www.beerwulf.com/fr-FR/api/search/searchProducts?country=France&container=Bouteille"
    beers = extract_beer_list_infos_parallele(URL_BEERLIST_FRANCE)
    print(beers)

if __name__ == '__main__':
    main()