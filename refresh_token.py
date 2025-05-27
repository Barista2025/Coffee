import requests
import base64
import time,os
import webbrowser
import json
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium_stealth import stealth
from selenium.webdriver import Chrome
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.support.expected_conditions import staleness_of
from selenium.common.exceptions import StaleElementReferenceException
from decrypt import decrypt

os.system("rm -rf access_token.txt")

input_file = open ('schwab.json')
config = json.load(input_file)
appKey = decrypt(config['appKey'])
appSecret = decrypt(config['appSecret'])
account_word = decrypt(config['account'])
pass_word = decrypt(config['password'])
options = webdriver.ChromeOptions()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
#options.add_experimental_option('useAutomationExtension', False)
options.add_argument('--disable-blink-features=AutomationControlled')
#options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
authUrl = f'https://api.schwabapi.com/v1/oauth/authorize?client_id={appKey}&redirect_uri=https://127.0.0.1'
driver.get(authUrl)
driver.implicitly_wait(10)
account = driver.find_element(By.XPATH,'//*[@id="loginIdInput"]')
password = driver.find_element(By.XPATH,'//*[@id="passwordInput"]')
button = driver.find_element(By.XPATH,'//*[@id="btnLogin"]')
account.send_keys(account_word)
password.send_keys(pass_word)
button.click()

driver.implicitly_wait(10)
checkBox = driver.find_element(By.XPATH,'//*[@id="acceptTerms"]')
checkBox.click()
cont = driver.find_element(By.XPATH,'//*[@id="submit-btn"]')
cont.click()

driver.implicitly_wait(10)
accept = driver.find_element(By.XPATH,'//*[@id="agree-modal-btn-"]')
accept.click()

wait = WebDriverWait(driver, 10)
while True:
    try:
        time.sleep(2)
        button = wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="submit-btn"]')))
        button.click()
        break
    except StaleElementReferenceException:
        print("元素失效，重試中...")

while True:
    try:
        time.sleep(2)
        button = wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="cancel-btn"]')))
        button.click()
        break
    except StaleElementReferenceException:
        print("元素失效，重試中...")

time.sleep(2)
returnedLink = driver.current_url
driver.quit()

code = f"{returnedLink[returnedLink.index('code')+5:returnedLink.index('%40')]}@"
headers = {'Authorization': f'Basic {base64.b64encode(bytes(f"{appKey}:{appSecret}", "utf-8")).decode("utf-8")}', 'Content-Type': 'application/x-www-form-urlencoded'}
data= {'grant_type': 'authorization_code', 'code': code, 'redirect_uri': 'https://127.0.0.1'}
response = requests.post('https://api.schwabapi.com/v1/oauth/token', headers=headers, data=data)
tD = response.json()
with open("access_token.txt", "w") as f:
  f.write(tD['access_token'])
print("Refresh token success.")
