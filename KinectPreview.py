#!/usr/bin/env python
import freenect
import cv
import frame_convert

cv.NamedWindow('Depth')
cv.NamedWindow('Video')
print('Press ESC in window to stop')


def get_depth():
    return frame_convert.pretty_depth_cv(freenect.sync_get_depth()[0])


def get_video():
    return frame_convert.video_cv(freenect.sync_get_video()[0])


width = 640
height = 480
writer = cv.CreateVideoWriter("video-out.avi",cv.CV_FOURCC("F","L","V","1"),15,(width,height),1)

while 1:
    frame = get_depth()
    cv.ShowImage('Depth', frame)
    cv.ShowImage('Video', get_video())
    cv.WriteFrame(writer, frame)
    if cv.WaitKey(10) == 27:
        break
del writer
