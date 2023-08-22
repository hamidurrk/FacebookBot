from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.action_chains import ActionChains
from tqdm import tqdm
import time, re, json, sys

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

def wait(duration):
    num_iterations = 100
    time_interval = (duration-1) / num_iterations

    with tqdm(total=num_iterations, desc="Loading", unit="iteration", ncols=100) as pbar:
        for _ in range(num_iterations):
            time.sleep(time_interval)
            pbar.update(1)
    print("\n")

def loading(i, total):
    progress = (i / total) * 100
    sys.stdout.write('\r')
    sys.stdout.write("Scrolling: | %-50s | %0.2f%%" % ('█' * int(progress/2), progress))
    sys.stdout.flush()

class FacebookBot:
    def __init__(self, username, password, browser_type=0):
        self.username = username
        self.password = password
        if (browser_type):
            self.bot = webdriver.Firefox(executable_path='/Users/hamid/Downloads/Programs/geckodriver.exe', service_args = ['--marionette-port', '2828', '--connect-existing'])
        else:
            self.bot = webdriver.Firefox(executable_path='/Users/hamid/Downloads/Programs/geckodriver.exe', options=options)
        self.bot.set_window_position(0, 0) 
        self.bot.set_window_size(960, 1043)
        gen_prompt("Bot initialized", char="#")
        print("\n")
    
    def highlight_element(self, element, color='yellow', delay=0.1):
        bot = self.bot
        unfriend_button_element = bot.find_element_by_xpath(element)
        highlight_script = f"arguments[0].style.backgroundColor = '{color}';"
        bot.execute_script(highlight_script, unfriend_button_element)

        time.sleep(delay)  
        remove_highlight_script = "arguments[0].style.backgroundColor = '';"
        bot.execute_script(remove_highlight_script, unfriend_button_element)

    def login(self):
        bot = self.bot
        bot.get("https://www.facebook.com/")
        time.sleep(1)
        gen_prompt("Navigated to Facebook", char="#")
        try:
            bot.find_element_by_xpath('//*[@id="email"]').send_keys(self.username)
            gen_prompt("Username Entered")
            bot.find_element_by_xpath('//*[@id="pass"]').send_keys(self.password)
            gen_prompt("Password Entered")
            time.sleep(1)
            
            bot.find_element_by_xpath('//*[@id="pass"]').send_keys(Keys.RETURN)
            gen_prompt("Login Requested")
            wait(5)
            
            print("\n"*4)
        except:
            pass

    def crawl_timeline(self, number_of_posts):
        bot = self.bot

        bot.get('https://www.facebook.com/' + self.username)
        wait(4)
        gen_prompt("Navigated to " + self.username, char="#")
        
        bot.find_element_by_id("facebook").click()
        with open("friends.txt", 'r', encoding='utf-8') as f:
            memory_list = json.loads(f.read())
        print(f"{len(memory_list)} people already exists in the database.")
        gen_prompt("Starting the search for new people",value=100, char="#")
        c = ActionChains(bot)
        for _ in range(2):
            c.send_keys(Keys.PAGE_DOWN).perform()
            time.sleep(2)
        total_new = 0
        for i in range(number_of_posts):
            i += 1
            # c = ActionChains(bot)
            # c.send_keys(Keys.PAGE_DOWN).perform()
            # time.sleep(0.5)
            wrt = "Post no: " + str(i) + " "
            print(wrt.center(70, "-"))
            react_bar_str = f"/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div[4]/div[2]/div/div[2]/div[3]/div[2]/div[{i+3}]/div/div/div/div/div/div/div/div/div/div/div[8]/div/div/div[4]/div/div/div[1]/div/div[1]/div/div[1]/div/span/div/span[2]/span/span"
            anchor_scroll = f"/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div[4]/div[2]/div/div[2]/div[3]/div[2]/div[{i+1}]/div/div/div/div/div/div/div/div/div/div/div[8]/div/div/div[4]/div/div/div[1]/div/div[1]/div/div[1]/div/span/div/span[2]/span/span"
            if(i > 2):
                anchor_scroll_element = bot.find_element_by_xpath(anchor_scroll)
                bot.execute_script("arguments[0].scrollIntoView();", anchor_scroll_element)
                time.sleep(1)
            info = bot.find_element_by_xpath(react_bar_str).text
            self.highlight_element(react_bar_str, delay=0.5)
            time.sleep(1.5)
            
            reacts = int_from_string(info) + 2
            if (reacts != None):
                print ("\nReacts: "+ str(reacts))
                try:
                    id_list = []
                    bot.find_element_by_xpath(react_bar_str).click()
                    time.sleep(2)

                    x = []
                    obj = bot.find_elements_by_xpath("//div[@class='x1rg5ohu']")
                    if (reacts >= 1):
                        countList = []
                        while True:
                            obj = bot.find_elements_by_xpath("//div[@class='x1rg5ohu']")
                            for elements in obj:
                                x.append(elements.text)
                            react_box = "/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[2]/div[2]/div[3]/div"
                            scroll_element = bot.find_element_by_xpath(react_box)
                            bot.execute_script(f"arguments[0].scrollTop += {200};", scroll_element)
                            time.sleep(0.5)
                            count = len(x)
                            loading(count, reacts)
                            countList.append(count)
                            counter = countList.count(count)

                            if ((len(x) == reacts) or counter >= 8):
                                loading(1, 1)
                                print("\n")
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

    def crawl_activity(self, number_of_activities):
        bot = self.bot

        activity_link = f"https://www.facebook.com/{self.username}/allactivity?activity_history=false&category_key=LIKEDPOSTS&manage_mode=false&should_load_landing_page=false"
        bot.get(activity_link)
        wait(4)
        gen_prompt("Navigated to " + self.username + "'s Activities", char="#")
        gen_prompt(f"Gathering past {number_of_activities} activities")

        with open("friends.txt", 'r', encoding='utf-8') as f:
            memory_list = json.loads(f.read())
        i = 2
        j = 4
        k = 0
        counter = 0
        id_list = []
        while(counter < number_of_activities):
            counter += 1
            try: 
                strong2_text = f"/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div[2]/div/div/div/div/div/div[{j}]/div[{i}]/div[2]/div[1]/div/a/div[1]/div[2]/div/div/div/div[1]/span/span/span/div/strong[2]"
                anchor_scroll = f"/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div[2]/div/div/div/div/div/div[{j}]/div[{i-2}]/div[2]/div[1]/div/a/div[1]/div[2]/div/div/div/div[1]/span/span/span/div/strong[2]"
                if(i%4 == 0 and i > 1):
                    anchor_scroll_element = bot.find_element_by_xpath(anchor_scroll)
                    bot.execute_script("arguments[0].scrollIntoView();", anchor_scroll_element)
                    time.sleep(2)
                
                reacted_to = bot.find_element_by_xpath(strong2_text).text
                self.highlight_element(strong2_text)
                print(reacted_to)
                id_list.append(reacted_to)
                
                i += 1
                k = 0
            except Exception as e:
                i += 1
                k += 1
                # print("An error occurred: " + str(e))
                if (k >= 5):
                    i = 2
                    j += 1
                    k = 0
                pass
        joint_list = memory_list + id_list
        main_list = list(dict.fromkeys(joint_list))
        new = len(main_list) - len(memory_list)
        print("\n" + "New added: " + str(new))
        with open("friends+activities.txt", 'w', encoding='utf-8') as f:
            f.write(json.dumps(main_list))

    def clean(self, txt_file=None):
        bot = self.bot

        bot.get('https://www.facebook.com/' + self.username + '/friends')
        wait(4)
        gen_prompt("Navigated to " + self.username + "'s Friendlist", char="#")

        bot.find_element_by_id("facebook").click()
        c = ActionChains(bot)
        c.send_keys(Keys.PAGE_DOWN).perform()
        time.sleep(1)

        with open(txt_file, 'r', encoding='utf-8') as f:
            memory_list = json.loads(f.read())
 
        for i in range(1, 20):
            name_text_str = f"/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div/div/div/div/div/div[3]/div[{i}]/div[2]/div[1]/a/span"
            three_dot_button = f"/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div/div/div/div/div/div[3]/div[{i}]/div[3]/div/div/div"
            unfriend_button = f"/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[2]/div/div/div[1]/div[1]/div/div/div/div/div/div/div[1]/div/div[4]"
            anchor_scroll = f"/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div/div/div/div/div/div[3]/div[{i-4}]/div[2]/div[1]/a/span"
            clickable = "/html/body/div[1]/div/div[1]/div/div[2]/div[3]/div/div"
            try:    
                if(i%5 == 0 and i > 1):
                    anchor_scroll_element = bot.find_element_by_xpath(anchor_scroll)
                    bot.execute_script("arguments[0].scrollIntoView();", anchor_scroll_element)
                    time.sleep(0.5)
                
                friend = bot.find_element_by_xpath(name_text_str).text
                self.highlight_element(name_text_str)
                print(friend)

                if(friend in memory_list):
                    pass
                else:
                    bot.find_element_by_xpath(three_dot_button).click()
                    time.sleep(1)

                    self.highlight_element(unfriend_button)
                    bot.find_element_by_xpath(clickable).click()
            except Exception as e:
                    print("An error occurred: Cannot process 'Deactivated'/ 'Non-English-Name' profile")
                    pass

with open("C:\\Users\\hamid\\OneDrive\\Documents\\credential.txt", 'r', encoding='utf-8') as f:
    password = f.read()

# fb = FacebookBot('hamidur.rk', password)

# fb.login()
# fb.crawl_timeline(20)
# fb.crawl_activity(300)
# fb.clean("friends.txt")
