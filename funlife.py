#!/Users/a1/anaconda3/bin/python

import sys
import configparser
from time import sleep

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class Funlife:
    def __init__(self, config):
        self.config = config
        self.driver = self.__init_webdriver(config)
        self.__login(config, self.driver)

    def __init_webdriver(self, config):
        options = webdriver.ChromeOptions()
        if config['webdriver']['headless'] == 'True':
            options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument("disable-gpu")
        print(config['path']['webdriver'])
        return webdriver.Chrome(config['path']['webdriver'], options=options)

    def __login(self, config, driver):
        url_login = config['url']['root'] + config['url']['login']
        driver.get(url_login)
        driver.find_element_by_id('user_id').send_keys(config['login']['id'])
        driver.find_element_by_id('password').send_keys(config['login']['password'])
        driver.execute_script("login()")

    def get_webdriver(self):
        return self.driver

    def __get_filtered_coupon_list(self):
        with open(self.config['path']['funcoupon'], 'r') as file:
            filter_coupon = self.config['funcoupon']['filter_coupon']
            coupones = ["".join(s.split()[2].split('-'))
                        for s in filter(lambda x: x.startswith(filter_coupon), file.readlines())]
        return coupones

    def register_coupon(self):
        sleep(0.5)
        url_coupon = self.config['url']['root'] + self.config['url']['coupon']
        self.driver.get(url_coupon)
        popopup_delay = int(self.config['funcoupon']['popup_delay'])

        coupon_list = self.__get_filtered_coupon_list()
        print("coupon num : %d" % len(coupon_list))

        cnt_coupon = 0

        for coupon in coupon_list:
            self.driver.execute_script("document.getElementById('coupon_id').value = '%s'" % coupon)
            self.driver.execute_script("regCoupon()")
            WebDriverWait(self.driver, popopup_delay).until(EC.alert_is_present(),
                                                            'Timed out waiting for PA creation ' +
                                                            'confirmation popup to appear.')
            self.driver.switch_to.alert.accept()
            WebDriverWait(self.driver, popopup_delay).until(EC.alert_is_present(),
                                                            'Timed out waiting for PA creation ' +
                                                            'confirmation popup to appear.')
            self.driver.switch_to.alert.accept()
            cnt_coupon += 1

        print("used coupon num : %d" % cnt_coupon)

    def buy_happy(self):
        try_count = int(self.config['happy']['try_count'])
        url_shop3 = "%s%s" % (self.config['url']['root'], self.config['url']['shop3'])
        sleep_sec = float(self.config['happy']['sleep_sec'])
        order_count_up = int(self.config['happy']['num_happy']) - 1
        price = int(self.config['happy']['price']) * (order_count_up + 1)

        for i in range(try_count):
            self.driver.get(url_shop3)
            href_list = self.driver.find_elements_by_xpath("//a[@href]")
            happy_url_list = [s.get_attribute("href") for s in href_list if self.config['url']['item'] in s.get_attribute("href")]

            if len(happy_url_list) > 0:
                for j in range(try_count):
                    print('today happy URL : %s' % happy_url_list[0])
                    self.driver.get(happy_url_list[0])
                    self.driver.execute_script("order_count_change(%d, false)" % order_count_up)
                    self.driver.execute_script("document.getElementById('check_info').checked = true")
                    self.driver.execute_script("document.getElementById('check_warn').checked = true")
                    self.driver.execute_script("document.getElementById('checkAll').checked = true")
                    self.driver.execute_script("document.getElementById('use_point').value = %d" % price )
                    self.driver.execute_script("click_card_btn()")
                    self.driver.execute_script("click_pay()")
                    print('success to buy : %s' % str(j+1))
                    sleep(sleep_sec)
                self.driver.quit()
                break
            else:
                print("Item is not opened!!")
            sleep(sleep_sec)


        '''
        url_item = self.config['url']['root'] + self.config['url']['item']

        url_happy_list = list(map(str, self.config['url']['happy_list'].split(',')))
        len_url_happy_list = len(url_happy_list)

        try_count = int(self.config['happy']['try_count'])
        order_count_up = int(self.config['happy']['num_happy']) - 1
        popup_delay = int(self.config['happy']['popup_delay'])

        for i in range(try_count):
            sleep(0.5)
            url_happy = url_item + '/' + url_happy_list[i % len_url_happy_list]
            self.driver.get(url_happy)

            try:
                WebDriverWait(self.driver, popup_delay).until(EC.alert_is_present(),
                                                   'Timed out waiting for PA creation ' +
                                                   'confirmation popup to appear.')
                self.driver.switch_to.alert.accept()
            except Exception:
                print('today happy URL : %s' % url_happy)
                self.driver.execute_script("order_count_change(%s, false)" % order_count_up)
                self.driver.execute_script("document.getElementById('check_info').checked = true")
                self.driver.execute_script("document.getElementById('check_warn').checked = true")
                self.driver.execute_script("document.getElementById('checkAll').checked = true")
                self.driver.execute_script("click_use_total_point()")
                self.driver.execute_script("click_card_btn()")
                self.driver.execute_script("click_pay()")
                self.driver.quit()
                print('success to buy')
                break
        '''


'''
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
'''