import cv
import multiprocessing as mp
import sys
from datetime import timedelta
import pygtk
pygtk.require('2.0')

class Video_File:

    def __init__(self, filename = None, timestamp = None):
        self.filename = filename#{{{
        self.capture = None
        if filename != None:
            self.capture = cv.CreateFileCapture(self.filename)
            self.length = int(cv.GetCaptureProperty(self.capture,cv.CV_CAP_PROP_FRAME_COUNT))
            self.width = int(cv.GetCaptureProperty(self.capture,cv.CV_CAP_PROP_FRAME_WIDTH))
            self.height = int(cv.GetCaptureProperty(self.capture,cv.CV_CAP_PROP_FRAME_HEIGHT))
            self.fps = int(cv.GetCaptureProperty(self.capture,cv.CV_CAP_PROP_FPS))
            self.dur = timedelta(seconds=self.length/self.fps)
            self.cur = 1
        self.startRec = timestamp#}}}


    def setTime(self,time):
        self.startRec = time


    def getFrame(self):
        if self.capture :#{{{
            frame = cv.QueryFrame(self.capture)
            self.cur += 1
        else :
            frame = None
        return frame#}}}

    def currentFrame(self):
        if self.capture :#{{{
            return cv.GetCaptureProperty(self.capture,cv.CV_CAP_PROP_POS_FRAMES)
        else :
            return "--"#}}}

    def rewindFrame(self):
        if self.capture :#{{{
            cv.SetCaptureProperty(self.capture,cv.CV_CAP_PROP_POS_FRAMES,int(cv.GetCaptureProperty(self.capture,cv.CV_CAP_PROP_POS_FRAMES))-2)
            self.cur -= 2#}}}

    def fullRewindFrame(self):
        if self.capture :#{{{
            cv.SetCaptureProperty(self.capture,cv.CV_CAP_PROP_POS_FRAMES,0)
            self.cur = 1#}}}


    def fullForwardFrame(self):
        if self.capture :#{{{
            cv.SetCaptureProperty(self.capture,cv.CV_CAP_PROP_POS_FRAMES,int(cv.GetCaptureProperty(self.capture,cv.CV_CAP_PROP_FRAME_COUNT))-1)
            self.cur = self.length#}}}


    def getFrameAsPixbuf(self):
        frame = self.getFrame()#{{{
        if not frame:
            return None
        cv.CvtColor(frame, frame, cv.CV_BGR2RGB)
        return gtk.gdk.pixbuf_new_from_data(frame.tostring(), gtk.gdk.COLORSPACE_RGB,False, 8, frame.width, frame.height, frame.width*frame.nChannels)#}}}


    def display(self):
        print 'Loading video file "' + self.filename + '"...'#{{{
        try:
            capture = cv.CreateFileCapture(self.filename)
        except IOError:
            print 'Couldn\'t read movie file'
            sys.exit(0)
        cv.NamedWindow("Video", cv.CV_WINDOW_AUTOSIZE)
        loop = True
        while(loop):
            frame = cv.QueryFrame(capture)
            if (frame == None):
                break;
            cv.ShowImage("Video", frame)
            char = cv.WaitKey(33)
            if (char == 27):
                loop = False
        #cv.ReleaseCapture(capture)
        cv.DestroyWindow("Video")#}}}


def previewCamera(self):
    cv.NamedWindow("Preview", cv.CV_WINDOW_AUTOSIZE)#{{{
    capture = cv.CaptureFromCAM(0)
    loop = True
    while(loop):
        frame = cv.QueryFrame(capture)
        if (frame == None):
            break;
        cv.ShowImage("Preview", frame)
        char = cv.WaitKey(33)
        if (char == 27):
            loop = False
    cv.DestroyWindow("Preview")#}}}


def captureCamera(RecordingEvent, StopEvent, capture):
    loop = True#{{{
    RecordingEvent.wait()
    width = int(cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_WIDTH))
    height = int(cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_HEIGHT))
    writer = cv.CreateVideoWriter("out.avi",cv.CV_FOURCC('F', 'L', 'V', '1'),20.0,(width,height),1)

    while (loop):
        print StopEvent.is_set()
        frame = cv.QueryFrame(capture)
        print StopEvent.is_set()
        cv.WriteFrame(writer, frame);
        print StopEvent.is_set()
        if StopEvent.is_set():
            loop = False

    del writer#}}}


