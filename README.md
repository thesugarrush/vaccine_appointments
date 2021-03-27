# Vaccine Appointments
Automatically searching for vaccine appointments

Thanks to the original repo that I forked from: https://github.com/TheIronicCurtain/vaccine_appointments

I made the improvement to bypass step-2 of the appointment process so it will choose the first available apointment i.e. first available date and first available time slot in that day. 
In order to simulate the presence of a live human to do step 2, i use the infamous Selenium WebDriver tools used for testing/QA of web applications. 
Read more about it here: https://www.selenium.dev/projects/

# Usage

To copy this package, run:

`git clone https://github.com/thesugarrush/vaccine_appointments.git`

## 1. Install conda

I use conda to manage my environment so pip is not dirtying-up other python projects that also use python. This is slightly different from the original author. I, however, kept the requirements.txt and wrap it with the conda environment.
How to install conda: https://conda.io/projects/conda/en/latest/user-guide/install/index.html. 

All you need to do to install the required packages is navigate to the repository and run the following line in the command line (assuming you have Python installed):
`conda env create -f environment.yml`



## 2. (OPTIONAL) Download your selenium web-driver if you are NOT using chrome as your browser

I assume you use <b>'CHROME'  version 89.x</b> as your browser i.e. you have it installed on your machine. You welcome to fork this repo if you need to make the Selenium WebDriver work for other browser.

Download the webdriver config for your browser here: 

Chrome:	https://sites.google.com/a/chromium.org/chromedriver/downloads
Edge:	https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/
Firefox:	https://github.com/mozilla/geckodriver/releases
Safari:	https://webkit.org/blog/6900/webdriver-support-in-safari-10/

Put the file in the root folder of this source code, and make sure you change the path in the texas_fancy_selenium.py file.

`driver = webdriver.Chrome('<RELATIVE_PATH/DRIVER_FILE_FOR_YOUR_BROWSER>')`



## 3. Run your python

Run `python texas_fancy_selenium.py --help` for usage:

```
usage: texas_fancy_selenium.py [-h] [-c CITIES [CITIES ...]] [-H HOME] [-d DISTANCE] [-Z ZIPCODES [ZIPCODES ...]]

Program to ping HEB for vaccine appointments in your area

optional arguments:
  -h, --help            show this help message and exit
  -c CITIES [CITIES ...], --cities CITIES [CITIES ...]
                        Cities to restrict the search to
  -H HOME, --home HOME  Home location: can be in the form of a zipcode, address, latitude/longitude, city, etc. (requires distance)
  -d DISTANCE, --distance DISTANCE
                        Maximum distance (in miles) from home (requires home)
  -Z ZIPCODES [ZIPCODES ...], --zipcodes ZIPCODES [ZIPCODES ...]
                        Zipcodes to restrict the search to

```
Examples:

 - `python texas_fancy_selenium.py -c "San Antonio" Jourdanton Pleasanton Leming Poteet` would do the same as the simple example
 - `python texas_fancy_selenium.py -H "San Antonio, TX" -d 50` would look for appointments 50 miles from San Antonio
 - `python texas_fancy_selenium.py -H 78023 -d 30` would look for appointments 30 miles from zip code 78023
 - `python texas_fancy_selenium.py -z 76028 75165` would look for appointments only in the zip codes 76028 and 75165