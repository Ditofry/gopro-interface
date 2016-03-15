import sys
import cv2
import numpy
import subprocess as sp
from goprohero import GoProHero

# network check
print "Make sure you are connected to your GoPro's wireless network: http://gopro.com/help/articles/Solutions_Troubleshooting/GoPro-App-Camera-Connection-Troubleshooting"

goProPass = None
camera = None
WEBURL = "http://10.5.5.9:8080/"
FFMPEG_BIN = "ffmpeg"
# Establish connection
while goProPass == None:
    goProPass = raw_input("enter GoPro password: ")
    camera = GoProHero(password=goProPass)

def streamToOpenCV ():
    # http://zulko.github.io/blog/2013/09/27/read-and-write-video-frames-in-python-using-ffmpeg/
    VIDEO_URL = WEBURL + "live/amba.m3u8"

    cv2.namedWindow("GoPro",cv2.CV_WINDOW_AUTOSIZE)

    pipe = sp.Popen([ FFMPEG_BIN, "-i", VIDEO_URL,
               "-loglevel", "quiet", # no text output
               "-an",   # disable audio
               "-f", "image2pipe",
               "-pix_fmt", "bgr24",
               "-vcodec", "rawvideo", "-"],
               stdin = sp.PIPE, stdout = sp.PIPE)
    while True:
        raw_image = pipe.stdout.read(432*240*3) # read 432*240*3 bytes (= 1 frame)
        image =  numpy.fromstring(raw_image, dtype='uint8').reshape((240,432,3))
        cv2.imshow("GoPro",image)
        if cv2.waitKey(5) == 27:
            break
    cv2.destroyAllWindows()

# MATT's Messed up version
# while True
#     command = int(input("What woudl you like to do: "))
#     command_map = {
#         1: (camera.command, ('record', 'on')),
#         2: (camera.command, ('record', 'off')),
#         3: (camera.command, ('preview', 'on')),
#         4: (camera.command, ('preview', 'off')),
#         5: (camera.image, ()),
#         6: (streamToOpenCV, ()),
#     }
#     if command == 0:
#         break
#     fn, args = command_map[command]
#     fn(*args)


# Start interfaceing
while True:
    command = int(input("What would you like to do: "))
    if command == 0:
        break
    # cameraOpts.get(command)
    if command == 1:
        camera.command('record', 'on')
    elif command == 2:
        camera.command('record', 'off')
    elif command == 3:
        camera.command('preview', 'on')
    elif command == 4:
        camera.command('preview', 'off')
    elif command == 5:
        camera.image()
    elif command == 6:
        # http://zulko.github.io/blog/2013/09/27/read-and-write-video-frames-in-python-using-ffmpeg/
        VIDEO_URL = WEBURL + "live/amba.m3u8"

        cv2.namedWindow("GoPro",cv2.CV_WINDOW_AUTOSIZE)

        pipe = sp.Popen([ FFMPEG_BIN, "-i", VIDEO_URL,
                   "-loglevel", "quiet", # no text output
                   "-an",   # disable audio
                   "-f", "image2pipe",
                   "-pix_fmt", "bgr24",
                   "-vcodec", "rawvideo", "-"],
                   stdin = sp.PIPE, stdout = sp.PIPE)
        while True:
            raw_image = pipe.stdout.read(432*240*3) # read 432*240*3 bytes (= 1 frame)
            image =  numpy.fromstring(raw_image, dtype='uint8').reshape((240,432,3))
            cv2.imshow("GoPro",image)
            if cv2.waitKey(5) == 27:
                break
        cv2.destroyAllWindows()
    else:
        pass
