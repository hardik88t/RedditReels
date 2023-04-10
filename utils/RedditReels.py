from PIL import Image, ImageSequence
from datetime import date
import os
import praw
import requests
import json
from models.Logger import logger

class RedditReels():
    def __init__(self):
        print(f"RedditReels : {os.getenv('client_id')}")
        self.reddit = praw.Reddit(
            client_id=os.getenv('client_id'),
            client_secret=os.getenv('client_secret'),
            user_agent=os.getenv('user_agent'),
        )
        self.display_name = "memes"
        dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        self.data_path = os.path.join(dir_path, "data/")
        self.post_data = []
        self.sreddit = "memes"
        self.already_posted = []
        self.posted_already_path = os.path.join(
            self.data_path, "posted_already.json")
        if os.path.isfile(self.posted_already_path):
            with open(self.posted_already_path, "r") as file:
                self.already_posted = json.load(file)
                
    def get_posts(self, sub="memes"):
        logger.info("Getting posts from Reddit")
        self.post_data = []
        self.sreddit = sub
        self.display_name = sub
        subreddit = self.reddit.subreddit(sub)
        posts = []
        logger.info("................. posts from Reddit")
        
        for submission in subreddit.top("day", limit=100):
            if submission.stickied:
                logger.debug(f'Skipping mod post: {submission.title}')
                continue
            if submission.over_18:
                logger.debug(f'Skipping NSFW post: {submission.title}')
                continue
            if submission.id in self.already_posted:
                logger.debug(f'Skipping already posted post: {submission.title}')
                continue
            if any(ext in submission.url.lower() for ext in [".jpg", ".png", ".jpeg"]):
                logger.debug(f'Taking only-image post: {submission.title}')
                posts.append(submission)
                continue
        logger.info("DONE posts from Reddit")
        return posts
    
    
    def create_data_folder(self):
        today = date.today()
        dt_string = today.strftime("%m%d%Y")
        data_folder_path = os.path.join(self.data_path, f"{dt_string}/")
        check_folder = os.path.isdir(data_folder_path)
        if not check_folder:
            os.makedirs(data_folder_path)


    def save_image(self, submission,scale=(720, 1280)):
        try:
            dt_string = date.today().strftime("%m%d%Y")
            data_folder_path = os.path.join(self.data_path, f"{dt_string}/")
            check_folder = os.path.isdir(data_folder_path)
            if check_folder and len(self.post_data) < 5 and not submission.over_18 and submission.id not in self.already_posted:
                image_path = f"{data_folder_path}Post-{submission.id}{submission.url.lower()[-4:]}"
                response = requests.get(submission.url.lower())
                with open(image_path, 'wb') as f:
                    f.write(response.content)

                scale_gif(image_path, scale)


                submission.comment_sort = 'best'
                best_comment = None
                best_comment_2 = None

                for top_level_comment in submission.comments:
                    if len(top_level_comment.body) <= 140 and "http" not in top_level_comment.body:
                        if best_comment is None:
                            best_comment = top_level_comment
                        else:
                            best_comment_2 = top_level_comment
                            break

                best_comment.reply_sort = "top"
                best_comment.refresh()
                replies = best_comment.replies

                best_reply = None
                for top_level_comment in replies:
                    best_reply = top_level_comment
                    if len(best_reply.body) <= 140 and "http" not in best_reply.body:
                        break

                if best_reply is not None:
                    best_reply = best_reply.body
                else:
                    best_reply = "No Best Reply"
                    if best_comment_2 is not None:
                        best_reply = best_comment_2.body

                data_file = {
                    "image_path": image_path,
                    'id': submission.id,
                    "title": submission.title,
                    "score": submission.score,
                    "18": submission.over_18,
                    "Best_comment": best_comment.body,
                    "best_reply": best_reply
                }

                self.post_data.append(data_file)
                self.already_posted.append(submission.id)
                with open(f"{data_folder_path}{submission.id}.json", "w") as outfile:
                    json.dump(data_file, outfile)
                with open(self.posted_already_path, "w") as outfile:
                    json.dump(self.already_posted, outfile)
        except Exception as e:
            logger.critical(f"{e} ---> Error occurred while processing post {submission.id}.")

    
    
    
def scale_gif(path, scale=(720,1280), new_path=None):
    gif = Image.open(path)
    if not new_path:
        new_path = path
    if path[-3:] == "gif":
        old_gif_information = {
            'loop': bool(gif.info.get('loop', 1)),
            'duration': gif.info.get('duration', 40),
            'background': gif.info.get('background', 0),
            'disposal': gif.info.get('disposal', 1),
            'transparency': gif.info.get('transparency', None)
        }
        new_frames = get_new_frames(gif, scale)
        save_new_gif(new_frames, old_gif_information, new_path)
    else:
        gif = gif.resize(scale)
        gif.save(path)

def get_new_frames(gif, scale):
    new_frames = []
    for frame in enumerate(ImageSequence.Iterator(gif)):
        if frame.mode != 'RGB':
            frame = frame.convert('RGB')
        new_frame = Image.new('RGBA', gif.size)
        new_frame.paste(frame)
        new_frame = new_frame.resize(scale, Image.ANTIALIAS)
        new_frames.append(new_frame)
    return new_frames

def save_new_gif(new_frames, old_gif_information, new_path):
    new_frames = list(new_frames)
    new_frames[0].save(new_path,
                        save_all=True,
                        append_images=new_frames[1:],
                        duration=old_gif_information['duration'],
                        loop=old_gif_information['loop'],
                        background=old_gif_information['background'],
                        disposal=old_gif_information['disposal'],
                        transparency=old_gif_information['transparency'])

