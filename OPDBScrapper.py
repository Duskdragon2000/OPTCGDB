import requests
from bs4 import BeautifulSoup

def opcard_scrape(series):
    r = requests.get(f'https://asia-en.onepiece-cardgame.com/cardlist/?series={series}')

    soup = BeautifulSoup(r.content, 'html.parser')

    site_card_data = soup.find_all(class_='modalCol')

    card_data = []

    for card in site_card_data:
        card_dict = {}

        card_dict['id'] = card.get('id')
        card_dict['card_number'] = card.get('id').split('-')[1].split('_')[0]
        card_dict['name'] = card.find('div', class_ = 'cardName').get_text()
        card_dict['category'] = card.find('div', class_ = 'infoCol').get_text().split('|')[2].strip()
        card_dict['cost'] = card.find('div', class_ = 'cost').get_text().strip('Cost').strip('Life')
        card_dict['attribute'] = card.find('div', class_='attribute').get_text().strip().split('\n')[1]
        card_dict['counter'] = card.find('div', class_='counter').get_text().strip('Counter')
        card_dict['color'] = card.find('div', class_='color').get_text().strip('Color')
        card_dict['feature'] = card.find('div', class_='feature').get_text()[4:]
        card_dict['effect'] = card.find('div', class_='text').get_text()[6:]
        card_dict['card_set'] = card.find('div', class_='getInfo').get_text().strip('Card Set(s)')
        card_dict['set_code'] = card.get('id').split('-')[0].split('_')[0]
        card_dict['image_src'] = 'https://asia-en.onepiece-cardgame.com/' + card.find('img', class_='lazy').get('data-src').strip('..')
        

        card_data.append(card_dict)

    return card_data

def series_scrape():
    r = requests.get('https://asia-en.onepiece-cardgame.com/cardlist/')

    soup = BeautifulSoup(r.content, 'html.parser')
    series_data = soup.find('select', class_='selectModal')
   
    options = series_data.find_all('option')

    set_list = [option.get('value') for option in options if option.get('value')]
        
    return(set_list)

