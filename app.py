from flask import Flask
from flask_misaka import Misaka


from routes.auth import auth
from routes.api import api
from routes.view import view
from routes.error import error
from routes.admin import admin


# logger = Logger(log_file='app.log')


app = Flask(__name__)
app.secret_key = 'mysecretkey'
# app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=5)


Misaka(app) # For Markdown

# blueprint for root "/" view
app.register_blueprint(view, url_prefix="/")
app.register_blueprint(auth, url_prefix="/auth")
app.register_blueprint(api, url_prefix="/api")
app.register_blueprint(error, url_prefix="/error")
app.register_blueprint(admin, url_prefix="/admin")

@app.route('/test')
def test():
    return "Test"



# from flask import Flask, send_file, render_template

# app = Flask(__name__)
# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/<username>/<videoid>')
# def play_video(username, videoid):
#     video_path = f'Videos/{username}/{videoid}.mp4'
#     return send_file(video_path, mimetype='video/mp4')


# if __name__ == '__main__':
#     app.run(debug=True, port=5121)




# @app.before_first_request  # runs before FIRST request (only once)
# def make_session_permanent():
#     session.permanent = True
#     app.permanent_session_lifetime = timedelta(minutes=5)


if __name__ == "__main__":
    app.run(port=5555, debug=True)
    
