import os
import json
from models.Video import Video
from models.Logger import logger

# import RedditCredentials
from utils.CreateMovie import CreateMovie
from utils.RedditReels import RedditReels
from utils.upload_video import upload_video,ytvideolink
from utils.shared import ytvideolink, errorMSG

class User:
    def __init__(self, username, password, email, isdeleted=False):
        self.username = username
        self.password = password
        self.email = email
        self.isdeleted = isdeleted
        self.foldername = f"Users/{self.username}"
        # self.appname = f"{self.foldername}/{self.username}.py"
        # self.videofile = f"{self.foldername}/videos.json"
        # self.redditfile = f"{self.foldername}/reddit.json"
        # self.client_secrets = f"{self.foldername}/client_secrets.json" 
    # class constructor
        
    @classmethod
    def from_dict(cls, user_dict):
        return cls(
            username=user_dict.get("username", ""),
            password=user_dict.get("password", ""),
            email=user_dict.get("email", ""),
            isdeleted=user_dict.get("isdeleted", False)
        )
    # gives the user the ability to create a new user from a dictionary

    @staticmethod
    def get_users(filename = "users.json"):
        try:
            with open(filename, "r") as f:
                users = json.load(f)
        except FileNotFoundError:
            users = []
        return [User.from_dict(user_dict) for user_dict in users]
    # gets all the users from the file specified
    
    # checks if self.username exists already and if not saves the user to the file specified
    
    def already_exists(self, filename = "users.json"):
        users = User.get_users(filename)
        for user in users:
            if user.username == self.username:
                return True
        return False

    @staticmethod
    def save_users(users, filename = "users.json"):
        with open(filename, "w") as f:
            users_dict = [vars(user) for user in users]
            json.dump(users_dict, f, indent=4)
    # saves all the users to the file specified

    def save(self, filename = "users.json"):
        if not os.path.exists(filename):
            with open(filename, "w") as f:
                f.write("[]")

        with open(filename, "r+") as f:
            data = json.load(f)
            for i, user in enumerate(data):
                if user["username"] == self.username:
                    data[i] = self.__dict__
                    break
            else:
                data.append(self.__dict__)

            f.seek(0)
            json.dump(data, f, indent=4)

        # self.create_user_folders()
    # saves the user to the file specified


                

    @staticmethod
    def get_user_by_username(username, filename = "users.json"):
        with open(filename, "r") as f:
            data = json.load(f)
            for user_dict in data:
                if user_dict["username"] == username:
                    return User(username=user_dict['username'], password=user_dict['password'],
                            email=user_dict['email'], isdeleted=user_dict['isdeleted'])

        return None
    # gets a user by their username
    
    @staticmethod
    def from_file(username, filename):
        with open(filename) as f:
            data = json.load(f)
            if username in data:
                user_data = data[username]
                return User(username=user_data['username'], password=user_data['password'],
                            email=user_data['email'], isdeleted=user_data['isdeleted'])
            else:
                raise ValueError(f"User with username {username} not found in file {filename}")


    def save_data(self, file_name = "users.json"):
        users_data = []
        if os.path.exists(file_name):
            with open(file_name, "r") as f:
                users_data = json.load(f)

        users_data.append({
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "isdeleted": self.isdeleted
        })

        with open(file_name, "w") as f:
            json.dump(users_data, f)
    # saves the user data to the file specified
                

    def create_user_space(self):
        user_folder_path = os.path.join("Users", self.username)
        os.makedirs(user_folder_path, exist_ok=True)
        videos_file_path = os.path.join(user_folder_path, "videos.json")
        reddit_key_path = os.path.join(user_folder_path, "reddit.json")
        if not os.path.exists(videos_file_path):
            with open(videos_file_path, "w") as f:
                json.dump({}, f)
        if not os.path.exists(reddit_key_path):
            with open(reddit_key_path, "w") as f:
                json.dump({}, f)
                
    @staticmethod
    def check_user_credentials(username, password, filename = "users.json"):
        user = User.get_user_by_username(username, filename)
        if user is None:
            return False
        if user.password == password:
            return True



    @staticmethod
    def make_new_video(username="videos", subreddit="memes", toupload=False): 

        logger.info("Starting to make new video!=================")
        user = User.get_user_by_username(username)
        logger.info("Done getting user!=========================")
        if user is None:
            return False # user does not exist
        redditReels = RedditReels()
        logger.info("Done creating RedditReels!==================")
        try:
            posts = redditReels.get_posts(sub=subreddit)
            logger.info("Done getting posts!========================")
            redditReels.create_data_folder()
            logger.info("Done creating folder!======================")
            for post in posts:
                redditReels.save_image(post)
            logger.info("Done saving images!========================")
            
            videoname = os.path.join(f'{redditReels.post_data[0]["id"]}.mp4')
            CreateMovie.CreateMP4(redditReels.post_data, savepath = user.foldername, vname=videoname)
            logger.info("Done creating video!=======================")
            
            newvideo = Video.from_reddit_reels(redditReels)
            print(newvideo.to_dict())
            path = os.path.join(user.foldername, "videos.json")
            # newvideo.save(path)
            newvideo.save_to_file(filename=path)
            logger.info("Done saving video!=========================")
            
            if toupload:
                try:
                    User.upload_the_video(username, newvideo.videoid)
                    logger.info("Done Making And uploading video!======================")
                except Exception as e:
                    logger.error(f"Error in uploading video: {e}")
                    return False
            return True
            
        except Exception as e:
            logger.error(f"========Error in making video: {e}")
            return False
        
    @staticmethod
    def upload_the_video(videoid, username = "videos"):
        user = User.get_user_by_username(username)
        if user is None:
            return False
        path = os.path.join(user.foldername, "videos.json")
        video_to_upload = Video.get_video_by_id(videoid, path)
        if video_to_upload is None:
            return False
        if video_to_upload.uploaded:
            logger.warning("Video already uploaded!====================")
            return False
        videopath = os.path.join(user.foldername, video_to_upload.file)
        upload_video(video_to_upload.to_dict(), path=videopath)
        # video_to_upload.uploaded = True
        # video_to_upload.ytvideolink = f"{ytvideolink}"
        # Video.update_uploaded_and_link(videoid=videoid, uploaded=True ,ytvideolink=ytvideolink, filename=path)
        return True
    
        
    @staticmethod
    def get_video(videoid, username = "videos"):
        # user = User.get_user_by_username(username)
        # if user is None:
        #     return False
        path = os.path.join(f"Users/{username}", "videos.json")
        return Video.get_video(videoid = videoid, filename = path)
    
    @staticmethod
    def get_all_videos(username = "videos"):
        # user = User.get_user_by_username(username)
        # if user is None:
        #     return False
        path = os.path.join(f"Users/{username}", "videos.json")
        videos = Video.get_all_videos(filename=path)
        # print(videos[1].to_dict())
        return videos
    
    @staticmethod
    def update_the_video(update_video : Video, username = "videos"):
        # user = User.get_user_by_username(username)
        # if user is None:
        #     return False
        logger.info("Here We Are!====================")
        path = os.path.join(f"Users/{username}", "videos.json")
        old_video = Video.get_video(videoid = update_video.videoid, filename = path)
        old_video.update_from_new_video(update_video)
        # save_video_data(old_video)
        old_video.save_to_file(filename=path)
        logger.info("Done updating video!====================")

    @staticmethod
    def delete_the_video(videoid, username = "videos"):
        # user = User.get_user_by_username(username)
        # if user is None:
        #     return False
        path = os.path.join(f"Users/{username}", "videos.json")
        video_to_delete = Video.delete_video_data(videoid = videoid, filename = path)
        logger.info("Done deleting video!====================")