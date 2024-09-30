import streamlit as st
import OPSQL
import OPDBScrapper as OPSC
import pickle
import os
import OPmassentry as OPMS
import pandas as pd

# Privileged user password


# Check if the user is privileged
def is_privileged(password):
    return password == PRIVILEGED_USER_PASSWORD

# Function to display the card database
def show_card_database():
    st.title('One Piece TCG Card Database')
    
    conn = OPSQL.sqlite3.connect('OPTCGDB.db')
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM card_data")
    rows = cur.fetchall()
    col_names = [description[0] for description in cur.description]
    df = pd.DataFrame(rows, columns=col_names)
    print(df)
    db = st.dataframe(df, height= 700)
    
    cols = st.columns(8)
    for i,row in enumerate(rows):
        cols[i % 8].image(row[12])
        #st.write(row)

    #for i in range(0,len(rows)):
        #cols[i % 8].image(r"C:\Users\Duskdragon2000\Downloads\1.24e_Windows\Builds_Windows\OPTCGSim_Data\StreamingAssets\Cards\OP01\OP01-060.png")
    
    conn.close()

# Function to update the database
def update_database():
    st.title('Update Card Database')
    
    if st.button('Update'):
        if os.path.exists('series_cache'):
            with open('series_cache', 'rb') as read:
                series = pickle.load(read)
                print(series)
        
        OPSQL.initialize_db()
        for s in series:
            pass
            #OPSQL.import_card_data(OPSC.opcard_scrape(s))
        st.success('Database updated successfully!')

# Function to format the decklist
def format_decklist_input():
    st.title('TCGplayer Decklist Formatter')

    decklist = st.text_area("Paste your decklist here:")
    uploaded_file = st.file_uploader("Or upload a decklist file")
    
    if uploaded_file:
        decklist = uploaded_file.read().decode('utf-8')

    if st.button('Format Decklist'):
        if decklist:
            try:
                formatted_decklist = OPMS.format_decklist(decklist)
                tcgplayer_link = OPMS.format_tcgplayer_link(formatted_decklist)
                st.text_area('Formatted Decklist:', formatted_decklist, height= 250)
                st.write(f"[Purchase on TCGplayer]({tcgplayer_link})")
                st.image(r"C:\Users\Duskdragon2000\Downloads\1.24e_Windows\Builds_Windows\OPTCGSim_Data\StreamingAssets\Cards\OP01\OP01-060.png", width =150)
            except IndexError:
                st.error("Please format the decklist correctly e.g. 1xST12-001")
        else:
            st.error("Please paste a decklist or upload a file.")

# Main Streamlit App
st.set_page_config(layout="wide")
st.sidebar.title("One Piece TCG Tool")
option = st.sidebar.selectbox("Select an option", ('Decklist Formatter', 'View Card Database', 'Update Card Database'))

if option == 'View Card Database':
    show_card_database()
    option2 = st.sidebar.checkbox("OP-01")
    option3 = st.sidebar.checkbox("OP-02")
    option4 = st.sidebar.checkbox("OP-03")



elif option == 'Update Card Database':
    st.text_input("Enter privileged user password:", type="password", key="priv_password")
    if is_privileged(st.session_state.priv_password):
        update_database()
    else:
        st.error("Incorrect password")

elif option == 'Decklist Formatter':
    format_decklist_input()
