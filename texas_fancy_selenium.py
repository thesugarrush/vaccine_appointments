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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.keys import Keys

import os
from sys import platform
from datetime import datetime

from decimal import *

from enum import Enum

store_name_to_distance = {}

# VERY IMPORTANT -- to work around blocking of selenium script
option = webdriver.ChromeOptions()
option.add_argument('--disable-blink-features=AutomationControlled')
driver = webdriver.Chrome(executable_path='./chromedriver',options=option)
# driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

# whether to play music in the end of SUCESSFUL search (or not)
bool_play_sound = True;


#vaccines_i_want = ['Pfizer', 'Moderna'] # specify your desired vaccine here
vaccines_i_want = ['Pfizer'] # specify your desired vaccine here


# class distance(Enum):
#     LEFT = "left"
#     RIGHT = "right"
#     UP = "up"
#     DOWN = "down"



def open_appointments(namespace, main_window):
    
    success = False
    
    #example: distance_sting = "177.9 miles from search area"
    distance_string = driver.find_element_by_xpath("/html/body/div[@id='root']/div[@class='sc-kstrdz khymNb']/div[@class='sc-bdfBwQ sc-bkzZxe iXgbQJ dHUsHE']/div[@class='sc-bdfBwQ sc-hBEYos iXgbQJ gBMEYn']/ul[@class='sc-fFubgz khwWvu']/li[@class='sc-iBPRYJ uDpEv'][1]/p[@class='sc-gsTCUz evtGGn']").text
    distance = distance_string.split( ) # i just want the 177.9

    # exit this function when the distance is too far
    if Decimal(distance[0]) > Decimal(ns.distance):
        print(f"ignoring venue - TOO FAR AWAY! distance is: {distance[0]}")
        return success

    vaccine_string = driver.find_element_by_xpath("/html/body/div[@id='root']/div[@class='sc-kstrdz khymNb']/div[@class='sc-bdfBwQ sc-bkzZxe iXgbQJ dHUsHE']/div[@class='sc-bdfBwQ sc-hBEYos iXgbQJ gBMEYn']/ul[@class='sc-fFubgz khwWvu']/li[@class='sc-iBPRYJ uDpEv'][1]/div[1]/p[@class='sc-gsTCUz jzOQjz']").text
    print (f"vaccine_string: {vaccine_string}")
    # TO DO: NEED TO BE parameterized
    # exit this function when there is no distance
    if vaccine_string not in vaccines_i_want:
        print(f"ignoring vaccines because it is not in the list of vaccines i want")
        return success

    #driver.implicitly_wait(1) # seconds

    # Get All Tabs or Window handles and iterate using for each loop. The auto-open should have opened a new tab
    handles = driver.window_handles
    for ii, hh in enumerate( handles ):
        if hh != main_window: 
            driver.switch_to.window(hh)
            #print(f"window {ii} has title {driver.title}")

    #driver.find_element_by_xpath("/html/body/div[@id='root']/div[@class='sc-kstrdz khymNb']/div[@class='sc-bdfBwQ sc-bkzZxe iXgbQJ dHUsHE']/div[@class='sc-bdfBwQ sc-hBEYos iXgbQJ gBMEYn']/ul[@class='sc-fFubgz khwWvu']/li[@class='sc-iBPRYJ uDpEv']/div[@class='sc-bdfBwQ kjxcKy']/a[@class='sc-hKgILt sc-fubCfw kRsWTW iOrfxa']").click()

    print(f"found a venue {distance_string}, trying to get time slot")

    driver.implicitly_wait(3.0) # seconds

    # try 3 times before giving up, each with interval backing
    # ..also try 3 timeslots
    i = 0
    while i < 4:
        i = i + 1
        try:
            driver.find_element_by_xpath("/html/body/span[@id='j_id0:j_id18']/div[@id='container']/c-f-s-registration/div[@class='page-container']/div[1]/div[@class='slds-m-bottom_medium'][3]/lightning-card/article[@class='slds-card']/div[@class='slds-card__body']/slot/div[@class='slds-m-around_medium']/form/div[@class='slds-p-around_medium form']/lightning-combobox[@class='slds-form-element']/div[@class='slds-form-element__control']/lightning-base-combobox[@class='slds-combobox_container']/div[@class='slds-combobox slds-dropdown-trigger slds-dropdown-trigger_click']/div[@class='slds-combobox__form-element slds-input-has-icon slds-input-has-icon_right']/input[@id='input-14']").click()
            
            driver.find_element_by_xpath("/html/body/span[@id='j_id0:j_id18']/div[@id='container']/c-f-s-registration/div[@class='page-container']/div[1]/div[@class='slds-m-bottom_medium'][3]/lightning-card/article[@class='slds-card']/div[@class='slds-card__body']/slot/div[@class='slds-m-around_medium']/form/div[@class='slds-p-around_medium form']/lightning-combobox[@class='slds-form-element'][2]/div[@class='slds-form-element__control']/lightning-base-combobox[@class='slds-combobox_container']/div[@class='slds-combobox slds-dropdown-trigger slds-dropdown-trigger_click slds-is-open']/div[@id='dropdown-element-14']/lightning-base-combobox-item[@id='input-14-0-14']/span[@class='slds-media__body']").click()

            driver.find_element_by_xpath("/html/body/span[@id='j_id0:j_id18']/div[@id='container']/c-f-s-registration/div[@class='page-container']/div[1]/div[@class='slds-m-bottom_medium'][3]/lightning-card/article[@class='slds-card']/div[@class='slds-card__body']/slot/div[@class='slds-m-around_medium']/form/div[@class='slds-p-around_medium form']/lightning-combobox[@class='slds-form-element'][3]/div[@class='slds-form-element__control']/lightning-base-combobox[@class='slds-combobox_container']/div[@class='slds-combobox slds-dropdown-trigger slds-dropdown-trigger_click']/div[@class='slds-combobox__form-element slds-input-has-icon slds-input-has-icon_right']/input[@id='input-18']").click()
            
            #driver.find_element_by_xpath("/html/body/span[@id='j_id0:j_id18']/div[@id='container']/c-f-s-registration/div[@class='page-container']/div[1]/div[@class='slds-m-bottom_medium'][3]/lightning-card/article[@class='slds-card']/div[@class='slds-card__body']/slot/div[@class='slds-m-around_medium']/form/div[@class='slds-p-around_medium form']/lightning-combobox[@class='slds-form-element'][3]/div[@class='slds-form-element__control']/lightning-base-combobox[@class='slds-combobox_container']/div[@class='slds-combobox slds-dropdown-trigger slds-dropdown-trigger_click slds-is-open']/div[@id='dropdown-element-18']/lightning-base-combobox-item[@id='input-18-0-18']/span[@class='slds-media__body']").click()

            tm_slot = 0
            while tm_slot < 4:
                tm_slot = tm_slot + 1
                try:
                    driver.find_element_by_xpath(f"/html/body/span[@id='j_id0:j_id18']/div[@id='container']/c-f-s-registration/div[@class='page-container']/div[1]/div[@class='slds-m-bottom_medium'][3]/lightning-card/article[@class='slds-card']/div[@class='slds-card__body']/slot/div[@class='slds-m-around_medium']/form/div[@class='slds-p-around_medium form']/lightning-combobox[@class='slds-form-element'][3]/div[@class='slds-form-element__control']/lightning-base-combobox[@class='slds-combobox_container']/div[@class='slds-combobox slds-dropdown-trigger slds-dropdown-trigger_click slds-is-open']/div[@id='dropdown-element-18']/lightning-base-combobox-item[@id='input-18-{tm_slot-1}-18']/span[@class='slds-media__body']").click()
                    break
                except:
                    continue

            #testing only
            driver.implicitly_wait(15.0) # seconds
    
            driver.find_element_by_xpath("/html/body/span[@id='j_id0:j_id18']/div[@id='container']/c-f-s-registration/div[@class='page-container']/div[1]/div[@class='slds-text-align_right margin-bottom']/lightning-button[@class='slds-m-left_x-small']/button[@class='slds-button slds-button_success']").click()

            # to do: check if the next page load properly i.e. do i got appoinment time?, if yes, then sound on
            driver.implicitly_wait(5.0) # seconds
            try:
                appoinment_details = driver.find_element_by_xpath("/html/body/span[@id='j_id0:j_id18']/div[@id='container']/c-f-s-registration/div[@class='page-container']/div[1]/lightning-card/article[@class='slds-card']/div[@class='slds-card__header slds-grid']/header[@class='slds-media slds-media_center slds-has-flexi-truncate']/div[@class='slds-media__body']/h2[@class='slds-card__header-title']").text

                if appoinment_details == 'Appointment Details':
                    success = True
                    break
                else:
                    # same #1
                    # switch to main window again, false alarm! but close the window that is false alarm
                    handles = driver.window_handles
                    for ii, hh in enumerate( handles ):
                        if hh != main_window:
                            driver.switch_to.window(hh)
                            print(f"false alarm URL: {driver.current_url}")
                            driver.close()
                    driver.switch_to.window(main_window)
                    continue
            except:
                # same #1
                # switch to main window again, false alarm! but close the window that is false alarm
                handles = driver.window_handles
                for ii, hh in enumerate( handles ):
                    if hh != main_window:
                        driver.switch_to.window(hh)
                        print(f"exception - false alarm URL: {driver.current_url}")
                        driver.close()
                driver.switch_to.window(main_window)
                continue

        except:
            driver.implicitly_wait(1) # seconds
            continue
            
    return success




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Program to ping HEB for vaccine appointments in your area")
    parser.add_argument('-z', '--zipcode', 
                    help='Zipcodes to restrict the search to')
    parser.add_argument('-d', '--distance',
                    help='Maximum distance (in miles) from zip code, value must match HEB spec: 5, 10, 25, 50, 100, 200')

    ns = parser.parse_args(sys.argv[1:])

    assert (ns.distance is None) == (ns.zipcode is None), 'zipcode and distance should be supplied together'
    
    print(f"distance: {str(ns.distance)}")

    # load the main page
    driver.get(f"https://vaccine.heb.com/scheduler?q={ns.zipcode}")

    #save current window handle
    main_window = driver.current_window_handle

    #click the autoopen and select it
    driver.implicitly_wait(5)
    driver.find_element_by_xpath("/html/body/div[@id='root']/div[@class='sc-kstrdz khymNb']/div[@class='sc-bdfBwQ sc-bkzZxe iXgbQJ dHUsHE']/div[@class='sc-bdfBwQ sc-hBEYos iXgbQJ gBMEYn']/div[@class='sc-bdfBwQ gNchlM']/div[@class='sc-bqyKva ehfErK']/div[@class='sc-bdfBwQ iXgbQJ']/label[1]/input[@id='autoopen']").click()
    
    # select radius and select it
    el = driver.find_element_by_xpath("/html/body/div[@id='root']/div[@class='sc-kstrdz khymNb']/div[@class='sc-bdfBwQ sc-bkzZxe iXgbQJ dHUsHE']/div[@class='sc-bdfBwQ sc-hBEYos iXgbQJ gBMEYn']/div[@class='sc-bdfBwQ gNchlM']/div[@class='sc-bqyKva ehfErK']/div[@class='sc-bdfBwQ iXgbQJ']/label[2]/select[@id='autoradius']")
    for option in el.find_elements_by_tag_name('option'):
        if option.text == ns.distance:
            option.click() # select() in earlier versions of webdriver
            break

    # select vaccine and select it
    el = driver.find_element_by_xpath("/html/body/div[@id='root']/div[@class='sc-kstrdz khymNb']/div[@class='sc-bdfBwQ sc-bkzZxe iXgbQJ dHUsHE']/div[@class='sc-bdfBwQ sc-hBEYos iXgbQJ gBMEYn']/div[@class='sc-bdfBwQ gNchlM']/div[@class='sc-bqyKva ehfErK']/div[@class='sc-bdfBwQ iXgbQJ']/label[3]/select[@id='automanufacturer']")
    for option in el.find_elements_by_tag_name('option'):
        if option.text == 'Any':
            option.click() # select() in earlier versions of webdriver
            break


    # we want to keep trying if there is an exception/error when trying to get an appointment in step 2
    # for example: if we are competing with other BOT as well.
    while True:
        
        with tqdm() as pbar:
            try:
                while not open_appointments(ns, main_window):
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
                print("Error:", sys.exc_info()[0])
                # if bool_play_sound:
                #     # optional - play song if error
                #     if platform == "linux" or platform == "linux2":
                #         os.system('mpg123 ./startrek-spock-illogical.aif')
                #     elif platform == "darwin":
                #         os.system('afplay ./startrek-spock-illogical.aif')
                    # elif platform == "win32":
                        # Windows...i dont have windows to test this.
                
                sleep(2)

                # switch to main window again
                handles = driver.window_handles
                for ii, hh in enumerate( handles ):
                    if hh != main_window:
                        driver.switch_to.window(hh)
                        print(f"tried this URL: {driver.current_url}")
                        driver.close()
                
                driver.switch_to.window(main_window)

                # break # debuging
                continue # continue looping
            
            break
            