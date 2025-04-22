import json
import os

import requests

from episode import Episode
from series import Series

backend_url = "http://localhost:8010"

http_headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJVc2VySUQiOjEsIlBlcm1pc3Npb24iOiJhZG1pbiIsIkpUSSI6ImQ2OWU5MjQ0LTM4NzQtNGUxZS04MTZmLTM1ZTllYzFjODRjYSIsImV4cCI6MTc0NTgyMTcwNH0.4lQYD4ms4XPP8N4gV8RXqH-vExrpjEVlMFcii-MPKuQ',
}


def send_series_post_request(series: Series):
    # 序列化 series 对象为 JSON
    payload = json.dumps(series.to_dict())

    response = requests.post(backend_url + "/api/series", headers=http_headers, data=payload)

    response_data = response.json()
    if response_data['code'] == 0:
        print(f"{series.title}上传成功")
        return response_data['data']['id']
    else:
        print(f"{series.title}上传失败")
        return None


def send_episode_post_request(episode: Episode):
    payload = json.dumps(episode.to_dict())
    response = requests.post(backend_url + "/api/episode", headers=http_headers, data=payload)
    if response.status_code == 200:
        # 响应正常，直接返回 ID
        print(f"{episode.title}请求成功")
    else:
        print(f"请求失败，状态码: {response.status_code}, 错误信息: {response.text}")
        return None


def send_upload_post_request(file_path):
    # 打开文件并上传
    with open(file_path, 'rb') as file:
        # 使用 files 参数指定上传的文件
        files = {'file': (file.name, file)}  # 这里 'file' 是表单字段的名称，'image/jpeg' 是文件类型

        # 发送 POST 请求上传文件
        response = requests.post(backend_url + "/upload", files=files)

    if response.status_code == 200:
        # 响应正常，返回上传后的 URL
        if response.json()['code'] == 0:
            print(f"{file_path} 上传成功")
            uploaded_url = response.json()['data']['url']

            # 上传成功后删除文件
            os.remove(file_path)
            print(f"{file_path} 已被删除")

            return uploaded_url
        else:
            print(f"{file_path} 上传失败")
            return None
    else:
        print(f"请求失败，状态码: {response.status_code}, 错误信息: {response.text}")
        return None


def send_category_post_request(category_name):
    payload = json.dumps({"name": category_name})
    response = requests.post(backend_url + "/api/category", headers=http_headers, data=payload)
    if response.status_code == 200:
        # 响应正常，直接返回 ID
        print(f"{category_name}上传成功")
        return response.json()['data']['id']
    else:
        print(f"请求失败，状态码: {response.status_code},错误信息: {response.text}")
