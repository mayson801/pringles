import json
import tweepy
import os
import shutil
from webdriver_wrapper import WebDriverWrapper

import time
from bs4 import BeautifulSoup


def close(self):
        # Remove specific tmp dir of this "run"
        shutil.rmtree(self._tmp_folder)

        # Remove possible core dumps
        folder = '/tmp'
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if 'core.headless-chromi' in file_path and os.path.exists(file_path) and os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)
def open_web_page(url,driver):
    driver.get(url)
    time.sleep(3)
    html = driver.page_source
    print("Finished!")
    return html

def get_prices(shop_name, element_type, class_value,html):
    soup = BeautifulSoup(html,features="html.parser")

    find_price_element = soup.findAll(element_type, {"class": class_value})
    find_price_text = find_price_element[0].text.strip()

    return shop_name,find_price_text

def tweet(tweet_text):
   CONSUMER_KEY =  '4pTl8EhkAEwK3uxqnA0Oi0bhF'
   CONSUMER_SECRET = '1jQm1gK2tOBoGSxX8psev7GyUiuBFbO2K5aZiEicE0eCzs8pxY'
   ACCESS_TOKEN = '1352749264892530688-dMWGRJPsbjdz8rheG2oHF8ELWxjwne'
   ACCESS_TOKEN_SECRET = '07qmGn9hZVqzvHZ7g2eMeEynU70DbijVxvZtrPlX2nqNH'
    #Authenticate to Twitter
   auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
   auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    #Create API object
   api = tweepy.API(auth)
    #Create a tweet
   api.update_status(tweet_text)

def get_all_super_markets():
    driver = WebDriverWrapper()
    driver.get_url('https://www.tesco.com/groceries/en-GB/products/296734865')
    html = driver.print_all


    tesco_price = get_prices("tesco","https://www.tesco.com/groceries/en-GB/products/296734865","span","value",html)
    asda_price = get_prices("asda","https://groceries.asda.com/product/pringles-tube-snacks/pringles-original-sharing-crisps/910003062100","strong","co-product__price pdp-main-details__price",driver)
    morrisons_price = get_prices("morrisons","https://groceries.morrisons.com/products/pringles-original-372817011", "h2", "bop-price__current",driver)
    sainsburys_price = get_prices("sainsburys","https://www.sainsburys.co.uk/gol-ui/product/pringles-original-190g","div","pd__cost__total undefined",driver)
    coop_price = get_prices("coop","https://www.coop.co.uk/products/pringles-original-200g","p","coop-c-card__price",driver)
    driver.close

    list_of_shop_prices=[tesco_price,asda_price,morrisons_price,sainsburys_price,coop_price]
    return list_of_shop_prices

if __name__ == '__main__':


    list_of_shop_prices = get_all_super_markets()
    with open('temp.txt', 'w') as f:
        for shop in list_of_shop_prices:
          if '£' in shop[1]:
                    f.write(shop[0] +" " + shop[1] + "\n")
          else:
                    f.write(shop[0] +" £" + shop[1]+ "\n")
    with open('temp.txt', 'r') as f:
        tweet(f.read())
