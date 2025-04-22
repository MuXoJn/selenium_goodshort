import os
import subprocess

import requests

# 下载 url 的图片，返回图片保存路径
# 下载图片并保存到本地
import requests
import os


import os
import requests

def download_image(image_url, file_name=None):
    try:
        # 发送 GET 请求获取图片
        response = requests.get(image_url)

        if response.status_code == 200:
            # 如果没有提供文件名，则从 URL 获取文件名
            if not file_name:
                file_name = os.path.basename(image_url)

            # 创建文件夹（如果不存在的话）
            if not os.path.exists('images'):
                os.makedirs('images')

            # 拼接文件路径
            file_path = os.path.join('images', file_name)

            # 检查文件是否已存在，如果存在，则修改文件名
            if os.path.exists(file_path):
                base_name, ext = os.path.splitext(file_name)
                counter = 1
                while os.path.exists(file_path):
                    file_path = os.path.join('images', f"{base_name}_{counter}{ext}")
                    counter += 1

            # 保存图片到本地文件
            with open(file_path, 'wb') as file:
                file.write(response.content)

            # 获取文件的绝对路径
            abs_file_path = os.path.abspath(file_path)

            print(f"Image successfully downloaded: {abs_file_path}")
            return abs_file_path  # 返回绝对路径

        else:
            print(f"Failed to download image from {image_url}, status code: {response.status_code}")
            return None

    except requests.RequestException as e:
        print(f"An error occurred while downloading the image: {e}")
        return None



# 调用 yt-dlp 命令下载 m3u8视频，然后
# 调用 ffprobe 获取视频时长
# 返回文件路径和视频时长
import subprocess
import os


def download_m3u8_video(video_url, title):
    # 使用 yt-dlp 下载视频
    file_name = f"{title}.mp4"

    # 获取文件的绝对路径

    command = [
        "yt-dlp",
        f"-o{file_name}",
        video_url
    ]

    try:
        # 执行命令并下载视频
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error while downloading the video: {e}")
        return None, None

    with os.popen(
            f"ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 {file_name}") as pipe:
        result = pipe.read().strip()  # 获取输出并去除前后空白字符


    # 返回文件的绝对路径和视频时长
    return os.path.abspath(file_name),float(result)


if __name__ == "__main__":
    file_name = "AMistakenSurrogatefortheRuthlessBillionaire-Episode1.mp4"


