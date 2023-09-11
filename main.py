# Import required modules
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException
from time import sleep
from decouple import config
from random import randint


# Read the values from the ".env" file
FB_EMAIL = config("FB_EMAIL")
FB_PASSWORD = config("FB_PASSWORD")

# Tinder URL
TINDER_URL = "http://www.tinder.com"



class TinderFinderBot():
    """A class responsible for (dis)liking profiles on Tinder"""

    def __init__(self):
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=self.chrome_options)
        self.driver.maximize_window()
        self.driver.get(TINDER_URL)


    def login(self):
        # Reject cookies
        sleep(2)
        cookie_reject_btn = self.driver.find_element(
            by=By.XPATH, value='//*[@id="q1388042758"]/div/div[2]/div/div/div[1]/div[2]/button/div[2]/div[2]')
        cookie_reject_btn.click()

        # Click on Login button
        sleep(2)
        login_btn = self.driver.find_element(by=By.LINK_TEXT, value="Log in")
        login_btn.click()

        # Choose to login with Facebook
        sleep(2)
        fb_login = self.driver.find_element(
            by=By.XPATH, value='//*[@id="q-340338318"]/main/div/div/div[1]/div/div/div[2]/div[2]/span/div[2]/button/div[2]/div[2]/div/div')
        fb_login.click()

        # Switch to Facebook login window
        sleep(2)
        base_window = self.driver.window_handles[0]
        fb_login_window = self.driver.window_handles[1]
        self.driver.switch_to.window(fb_login_window)

        # Login with Facebook
        email = self.driver.find_element(by=By.ID, value="email")
        email.send_keys(FB_EMAIL)
        password = self.driver.find_element(by=By.ID, value="pass")
        password.send_keys(FB_PASSWORD)
        password.send_keys(Keys.ENTER)

        # Switch back to Tinder window
        self.driver.switch_to.window(base_window)
        # Delay 5 seconds to allow pop-ups to load
        sleep(5)


    def manage_swipes(self):
        # Allow location
        allow_location_btn = self.driver.find_element(
            by=By.XPATH, value='//*[@id="q-340338318"]/main/div/div/div/div[3]/button[1]/div[2]/div[2]')
        allow_location_btn.click()

        # Disallow notifications
        notifications_btn = self.driver.find_element(
            by=By.XPATH, value='//*[@id="q-340338318"]/main/div/div/div/div[3]/button[2]/div[2]/div[2]')
        notifications_btn.click()

        # Allow cookies
        # cookies = driver.find_element(
        #     by=By.XPATH, value='//*[@id="content"]/div/div[2]/div/div/div[1]/button')
        # cookies.click()


        # Swipe counter
        swipe_count = 0

        # Hit those Like and Dislike buttons - we'll use arrow keys
        actions = ActionChains(self.driver)

        for n in range(1000): # Adjust the number of profiles you'd like to go through
            # Add 2 seconds delay between likes
            sleep(2)

            try:
                actions.send_keys(Keys.ARROW_RIGHT)
                actions.perform()
                swipe_count += 1  # Increment the number of likes

                # Generate a random number between 3 and 7
                random_dislike = randint(3, 7)

                # Check if it's time to dislike after 5 likes
                if swipe_count == random_dislike or swipe_count >= 9:
                    sleep(5)  # Add a delay to ensure I can override some stupid decision
                    actions.send_keys(Keys.ARROW_LEFT)
                    actions.perform()
                    swipe_count = 0
            except ElementClickInterceptedException:
                try:
                    match_popup = self.driver.find_element(
                        by=By.CSS_SELECTOR, value=".itsAMatch a")
                    match_popup.click()

                except NoSuchElementException:
                    sleep(2)

    
    def quit(self):
        sleep(3)
        self.driver.quit(3)


def main():
    tf_bot = TinderFinderBot()
    tf_bot.login()
    tf_bot.manage_swipes()
    tf_bot.quit()


if __name__ == "__main__":
    main()