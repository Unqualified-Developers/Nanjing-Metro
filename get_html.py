import random
import time

from selenium import webdriver
from selenium.webdriver.edge.options import Options

edge_options = Options()

driver = webdriver.Edge(options=edge_options)
driver.get("https://m.weibo.cn/u/2638276292")
time.sleep(10)


def smooth_scroll_to_bottom():
    current_position = 0
    step = random.randint(300, 700)

    while current_position < 50000:
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
