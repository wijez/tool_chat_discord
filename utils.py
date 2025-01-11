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

# import random
# import threading
# import time
# from selenium.webdriver import Keys, ActionChains
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.support import expected_conditions as ec
# from selenium.common.exceptions import (
#     TimeoutException,
#     ElementNotInteractableException,
#     StaleElementReferenceException
# )
#
#
# def send_random_message(driver, input_xpath, messages, wait_time=5):
#     """
#     Discord-specific message sender that handles Discord's contenteditable input field.
#
#     Args:
#         driver: Selenium WebDriver instance
#         input_xpath: XPath of Discord's message input
#         messages: List of messages to send
#         wait_time: Time between messages in seconds
#     """
#
#     def find_chat_input():
#         # Wait for the chat input to be present and visible
#         input_element = WebDriverWait(driver, 10).until(
#             ec.presence_of_element_located((By.CSS_SELECTOR, '[role="textbox"][contenteditable="true"]'))
#         )
#         return input_element
#
#     def focus_input(input_element):
#         # Multiple methods to try to focus the input
#         try:
#             # Try clicking
#             input_element.click()
#         except:
#             try:
#                 # Try ActionChains click
#                 ActionChains(driver).move_to_element(input_element).click().perform()
#             except:
#                 try:
#                     # Try JavaScript focus
#                     driver.execute_script("arguments[0].focus();", input_element)
#                 except:
#                     pass
#
#     def send_message():
#         while True:
#             try:
#                 # Find the input element fresh each time
#                 input_element = find_chat_input()
#
#                 # Ensure we're scrolled to the input
#                 driver.execute_script("arguments[0].scrollIntoView(true);", input_element)
#                 time.sleep(0.5)  # Short wait after scroll
#
#                 # Focus the input
#                 focus_input(input_element)
#
#                 # Select a random message
#                 message = random.choice(messages)
#
#                 # Clear existing text using JavaScript
#                 driver.execute_script("arguments[0].innerHTML = '';", input_element)
#
#                 # Send the message using ActionChains
#                 actions = ActionChains(driver)
#                 actions.send_keys_to_element(input_element, message)
#                 actions.send_keys(Keys.ENTER)
#                 actions.perform()
#
#                 print(f"Message sent successfully: {message}")
#                 time.sleep(wait_time)
#
#             except StaleElementReferenceException:
#                 print("Chat input changed, finding new input...")
#                 time.sleep(1)
#                 continue
#
#             except ElementNotInteractableException:
#                 print("Chat input not interactable, retrying...")
#                 time.sleep(2)
#                 continue
#
#             except Exception as e:
#                 print(f"Error sending message: {str(e)}")
#                 time.sleep(1)
#                 continue
#
#     try:
#         # Verify we can find the chat input before starting
#         find_chat_input()
#
#         # Start the message thread
#         message_thread = threading.Thread(target=send_message)
#         message_thread.daemon = True
#         message_thread.start()
#
#         return message_thread
#
#     except TimeoutException:
#         print("Could not find Discord chat input")
#         raise
#     except Exception as e:
#         print(f"Failed to initialize message sender: {str(e)}")
#         raise