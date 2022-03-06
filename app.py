import time
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
import fake_useragent
# make chrome headless function


def chrome(headless=False):
    # add fake user agent
    chrome_options = Options()

    # return webdriver
    # support to get response status and headers
    d = webdriver.DesiredCapabilities.CHROME
    d['loggingPrefs'] = {'performance': 'ALL'}

    if headless:
        chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    # chrome_options.add_argument("user-agent={}".format(
    #     fake_useragent.UserAgent().random))
    chrome_options.add_experimental_option(
        'excludeSwitches', ['enable-logging'])
    chrome_options.add_argument("--disable-popup-blocking")
    driver = webdriver.Chrome(
        executable_path=r'i://clients//chromedriver.exe', options=chrome_options, desired_capabilities=d)
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


def clicking_next_button(driver):
    # click next button
    try:
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="pnnext"]/span[2]')))
        next_button.click()
        print("click next button")
    except TimeoutException:
        print("TimeoutException")
    except Exception as e:
        try:
            next_button = driver.element_by_link_text('Next')
            next_button.click()
            print("click next button")
        except Exception as e:
            print(e)


# driver.get('https://www.google.com/')
keywords = get_data('Keywords')
locations = get_data('Locations')
Pages = get_data('Pages')

driver = chrome()

driver.set_page_load_timeout(30)
driver.maximize_window()

driver.get('https://www.google.com/')
for keyword in keywords:
    for index in range(len(locations)):
        print("Location: " + str(locations[index]))
        print("Keyword: " + str(keyword))
        print("Pages: " + str(Pages[index]))

        if(str(keyword) == 'nan'):
            continue
        # if there is sorry keyword in current_url thhen wait for 10 seconds

        search_box = driver.find_element_by_name('q')
        # clear the search box
        search_box.clear()
        search_box.send_keys(
            "'"+str(keyword)+"'" + ' site:facebook.com/groups in ' + str(locations[index]))
        search_box.send_keys(Keys.RETURN)
        try:
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "search")))
            print("Page is ready!")
        except TimeoutException:
            print("Loading took too much time!")
        except Exception as e:
            print(e)

        def fill_captcha():
            if 'sorry' in str(driver.current_url):
                print("info : please try to fill the captcha")
                time.sleep(10)
                fill_captcha()
            else:
                pass
        fill_captcha()
        count = Pages[index]
        for i in range(count):
            scroll_down_page(40)
            # get page source
            page_source = driver.page_source
            # make soup
            soup = BeautifulSoup(page_source, 'html.parser')
            # get all the links in div with attribute id="search"
            search_links = soup.find('div', attrs={'id': 'search'})
            # extract the anchor tags from the links which are in div with class="yuRUbf"
            div_links = search_links.find_all('div', attrs={'class': 'yuRUbf'})
            # get anchor tags from div_links
            anchor_tags = [div_link.find('a') for div_link in div_links]

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
                    with open('groups.txt', 'a', encoding='UTF-8') as f:
                        f.write(group_name + '\n')
                        f.write(group_link + '\n')

            clicking_next_button(driver)


print("success: Done")
# driver.quit()
