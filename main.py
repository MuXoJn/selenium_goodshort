import json
import random
import re
import string
import time
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

import download
import request
from episode import Episode
from request import backend_url
from series import Series

# 设置浏览器选项
chrome_options = Options()
# chrome_options.add_argument("--headless")  # 无头模式（不显示浏览器界面）
chrome_options.add_argument("--disable-gpu")  # 禁用 GPU 加速
chrome_options.add_argument("--no-sandbox")  # 禁用沙盒模式
categoryIdMap = {"Romance": 1, "Fantasy-Female": 2, "Revenge": 3}
# 启动 Selenium WebDriver
driver = webdriver.Chrome(options=chrome_options)
url = "https://www.goodshort.com/dramas/playlets?page="
for i in range(1, 6):
    try:
        # 访问目标 URL
        driver.execute_script(f"window.open('{url}{i}', '_blank');")

        time.sleep(3)

        driver.switch_to.window(driver.window_handles[-1])

        first_window = driver.current_window_handle

        ## 查找所有 book div 元素
        books = driver.find_elements(By.CSS_SELECTOR, "div.books div.book")

        # 遍历每个 book 元素并提取信息
        for index, book in enumerate(books):
            try:
                # 获取书的链接
                href = book.find_element(By.CSS_SELECTOR, "a.book").get_attribute("href")

                # 打开新标签页
                driver.execute_script(f"window.open('{href}', '_blank');")

                driver.switch_to.window(driver.window_handles[-1])  # 切换到新标签页

                second_window = driver.current_window_handle

                # 获取图片
                image_src = driver.find_element(By.CSS_SELECTOR, "div.book div.cover img").get_attribute("src")

                # 获取书名
                book_name = driver.find_element(By.CSS_SELECTOR, "h1.book-name").text

                # 获取类别
                browse = driver.find_element(By.CSS_SELECTOR, "h3.browse").text
                category_id = categoryIdMap.get(browse, None)  # 如果没有找到，返回 None
                if category_id is None:
                    category_id = request.send_category_post_request(browse)
                    categoryIdMap[browse] = category_id
                # 获取简介
                intro = driver.find_element(By.CSS_SELECTOR, "div.intro").text

                # 获取标签
                tags_elements = driver.find_elements(By.CSS_SELECTOR, "div.tags a.tag")
                tags = [{"text": tag.text, "order": idx + 1} for idx, tag in enumerate(tags_elements)]

                # 将获取的数据构造 series 发送请求到后台接口存入数据库中，获取返回的id
                image_path = download.download_image(image_src, f"{book_name}.jpg")
                if image_path:
                    image_url = request.send_upload_post_request(image_path)
                    if image_url:
                        series_id = request.send_series_post_request(
                            Series(title=book_name,
                                   releaseDate=datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d'),
                                   status=1, coverImageUrl=f"{backend_url}{image_url}", isRecommended=1,
                                   description=intro, tags=json.dumps(tags), categoryId=category_id))
                # 获取所有 div.chapter 元素
                chapters = driver.find_elements(By.CSS_SELECTOR, "div.chapter-list a.chapter")
                print(len(chapters))
                # 遍历每一个 div.chapter 元素
                for chapter_index, chapter in enumerate(chapters):
                    try:
                        # 获取 href 属性
                        chapter_href = chapter.get_attribute("href")
                        chapter_name = chapter.find_element(By.CSS_SELECTOR, "h3.chapter-name").text

                        # 打开章节的链接
                        driver.execute_script(f"window.open('{chapter_href}', '_blank');")
                        # 获取章节名称
                        driver.switch_to.window(driver.window_handles[-1])  # 切换到新标签页

                        # chapter_name = driver.find_element(By.CSS_SELECTOR, "h1.book-name").text.replace(" ", "")
                        page_source = driver.page_source
                        # 使用正则表达式查找所有 JSON-LD 数据块
                        json_pattern = r'<script type="application/ld\+json">(.+?)</script>'

                        # 查找所有匹配的 JSON-LD 数据
                        matches = re.findall(json_pattern, page_source, re.DOTALL)
                        # 遍历找到的所有 JSON 数据块
                        for match in matches:
                            data = json.loads(match)
                            # 提取 contentUrl
                            content_url = data.get("contentUrl")
                            if content_url:
                                print(content_url)  # 输出 contentUrl
                                break  # 找到第一个包含 contentUrl 的数据块后就停止

                        driver.close()

                        # 切换回原标签页
                        driver.switch_to.window(second_window)
                        # 调用 m3u8视频下载器，然后合并视频，然后上传到服务器，获取到返回链接
                        video_path, duration = download.download_m3u8_video(content_url, ''.join(
                            random.choices(string.ascii_letters + string.digits, k=10)))
                        if video_path:
                            video_url = request.send_upload_post_request(video_path)
                            if video_url and duration:
                                request.send_episode_post_request(
                                    Episode(title=chapter_name, duration=duration, videoUrl=f"{backend_url}{video_url}",
                                            seriesId=series_id))
                    except Exception as e:
                        continue
                # 关闭当前标签页并切换回原标签页
                driver.close()
                driver.switch_to.window(first_window)  # 切换回原始目标页面标签页
            except Exception as e:
                continue
    except Exception as e:
        continue
# 关闭浏览器
driver.quit()
