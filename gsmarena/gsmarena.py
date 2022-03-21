import time
import csv
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from pynput.keyboard import Key, Controller


opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36")

# gecko_path = '/home/tobia/Repos/Scraping/geckodriver'
# driver = webdriver.Firefox(executable_path=gecko_path)
driver = webdriver.Chrome('/home/tobia/Repos/randomstats/chromedriver', options=opts)
actions = ActionChains(driver)
keyboard = Controller()
driver.get('https://www.gsmarena.com/makers.php3')

time.sleep(4)

all_data_dict = {}

brands_list = driver.find_element_by_xpath("//div[@class='st-text']").find_elements_by_xpath('.//a')
brand_links = [brand.get_attribute('href') for brand in brands_list]
print(brand_links)
for brand_link in brand_links[89:]:
    time.sleep(2)
    while True:
        driver.get(brand_link)
        time.sleep(2)
        models = driver.find_element_by_xpath("//div[@class='makers']").find_elements_by_xpath(".//a")
        for model in models:
            time.sleep(2)
            tries = 0
            while tries < 2:
                try:
                    model_link = model.get_attribute('href')
                    model.send_keys(Keys.CONTROL + Keys.RETURN)
                    keyboard.press(Key.ctrl)
                    keyboard.press(Key.tab)
                    keyboard.release(Key.ctrl)
                    keyboard.release(Key.tab)
                    driver.switch_to.window(driver.window_handles[-1])
                    time.sleep(2)
                    phone_name = driver.find_element_by_xpath("//h1[@class='specs-phone-name-title']").text
                    print(phone_name)
                    if phone_name not in all_data_dict:
                        all_data_dict[phone_name] = {}
                    else:
                        continue
                    if 'Fujitsu Siemens' in phone_name or 'Sony Ericsson' in phone_name:
                        manufacturer = ' '.join(phone_name.split()[:1])
                        model = phone_name.replace(manufacturer, '').strip()
                    else:
                        manufacturer = phone_name.split()[0]
                        model = phone_name.replace(manufacturer, '').strip()
                    all_data_dict[phone_name]['manufacturer'] = manufacturer
                    all_data_dict[phone_name]['model'] = model
                    for spec in driver.find_elements_by_xpath("//td[@class='nfo']"):
                        spec_name = spec.get_attribute('data-spec')
                        spec_value = spec.text if spec.text else None
                        all_data_dict[phone_name][spec_name] = spec_value
                    keyboard.press(Key.ctrl)
                    keyboard.press('w')
                    keyboard.release(Key.ctrl)
                    keyboard.release('w')
                    driver.switch_to.window(driver.window_handles[0])
                    break
                except:
                    tries += 1
                    input('ERROR')
                    time.sleep(4)
        try:
            if 'disabled' not in driver.find_element_by_xpath("//a[@title='Next page']").get_attribute('class'):
                brand_link = 'https://www.gsmarena.com/' + driver.find_element_by_xpath("//a[@title='Next page']").get_attribute('href')
            else:
                break
        except:
            break
    with open('phones_dict_3.json', 'w') as f:
        json.dump(all_data_dict, f)




# import requests
# import time
# import pickle
# from bs4 import BeautifulSoup


# headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
# session = requests.Session()

# response = session.get('https://www.gsmarena.com/makers.php3')
# main_page = BeautifulSoup(response.content, 'html.parser')

# data_dict = {}

# for brand in main_page.find('div', class_='st-text').find_all('a'):
#     time.sleep(5)
#     print('\n' + 'https://www.gsmarena.com/' + brand.get('href') + '\n')
#     response_brand = session.get('https://www.gsmarena.com/' + brand.get('href'))
#     content_brand = BeautifulSoup(response_brand.content, 'html.parser')
#     while True:
#         for model in content_brand.find('div', class_='makers').find_all('a'):
#             time.sleep(5)
#             response_model = session.get('https://www.gsmarena.com/' + model.get('href'))
#             content_model = BeautifulSoup(response_model.content, 'html.parser')
#             model_name = content_model.find('h1', class_='specs-phone-name-title').text
#             print(model_name)
#             spec_list = []
#             for spec_group in content_model.find('div', id='specs-list').find_all('table'):
#                 for spec in spec_group.find_all('tr'):
#                     try:
#                         spec_name = spec.find('td', class_='nfo').get('data-spec')
#                         spec_value = spec.find('td', class_='nfo').text.replace('\n', ';')
#                         spec_list.append((spec_name, spec_value))
#                     except:
#                         print(spec.text)
#             if model_name not in data_dict:
#                 data_dict[model_name] = spec_list
#         if content_brand.find('a', class_='pages-next').get('href') != '#1':
#             response_brand = session.get('https://www.gsmarena.com/' + content_brand.find('a', class_='pages-next').get('href'))
#             content_brand = BeautifulSoup(response_brand.content, 'html.parser')
#         else:
#             break

#     with open('gsmarena.p', 'wb') as f:
#         pickle.dump(data_dict, f)
