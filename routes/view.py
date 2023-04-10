import json
import os

from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from models.Logger import logger
from models.RedditCredentials import RedditCredentials
from models.Video import Video
from models.User import User
from utils.util import (
    already_logged_in,
    login_required,
)



# DONE
# VIEW ==========================================================================
view = Blueprint("view", __name__)


# DONE
@view.route('/')
@login_required
def index():
    errorMSG = request.args.get('error')
    successMSG = request.args.get('success')
    with open("markdown/guid.md", "r") as file:
        mkdown = file.read()
    
    logger.info("=================Index===========================")
    # senf markdown to template
    return render_template('index.html', mkdown=mkdown, error=errorMSG, success=successMSG)

# DONE
@view.route('/index')
@login_required
def toindex():
    logger.info("=================To Index===========================")
    errorMSG = request.args.get('error')
    successMSG = request.args.get('success')
    return redirect(url_for("index"), error=errorMSG, success=successMSG)
    
# 
@view.route('/secrets')
@login_required
def secrets():    
    try:
        rCred = RedditCredentials()
        # print(rCred)
        rCred.update_from_env()
        with open('client_secrets.json', 'r') as f:
            ytdataapicredentials = json.load(f)
        # print(ytdataapicredentials["installed"]["client_id"])
        logger.info("=================Secrets===========================")
        
        return render_template('secrets.html',
                                redditdata = rCred,
                                ytdata=ytdataapicredentials
                                )
    except:
        error = "Error in secrets"
        # flash(error, 'error')
        logger.error("Error in secrets========================")
        return redirect(url_for("view.addkeys"))
    

@view.route('/addkeys')
@login_required
def addkeys():
    rCred = RedditCredentials(
        client_id = os.getenv("client_id"),
        client_secret = os.getenv("client_secret"),
        username = os.getenv("username"),
        user_agent = os.getenv("user_agent"),
        password = os.getenv("password"),
        twofa= os.getenv("2fa") == "true"
    )
    
    with open("markdown/addkeys.md", "r") as file:
        mkdown = file.read()

    
    try:
        rCred.update_from_env()
        
        with open('client_secrets.json', 'r') as f:
            ytdataapicredentials = json.load(f)

        error = request.args.get('error')
        logger.info("=================Add Keys===========================")
        return render_template('addkeys.html', error=error, redditdata = rCred, ytdata=ytdataapicredentials, mkdown=mkdown)
    except:
        return render_template('addkeys.html', error="Error in addkeys", redditdata = rCred, ytdata=None, mkdown=mkdown)

# DONE
@view.route('/makevideo')
@login_required
def make_video():
    with open("markdown/newvideo.md", "r") as file:
        newvideomd = file.read()
    logger.info("=================Make Video===========================")
    return render_template('makevideo.html',newvideomd=newvideomd)


# DONE
@view.route('/updatevideo/<video_id>')
@login_required
def update_video(video_id):
    logger.info(f"=================Update Video {video_id}===========================")
    videoData= User.get_video(video_id, session["username"])
    return render_template('updatevideo.html',video_data = videoData.to_dict())


# DONE
@view.route('/videos')
@login_required
def videos():
    errorMSG = request.args.get('error')
    successMSG = request.args.get('success')
    logger.info("=================Videos===========================")
    # video_data = User.get_all_videos(session["username"])
    path = os.path.join("Users",session["username"])
    path = os.path.join(path,"videos.json")
    video_data = Video.get_all_videos(filename = path)
    # print(video_data[0].to_dict())
    return render_template('videos.html',video_data = video_data,error=errorMSG,success=successMSG)

@view.route('/video/<video_id>')
@login_required
def video(video_id):
    logger.info(f"=================See Video {video_id}===========================")
    videoData = User.get_video(video_id, session["username"])
    if videoData is None:
        errorMSG = 'this video does not exist : 404 error'
        return render_template('404.html',error=errorMSG), 404
    return render_template('video.html',video_data= videoData.to_dict() ,path = f"api/video/{video_id}")

# DONE
@view.route('/login')
@already_logged_in
def login():
    errorMSG = request.args.get('error')
    logger.info("=================Login===========================")
    return render_template('login.html', error=errorMSG)

# DONE
@view.route('/signup')
@already_logged_in
def signup():
    errorMSG = request.args.get('error')
    logger.info("=================Signup===========================")
    return render_template('signup.html', error=errorMSG)

