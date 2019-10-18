# 照片物件 包含路徑與姓名
class video():
    def __init__(self,id, videoUrl , isRecoged , date , classNo):
        self.videoUrl = videoUrl # 封面照片路徑
        self.id = id
        self.isRecoged = isRecoged
        self.date = date
        self.classNo = classNo