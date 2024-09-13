import OPSQL
import OPDBScrapper as OPSC
import pickle
import os
from flask import Flask, render_template, request

app = Flask(__name__)

def format_decklist(decklist):
    formatted_list = []
    for line in decklist.splitlines():
        if 'x' in line:
            quantity, card_set_id = line.split('x')
            quantity = quantity.strip()
            card_set_id = card_set_id.strip()

            card_info = OPSQL.get_card(card_set_id)
            
            if card_info:
                card_name = card_info[2]
                card_number = card_info[1]
                card_set = card_info[11]

                # Format the set number (OP-XX -> OPXX, ST-XX remains unchanged)
                if card_set.startswith('ST') or card_set.startswith('EB'):
                    card_set = card_set[:2] + '-' + card_set[2:]

                # Check if there are multiple cards with the same name in the set
                same_name_cards = OPSQL.get_cards_by_name_and_set(card_name,card_set)
                if len(same_name_cards) > 1:
                    formatted_list.append(f'{quantity} {card_name} ({card_number}) [{card_set}]')
                else:
                    formatted_list.append(f'{quantity} {card_name} [{card_set}]')

    return '\n'.join(formatted_list)

def format_tcgplayer_link(formatted_list):
    base_url = "https://www.tcgplayer.com/massentry/?productline=One%20piece%20card%20game&c="
    encoded_list = []
    for line in formatted_list.split('\n'):
        parts = line.split(' ', 1)
        quantity = parts[0]
        card_info = parts[1].rsplit('[', 1)
        card_name = card_info[0].strip()
        set_code = card_info[1].strip(']')
        encoded_card_name = card_name.replace(' ', '+').replace('&', '%26')
        encoded_list.append(f"{quantity}+{encoded_card_name}+[{set_code}]")
    return base_url + "%7c%7c".join(encoded_list)
    
@app.route('/', methods=['GET', 'POST'])
def decklist_form():
    if request.method == 'POST':
        decklist = request.form.get('decklist', '')
        
        # Check if a file is uploaded
        if 'deckfile' in request.files:
            file = request.files['deckfile']
            if file:
                decklist = file.read().decode('utf-8')

        print(f'Decklist: {decklist}')  # Debug print statement
        
        formatted_output = format_decklist(decklist)
        tcgplayer_link = format_tcgplayer_link(formatted_output)
        return render_template('decklist_form.html', output=formatted_output, tcgplayer_link=tcgplayer_link)
    
    return render_template('decklist_form.html')





if __name__ == '__main__':
    app.run(debug=True)
