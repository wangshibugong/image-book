import time
import json
import redis
from selenium import webdriver

client = redis.StrictRedis()

# driver = webdriver.Chrome()
# driver.get('http://exercise.kingname.info/exercise_login_success')
browser = webdriver.Chrome()
browser.get("https://passport.lagou.com/login/login.html")
# user = driver.find_element_by_xpath('//input[@name="username"]')
# user.clear()
# user.send_keys('kingname')
#
# password = driver.find_element_by_xpath('//input[@name="password"]')
# password.clear()
# password.send_keys('genius')
#
# remember = driver.find_element_by_xpath('//input[@name="rememberme"]')
# remember.click()
#
# login = driver.find_element_by_xpath('//button[@class="login"]')
# login.click()
# time.sleep(2)
# cookies = driver.get_cookies()
browser.get("https://passport.lagou.com/login/login.html")
browser.find_element_by_css_selector(".form_body .input.input_white").send_keys("15670567903")
browser.find_element_by_css_selector('.form_body input[type="password"]').send_keys("biao15670567903")
browser.find_element_by_css_selector('div[data-view="passwordLogin"] input.btn_lg').click()
import time
time.sleep(30)
cookies = browser.get_cookies()
client.lpush('cookies_lagou', json.dumps(cookies))
browser.quit()
