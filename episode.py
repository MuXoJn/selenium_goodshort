
class Episode:

    def __init__(self, title: str, duration:int, videoUrl: str, seriesId: int):
        self.title = title
        self.duration = duration
        self.videoUrl = videoUrl
        self.seriesId = seriesId

    def to_dict(self):
        return {
            "title": self.title,
            "duration": self.duration,
            "videoUrl": self.videoUrl,
            "seriesId": self.seriesId
        }
