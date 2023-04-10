# RedditReels
My software that make videos by taking content from reddit posts. 


# YouTube Video / Shorts Maker


## Software Requirement Specification (SRS)

## Project Title:  RedditReels


    NAME        	: Hardik Thanth
    Roll No.    	: CE162
    ID          	: 19CEUBS082
    Sem         	: 6
    Subject     	: SDP
    Batch       	: B4
    Aim         	: Write SRS for Project Video making Software
    Repository 	: https://github.com/hardik88t/RedditReels

**Introduction**
-----

   This document details the project plan for the development of “RedditReels”.
   
   This plan will include a summary of:
   
        •	how the system will function
        
        •	the scope of the project from the development viewpoint
        
        •	the technology used to develop the project, and
        
        •	the metrics used to determine the project’s progress
        
        •	Overall Description
        
  This tool can be used to make and upload contents automatically from anywhere. It will only require effort until setting it up and can be used easily with web interface.

**Intended Audience**
----

      The Users will be General public and Content Creators as anyone can use it easily.

**Intended Use**
----


      It is intended for Content Creators. Which can be used to automate making of videos from contents from Reddit, and upload it on YouTube.
      To be used to make videos.
   

**User Interfaces**
----


         •	Front-end software: React

         •	Back-end software: REST API in python


**Hardware Interfaces**
------


         All devices (Android, iPhone, Windows, Linux, Mac) through web browser


**Functional Requirements**
------

R1. Enter Credentials

       Description : 
         Provide the authentication information for APIs of Reddit and YouTube.
      
      Input : User Input

R2. Get Video Details
       
       Description : 
         Enter the details about the video including :
         -	Background video choice 
         -	Audio voice Choice
         -	Video Theme
         -	Video Length
         -	Content Selection
         -	Content Restriction
         -	Other control details
       
       Input : User Selection and Input with GUI

R3. Make Audio
      
       Description : 
         Make Audio for video from the text taken from Reddit.
       
       Input : Text and Audio voice chose
       
       Output :  Audio generated and saved in temp file

R4. Make Video Visual
   
       Description : 
         Make Visual By taking clip from Background and posting screen shots of content.

R5. Making Video
   
       Description : 
         Combine the audio with visuals with proper timing and create final video.

       Input : Audio clips and visual

       Output : Final video and deletion of temporary files

R6. Upload Video
        
        Description : 
         Upload the video to YouTube via YouTube API.
        
        Input : Finished Video
        
        Output : Upload on YouTube


**Non-Functional Requirements**
-------


N.1 : Usability

      The interface should be easy to learn without a tutorial and allow users to accomplish their goals without errors.
      Good GUI and High performance in network traffic and stress testing.

N.2 : Security

      Can ensure and preserve information of users.

N.3 : Web-support

      It should be possible to access the system from any place by using a web browser.


## References   

- [Reddit API](https://www.reddit.com/dev/api/)
- [YouTube Data API](https://developers.google.com/youtube/v3)
- [Moviepy](https://zulko.github.io/moviepy/)
- [Flask](https://flask.palletsprojects.com/en/2.0.x/)
- [Python](https://www.python.org/)
- [Bootstrap](https://getbootstrap.com/)
- [HTML](https://www.w3schools.com/html/)
- [CSS](https://www.w3schools.com/css/)
- [JavaScript](https://www.w3schools.com/js/)
- [Jinja](https://jinja.palletsprojects.com/en/3.0.x/)
- [GitHub](https://github.com/)
- [Markdown](https://www.markdownguide.org/)
- [Google Fonts](https://fonts.google.com/)
- [Google Chrome](https://www.google.com/chrome/)
