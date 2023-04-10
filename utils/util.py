from functools import wraps
from flask import redirect, url_for, session

from models.Video import Video
from models.Logger import logger
from utils.RedditReels import RedditReels

# NUM_VIDEOS_TO_CREATE = 1
# VIDEOS_JSON_FILE_PATH = os.path.join("static/videos", "videos.json")
# VIDEOS_MP4_FILE_PATH = os.path.join("static/videos")
# logger = Logger(log_file='utils.log')

# def update_path():
#     global VIDEOS_JSON_FILE_PATH
#     global VIDEOS_MP4_FILE_PATH
#     VIDEOS_JSON_FILE_PATH = os.path.join(f'static/{session["username"]}', "videos.json")
#     VIDEOS_MP4_FILE_PATH = os.path.join(f'static/{session["username"]}')
#     print(f"JSON : {VIDEOS_JSON_FILE_PATH} ")
#     print(f"MP4  : {VIDEOS_MP4_FILE_PATH} ")


def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if 'username' in session:
            # update_path()
            logger.debug(f"Decorator : Logged in=================================={session['username']}")
        if 'username' not in session:
            logger.info("Decorator : Not logged in=====================")
            return redirect(url_for('view.login'))
        return view(**kwargs)
    return wrapped_view

def already_logged_in(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' in session:
            logger.info("Decorator : Already logged in=====================")
            return redirect(url_for('view.index'))
        return f(*args, **kwargs)
    return decorated_function


# def update_video_async(update_video: Video, uname="videos"):
#     old_video = Video.get_video(update_video.videoid, uname.)
#     old_video.update_from_new_video(update_video)
#     # save_video_data(old_video)
#     old_video.save_to_file()
#     logger.info("Done updating video!====================")

# def upload_video_async(videoid):
#     videodata = Video.get_video(videoid,True)
#     print("Video data:=====================")
#     print(videodata.to_dict())
#     videopath = os.path.join(VIDEOS_MP4_FILE_PATH, videodata.videoid + ".mp4")
#     if videodata.uploaded:
#         logger.warning("Video already uploaded!====================")
#         return {"status": "error", "message": "Video already uploaded"}
#     else:
#         msg = upload_video(videodata.to_dict(),path = videopath)
#         videodata.uploaded = True
#         videodata.ytvideolink = ytvideolink
#         # save_video_data(videodata)
#         videodata.save_to_file()
#         logger.info(f"Done uploading video to YT! : {ytvideolink}====================")
#     print("Video data:=====================")
#     print(videodata.to_dict())
#     if msg:
#         return msg
#     return {"status": "success", "data": videodata.to_dict()}

    


# def create_video(subreddit="memes", toupload=False, uname="videos"):
#     redditReels = RedditReels()
#     # uname = session['username']
#     logger.info(f"Creating video for ===================={uname}====================")
#     # Gets our new posts pass if image related subs. Default is memes
#     try:
#         posts = redditReels.get_posts(sub=subreddit)
#         logger.info("Done getting posts!========================")
#         redditReels.create_data_folder()
#         logger.info("Done creating folder!======================")
#         for post in posts:
#             redditReels.save_image(post)
#         logger.info("Done saving images!========================")
        
        
        
#         # Create movie
#         path = os.path.join(f"{redditReels.post_data[0]['id']}.mp4")
#         CreateMovie.CreateMP4(redditReels.post_data, savepath=VIDEOS_MP4_FILE_PATH, vname=path)
#         videopath = os.path.join(VIDEOS_MP4_FILE_PATH, path)
#         logger.info("Done creating movie!=======================")
#         logger.info(f"Data saved as : {VIDEOS_MP4_FILE_PATH}.{path}")
        
        
#         video_data = Video()
#         video_data.from_reddit_reels(redditReels)
#         # video_data.update_from_new_video(new_video)
#         print("\n\n Video Final Data :")
#         print(video_data.to_dict())
#         # Write video data to JSON file
#         # save_video_data(video_data)
#         video_data.save_to_file()

#         if toupload:
#             try:
#                 logger.info("===================Uploading After Making video...")
#                 upload_video(video_data.to_dict(), path=videopath)
#                 video_data.uploaded = True
#                 video_data.ytvideolink = ytvideolink
#                 # save_video_data(video_data)
#                 video_data.save_to_file()
#                 logger.info(f"=================== video uploaded! : {ytvideolink}")
#             except Exception as e:
#                 logger.error(f"===================Error uploading video : {e}")
#         return video_data.to_dict()
#     except Exception as e:
#         logger.error(f"=======================ERROR HERE================================")
#         logger.error(f"Error in create_video : {e}")
#         return e

        
# def save_video_data(video_data: Video):
#     logger.info("Saving video data to file...")
#     try:
#         os.makedirs(os.path.dirname(VIDEOS_JSON_FILE_PATH), exist_ok=True)
#         with open(VIDEOS_JSON_FILE_PATH, "r") as json_file:
#             existing_data = json.load(json_file)
#     except (FileNotFoundError, json.JSONDecodeError):
#         existing_data = {}
#         logger.error("Error: File not found or JSONDecodeError!")
        
#     existing_data[video_data.videoid] = video_data.to_dict()

#     try:
#         with open(VIDEOS_JSON_FILE_PATH, "w") as json_file:
#             json.dump(existing_data, json_file)
#     except PermissionError:
#         logger.error(f"Error: Could not write to {VIDEOS_JSON_FILE_PATH}")
#     print("Done saving video data to file!")



# def get_video_data():
#     existing_data = []
#     try:
#         os.makedirs(os.path.dirname(VIDEOS_JSON_FILE_PATH), exist_ok=True)
#         with open(VIDEOS_JSON_FILE_PATH, "r") as json_file:
#             data = json.load(json_file)
#         for videoid, info in data.items():
#             existing_data.append(info)
#         # return json.dumps(existing_data)
#         return existing_data
#     except FileNotFoundError:
#         logger.error("Error: File not found!")
#         # create empty file
#         with open(VIDEOS_JSON_FILE_PATH, "w") as json_file:
#             json.dump(existing_data, json_file)
#         return existing_data    
#     except json.JSONDecodeError:
#         existing_data = []
#         logger.error("Error: JSONDecodeError!")
#         return existing_data

    

# def get_video(videoid, inVideo = False):
#     logger.info("Getting video data ...")
#     try:
#         os.makedirs(os.path.dirname(VIDEOS_JSON_FILE_PATH), exist_ok=True)
#         with open(VIDEOS_JSON_FILE_PATH, "r") as json_file:
#             data = json.load(json_file)
#         info = data[videoid]
#         video_data = Video(
#                 file = info["file"],
#                 title = info["title"],
#                 description = info["description"],
#                 keywords = info["keywords"],
#                 privacyStatus = info["privacyStatus"],
#                 videoid = info["videoid"],
#                 uploaded = info["uploaded"],
#                 ytvideolink = info["ytvideolink"],
#                 timestamp = info["timestamp"]
#             )
#         logger.info("Done getting video data!")
#         print(video_data.to_dict())
#         return video_data
#     except (FileNotFoundError, json.JSONDecodeError):
#         data = {}
#         logger.error("Error: File not found or JSONDecodeError!")
#         return None
#     except KeyError:
#         logger.error("Error: Video not found!")
#         return None


# def delete_video_async(videoid):
#     logger.info("Deleting video data ...")
#     try:
#         os.makedirs(os.path.dirname(VIDEOS_JSON_FILE_PATH), exist_ok=True)
#         with open(VIDEOS_JSON_FILE_PATH, "r") as json_file:
#             data = json.load(json_file)
#         print(data[videoid])
#         del data[videoid]
#         with open(VIDEOS_JSON_FILE_PATH, "w") as json_file:
#             json.dump(data, json_file)
#         logger.info("Done deleting video data!")
#         delete_video_mp4(videoid)
#         return {"status": "success"}
#     except (FileNotFoundError, json.JSONDecodeError):
#         data = {}
#         logger.error("Error: File not found or JSONDecodeError!")
#     except KeyError:
#         logger.error("Error: Video not found!")
        
# def delete_video_mp4(videoid):
#     logger.error(f"Deleting video 'static/{session['username']}/{videoid}.mp4 ...")
#     try:
#         os.makedirs(os.path.dirname(VIDEOS_JSON_FILE_PATH), exist_ok=True)
#         os.remove(os.path.join(VIDEOS_MP4_FILE_PATH, videoid + ".mp4"))
#         logger.info("Done deleting video data!")
#         return {"status": "success"}
#     except (FileNotFoundError):
#         data = {}
#         logger.error("Error: File not found")
#         return {"status": "error"}

