from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import SessionNotCreatedException, WebDriverException
from time import sleep
import numpy as np

import pdb


def rnd_nr():
    """
        creates random number between 0 and 1
    """
    return np.random.uniform(100) / 100


def sleep_rand(scaling_factor, duration):
    """
        Extends sleeping to user inputs and includes some randomization

        :param scaling_factor: adjusting sleeping time to user needs
        :param duration: base sleeping time
        :return:
    """
    sleep(scaling_factor * duration + rnd_nr())
    pass


def get_follow_number(follows):
    """
        converts the instagram string of followings/followers to a real number. If there are less than
        1000 followers the number is just converted into an int, the number needs to be converted to an
        integer first. If the follower number is really high, instagram uses M or K which needs to be
        taken care of.

        :param follows: string which contains number of followings/followers
            of structure 'XXX abonniert'
        :return: int of followers
    """
    num_str = follows.text[0:follows.text.find(" ")]
    if "M" in num_str:
        return int(num_str[0:num_str.find("M")]) * 1E6
    if "K" in num_str:
        return int(num_str[0:num_str.find("K")]) * 1E3
    return int(float(num_str) * 10 ** (len(num_str) - num_str.find(".") - 1)) \
        if num_str.find(".") != -1 else int(num_str)


class UnfollowBot:

    def __init__(
            self,
            username: str,
            password: str,
            sleeping_factor: int = 1,
            bl_threshold: int = 10000,
            nb_accs_follow_page: int = 7
    ):
        """
        :param username: username of instagram account to log into
        :param password: respective instagram password
        :param sleeping_factor: sleeping factor for wait times - the higher the better
        :param bl_threshold: accounts which are followed and do not follow back, but
            have more than bl_threshold are not unfollowed
        :param nb_accs_follow_page: number of accounts displayed when clicked on a profiles
            "followers" or "followings". This number can change with the browser and might
            need to be updated
        """
        self.username = username
        self.password = password
        self.followings = []
        self.followers = []
        try:
            self.driver = webdriver.Chrome(
                executable_path=r'C:\Users\Max\ChromeDriver\chromedriver.exe')
        except SessionNotCreatedException:
            raise Exception("Current chromedriver used not aligned with your version of Chrome\\"
                            "-> Please download the curresponding chromedriver at\\"
                            "https://chromedriver.chromium.org/downloads")
        except WebDriverException:
            raise Exception("Please select the right executable path for the chromedriver.exe")
        self.whitelist = []
        self.blacklist = []
        self.sf = sleeping_factor
        self.bl_threshold = bl_threshold
        # TODO: find better way to find nb_accs_follow_page
        self.nb_accs_follow_page = nb_accs_follow_page  # num of accounts shown when clicked on followers/followings

        self.login(self.username, self.password)

    def login(self, username, password):
        """
            Function logs into instagram via the Chrome webdriver

            :param username: username to log into instagram (provided from __init__)
            :param password: password to log into instagram (provided from __init__)
            :return:
        """
        self.driver.get(f'https://www.instagram.com/')
        sleep_rand(self.sf, 3)
        self.driver.find_element_by_xpath("/html/body/div[4]/div/div/button[1]").click()  # accept cookies
        sleep_rand(self.sf, 3)

        username_input = self.driver.find_element_by_xpath("//*[@id='loginForm']/div/div[1]/div/label/input")
        username_input.send_keys(username)
        sleep_rand(self.sf, 1)
        password_input = self.driver.find_element_by_xpath("//*[@id='loginForm']/div/div[2]/div/label/input")
        password_input.send_keys(password)
        sleep_rand(self.sf, 1)
        self.driver.find_element_by_xpath("//*[@id='loginForm']/div/div[3]").click()
        sleep_rand(self.sf, 10)
        self.driver.find_element_by_xpath("//button[contains(text(), 'Jetzt nicht')]").click()  # don't save credentials
        sleep_rand(self.sf, 2)
        self.driver.find_element_by_xpath("//button[contains(text(), 'Jetzt nicht')]").click()  # don't save credentials
        sleep_rand(self.sf, 2)

    def get_follow_number_from_insta(self, account: str):
        """
            Extracts the number of followers of a given account

            :param: account: url of account to get followers of
            :return: number of followers of account
        """
        sleep_rand(self.sf, 2)
        self.driver.get(f"{account}")
        sleep_rand(self.sf, 2)
        followers = self.driver.find_element_by_xpath("//a[contains(@href,'/followers')]")
        return get_follow_number(followers)

    def get_followings(self):
        """
            Finds the accounts which are followed and appends them to self.followings

            :return:
        """

        sleep_rand(self.sf, 2)
        self.driver.get(f"https://www.instagram.com/{self.username}/")
        sleep_rand(self.sf, 2)
        followings = self.driver.find_element_by_xpath("//a[contains(@href,'/following')]")

        followings_number = self.get_follow_number_from_insta(f"https://www.instagram.com/{self.username}/")

        followings.click()
        sleep_rand(self.sf, 2)

        for i in range(0, followings_number, self.nb_accs_follow_page):
            following_window = self.driver.find_element_by_xpath("//div[@role='dialog']//a")
            following_window.send_keys(Keys.PAGE_DOWN)
            sleep_rand(self.sf, 2)

        followings = self.driver.find_elements_by_xpath("//a[contains(@class,'notranslate')]")
        followings_links = [following.get_attribute('href') for following in followings]
        self.followings.extend(followings_links)
        pdb.set_trace()
        print(len(self.followings))

    def get_followers(self):
        """
            Finds the accounts which follow and appends them to self.followers

            :return:
        """
        sleep_rand(self.sf, 2)
        self.driver.get(f"https://www.instagram.com/{self.username}/")
        sleep_rand(self.sf, 2)
        followers = self.driver.find_element_by_xpath("//a[contains(@href,'/followers')]")

        followers_number = self.get_follow_number_from_insta(f"https://www.instagram.com/{self.username}/")

        followers.click()
        sleep_rand(self.sf, 2)

        for i in range(0, followers_number, self.nb_accs_follow_page):
            following_window = self.driver.find_element_by_xpath("//div[@role='dialog']//a")
            following_window.send_keys(Keys.PAGE_DOWN)
            sleep_rand(self.sf, 2)

        followers = self.driver.find_elements_by_xpath("//a[contains(@class,'notranslate')]")  # .get_attribute('href')
        followers_links = [follower.get_attribute('href') for follower in followers]
        pdb.set_trace()
        print(followers_links)
        print("len: " + str(len(followers_links)))
        self.followers.extend(followers_links)
        print(len(self.followers))

    def compare_follower_and_followings(self):
        """
            Compares list of followers and followings and adds all accounts which
            are followed but do not follow back to blacklist and all accounts which
            are followed and follow back to whitelist

            :return:
        """
        self.whitelist.extend(list(set(self.followings).intersection(set(self.followers))))
        self.blacklist.extend(list(set(self.followings).difference(set(self.followers))))

        # TODO: remove the following hardcoding after development
        self.blacklist = ['https://www.instagram.com/kyliejenner/', 'https://www.instagram.com/khloekardashian/',
                          'https://www.instagram.com/nickiminaj/', 'https://www.instagram.com/leomessi/']

    def unfollow_targets(self):
        """
            Unfollows every account from blacklist which has less followers than bl_threshold

            :return:
        """
        for account in self.blacklist:
            self.driver.get(account)
            sleep_rand(self.sf, 2)

            followers_number = self.get_follow_number_from_insta(account)
            if followers_number <= self.bl_threshold:
                self.driver.find_element_by_xpath("//button[@class='_abn9 _abnd _abni _abnn']").click()
                sleep_rand(self.sf, 2)
                self.driver.find_element_by_xpath("//button[contains(text(),'Nicht mehr folgen') "
                                                  "or contains(text(), 'Unfollow')]").click()
                sleep_rand(self.sf, 2)