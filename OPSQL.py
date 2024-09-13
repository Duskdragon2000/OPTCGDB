import sqlite3

def initialize_db():
    conn = sqlite3.connect('OPTCGDB.db')
    cur = conn.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS card_data (
            id TEXT PRIMARY KEY,
            card_number TEXT,
            name TEXT,
            category TEXT,
            cost TEXT,
            attribute TEXT,
            counter TEXT,
            color TEXT,
            feature TEXT,
            effect TEXT,
            card_set TEXT,
            set_code TEXT,
            image_src TEXT
        )
    ''')

    conn.commit()
    conn.close()

def import_card_data(card_data):

    conn = sqlite3.connect('OPTCGDB.db')
    cur = conn.cursor()

    for card in card_data:
            
            cur.execute('''
            INSERT OR REPLACE INTO card_data (id, card_number, name, category, cost, attribute, counter, color, feature, effect, card_set, set_code, image_src)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
            card['id'],
            card['card_number'],
            card['name'],
            card['category'],
            card['cost'],
            card['attribute'],
            card['counter'],
            card['color'],
            card['feature'],
            card['effect'],
            card['card_set'],
            card['set_code'],
            card['image_src']
        ))
    # Commit the transaction
    conn.commit()

    # Close the connection
    conn.close()

def get_card(card_id):
    conn = sqlite3.connect('OPTCGDB.db')
    cur = conn.cursor()

    cur.execute('''
    SELECT id, card_number, name, category, cost, attribute, counter, color, feature, effect, card_set, set_code, image_src
    FROM card_data
    WHERE id = ?
    ''', (card_id,))

    card_info = cur.fetchone()
    conn.commit()
    conn.close()
    return(card_info)

def reset_db():

    conn = sqlite3.connect('OPTCGDB.db')
    cur = conn.cursor()

    cur.execute('''
    DROP TABLE card_data;
    ''')
    conn.commit()
    conn.close()


def get_cards_by_name_and_set(card_name,set_code):
    connection = sqlite3.connect('OPTCGDB.db')  # Update with your DB file path
    cur = connection.cursor()

    cur.execute('''
        SELECT id, card_number, name, category, cost, attribute, counter, color, feature, effect, card_set, set_code, image_src
        FROM card_data
        WHERE name = ?
        AND set_code = ?
    ''', (card_name, set_code))
    
    cards = cur.fetchall()

    card_map = {}
    for card in cards:
        base_id = card[0].split('_')[0]  # Take base ID before underscore
        if base_id not in card_map:
            card_map[base_id] = card

    connection.close()

    return list(card_map.values())

