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
        self.__login()

    def __init_webdriver(self, config):
        options = webdriver.ChromeOptions()

        options.add_argument("--disable-gpu")
        if config['webdriver']['headless'] == 'True':
            options.add_argument('headless')
        options.add_argument('no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        print(config['path']['webdriver'])
        driver = webdriver.Chrome(config['path']['webdriver'], options=options)
        driver.implicitly_wait(int(self.config['webdriver']['timeout']))
        return driver

    def __login(self):
        url_login = self.config['url']['root'] + self.config['url']['login']
        self.driver.get(url_login)
        self.driver.find_element_by_id('user_id').send_keys(self.config['login']['id'])
        self.driver.find_element_by_id('password').send_keys(self.config['login']['password'])
        self.driver.execute_script("login()")


    def get_webdriver(self):
        return self.driver

    def __get_filtered_coupon_list(self):
        with open(self.config['path']['funcoupon'], 'r') as file:
            coupones = ["".join(s.split()[2].split('-'))
                        for s in filter(lambda x: x.count('-') == 3, file.readlines())]
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
            print(coupon)
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
        num_happy = int(self.config['happy']['num_happy'])
        price = int(self.config['happy']['price']) * num_happy

        for i in range(try_count):
            self.driver.get(url_shop3)

            try:
                href_list = self.driver.find_elements_by_xpath("//a[@href]")
                happy_url_list = [s.get_attribute("href") for s in href_list if self.config['url']['item'] in s.get_attribute("href")]

                if len(happy_url_list) > 0:
                    self.driver.get(happy_url_list[0])
                    for j in range(try_count):
                        print('today happy URL : %s' % happy_url_list[0])

                        self.driver.execute_script("order_count_change(%d, true)" % num_happy)
                        self.driver.execute_script("document.getElementById('check_info').checked = true")
                        self.driver.execute_script("document.getElementById('check_warn').checked = true")
                        self.driver.execute_script("document.getElementById('checkAll').checked = true")
                        self.driver.execute_script("$('#use_point').val('%d')" % price)
                        self.driver.execute_script("$('#use_point').blur()")
                        self.driver.execute_script("click_card_btn()")
                        self.driver.execute_script("click_pay()")

                        print('success to buy : %s' % str(j+1))

                        sleep(sleep_sec)

                        self.driver.get(happy_url_list[0])

                    self.driver.quit()
                    break
                else:
                    print("Item is not opened!!")
            except Exception:
                print("unexpected error!!")
            sleep(sleep_sec)
