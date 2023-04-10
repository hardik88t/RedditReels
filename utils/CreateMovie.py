from moviepy.editor import *
import random
import os
from models.Logger import logger

dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

def GetDaySuffix(day):
    if day == 1 or day == 21 or day == 31:
        return "st"
    elif day == 2 or day == 22:
        return "nd"
    elif day == 3 or day == 23:
        return "rd"
    else:
        return "th"

dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
music_path = os.path.join(dir_path, "Music/")

class CreateMovie():

    @classmethod
    def CreateMP4(cls, post_data, savepath="static/videos", vname="video.mp4"):
        try:
            clips = []
            for post in post_data:
                if "gif" not in post['image_path']:
                    clip = ImageSequenceClip([post['image_path']], durations=[12])
                else:
                    clip = VideoFileClip(post['image_path'])
                    clip_lengthener = [clip] * 60
                    clip = concatenate_videoclips(clip_lengthener)
                    clip = clip.subclip(0,12)
                clips.append(clip)
            
            # After we have out clip.
            clip = concatenate_videoclips(clips)

            # Hack to fix getting extra frame errors??
            clip = clip.subclip(0,60)

            music_file = os.path.join(music_path, f"music{random.randint(0,4)}.mp3")
            music = AudioFileClip(music_file)
            music = music.set_start((0,0))
            music = music.volumex(.4)
            music = music.set_duration(59)

            new_audioclip = CompositeAudioClip([music])
            clip.audio = new_audioclip
            
            if not os.path.exists(savepath):
                os.makedirs(savepath)
            path = os.path.join(savepath, vname)
            clip.write_videofile( path , fps=24)

        except Exception as e:
            print(f"Error: {e}")

# if __name__ == '__main__':
#     logger.debug(TextClip.list('color'))