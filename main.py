import os # to work with saving pictures and making folders
import time # for sleep time between download requests
import json # to convert file types
import requests # to sent GET requests
#import urllib.request # to download images
from bs4 import BeautifulSoup # to parse HTML

URL = 'http://prnt.sc/'

# used for identifying the type of search
usr_agent = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive',
}

# name of folder that the saved images are saved in 
SAVE_FOLDER_GLOBAL = 'images'

# verifys that the "images" folder exists and creates on if it doesn't.
def main():
    if not os.path.exists(SAVE_FOLDER_GLOBAL):
        os.mkdir(SAVE_FOLDER_GLOBAL)
    download_images()
    
def download_images():
    # introduction to program
    print('\nPRNT.SC SCRAPPER BOT - Coded by Tyler Bowers')
    print('\n - - Documentation - - ')
    print(' - Scraping can take a LONG time, be prepared to let this program run for awhile.')
    print(' - Time estimates: 100 photos = 1m; 1000 photos = 10m; 10000 photos = 1h40m ')
    print(' - Every prnt.sc link has a 6 digit extension, first followed by aa and then by 4 numbers.')
    print(' - Example: prnt.sc/aa0000; two letter extension: "aa"; four number extension: "0000".')
    print(' - Size estimates: 100 photos = 20MB; 1000 photos = 200MB; 10000 photos = 2GB')
    
    # user input
    print('\n - - User Input Area - - ')
    preextension = input('Two letter code extension: ')
    ros_lower = int(input('Lower bound range (min:0,max:9999) (default:0): ') or '0')
    ros_upper = int(input('Upper bound range (min:1,max:10000) (default:10000): ') or '10000')
    wait_time = float(input('Wait time between requests (seconds) (default:0.05): ') or '0.05')
    
    # make a folder with the two letter extension if it doesn't already exist
    if not os.path.exists(SAVE_FOLDER_GLOBAL + '/' + preextension):
        os.mkdir(SAVE_FOLDER_GLOBAL + '/' + preextension)
    SAVE_FOLDER = SAVE_FOLDER_GLOBAL + '/' + preextension
    
    # a for loop for the range provided
    for number in range(ros_lower, ros_upper):
        extension_full = preextension + ('{:0>4}'.format(str(number)))
        print('DOWNLOADING IMAGE: ' + extension_full)

        # get url query string
        searchurl = URL + extension_full
        #print("URL: " + searchurl)

        # requests url without usr_agent the permission gets denied
        response = requests.get(searchurl, headers=usr_agent)
        html = response.text
        
        # extract link from webpage
        soup = BeautifulSoup(html, 'html.parser')
        results = soup.findAll('img', {'class': 'no-click screenshot-image'})
        for link in results:
            imglink = (link['src'])
        filename = os.path.join(SAVE_FOLDER, extension_full + ".png")
        
        # checks to see if the image has been removed
        if imglink == '//st.prntscr.com/2021/04/08/1538/img/0_173a7b_211be8ff.png':
            result = 'null'
        else:
            # saves and downloads image 
            r = requests.get(imglink, allow_redirects=True)
            open(filename, 'wb').write(r.content)
            #urllib request - does not work with some links, if you are going to use it instead remember to uncomment "import urllib.request" from the beginning of the document.
            #urllib.request.urlretrieve(imglink, filename)
        
        # used to delay download requests (spreads load over time for both you and the webserver)
        time.sleep(wait_time)
    print(' - - Downloading Completed - - ')

if __name__ == '__main__':
    main()
