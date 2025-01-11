
from selenium import webdriver
from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from constant import constant
from selenium.webdriver.chrome.options import Options

from read_file import read_file
from utils import send_random_message

should_stop = False
driver = None

def run_discord_bot(server, subchannel, account, password, file_path, time_step):
    global should_stop, driver

    if not driver:
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        driver = webdriver.Chrome(options=chrome_options)

        driver.get('https://discord.com')

    # login
        WebDriverWait(driver, 10).until(ec.element_to_be_clickable((By.XPATH, constant.LOGIN))).click()

        try:
            WebDriverWait(driver, 5).until(ec.element_to_be_clickable((By.XPATH, constant.RELOGIN))).click()
        except (TimeoutException, NoSuchElementException):
            print("Phần tử RELOGIN không tồn tại, tiếp tục các bước tiếp theo.")

        driver.find_element(By.XPATH, constant.ACCOUNT).send_keys(account)

        driver.find_element(By.XPATH, constant.PASSWORD).send_keys(password)
        driver.find_element(By.XPATH, constant.SUBMIT).click()
        driver.implicitly_wait(10)

    # capcha
        try:
            WebDriverWait(driver, 5).until(ec.element_to_be_clickable((By.XPATH,  constant.HCAPCHA))).click()
        except (TimeoutException, NoSuchElementException):
            print("Phần tử HCAPCHA không tồn tại, tiếp tục các bước tiếp theo.")

    # find channel server
    if driver:
        channels = driver.find_elements(By.CLASS_NAME, constant.CHANNELS_CLASS)

        desired_channel = None
        for channel in channels:
            aria_label = channel.get_attribute('aria-label')
            if server in aria_label:
                desired_channel = channel
                break
    # find subchannel
        if desired_channel:
            driver.execute_script("arguments[0].scrollIntoView();", desired_channel)
            desired_channel.click()
            driver.implicitly_wait(10)
            sub_channels = driver.find_elements(By.CLASS_NAME, constant.SUB_CHANNELS_CLASS)

            for sub_channel in sub_channels:
                if subchannel in sub_channel.text.lower():
                    driver.execute_script("arguments[0].scrollIntoView();", sub_channel)
                    sub_channel.click()
                    driver.implicitly_wait(10)
                    while not should_stop:
                        messages = read_file(file_path)
                        send_random_message(driver, constant.INPUT, messages, wait_time=int(time_step))

            else:
                print(f"Không tìm thấy kênh con {subchannel}.")
        else:
            print(f"Không tìm thấy kênh {server}.")
        driver.implicitly_wait(10)
