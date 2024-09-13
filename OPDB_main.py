import OPSQL
import OPDBScrapper as OPSC
import pickle
import os

def updateDatabase(series):
    
    OPSQL.initialize_db()

    for series in series:
        OPSQL.import_card_data(OPSC.opcard_scrape(series))

def checkUpdate():
    loaded_series = []

    if os.path.exists('series_cache'):
        with open('series_cache', 'rb') as read:
            loaded_series = pickle.load(read)
        print("Series cache loaded successfully.")
    else:
         print("Series cache file does not exist.")

    new_series = OPSC.series_scrape()

    if loaded_series == new_series:
        print('[ALL SETS ARE UP TO DATE]')
        return True


    else:
        print('[UPDATE FOUND]')
        print('[UPDATING SETS...]')
        with open('series_cache', 'wb') as write:
             pickle.dump(new_series, write) 

        print('[DONE]')
        return False
    
    

        
#OPSQL.reset_db()


print(checkUpdate())

if not checkUpdate():
    print('[UPDATING CARD DATABASE...]')

    with open('series_cache', 'rb') as read:
        series = pickle.load(read)

    updateDatabase(series)

    print('[DONE]')

else:
    print('[ALL CARDS ARE UP TO DATE]')


#print(OPSQL.get_card('OP01-060'))