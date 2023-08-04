from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.action_chains import ActionChains
import time, re, json

options = FirefoxOptions()
#options.add_argument("--headless")

def int_from_string(input_string):
    integers = re.findall(r'\d+', input_string)
    if not integers:
        return None
    extracted_int = int(integers[0])
    return extracted_int

def gen_prompt(message, value = 70, char="-"):
    print("\n")
    wrt = " " + message + " "
    print(wrt.center(value, char))
    print("\n")

class FacebookBot:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.bot = webdriver.Firefox(executable_path='/Users/hamid/Downloads/Programs/geckodriver.exe', service_args = ['--marionette-port', '2828', '--connect-existing'])
        self.bot.set_window_position(0, 0) 
        self.bot.set_window_size(960, 1080)
        gen_prompt("Bot initialized", char="#")
        print("\n")
    
    def login(self):
        bot = self.bot
        bot.get("https://www.facebook.com/")
        time.sleep(1)
        gen_prompt("Navigated to Facebook", char="#")

        bot.find_element_by_xpath('//*[@id="email"]').send_keys(self.username)
        gen_prompt("Username Entered")
        bot.find_element_by_xpath('//*[@id="pass"]').send_keys(self.password)
        gen_prompt("Password Entered")
        time.sleep(1)
        
        bot.find_element_by_xpath('//*[@id="pass"]').send_keys(Keys.RETURN)
        time.sleep(5)
        gen_prompt("Login Requested")
        print("\n"*4)

    def crawl(self, number_of_posts):
        bot = self.bot

        bot.get('https://www.facebook.com/' + self.username)
        time.sleep(4)
        gen_prompt("Navigated to " + self.username, char="#")
        
        bot.find_element_by_id("facebook").click()
        with open("friends.txt", 'r', encoding='utf-8') as f:
            memory_list = json.loads(f.read())
        print(f"{len(memory_list)} people already exists in the database.")
        gen_prompt("Starting the search for new people",value=100, char="#")

        total_new = 0
        for i in range(number_of_posts):
            i += 1
            c = ActionChains(bot)
            c.send_keys(Keys.PAGE_DOWN).perform()
            time.sleep(0.5)
            wrt = "Post no: " + str(i) + " "
            print(wrt.center(70, "-"))
            react_bar_str = f"/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div[4]/div[2]/div/div[2]/div[3]/div[2]/div[{i+1}]/div/div/div/div/div/div/div/div/div/div/div[8]/div/div/div[4]/div/div/div[1]/div/div[1]/div/div[1]/div/span/div/span[2]/span/span"
            info = bot.find_element_by_xpath(react_bar_str).text
            time.sleep(1.5)
            
            reacts = int_from_string(info) + 2
            if (reacts != None):
                print ("\nReacts: "+ str(reacts))
                try:
                    id_list = []
                    bot.find_element_by_xpath(react_bar_str).click()
                    time.sleep(2)

                    react_box = "/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[2]/div[2]/div[3]/div"
                    x = []
                    obj = bot.find_elements_by_xpath("//div[@class='x1rg5ohu']")
                    if (reacts >= 10):
                        countList = []
                        while True:
                            obj = bot.find_elements_by_xpath("//div[@class='x1rg5ohu']")
                            for elements in obj:
                                x.append(elements.text)
                            scroll_element = bot.find_element_by_xpath(react_box)
                            bot.execute_script(f"arguments[0].scrollTop += {200};", scroll_element)
                            time.sleep(0.5)
                            count = len(x)
                            countList.append(count)
                            counter = countList.count(count)

                            if ((len(x) == reacts) or counter >= 8):
                                break
                            x.clear()

                    for elements in obj:
                        id = elements.text
                        id_list.append(id)  
                        print("\t" + id)

                    joint_list = memory_list + id_list
                    main_list = list(dict.fromkeys(joint_list))
                    new = len(main_list) - len(memory_list)
                    print("\n" + "New added: " + str(new))
                    total_new += new
                    with open("friends.txt", 'w', encoding='utf-8') as f:
                        f.write(json.dumps(main_list))

                    with open("friends.txt", 'r', encoding='utf-8') as f:
                        memory_list = json.loads(f.read())

                    time.sleep(0.5)

                    bot.find_element_by_xpath("//div[@aria-label= 'Close'and @role='button']").click()
                    time.sleep(0.5)

                
                except Exception as e:
                    print("An error occurred: ", str(e))
                    pass
        gen_prompt("Crawl ended", char="#")
        print("\n"*4)
        gen_prompt("Summary")
        print(f"Number of new entries to the database: {total_new}")
        print(f"Size of database: {len(memory_list)}")
        print("\n"*4)



fb = FacebookBot('hamidur.rk', 'WhyS0SEr10us?')

# fb.login()
fb.crawl(10)
