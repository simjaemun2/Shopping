#!/Users/a1/anaconda3/bin/python

import sys
import configparser
from time import sleep

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


if len(sys.argv) < 2:
    print("There is no path of config!!")
    exit(1)

path_config = sys.argv[1]
config = configparser.ConfigParser()
config.read(path_config)
config = config['funlife']

order_count_up = int(config['num_of_happy']) - 1

#num of click to buy happy
if len(sys.argv) > 3:
    order_count_up = sys.argv[2] - 1

print("order_count_up : %s\n" % order_count_up)

url_root = config['url_root']
url_login = url_root + config['url_login']
url_item = url_root + config['url_item']
url_happy_list = list(map(str, config['url_happy_list'].split(',')))

path_webdriver = config['path_webdriver']

#login
options = webdriver.ChromeOptions()
#options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")

driver = webdriver.Chrome(path_webdriver, options=options)
driver.get(url_login)
driver.find_element_by_id('user_id').send_keys(config['id'])
driver.find_element_by_id('password').send_keys(config['password'])
driver.execute_script("login()")

#try to buy happy money
try_num = 1000
delay = 10
len_url_happy_list = len(url_happy_list)

for i in range(try_num):
    sleep(0.5)
    url_happy = url_item + '/' + url_happy_list[i % len_url_happy_list]
    driver.get(url_happy)

    try:
        WebDriverWait(driver, delay).until(EC.alert_is_present(),
                                           'Timed out waiting for PA creation ' +
                                           'confirmation popup to appear.')
        driver.switch_to.alert.accept()
    except Exception:
        print('today happy URL : %s' % url_happy)
        driver.execute_script("order_count_change(%s, false)" % order_count_up)
        driver.execute_script("document.getElementById('check_info').checked = true")
        driver.execute_script("document.getElementById('check_warn').checked = true")
        driver.execute_script("document.getElementById('checkAll').checked = true")
        driver.execute_script("click_use_total_point()")
        driver.execute_script("click_card_btn()")
        driver.execute_script("click_pay()")
        driver.quit()
        print('success to buy')
        break
