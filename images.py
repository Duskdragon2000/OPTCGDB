import os
import sqlite3
import requests 
import logging

# Database file path
db_path = 'OPTCGDB.db'  # Update with your actual database path

# Folder to save the images
image_root_folder = r"./images"  # Update this to the folder where images should be saved

# Base URLs for image download
base_url_english = 'https://en.onepiece-cardgame.com/images/cardlist/card/'
base_url_asia = 'https://asia-en.onepiece-cardgame.com/images/cardlist/card/'

logging.basicConfig(filename= "card.log", encoding="utf-8", filemode="a", level=logging.INFO, format='%(asctime)s - %(message)s')

# Asynchronous function to download an image
def download_image(card_id, set_code):
    folder_path = os.path.join(image_root_folder, set_code)
    os.makedirs(folder_path, exist_ok=True)

    image_file_path = os.path.join(folder_path, f"{card_id}.png")

    # Skip downloading if the image already exist
    if os.path.exists(image_file_path):
        print(f"Image already exists: {image_file_path}")
        return


    # Try downloading from the English URL first
    image_url_english = f"{base_url_english}{card_id}.png"
    image_url_asia = f"{base_url_asia}{card_id}.png"

    print(image_url_english)
    try:
        img = requests.get(image_url_english)
        print(img)
        if img.status_code == 200:
            with open(image_file_path, 'wb') as file:
                file.write(img.content)
                print(f"Downloaded image from English URL: {image_file_path} (Source: {image_url_english})")
                return  # Exit after successful download
        if img.status_code == 404:
            logging.info(f"English card not found for: {card_id}")
            try:
                img = requests.get(image_url_asia)
                print(img)
                if img.status_code == 200:
                    with open(image_file_path, 'wb') as file:
                        file.write(img.content)
                        print(f"Downloaded image from Asian URL: {image_file_path} (Source: {image_url_asia})")
                        logging.info(f"Downloaded image from Asian URL: {card_id}")
                        return  # Exit after successful download
                if img.status_code == 404:
                    logging.info(f"Asian card not found for: {card_id}")
                    
                    
            except Exception as e:
                logging.error(f"Error downloading asian {card_id}: {e}")
           
    except Exception as e:
        logging.error(f"Error downloading english {card_id}: {e}")


# Asynchronous function to download images concurrently
def download_images_all():
    connection = sqlite3.connect(db_path)
    cur = connection.cursor()
    cur.execute('SELECT id, set_code FROM card_data')
    cards = cur.fetchall()
    connection.close()


    for card_id, set_code in cards:
        download_image(card_id, set_code)


    print("Image download process completed.")

def retry_asian_images():

    retry_arr = []
    

    with open('card.log') as log_file:
        for line in log_file:
            if 'Downloaded image from Asian URL:' in line:
                retry_arr.append(line.rsplit(':')[-1].strip())

    for card in retry_arr:

        card_id = card 
        set_code = card.split('-')[0]
        folder_path = os.path.join(image_root_folder, set_code)
        image_file_path = os.path.join(folder_path, f"{card_id}.png")

        print("Trying: ", card_id)
        os.remove(image_file_path)

        download_image(card_id, set_code)
        print("Done with: ", card_id)

    #print(retry_arr)

# Entry point
if __name__ == "__main__":
    download_image("PRB01-001", "PRB01")
    #download_images_all()
    #retry_asian_images()

    

