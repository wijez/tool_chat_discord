import random
import threading
import time

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

import main


def send_random_message(driver, input_xpath, messages, wait_time):
    input_element = None
    try:
        input_element = WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.XPATH, input_xpath))
        )

        def send_message():
            while not main.should_stop:
                try:
                    start_time = time.time()
                    message = random.choice(messages)
                    input_element.send_keys(message)
                    input_element.send_keys(Keys.ENTER)
                    time.sleep(wait_time)
                    end_time = time.time()
                    print(f"Gửi tin nhắn: {message}, Thời gian gửi: {end_time - start_time}s")
                except Exception as e:
                    print(f"Lỗi khi gửi tin nhắn: {e}")
                    continue
        message_thread = threading.Thread(target=send_message)
        message_thread.daemon = True
        message_thread.start()

    except Exception as e:
        print(f"Lỗi khi gửi tin nhắn: {e}")
