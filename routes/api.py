from concurrent.futures import ThreadPoolExecutor
import json
from flask import (
    Blueprint,
    jsonify,
    redirect,
    request,
    session,
    url_for,
    send_file,
)

# from flask_login import login_user, logout_user, login_required

from models.Logger import logger
from models.RedditCredentials import RedditCredentials
from models.Video import Video
from models.User import User
from utils.util import login_required



# API ==========================================================================
api = Blueprint("api", __name__)


# 
@api.route('/keys', methods=['POST'])
@login_required
def api_keys():
    logger.info("Adding API Keys =====================================")
    # Create a RedditCredentials object
    try:
        redditCredential = RedditCredentials(
            client_id = request.form['client_id'],
            client_secret = request.form['client_secret'],
            user_agent = request.form['user_agent'],
            username = request.form['user_agent'],
            password = request.form['password'],
            twofa= "false"
        )
        ytdataapicerdentials = request.form['ytdata']
        # secret = from_ytdata(ytdataapicerdentials)
        
        print(redditCredential)
        # Save the credentials to a file
        # redditCredential.save_to_file(".env")
        

        
        # secret.save_to_file("client_secrets.json")
        with open("client_secrets.json", 'w') as f:
            json.dump(ytdataapicerdentials, f)
            
        # redditCredential.save_to_file(".env")
        with open(".env", "w") as file:
            file.write(f"client_id=\"{redditCredential.client_id}\"\n")
            file.write(f"client_secret=\"{redditCredential.client_secret}\"\n")
            file.write(f"username=\"{redditCredential.username}\"\n")
            file.write(f"user_agent=\"{redditCredential.user_agent}\"\n")
            file.write(f"password=\"{redditCredential.password}\"\n")
            file.write(f"2fa=\"{redditCredential.twofa}\"")

        logger.info("Keys Added =====================================")
        return redirect(url_for("view.secrets"))
    except Exception as e:
        logger.error("Error in adding keys =====================================")
        return redirect(url_for("view.addkeys", error=str(e)))


# DONE
@api.route('/video', methods=['GET'])
@login_required
def api_video():
    logger.info("All Videos =====================================")
    data = User.get_all_videos(session["username"])
    # return redirect(url_for("view.videos"),Response=jsonify(data))
    return jsonify(data)

# DONE
@api.route('/video', methods=['POST'])
@login_required
def api_create_video():
    toyt = request.form.get('toyt')
    toup = False
    if toyt == "on":
        toup = True
    
    logger.critical(f"toyt ==========UPLOADTOYT======== {toyt}")
    print("Creating Video =====================================")
    subreddit = request.form.get('subreddit') or "memes"
    logger.info("API Create Video With Input ============================")
    executor = ThreadPoolExecutor()
    executor.submit(User.make_new_video, session['username'], subreddit, toup)
    successMSG = "Video is being created"    
    return redirect(url_for("view.index", success=successMSG))

# DONE
@api.route('/video/<videoid>', methods=['GET'])
def api_get_video(videoid):
    logger.info("Getting Video MP4 =====================================")
    video_path = f'Users/{session["username"]}/{videoid}.mp4'
    return send_file(video_path, mimetype='video/mp4')


# DONE
@api.route('/upload/<video_id>')
@login_required
def api_upload_video(video_id):
    logger.info("Uploading Video =====================================")
    executor = ThreadPoolExecutor()
    executor.submit(User.upload_the_video,video_id,session['username'])
    successMsg = "Video is being uploaded"
    return redirect(url_for("view.videos", success=successMsg))

# DONE
@api.route('/update/<video_id>', methods=['POST'])
@login_required
def api_update_video(video_id):
    logger.info("Updating Video =====================================")
    newVideo = Video(
        title = request.form['title'],
        description = request.form['description'],
        keywords = request.form['keywords'],
        privacyStatus = request.form['privacyStatus'],
        videoid=video_id
    )
    User.update_the_video(newVideo,session['username'])
    return redirect(url_for("view.videos"))

# DONE
@api.route('/delete/<video_id>')
@login_required
def api_delete_video(video_id):
    logger.info("Deleting Video =====================================")
    executor = ThreadPoolExecutor()
    executor.submit(User.delete_the_video, video_id, session['username'])
    return redirect(url_for("view.videos", success="Video is being deleted"))
