from selenium import webdriver
import time
browser = webdriver.Chrome(r"R:\Softwares\chromedriver_win32\chromedriver.exe")
url = r'https://www.youtube.com/results?search_query='+'pubg'
browser.get(url)
try:
    elem = browser.find_element_by_css_selector(
        r'#contents > ytd-video-renderer:nth-child(1)')
except Exception as e:
    elem = browser.find_element_by_css_selector(
        r'#contents > ytd-video-renderer:nth-child(2)')
elem.click()
print('wait 2.5 sec')

try:
    time.sleep(8)
    elem = browser.find_element_by_css_selector(
        r'#skip-button\:b > span > button')
    elem.click()
except Exception as e:
    print(e)
