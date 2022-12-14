from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time

USER_ID = ""
PASSWORD = ""
PROFILE_PATH=""
ENTRYPOINT=""
ELEMENTS_SEQ = {
    "purchase_btn1": "/html/body/div[8]/table/tbody/tr/td/table[2]/tbody/tr/td/table/tbody/tr[2]/td[3]/table[2]/tbody/tr/td/table[4]/tbody/tr[2]/td[3]/div[5]/table[1]/tbody/tr[2]/td/span[2]/span/span[2]/button",
    "purchase_btn2": "/html/body/div[4]/div[5]/div[2]/div[2]/div[1]/form/div/div[1]/input[3]",
    "login_usrid_textbox": "/html/body/div[2]/div[3]/form[1]/div[2]/div/div[1]/div[2]/input",
    "login_password_textbox": "/html/body/div[2]/div[3]/form[1]/div[2]/div/div[1]/div[4]/input",
    "login_btn": "/html/body/div[2]/div[3]/form[1]/div[2]/div/div[2]/div/input[1]",
    "deal": "/html/body/div[2]/form/div[1]/div[5]/div/div/input",
}

options = webdriver.ChromeOptions()
# if you want to use chrome profile,set PROFILE_PATH
# options.add_argument("--user-data-dir="+PROFILE_PATH)
options.add_argument("--headless")
options.add_argument("--blink-settings=imagesEnabled=false")
driver = webdriver.Chrome(options=options)

def click(xpath: str, timeout=5):
    assert EC.element_to_be_clickable((By.XPATH, xpath))
    WebDriverWait(driver, timeout=timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))
    elem = driver.find_element_by_xpath(xpath=xpath)
    print(elem)
    ActionChains(driver).move_to_element(elem).perform()
    elem.click()


def write(xpath: str, input: str, timeout=5):
    WebDriverWait(driver, timeout=timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))
    elem = driver.find_element_by_xpath(xpath=xpath)
    ActionChains(driver).move_to_element(elem).perform()
    elem.send_keys(input)


def main():
    driver.implicitly_wait(time_to_wait=20)
    driver.get(ENTRYPOINT)
    click(xpath=ELEMENTS_SEQ["purchase_btn1"])
    click(xpath=ELEMENTS_SEQ["purchase_btn2"])
    write(xpath=ELEMENTS_SEQ["login_usrid_textbox"], input=USER_ID)
    write(xpath=ELEMENTS_SEQ["login_password_textbox"], input=PASSWORD)
    click(xpath=ELEMENTS_SEQ["login_btn"])
    click(xpath=ELEMENTS_SEQ["deal"])
    print(driver.page_source)
    driver.quit()

if __name__ == "__main__":
    main()