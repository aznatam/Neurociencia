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

while 1:
    frame = get_depth()
    cv.ShowImage('Depth', frame)
    cv.ShowImage('Video', get_video())
    if cv.WaitKey(20) == 27:
        break

freenect.sync_stop
del writer
