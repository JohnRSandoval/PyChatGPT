# Import the necessary modules
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import flask

from flask import g

APP = flask.Flask(__name__)
USERNAME = "User"
PASSWORD = "Pass"

executable_path = r'c:\chromedriver.exe'
# use chrome options to disguise the browser as a real browser
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
options.add_argument('log-level=3')
driver = webdriver.Chrome(executable_path)

@APP.route("/chat", methods=["GET"])
def chat():
    message = flask.request.args.get("q")
    if message is not None:
      loadBrowser()
      print("Sending message: ", message)
      send_message(message)
      response = get_last_message()
      print("Response: ", response)
      return response
    else:
      return "No message provided"

def waitForStreaming():
  #find the div with the class that contains 'request'
  rprocess = True
  requests = driver.find_elements_by_css_selector("div[class*='request']")
  # loop through requests and find the one with the class that contains 'streaming'
  for request in requests:
    if 'streaming' in request.get_attribute('class'):
      true_request = request
      break
  while rprocess:
    # if the class contains 'streaming' run below
    if 'streaming' in true_request.get_attribute('class'):
      time.sleep(.1)
    else:
      rprocess = False

def send_message(message):
    # Send the message
    box = get_input_box()
    box.send_keys(message)
    box.send_keys(Keys.RETURN)
    time.sleep(.5)
    


def get_last_message():
    """Get the latest message"""
    waitForStreaming()
    requests = driver.find_elements_by_css_selector("div[class*='request']")
    # set request to the last request
    request = requests[-1]
    # get all child nodes with text from the request
    text = request.find_elements_by_xpath(".//*[text()]")
    # return text from all child nodes
    return [t.text for t in text]


def get_input_box():
    try:
      return driver.find_element_by_tag_name("textarea")
    except:
      return None


def tryAgain():
  try:
    waitForStreaming()
    driver.find_element_by_css_selector("button[class*='btn flex gap-2 justify-center btn-neutral']").click()
    waitForStreaming()
  except:
    print('No try again button')

def loadBrowser():
  url = "https://chat.openai.com/chat"
  driver.get(url)
  if not is_logged_in():
    driver.find_element_by_css_selector("button[class*='btn flex gap-2 justify-center btn-primary']").click()
    # Wait for the page to load
    time.sleep(2)
    driver.find_element_by_id("username").send_keys(USERNAME)
    driver.find_element_by_name("action").click()
    time.sleep(2)
    driver.find_element_by_id("password").send_keys(PASSWORD)
    driver.find_element_by_name("action").click()
    time.sleep(2)
    # set opacity = to the div with class="fixed inset-0 transition-opacity bg-gray-500/75 dark:bg-gray-800/75 opacity-100"
    poup = driver.find_element_by_css_selector("div[class*='relative z-60']")
    driver.execute_script("arguments[0].remove()", poup)
    print('Logged in')
  else:
    print('Logged in')

def is_logged_in():
    try:
      return get_input_box() is not None
    except AttributeError:
        return False
