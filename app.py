from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd

# make chrome headless function


def chrome(headless=False):
    # support to get response status and headers
    d = webdriver.DesiredCapabilities.CHROME
    d['loggingPrefs'] = {'performance': 'ALL'}
    opt = webdriver.ChromeOptions()
    if headless:
        opt.add_argument("--headless")
    opt.add_experimental_option('excludeSwitches', ['enable-logging'])
    opt.add_argument("--disable-popup-blocking")
    driver = webdriver.Chrome(
        executable_path=r'i://clients//chromedriver.exe', options=opt, desired_capabilities=d)
    driver.implicitly_wait(10)
    driver.maximize_window()
    return driver


# get excel data from data.xlsx
def get_data(col_name):
    df = pd.read_excel('data.xlsx', sheet_name='Sheet1')
    return df[col_name]

# driver = chrome()

# This function iteratively clicks on the "Next" button at the bottom right of the search page.


def scroll_down_page(speed=8):
    current_scroll_position, new_height = 0, 1
    while current_scroll_position <= new_height:
        current_scroll_position += speed
        driver.execute_script(
            "window.scrollTo(0, {});".format(current_scroll_position))
        new_height = driver.execute_script(
            "return document.body.scrollHeight")


# driver.get('https://www.google.com/')
keywords = get_data('Keywords')
locations = get_data('Locations')

driver = chrome()

driver.set_page_load_timeout(30)
driver.maximize_window()

driver.get('https://www.google.com/')
for keyword in keywords:
    for location in locations:
        print("Location: " + str(location))
        print("Keyword: " + str(keyword))

        if(str(keyword) == 'nan'):
            continue
        search_box = driver.find_element_by_name('q')
        # clear the search box
        search_box.clear()
        search_box.send_keys(
            "'"+str(keyword)+"'" + ' site:facebook.com/groups in ' + str(location))
        search_box.send_keys(Keys.RETURN)
        try:
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "search")))
            print("Page is ready!")
        except TimeoutException:
            print("Loading took too much time!")
        except Exception as e:
            print(e)
        scroll_down_page(40)
        # get page source
        page_source = driver.page_source
        # make soup
        soup = BeautifulSoup(page_source, 'html.parser')
        # get all the links in div with attribute id="search"
        search_links = soup.find_all('div', attrs={'id': 'search'})
        # extract the anchor tags from the links which are in div with class="yuRUbf"
        div_links = search_.find_all('div', attrs={'class': 'yuRUbf'})
        # get anchor tags from div_links
        anchor_tags = [div_link.find_all('a') for div_link in div_links]

        # iterate over the anchor tags
        for tag in anchor_tags:
            # get the href attribute
            href = tag.get('href')
            # check if the href attribute is a facebook group
            if 'facebook.com/groups' in href:
                # get the group name
                group_name = tag.text
                # get the group link
                group_link = tag.get('href')
                # print the group name and link
                print(group_name)
                print(group_link)
                # write the group name and link to a file
                with open('groups.txt', 'a') as f:
                    f.write(group_name + '\n')
                    f.write(group_link + '\n')


print("success: Done")
# driver.quit()
