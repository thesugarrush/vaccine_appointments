from time import sleep
from urllib.request import urlopen, Request

import argparse
import json
import sys
from tqdm import tqdm
import webbrowser
import urllib.request

from geopy.geocoders import Nominatim
from geopy.distance import geodesic

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import os
from sys import platform

from datetime import datetime

store_name_to_distance = {}

driver = webdriver.Chrome('./chromedriver')

bool_play_sound = False;


def open_appointments(namespace, geolocator, request_object, cookie1=None, cookie2=None):
    
    locations = json.loads(urlopen(request_object).read())['locations']

    success = False
    for location in locations:
        if namespace.cities is not None and location['city'].lower() not in namespace.cities:
            continue
        if namespace.zipcodes is not None and location['zip'] not in namespace.zipcodes:
            continue
        distance = None
        if namespace.distance is not None:
            if location['name'] in store_name_to_distance:
                distance = store_name_to_distance[location['name']]
            else:
                latlong = (location['latitude'], location['longitude'])
                if any(l is None for l in latlong):
                    geoloc = geolocator.geocode(', '.join(location[key] for key in ['street', 'city', 'state', 'zip']))
                    if geoloc is None:
                        geoloc = geolocator.geocode(location['zip'])
                    latlong = (geoloc.latitude, geoloc.longitude)
                distance = geodesic(ns.latlong, latlong)
                store_name_to_distance[location['name']] = distance
            if distance.miles > namespace.distance:
                continue
        if location['openTimeslots'] > 0:
            contents = urllib.request.urlopen(f"{location['url']}&lang=en-us").read().decode('utf-8')
            if 'Appointments are no longer available for this location' not in contents:
                
                url = f"{location['url']}&lang=en-us"

                driver.get(url)
                
                #driver.implicitly_wait(0.25) # seconds

                drp_date_1a = driver.find_element_by_xpath("/html/body/span[@id='j_id0:j_id18']/div[@id='container']/c-f-s-registration/div[@class='page-container']/div[1]/div[@class='slds-m-bottom_medium'][3]/lightning-card/article[@class='slds-card']/div[@class='slds-card__body']/slot/div[@class='slds-m-around_medium']/form/div[@class='slds-p-around_medium form']/lightning-combobox[@class='slds-form-element']/div[@class='slds-form-element__control']/lightning-base-combobox[@class='slds-combobox_container']/div[@class='slds-combobox slds-dropdown-trigger slds-dropdown-trigger_click']/div[@class='slds-combobox__form-element slds-input-has-icon slds-input-has-icon_right']/input[@id='input-14']").click()
                
                drp_date_1b = driver.find_element_by_xpath("/html/body/span[@id='j_id0:j_id18']/div[@id='container']/c-f-s-registration/div[@class='page-container']/div[1]/div[@class='slds-m-bottom_medium'][3]/lightning-card/article[@class='slds-card']/div[@class='slds-card__body']/slot/div[@class='slds-m-around_medium']/form/div[@class='slds-p-around_medium form']/lightning-combobox[@class='slds-form-element'][2]/div[@class='slds-form-element__control']/lightning-base-combobox[@class='slds-combobox_container']/div[@class='slds-combobox slds-dropdown-trigger slds-dropdown-trigger_click slds-is-open']/div[@id='dropdown-element-14']/lightning-base-combobox-item[@id='input-14-0-14']/span[@class='slds-media__body']").click()

                drp_session_2a = driver.find_element_by_xpath("/html/body/span[@id='j_id0:j_id18']/div[@id='container']/c-f-s-registration/div[@class='page-container']/div[1]/div[@class='slds-m-bottom_medium'][3]/lightning-card/article[@class='slds-card']/div[@class='slds-card__body']/slot/div[@class='slds-m-around_medium']/form/div[@class='slds-p-around_medium form']/lightning-combobox[@class='slds-form-element'][3]/div[@class='slds-form-element__control']/lightning-base-combobox[@class='slds-combobox_container']/div[@class='slds-combobox slds-dropdown-trigger slds-dropdown-trigger_click']/div[@class='slds-combobox__form-element slds-input-has-icon slds-input-has-icon_right']/input[@id='input-18']").click()
                
                drp_session_2b = driver.find_element_by_xpath("/html/body/span[@id='j_id0:j_id18']/div[@id='container']/c-f-s-registration/div[@class='page-container']/div[1]/div[@class='slds-m-bottom_medium'][3]/lightning-card/article[@class='slds-card']/div[@class='slds-card__body']/slot/div[@class='slds-m-around_medium']/form/div[@class='slds-p-around_medium form']/lightning-combobox[@class='slds-form-element'][3]/div[@class='slds-form-element__control']/lightning-base-combobox[@class='slds-combobox_container']/div[@class='slds-combobox slds-dropdown-trigger slds-dropdown-trigger_click slds-is-open']/div[@id='dropdown-element-18']/lightning-base-combobox-item[@id='input-18-0-18']/span[@class='slds-media__body']").click()

                btnContinue = driver.find_element_by_xpath("/html/body/span[@id='j_id0:j_id18']/div[@id='container']/c-f-s-registration/div[@class='page-container']/div[1]/div[@class='slds-text-align_right margin-bottom']/lightning-button[@class='slds-m-left_x-small']/button[@class='slds-button slds-button_success']").click()
                print(f"btnContinue: {btnContinue}")

                # webbrowser.open(location['url'])
                print('\n'.join(f'{k}={v}' for k, v in location.items() if k not in ['url', 'slotDetails'] and v is not None))
                if distance is not None:
                    print(f'Distance from home: {distance.miles} miles')
                
                print(f"url: {url}")
                
                success = True
    return success


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Program to ping HEB for vaccine appointments in your area")
    parser.add_argument('-c', '--cities', nargs='+', help='Cities to restrict the search to')
    parser.add_argument('-H', '--home',
                        help='Home location: can be in the form of a zipcode, address, latitude/longitude, city, etc. (requires distance)')
    parser.add_argument('-d', '--distance', type=float,
                        help='Maximum distance (in miles) from home (requires home)')
    parser.add_argument('-Z', '--zipcodes', nargs='+', help='Zipcodes to restrict the search to')

    ns = parser.parse_args(sys.argv[1:])

    assert (ns.distance is None) == (ns.home is None), 'Home location and distance should be supplied together'

    geolocator = Nominatim(user_agent='vaccine_appointments')

    if ns.cities:
        ns.cities = {city.lower() for city in ns.cities}
    if ns.distance:
        home = geolocator.geocode(ns.home)
        ns.latlong = (home.latitude, home.longitude)
        print(f'Looking for appointments {ns.distance} miles from {home}')
    

    # we want to keep trying if there is an exception/error when trying to get an appointment in step 2
    # for example: if we are competing with other BOT as well.
    while True:
        
        # get cookies so it can be included in the headers when hitting the backend
        driver.get('https://vaccine.heb.com/scheduler?q=78717') #q=xxxxx can be any zip code, does not matter, we just want to get the cookie
        cookie1 = driver.get_cookie("_ga")
        cookie2 = driver.get_cookie("_ga_PL4YBQB4CC")
        # print(f"cookie1: {cookie1}, cookie2: {cookie2}")

        # add header information here to 'trick' backend to think it is from web browser
        # more doc: https://docs.python.org/3/howto/urllib2.html
        user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
        cookies = f"_ga_PL4YBQB4CC={cookie1['value']}; _ga={cookie2['value']}"

        #fake gmt time
        fake_dt = datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT")

        fake_uuid = 'fe99b415fbeac2fe575ec4911d1755d9'

        headers = {
            'Accept': '*/*', 
            'Accept-Encoding': 'gzip, deflate, br',
            'TE': 'Trailers',
            'Accept-Language': 'en-US,en;q=0.5',
            'Origin': 'https://vaccine.heb.com',
            'Referer': 'https://vaccine.heb.com/',
            'User-Agent': user_agent,
            'Cookies': cookies,
            'Host': 'heb-ecom-covid-vaccine.hebdigital-prd.com',
            'If-Modified-Since': fake_dt,
            'If-None-Match': fake_uuid
        }

        url = 'https://heb-ecom-covid-vaccine.hebdigital-prd.com/vaccine_locations.json'
        req_object = Request(url, headers=headers)

        with tqdm() as pbar:
            try:
                while not open_appointments(ns, geolocator, req_object, cookie1, cookie2):
                    sleep(1)
                    pbar.update(1)
                
                if bool_play_sound:
                    # optional - use case: wear your bluetooth headset and just walk away
                    # play song if found
                    if platform == "linux" or platform == "linux2":
                        os.system('mpg123 ./startrek-tos-closing.aif')
                    elif platform == "darwin":
                        os.system('afplay ./startrek-tos-closing.aif')
                    # elif platform == "win32":
                        # Windows...i dont have windows to test this.

            except:
                print("Unexpected error:", sys.exc_info()[0])
                # if bool_play_sound:
                #     # optional - play song if error
                #     if platform == "linux" or platform == "linux2":
                #         os.system('mpg123 ./startrek-spock-illogical.aif')
                #     elif platform == "darwin":
                #         os.system('afplay ./startrek-spock-illogical.aif')
                    # elif platform == "win32":
                        # Windows...i dont have windows to test this.
                
                #continue loop
                sleep(5)
                continue

            break
            