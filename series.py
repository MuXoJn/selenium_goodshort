import json
import requests
from typing import List


# 定义 Series 类
class Series:
    def __init__(self, title: str, releaseDate: str, status: int, coverImageUrl: str, isRecommended: bool,
                 description: str, tags: List[str], categoryId: int):
        self.title = title
        self.releaseDate = releaseDate
        self.status = status
        self.coverImageUrl = coverImageUrl
        self.isRecommended = isRecommended
        self.description = description
        self.tags = tags
        self.categoryId = categoryId

    # 序列化函数，将 Series 转换为字典
    def to_dict(self):
        return {
            "title": self.title,
            "releaseDate": self.releaseDate,
            "status": self.status,
            "coverImageUrl": self.coverImageUrl,
            "isRecommend": self.isRecommended,
            "description": self.description,
            "tags": self.tags,
            "categoryId": self.categoryId
        }


