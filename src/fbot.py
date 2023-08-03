from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import time

options = FirefoxOptions()
#options.add_argument("--headless")

class FacebookBot:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.bot = webdriver.Firefox(executable_path='/Users/hamid/Downloads/Programs/geckodriver.exe', service_args = ['--marionette-port', '2828', '--connect-existing'])
        self.bot.set_window_position(0, 0) 
        self.bot.set_window_size(960, 1080)
    
    def login(self):
        bot = self.bot
        bot.get("https://www.facebook.com/")
        time.sleep(1)
        
        bot.find_element_by_xpath('//*[@id="email"]').send_keys(self.username)
        bot.find_element_by_xpath('//*[@id="pass"]').send_keys(self.password)
        time.sleep(1)
        
        bot.find_element_by_xpath('//*[@id="pass"]').send_keys(Keys.RETURN)
        time.sleep(5)

    def crawl(self, number_of_posts):
        bot = self.bot

        bot.get('https://www.facebook.com/hamidur.rk')
        time.sleep(4)



fb = FacebookBot('hamidur.rk', 'WhyS0SEr10us?')

# fb.login()
fb.crawl(1)
