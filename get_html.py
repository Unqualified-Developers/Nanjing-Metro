import random
import time
import os

from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


edge_options = Options()

driver = webdriver.Edge(options=edge_options)

driver.get(
    "https://m.weibo.cn/search?containerid=231522type%3D1%26t%3D10%26q%3D%23%E6%98%A8%E6%97%A5%E5%AE%A2%E6%B5%81%23&isnewpage=1&luicode=10000011&lfid=231522type%3D1%26t%3D10%26q%3D%23%E6%98%A8%E6%97%A5%E5%AE%A2%E6%B5%81%23&launchid=10000360-page_H5"
)

time.sleep(5)


# 点击“实时”
try:
    realtime_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//*[contains(text(),'实时')]")
        )
    )

    realtime_button.click()
    print("Click Real-time Success")

except Exception as e:
    print("The real-time button was not found", e)


# 等待实时内容加载
time.sleep(3)


def smooth_scroll_to_bottom():
    current_position = 0

    while current_position < 2500:
        step = random.randint(300, 700)
        current_position += step

        driver.execute_script(
            f"window.scrollTo(0, {current_position});"
        )

        time.sleep(random.uniform(0.3, 0.8))


smooth_scroll_to_bottom()


time.sleep(random.uniform(1, 2))


# 自动创建目录
os.makedirs("docs/data", exist_ok=True)


# 保存网页源码
html_source = driver.page_source

with open("docs/data/page.html", "w", encoding="utf-8") as f:
    f.write(html_source)


driver.quit()
