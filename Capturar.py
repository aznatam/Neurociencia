import VideoReader
from socket import socket, AF_INET, SOCK_STREAM
import parallel
import time
import cv
import pygtk
import multiprocessing as mp
pygtk.require('2.0')
import gtk
from os import getcwd

RecordingEvent = mp.Event()
StopEvent = mp.Event()
Psychopy_file = ''
HOST = '192.168.0.101'
PORT = 15555

class MainWindow(gtk.Window):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.set_title("Captura NeuroCiencias")
        self.set_size_request(200, 100)
        self.set_position(gtk.WIN_POS_CENTER)

        #################################################################
        #################################################################
        #################                               #################
        #################           TOP MENU            #################
        #################                               #################
        #################################################################
        #################################################################
        # top level menu bar#{{{
        menubar = gtk.MenuBar()
        # top items on the menu bar
        filem = gtk.MenuItem("File")
        aboutm = gtk.MenuItem("About")

        # now, create for FILE item the menu
        filemenu = gtk.Menu()
        filem.set_submenu(filemenu)
        # create the items for File menu
        save = gtk.MenuItem("Save")
        save.connect("activate", self.fileSelected)
        filemenu.append(save)
        # separator
        separat = gtk.SeparatorMenuItem()
        filemenu.append(separat)
        # now, Quit item with accelerator and image
        # generic accelerator
        agr = gtk.AccelGroup()
        self.add_accel_group(agr)
        quitImg = gtk.ImageMenuItem(gtk.STOCK_QUIT, agr)
        key, mod = gtk.accelerator_parse("Q")
        quitImg.add_accelerator("activate", agr, key, mod, gtk.ACCEL_VISIBLE)
        filemenu.append(quitImg)
        # connect to Quit the activate event
        quitImg.connect("activate", gtk.main_quit)

        # now, create for ABOUT item the menu
        aboutmenu = gtk.Menu()
        aboutm.set_submenu(aboutmenu)
        # create the items for File menu
        help = gtk.MenuItem("Help")
        aboutmenu.append(help)

        # append the top items
        menubar.append(filem)
        menubar.append(aboutm)
        # pack in a vbox
        vbox = gtk.VBox(False, 2)
        vbox.pack_start(menubar, False, False, 0)

        # add the vbox to the window
        self.add(vbox)#}}}

        #################################################################
        #################################################################
        #################                               #################
        #################         MEDIA BUTTONS         #################
        #################                               #################
        #################################################################
        #################################################################

        hbox = gtk.HBox(False,2)
        hbox.show()

        # crear varias imagenes con datos de archivos y cargarlos
        image = gtk.Image()
        image.set_from_file("./Images/RecordOff.png")
        image.show()
        # un boton que cotenga el control de imagen
        self.buttonrec = gtk.Button()
        self.buttonrec.add(image)
        self.buttonrec.show()
        hbox.pack_start(self.buttonrec, False, False, 2)
        self.buttonrec.connect("clicked", self.record_clicked, "2")

        # crear varias imagenes con datos de archivos y cargarlos
        image = gtk.Image()
        image.set_from_file("./Images/Stop.png")
        image.show()
        # un boton que cotenga el control de imagen
        self.buttonstop = gtk.Button()
        self.buttonstop.add(image)
        self.buttonstop.show()
        self.buttonstop.set_sensitive(False)
        hbox.pack_start(self.buttonstop, False, False, 2)
        self.buttonstop.connect("clicked", self.stop_clicked, "2")
        # add the hbox to the window
        vbox.pack_start(hbox, False, False,5)

        self.connect("destroy", gtk.main_quit)
        self.show_all()


    def fileSelected(self, widget):
        global Psychopy_file
        dialog = gtk.FileChooserDialog("Save...", None, action=gtk.FILE_CHOOSER_ACTION_SAVE, buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_SAVE,gtk.RESPONSE_OK))
        dialog.set_default_response(gtk.RESPONSE_OK)
        dialog.set_current_folder(getcwd())
        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            Psychopy_file = dialog.get_filename()
            "Saving "+Psychopy_file
        dialog.destroy()

    def stop_clicked(self, widget, data=None):
        global StopEvent
        StopEvent.set()
        print "Stop"

    def record_clicked(self, widget, data=None):
        global RecordingEvent
        self.buttonstop.set_sensitive(True)
        RecordingEvent.set()
        print "Recording"

    def main(self):
        gtk.main()

    def destroy(self, widget, data=None):
        global StopEvent
        global RecordingEvent
        StopEvent.set()
        RecordingEvent.set()
        gtk.main_quit()

    def runCapture(self):
        global RecordingEvent
        global StopEvent

        p = parallel.Parallel()
        s = socket(AF_INET, SOCK_STREAM)
        s.connect((HOST, PORT))
        loop = True
        capture = cv.CaptureFromCAM(0)
        RecordingEvent.wait()
        width = int(cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_WIDTH))
        height = int(cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_HEIGHT))
        writer = cv.CreateVideoWriter("video-out.avi",cv.CV_FOURCC("F","L","V","1"),15,(width,height),1)
        p.setData(1)
        s.send('{"code":1,"time":"'+str(time.time())+'"}')

        mov=0
        while (loop):
            p.setData(250)
            frame = cv.QueryFrame(capture)
            p.setData(251)
            s.send('{"code":'+str(221+mov%20)+',"time":"'+str(time.time())+'"}')
            cv.WriteFrame(writer, frame)
            if StopEvent.is_set():
                loop = False
            mov = mov+1

        p.setData(2)
        s.send('{"code":2,"time":"'+str(time.time())+'"}')
        del writer
        s.close()

if __name__ == "__main__":
    principal = MainWindow()
    proceso = mp.Process(target=principal.main, args=())
    proceso.start()
    principal.runCapture()
