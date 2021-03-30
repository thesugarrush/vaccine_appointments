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

store_name_to_distance = {}

driver = webdriver.Chrome('./chromedriver')

def open_appointments(namespace, geolocator):
    
    # add header information here to 'trick' backend to think it is from web browser
    # more doc: https://docs.python.org/3/howto/urllib2.html
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
    cookies = '_ga_PL4YBQB4CC=GS1.1.1617070859.1.1.1617073263.0; _ga=GA1.1.1302840320.1617070860'
    headers = {
        'Accept': '*/*', 
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://vaccine.heb.com/scheduler?q=78717',
        'User-Agent': user_agent,
        'Cookies': cookies
    }

    url = 'https://heb-ecom-covid-vaccine.hebdigital-prd.com/vaccine_locations.json'
    req = Request(url, headers=headers)
    locations = json.loads(urlopen(req).read())['locations']

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
            contents = urllib.request.urlopen(location['url'] + "&lang=en-us").read().decode('utf-8')
            if 'Appointments are no longer available for this location' not in contents:
                
                driver.get(location['url'] + "&lang=en-us")
                
                driver.implicitly_wait(1.0) # seconds

                drp_date_1a = driver.find_element_by_xpath("/html/body/span[@id='j_id0:j_id18']/div[@id='container']/c-f-s-registration/div[@class='page-container']/div[1]/div[@class='slds-m-bottom_medium'][3]/lightning-card/article[@class='slds-card']/div[@class='slds-card__body']/slot/div[@class='slds-m-around_medium']/form/div[@class='slds-p-around_medium form']/lightning-combobox[@class='slds-form-element']/div[@class='slds-form-element__control']/lightning-base-combobox[@class='slds-combobox_container']/div[@class='slds-combobox slds-dropdown-trigger slds-dropdown-trigger_click']/div[@class='slds-combobox__form-element slds-input-has-icon slds-input-has-icon_right']/input[@id='input-14']")
                drp_date_1a.click()
                
                drp_date_1b = driver.find_element_by_xpath("/html/body/span[@id='j_id0:j_id18']/div[@id='container']/c-f-s-registration/div[@class='page-container']/div[1]/div[@class='slds-m-bottom_medium'][3]/lightning-card/article[@class='slds-card']/div[@class='slds-card__body']/slot/div[@class='slds-m-around_medium']/form/div[@class='slds-p-around_medium form']/lightning-combobox[@class='slds-form-element'][2]/div[@class='slds-form-element__control']/lightning-base-combobox[@class='slds-combobox_container']/div[@class='slds-combobox slds-dropdown-trigger slds-dropdown-trigger_click slds-is-open']/div[@id='dropdown-element-14']/lightning-base-combobox-item[@id='input-14-0-14']/span[@class='slds-media__body']")
                drp_date_1b.click()

                drp_session_2a = driver.find_element_by_xpath("/html/body/span[@id='j_id0:j_id18']/div[@id='container']/c-f-s-registration/div[@class='page-container']/div[1]/div[@class='slds-m-bottom_medium'][3]/lightning-card/article[@class='slds-card']/div[@class='slds-card__body']/slot/div[@class='slds-m-around_medium']/form/div[@class='slds-p-around_medium form']/lightning-combobox[@class='slds-form-element'][3]/div[@class='slds-form-element__control']/lightning-base-combobox[@class='slds-combobox_container']/div[@class='slds-combobox slds-dropdown-trigger slds-dropdown-trigger_click']/div[@class='slds-combobox__form-element slds-input-has-icon slds-input-has-icon_right']/input[@id='input-18']")
                drp_session_2a.click()
                
                drp_session_2b = driver.find_element_by_xpath("/html/body/span[@id='j_id0:j_id18']/div[@id='container']/c-f-s-registration/div[@class='page-container']/div[1]/div[@class='slds-m-bottom_medium'][3]/lightning-card/article[@class='slds-card']/div[@class='slds-card__body']/slot/div[@class='slds-m-around_medium']/form/div[@class='slds-p-around_medium form']/lightning-combobox[@class='slds-form-element'][3]/div[@class='slds-form-element__control']/lightning-base-combobox[@class='slds-combobox_container']/div[@class='slds-combobox slds-dropdown-trigger slds-dropdown-trigger_click slds-is-open']/div[@id='dropdown-element-18']/lightning-base-combobox-item[@id='input-18-0-18']/span[@class='slds-media__body']")
                drp_session_2b.click()
    
                btnContinue = driver.find_element_by_xpath("/html/body/span[@id='j_id0:j_id18']/div[@id='container']/c-f-s-registration/div[@class='page-container']/div[1]/div[@class='slds-text-align_right margin-bottom']/lightning-button[@class='slds-m-left_x-small']/button[@class='slds-button slds-button_success']")
                print(f"btnContinue: {btnContinue}")
                btnContinue.click()

                # webbrowser.open(location['url'])
                print('\n'.join(f'{k}={v}' for k, v in location.items() if k not in ['url', 'slotDetails'] and v is not None))
                if distance is not None:
                    print(f'Distance from home: {distance.miles} miles')
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
    with tqdm() as pbar:
        #try:
        while not open_appointments(ns, geolocator):
            sleep(1)
            pbar.update(1)
        
        # optional - use case: wear your bluetooth headset and just walk away
        # play song if found
        if platform == "linux" or platform == "linux2":
            os.system('mpg123 ./startrek-tos-closing.aif')
        elif platform == "darwin":
            os.system('afplay ./startrek-tos-closing.aif')
            # elif platform == "win32":
                # Windows...i dont have windows to test this.
        # except:
        #     # optional
        #     # play song if error
        #     if platform == "linux" or platform == "linux2":
        #         os.system('mpg123 ./startrek-spock-illogical.aif')
        #     elif platform == "darwin":
        #         os.system('afplay ./startrek-spock-illogical.aif')
            # elif platform == "win32":
                # Windows...i dont have windows to test this.
