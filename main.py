from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

'''This code is save my time, if the Internet connection is not working properly. 

1. function: Program going to speedtest.net website to run a test.
If the "PROMISED_DOWN" or "PROMISED UP" values (Internet Providers promising values)
are lower than result of test:

2. function: the algorithm will log in my Twitter Account and - with @  - write a 
complain tweet for my Internet Provider.

Else: if everything is ok with the connection, program will give a feedback in the
console and will quit.'''


PROMISED_DOWN = 150
PROMISED_UP = 10
CHROME_DRIVER_PATH = "C:/Users/Csaba/Development/chromedriver.exe"
TWITTER_PHONE_NR = os.environ["TWITTER_PHONE_NR"]
TWITTER_PASSWORD = os.environ["TWITTER_PASSWORD"]

class InternetSpeedTwitterBot:
    def __init__(self, CHROME_DRIVER_PATH):
        self.driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)
        self.up = 0
        self.down = 0

    def get_internet_speed(self):
        self.driver.get("https://www.speedtest.net/")

        # Accept cookie popup
        time.sleep(1)
        self.driver.find_element(By.XPATH, "/html/body/div[7]/div[2]/div/div/div[2]/div/div/button[2]").click()

        # Click Go
        time.sleep(2)
        self.driver.find_element(By.XPATH, '//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[1]/a').click()

        # Get result
        time.sleep(60)
        self.down = self.driver.find_element(By.XPATH, '//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div[1]/div/div[2]/span').text
        self.up = self.driver.find_element(By.XPATH, '//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div[2]/div/div[2]/span').text

        # Print result
        print(type(self.down))
        print(self.down)

        print(type(self.up))
        print(self.up)


    def tweet_at_provider(self):
        if float(self.down) < PROMISED_DOWN or float(self.up) < PROMISED_UP:
            print("Internet speed is lower, than promised speed. We are going to tweet ... 😒")

            # Open Twitter Website
            self.driver.get("https://twitter.com/")

            time.sleep(5)
            # Accept cookie popup
            self.driver.find_element(By.XPATH, '//*[@id="layers"]/div/div[2]/div/div/div/div[2]/div[1]/div/span/span').click()

            time.sleep(5)
            # Log in on Twitter Button
            self.driver.find_element(By.XPATH, '//*[@id="layers"]/div/div[1]/div/div/div/div[2]/div[2]/div/div/div[1]/a/div/span/span').click()

            time.sleep(5)
            # Fill in Phone form
            self.driver.find_element(By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input').send_keys(TWITTER_PHONE_NR)

            time.sleep(1)
            # Next Button
            self.driver.find_element(By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]/div/span/span').click()

            time.sleep(5)
            # Fill in Password
            self.driver.find_element(By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[2]/div/label/div/div[2]/div[1]/input').send_keys(TWITTER_PASSWORD)

            time.sleep(1)
            # Log in Button to Twitter Account
            self.driver.find_element(By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div/div/span/span').click()

            time.sleep(5)
            # Tweet #1 - we can use this locator:By.CLASS_NAME, 'DraftEditor-root'.
            self.autotw1 = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'DraftEditor-root')))
            self.autotw1.click()

            tweet_message = f"Hey @telekomHU Internet Provider, why is my internet speed {self.down}down/{self.up}up when I pay for {PROMISED_DOWN}down/{PROMISED_UP}up?"

            # Tweet #2 - We must click on the element to bring up other elements to write the tweet, which is:By.CLASS_NAME, 'public-DraftEditorPlaceholder-root'), and use ActionChains to send text.
            self.element = WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable((By.CLASS_NAME, 'public-DraftEditorPlaceholder-root')))
            ActionChains(self.driver).move_to_element(self.element).send_keys(f"{tweet_message}").perform()

            # Send Tweet
            self.sendTw = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[3]/div/div/div[2]/div[3]/div/span/span')))
            self.sendTw.click()

            time.sleep(10)

        else:
            print("Everything is all right with your internet, you don't need to write a complain tweet.👌")


bot = InternetSpeedTwitterBot(CHROME_DRIVER_PATH)
bot.get_internet_speed()
bot.tweet_at_provider()

