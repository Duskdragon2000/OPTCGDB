import streamlit as st
import OPSQL
import pickle
import os
import pandas as pd


# Function to display the card database
def show_card_database():
    st.title('One Piece TCG Card Database')
    
    conn = OPSQL.sqlite3.connect('OPTCGDB.db')
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM card_data")
    rows = cur.fetchall()
    col_names = [description[0] for description in cur.description]
    df = pd.DataFrame(rows, columns=col_names)
    #print(df)
    db = st.dataframe(df, height= 700)
    
    
    #cols = st.columns(8)
    #for i,row in enumerate(rows):
        #cols[i % 8].image(f"./images/{row[11]}/{row[0]}.png", caption= row[2])
        
    
    conn.close()


# Function to format the decklist
def format_decklist_input():
    st.title('TCGplayer Decklist Formatter')
    st.divider()
    topcol1, divider, topcol2 = st.columns([10,1,5])
    with topcol1:
        decklist = st.text_area("Paste your decklist here:", height = 300)
    with topcol2:
        uploaded_file = st.file_uploader("Or upload a decklist file", accept_multiple_files=False)
        #st.image(r"C:\Users\Duskdragon2000\Desktop\full-m2H7Z5K9K9K9G6i8.png", width= 400)
    
    if uploaded_file:
        decklist = uploaded_file.read().decode('utf-8')

    if st.button('Format Decklist', icon="📝"):
        if decklist:
            try:
                st.divider()
                col1, divider, col2 = st.columns([4,1,10])
                with col1:
                    formatted_decklist = format_decklist(decklist)
                    tcgplayer_link = format_tcgplayer_link(formatted_decklist)
                    st.link_button("Purchase on TCGplayer", tcgplayer_link, icon="🎴")
                    st.text_area('Formatted Decklist:', formatted_decklist, height= 400)
                    
                    
                    

                with col2:
                    display_decklist(decklist)
                #st.image(r"C:\Users\Duskdragon2000\Downloads\1.24e_Windows\Builds_Windows\OPTCGSim_Data\StreamingAssets\Cards\OP01\OP01-060.png", width =150)
            except IndexError:
                st.error("Please format the decklist correctly e.g. 1xST12-001")
        else:
            st.error("Please paste a decklist or upload a file.")

def display_decklist(decklist):
    deck= decklist.split()
    #print(deck)
    cols = st.columns(5)
    for i,row in enumerate(deck):
        #print(row)
        cols[(i % 5)].image(f"./images/{row.split('x')[1].split('-')[0]}/{row.split('x')[1]}.png")
        
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

                set_code = card_info[11] #Had to add this because same_name_cards needs unformated set code for starter decks to work

                # Format the set number (OP-XX -> OPXX, ST-XX remains unchanged)
                if card_set.startswith('ST') or card_set.startswith('EB'):
                    card_set = card_set[:2] + '-' + card_set[2:]

                # Check if there are multiple cards with the same name in the set
                same_name_cards = OPSQL.get_cards_by_name_and_set(card_name,set_code)
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
      

# Main Streamlit App
st.set_page_config(layout="wide")
st.sidebar.title("One Piece TCG Tool")
option = st.sidebar.selectbox("Select an option", ('Decklist to TCGPlayer', 'View Card Database'))

if option == 'View Card Database':
    show_card_database()
    #option2 = st.sidebar.checkbox("OP-01")
    #option3 = st.sidebar.checkbox("OP-02")
    #option4 = st.sidebar.checkbox("OP-03")


elif option == 'Decklist to TCGPlayer':
    format_decklist_input()