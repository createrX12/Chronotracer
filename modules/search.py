# coding=utf-8
"""
@author B1lli
@date 2023年02月12日 16:01:22
@File:search.py
"""
from modules.db.save_to_sqlite import *
from moviepy.video.io.VideoFileClip import VideoFileClip
from modules.utils.multiprocesser import background_thread
import cv2
import numpy as np

@background_thread
def play_video(path,frame_indices):
    # Open the video file
    video = VideoFileClip(path)

    # Get the total number of frames in the video
    # total_frames = int(video.fps * video.duration)

    # Specify the frame indices that you want to play


    # Loop through the specified frames
    for frame_index in frame_indices:
        # Get the specified frame as a numpy array
        frame = video.get_frame(frame_index / video.fps)

        # Convert the frame from RGB to BGR format
        frame = frame[:, :, ::-1]

        # Display the frame
        cv2.imshow("Frame", frame)

        # Wait for the specified amount of time (in milliseconds)
        # cv2.waitKey(100)
        # Wait for a key press
        key = cv2.waitKey ( 100 )

        # Check if the key pressed is the spacebar
        if key == 32 :
            # Pause the video
            while True :
                # Wait for a key press
                key = cv2.waitKey ( 10 )

                # Check if the key pressed is the spacebar
                if key == 32 :
                    # Play the video
                    break

    # Close all OpenCV windows
    cv2.destroyAllWindows()

sql = Sqlite_interact()

def search_pic(pic_text=None,pic_date=None):
    # search_dict = {}
    results = sql.query_db('pic_data', {'pic_text' : f'{pic_text}','pic_date' : f'{pic_date}'},['pic_seq','pic_date','pic_resolution'])
    res_set = set()
    for result in results:
        res_set.add(result[2])
    for res in res_set:
        frame_lst = []
        for result in results :
            if result[2] == res:
                frame_lst.append ( result[0] )
        if pic_date :
            play_video ( rf"D:\ManicTime_Screenshots\{pic_date}_{res}.mp4", frame_lst )






#
# def show_result(result):
#     frame_lst = []
#     for i in result :
#         frame_lst.append ( i[0] )
#     play_video ( r"D:\ManicTime_Screenshots\2023-01-26_1920x1080.mp4", frame_lst )


if __name__ == '__main__':
    # frame_lst = []
    # result = sql.query_db('pic_data', {'pic_text' : f'','pic_date' : '2023-01-26'},['pic_seq','pic_date'])
    # for i in result :
    #     frame_lst.append ( i[0] )
    # play_video ( r"D:\ManicTime_Screenshots\2023-01-26_1920x1080.mp4", frame_lst )
    search('赵婉秋','2023-01-29')