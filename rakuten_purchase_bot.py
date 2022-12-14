from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import sched
import time
from datetime import datetime

USER_ID = ""
PASSWORD = ""
ELEMENTS_SEQ = {
    "ご購入手続きへ": ".cart-button.checkout.new-cart-button",
    "ご購入手続き": ".big-red-button.large-button.purchaseButton.ratTrackingEvent",
    "userid": "u",
    "password": "p",
    "ログイン": "login_submit",
    "注文を確定する": "commit",
}
ENTRYPOINT = ""
PURCHASE_FLG = False
EXECUTION_TIME = "2022-12-10 20:00:00"


def purchase():
    options = webdriver.ChromeOptions()
    options.add_argument("--blink-settings=imagesEnabled=false")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(time_to_wait=3600)

    driver.get(ENTRYPOINT)

    WebDriverWait(driver, timeout=3600).until(EC.presence_of_element_located((By.CSS_SELECTOR, ELEMENTS_SEQ["ご購入手続きへ"])))
    elem = driver.find_element_by_css_selector(ELEMENTS_SEQ["ご購入手続きへ"])
    # refresh until loaded
    refresh_cnt = 0
    while ~(elem.is_enabled()) & (refresh_cnt <= 1000):
        driver.refresh()
        WebDriverWait(driver, timeout=3600).until(EC.presence_of_all_elements_located)
        while driver.find_elements_by_id(id_="errorTxt"):
            driver.refresh()
            WebDriverWait(driver, timeout=3600).until(EC.presence_of_all_elements_located)
            refresh_cnt += 1
            print(refresh_cnt)
        elem = driver.find_element_by_css_selector(ELEMENTS_SEQ["ご購入手続きへ"])
        refresh_cnt += 1
        print(refresh_cnt)
    elem.click()

    WebDriverWait(driver, timeout=3600).until(EC.presence_of_element_located((By.CSS_SELECTOR, ELEMENTS_SEQ["ご購入手続き"])))
    driver.find_element_by_css_selector(ELEMENTS_SEQ["ご購入手続き"]).click()

    WebDriverWait(driver, timeout=3600).until(EC.presence_of_element_located((By.NAME, ELEMENTS_SEQ["userid"])))
    driver.find_element_by_name(ELEMENTS_SEQ["userid"]).send_keys(USER_ID)

    WebDriverWait(driver, timeout=3600).until(EC.presence_of_element_located((By.NAME, ELEMENTS_SEQ["password"])))
    driver.find_element_by_name(ELEMENTS_SEQ["password"]).send_keys(PASSWORD)

    WebDriverWait(driver, timeout=3600).until(EC.presence_of_element_located((By.NAME, ELEMENTS_SEQ["ログイン"])))
    driver.find_element_by_name(ELEMENTS_SEQ["ログイン"]).click()

    WebDriverWait(driver, timeout=5).until(EC.presence_of_element_located((By.NAME, ELEMENTS_SEQ["注文を確定する"])))
    driver.find_element_by_name(ELEMENTS_SEQ["注文を確定する"]).click()

    time.sleep(60)
    driver.save_screenshot(filename="images/screen.png")
    driver.quit()
    PURCHASE_FLG = True


def main():
    try_cnt = 0
    while ~(PURCHASE_FLG) & (try_cnt <= 100):
        try:
            purchase()
        except Exception as e:
            print(e)
            try_cnt += 1


if __name__ == "__main__":
    if EXECUTION_TIME == "":
        main()
    else:
        scheduler = sched.scheduler(time.time, time.sleep)
        run_at = datetime.strptime(EXECUTION_TIME, "%Y-%m-%d %H:%M:%S")
        run_at = int(time.mktime(run_at.utctimetuple()))
        scheduler.enterabs(run_at, 1, main)
        scheduler.run()
