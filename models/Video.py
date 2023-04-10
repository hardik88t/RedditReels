import os, json, datetime
from datetime import date
from utils.RedditReels import RedditReels
from utils.CreateMovie import GetDaySuffix
from models.Logger import logger

class Video:
    def __init__(self, file=None, title=None, description=None, keywords=None, privacyStatus=None, videoid=None, uploaded=False, ytvideolink="none", timestamp=None):
        self.file = file
        self.title = title
        self.description = description
        self.keywords = keywords
        self.privacyStatus = privacyStatus
        self.videoid = videoid
        self.uploaded = uploaded
        self.ytvideolink = ytvideolink
        self.timestamp = timestamp
        if timestamp is None:
            day = date.today().strftime("%d")
            day = str(int(day)) + GetDaySuffix(int(day))
            self.timestamp = datetime.date.today().strftime("%A %B") + f" {day}"

    # def update_from_new_video(self, new_video):
    #     logger.info("=============All good here Updating video data ...")
    #     for attr in ["file", "title", "description", "keywords", "privacyStatus", "videoid", "uploaded",  "ytvideolink", "timestamp"]:
    #         value = getattr(new_video, attr, None)
    #         if value is not None and value != "":
    #             setattr(self, attr, value)
    #     logger.info("=============Done updating video data!")    
        
        
    def update_from_new_video(self, new_video):
        if new_video.file:
            self.file = new_video.file
        if new_video.title:
            self.title = new_video.title
        if new_video.description:
            self.description = new_video.description
        if new_video.keywords:
            self.keywords = new_video.keywords
        if new_video.privacyStatus:
            self.privacyStatus = new_video.privacyStatus
        if new_video.uploaded:
            self.uploaded = new_video.uploaded
        if new_video.ytvideolink != "none":
            self.ytvideolink = new_video.ytvideolink

    '''
    def to_json(self): upload will be True
    '''
    def to_json(self):
        self.uploaded = True
        return {
            "file": self.file,
            "title": self.title,
            "description": self.description,
            "keywords": self.keywords,
            "privacyStatus": self.privacyStatus,
            "videoid": self.videoid,
            "ytvideolink": self.ytvideolink,
            "timestamp": self.timestamp
        }
    
    def to_dict(self):
        return {
                "file": self.file,
                "title": self.title,
                "description": self.description,
                "keywords": self.keywords,
                "privacyStatus": self.privacyStatus,
                "videoid": self.videoid,
                "uploaded": self.uploaded,
                "ytvideolink": self.ytvideolink,
                "timestamp": self.timestamp,
            }
        
            
    def save_to_file(self, filename = "videos.json"):
        try:
            with open(filename) as f:
                if f.read().strip() == "":
                    videos = {}
                else:
                    f.seek(0)
                    videos = json.load(f)
        except FileNotFoundError:
            with open(filename, 'w') as f:
                f.write("{}")
            videos = {}

        videos[self.videoid] = self.to_dict()

        with open(filename, 'w') as f:
            json.dump(videos, f, indent=4)



    @staticmethod
    def get_video(videoid, filename = "videos.json"):
        if not os.path.exists(filename):
            with open(filename, "w") as f:
                f.write("{}")
            return None

        with open(filename, "r") as f:
            videos = json.load(f)
            if videoid not in videos:
                return None
            video_data = videos[videoid]
            video = Video(
                file =  video_data["file"],
                title =  video_data["title"],
                description = video_data["description"],
                keywords = video_data["keywords"],
                privacyStatus = video_data["privacyStatus"],
                videoid = video_data["videoid"],
                uploaded = video_data["uploaded"],
                ytvideolink = video_data["ytvideolink"],
                timestamp = video_data["timestamp"]
            )
            return video
        
    # get all videos from filename
    # @staticmethod
    # def get_all_videos(filename = "videos.json"):
    #     # if not os.path.exists(filename):
    #     #     with open(filename, "w") as f:
    #     #         f.write("{}")
    #     #     return None

    #     with open(filename, "r") as f:
    #         videos = json.load(f)
    #         video_list = []
    #         for videoid in videos:
    #             video_list.append(Video.get_video(videoid))
    #         logger.critical(f"Found {len(video_list)} videos in {filename}")
    #         # logger.critical(f"Videos: {video_list[0].to_dict()}")
    #         return video_list
                
                
    @staticmethod
    def get_all_videos(filename="videos.json"):
        with open(filename, 'r') as f:
            videos_data = json.load(f)

        videos = []
        for videoid, video_data in videos_data.items():
            video = Video.from_dict(video_data)
            videos.append(video)

        return videos
            
    

    # same as above but with try/except 
    @staticmethod
    def get_video_by_id(videoid, filename="videos.json"):
        try:
            with open(filename) as f:
                videos = json.load(f)
        except FileNotFoundError:
            with open(filename, 'w') as f:
                f.write("{}")
            videos = {}

        video_data = videos.get(videoid, None)
        if video_data:
            return Video(**video_data)
        else:
            return None

        

    @staticmethod
    def from_reddit_reels(reddit_reels: RedditReels):
        day = date.today().strftime("%d")
        day = str(int(day)) + GetDaySuffix(int(day))
        dt_date = date.today().strftime("%A %B") + f" {day}"

        dt_string = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        dt_date = datetime.date.today().strftime("%A %B") + f" {day}"
        

        file = f"{reddit_reels.post_data[0]['id']}.mp4"
        title = f"{reddit_reels.post_data[0]['title']} - Dankest memes {dt_date}!"
        description = "#shorts\nGiving you the hottest memes of the day!"
        keywords = f'meme,reddit,Dankestmemes,{reddit_reels.sreddit}'
        privacyStatus = "private"
        videoid = f"{reddit_reels.post_data[0]['id']}"
        uploaded = False
        ytvideolink = "none"
        timestamp = dt_string

        video = Video(file, title, description, keywords, privacyStatus, videoid, uploaded, ytvideolink, timestamp)

        return video

    @staticmethod
    def update_uploaded_and_link(videoid, uploaded, ytvideolink, filename="videos.json"):
        logger.critical(f"Updating {videoid} with uploaded: {uploaded} and ytvideolink: {ytvideolink}")
        with open(filename, "r+") as f:
            data = json.load(f)
            video_data = data.get(videoid, {})
            video_data["uploaded"] = uploaded
            video_data["ytvideolink"] = ytvideolink
            data[videoid] = video_data
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()
            
    @staticmethod
    def from_dict(video_dict):
        video = Video(
            file = video_dict["file"],
            title = video_dict["title"],
            description = video_dict["description"],
            keywords = video_dict["keywords"],
            privacyStatus = video_dict["privacyStatus"],
            videoid = video_dict["videoid"],
            uploaded = video_dict["uploaded"],
            timestamp = video_dict["timestamp"],
            ytvideolink = video_dict["ytvideolink"]
        )
        return video

    @staticmethod
    def delete_video_data(videoid, filename="videos.json"):
        try:
            with open(filename) as f:
                videos = json.load(f)
        except FileNotFoundError:
            print(f"{filename} file not found.")
            return

        if videoid not in videos:
            print(f"No video with videoid {videoid} found in {filename}")
            return

        del videos[videoid]
        Video.delete_video(videoid)
        with open(filename, 'w') as f:
            json.dump(videos, f)
        print(f"{videoid} deleted from {filename} file.")

    @staticmethod
    def delete_video(videoid, folder="./"):
        filename = folder + videoid + ".mp4"
        try:
            os.remove(filename)
            return True
        except FileNotFoundError:
            return False

