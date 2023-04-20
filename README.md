# RedditReels
##### Automatic Video with Reddit Memes in 5 Minutes !!! 
----
A software that make videos by taking content from reddit posts and upload on YouTube.


### Project launch plan
- [ ] Add payment gateway to the website.
- [ ] Use Product Hunt to launch the website.
- [ ] Get a good Domain name from GitHub Student Developer Pack.
- [ ] Use Free Tier of AWS to host the website.

    Use other free services like MongoDB Atlas, SendGrid, etc.
- [ ] Improve [RedditVideoMaker](https://github.com/elebumm/RedditVideoMakerBot) to add all the features of [RedditReels](https://github.com/hardik88t/RedditReels) and make it a web application.


### New Features To add 
<!-- todo check box in markdown -->
- [ ] Add feature to make video with multiple subreddits.
            
    For example, if you want to make a video with memes from r/memes and r/dankmemes, you can add both subreddits and the video will be made with content from both subreddits.
- [ ] Add more social Media Platforms to upload the video.
            
            
    YouTube, Instagram, TikTok(and similar apps), Facebook, Twitter, Reddit, Dailymotion, Vine, and more.

- [ ] Add more Source social media platforms to get content from.

    Reddit, Instagram, TikTok, Facebook, Twitter, Pinterest, Tumblr, LinkedIn, Vimeo, Dailymotion, Imgur, Flickr, Gfycat, Streamable, Vine, Imgflip, Giphy, Tenor, and more.
- [ ] Add feature to help manually upload video to website like YouTube.
- [ ] Improve the UI of the website.

### Future Plans
- [ ] Use Product Hunt API to get trending products and make a video with them.
- [ ] Explore other APIs to get content from.




##### Make Video with Reddit Memes in 5 Minutes !!! 

# Guide for RedditReels Web Application

**Introduction**
-----

- This tool can be used to make and upload contents automatically from anywhere.It will only require effort until setting it up and can be used easily with web interface.

- It is intended for Content Creators.Which can be used to automate making of videos from contents from Reddit, and upload it on YouTube.

---------------------
---------------------


# Guide for RedditReels Web Application

RedditReels is a Python-based web application that enables users to create Instagram reels or YouTube shorts by combining memes and adding background music. This guide provides an overview of the application's functionality and instructions on how to use it effectively.

## Technologies Used

RedditReels uses the Flask web framework and is built with Python. It also integrates with the Reddit API to obtain memes and their top comments. The application uses the moviepy library to create videos by combining memes and adding background music. Finally, it uses the YouTube Data API to upload videos directly to YouTube.

## Functionality

Follow these steps to use RedditReels:

1. Login to the application OR create a new account.
2. Add your Reddit and YouTube account credentials. 
    - To get Reddit API credentials, follow the instructions in this article: [How to Use the Reddit API in Python](https://towardsdatascience.com/how-to-use-the-reddit-api-in-python-5e05ddfd1e5c)
    - To Get your YouTube API key, follow the instructions in this video tutorial: [How to Get YouTube API Key](https://www.youtube.com/watch?v=yuM7KH-JLu8&feature=youtu.be&ab_channel=DAIMTODeveloperTips)

            There is already a YouTube account and API key added to the application. 
            You can use it to test the application. 
            However, if you want to upload videos to your own YouTube account, you will need to add your own credentials.

3. Enter the subreddit name from which you want to obtain memes. 


    - For Example (memes, dankmemes, raimimemes, historymemes, okbuddyretard, comedyheaven).

4. Click the "Create Video" button and wait for the video to be generated. Video generation can take up to 5 minutes.
5. View all videos details (video title, description, and tags), and play them by clicking the "Play" button.
6. Click the "Upload to YouTube" button to upload the video directly to your YouTube account.
7. You can also download the video to your computer by clicking the "Download" on the Video played.
8. You can also delete the video by clicking the "Delete" button on the Video played.


## Conclusion

RedditReels is an easy-to-use and powerful web application that simplifies the process of creating engaging videos for social media. By integrating with popular APIs such as Reddit and YouTube, RedditReels makes it easy to find and use high-quality content to create your videos. Whether you're an influencer or just looking to make some fun videos to share with your friends, RedditReels is the perfect tool for you.
