import random
import time

from selenium import webdriver
from selenium.webdriver.edge.options import Options

edge_options = Options()

driver = webdriver.Edge(options=edge_options)
driver.get("https://m.weibo.cn/search?containerid=231522type%3D1%26t%3D10%26q%3D%23%E6%98%A8%E6%97%A5%E5%AE%A2%E6%B5%81%23&isnewpage=1&luicode=10000011&lfid=1005052638276292&launchid=10000360-page_H5")
time.sleep(5)


def smooth_scroll_to_bottom():
    current_position = 0
    step = random.randint(300, 700)

    while current_position < 3600:
        current_position += step
        driver.execute_script(f"window.scrollTo(0, {current_position});")
        time.sleep(random.uniform(0.05, 0.2))
        step = random.randint(200, 600)


smooth_scroll_to_bottom()
time.sleep(random.uniform(1, 2))

html_source = driver.page_source

with open("docs/data/page.html", "w", encoding="utf-8") as f:
    f.write(html_source)

driver.quit()
