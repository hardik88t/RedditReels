import json
from flask import (
    Blueprint,
    redirect,
    request,
    session,
    url_for,
)
from models.Logger import logger
from models.User import User
from utils.util import (
    already_logged_in,
    login_required,
)
# DONE
# AUTH ==========================================================================
auth = Blueprint("auth", __name__)



@auth.route('/login', methods=['POST'])
@already_logged_in
def auth_login():
    # get the form data submitted by the user
    username = request.form['username']
    password = request.form['password']
    print(username)
    print(password)
    # check if the user is valid (you will need to implement your own logic here)
    if User.check_user_credentials(username, password):
        # if the user is valid, set the session variables
        session['username'] = username
        session['logged_in'] = True
        logger.info("Logged in ============================================")
        # redirect the user to the home page or another protected page
        return redirect(url_for('view.index'))
    else:
        # if the user is not valid, show an error message
        error = 'Invalid credentials. Please try again.'
        logger.error("Not Logged in ============================================")
        return redirect(url_for('view.login', error=error))



# @auth.route('/signup', methods=['POST'])
# @already_logged_in
# def auth_signup():
#     # get the form data from the request
#     username = request.form['username']
#     email = request.form['email']
#     password = request.form['password']
#     password2 = request.form['password']
#     # password2 = request.form['password2']

#     # check if the passwords match
#     if password != password2:
#         error = 'Passwords do not match'
#         logger.info("Passwords do not match =========================================")
#         return redirect(url_for('signup', error=error))

#     # check if the username is already taken
#     with open('users.json', 'r') as f:
#         users = json.load(f)

#     for user in users:
#         if user['username'] == username:
#             error = 'Username is already taken !!!'
#             logger.info("Username is already taken====================================")
#             return redirect(url_for('signup', error=error))

#     # create a new user object
#     new_user = {
#         'username': username,
#         'email': email,
#         'password': password
#     }

#     # add the new user to the users list and save to file
#     users.append(new_user)

#     with open('users.json', 'w') as f:
#         json.dump(users, f)

#     # set the session variable and redirect to the home page
#     session['username'] = username
#     logger.info("User created =========================================")
#     return redirect(url_for('index'))


@auth.route('/signup', methods=['POST'])
@already_logged_in
def auth_signup():
    # get the form data from the request
    # make User object
    
    new_user = User(    
        username = request.form['username'],
        email = request.form['email'],
        password = request.form['password'],
    )
    password2 = request.form['password']
    # password2 = request.form['password2']

    # check if the passwords match
    if new_user.password != password2:
        error = 'Passwords do not match!!!'
        logger.info("Passwords do not match =========================================")
        return redirect(url_for('view.signup', error=error))

    # check if the username is already taken
    if new_user.already_exists():
        error = 'Username is already taken !!!'
        logger.info("Username is already taken====================================")
        return redirect(url_for('view.signup', error=error))

    # add the new user to the users list and save to file
    new_user.save()

    # set the session variable and redirect to the home page
    session['username'] = new_user.username

    # create user space
    new_user.create_user_space()

    logger.info("User created =========================================")
    return redirect(url_for('view.index'))



@auth.route('/logout')
@login_required
def auth_logout():
    logger.info("Logging out =====================================")
    session.clear()
    return redirect(url_for('view.login'))
