import json
import tweepy

import time
from bs4 import BeautifulSoup
from selenium import webdriver
from requests_html import HTMLSession


def open_web_page(url,driver):
    driver.get(url)
    time.sleep(3)
    html = driver.page_source
    print("Finished!")
    return html

def get_prices(shop_name,url, element_type, class_value,driver):
    html = open_web_page(url,driver)
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
    driver = webdriver.Chrome()
    tesco_price = get_prices("tesco","https://www.tesco.com/groceries/en-GB/products/296734865","span","value",driver)
    asda_price = get_prices("asda","https://groceries.asda.com/product/pringles-tube-snacks/pringles-original-sharing-crisps/910003062100","strong","co-product__price pdp-main-details__price",driver)
    morrisons_price = get_prices("morrisons","https://groceries.morrisons.com/products/pringles-original-372817011", "h2", "bop-price__current",driver)
    sainsburys_price = get_prices("sainsburys","https://www.sainsburys.co.uk/gol-ui/product/pringles-original-190g","div","pd__cost__total undefined",driver)
    coop_price = get_prices("coop","https://www.coop.co.uk/products/pringles-original-200g","p","coop-c-card__price",driver)
    driver.quit()

    list_of_shop_prices=[tesco_price,asda_price,morrisons_price,sainsburys_price,coop_price]
    return list_of_shop_prices

#if __name__ == '__main__':

    #use for testing
    #list_of_shop_prices=[('tesco', '2.50'), ('asda', '£1.50'), ('morrisons', '£3'), ('sainsburys', '£3.00'), ('coop', '£3')]

    #list_of_shop_prices = get_all_super_markets()
    #with open('temp.txt', 'w') as f:
     #   for shop in list_of_shop_prices:
      #      if '£' in shop[1]:
       #         f.write(shop[0] +" " + shop[1] + "\n")
        #    else:
         #       f.write(shop[0] +" £" + shop[1]+ "\n")

    #with open('temp.txt', 'r') as f:
        #tweet(f.read())

def testing():
    # create an HTML Session object
    session = HTMLSession()
    # Use the object above to connect to needed webpage
    resp = session.get("https://finance.yahoo.com/quote/NFLX/options?p=NFLX")
    # Run JavaScript code on webpage
    resp.html.render()
def lambda_handler(event, context):
    #tweet("hello")
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "hello world",
            # "location": ip.text.replace("\n", "")
        }),
    }
testing()

#tweet_text = get_all_super_markets()
#print(tweet_text)
