from BDFReader import *
from VideoReader import *
import pygtk
pygtk.require('2.0')
import gtk, gobject
import matplotlib
matplotlib.use('GTKAgg')
from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np
from os import getcwd
from datetime import timedelta
import multiprocessing as mp


videofile = Video_File()
lines = []
elines = []
validlines = []
evalidlines = []
StopEvent = True
canvas = None
inc = 10

class OptionsWindow:
    def __init__(self):
        self.BDF_file = BDF_File()
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title("Opciones")
        self.window.show()


class MainWindow:
    def __init__(self):
        global validlines
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_border_width(15)
        self.window.connect("destroy", self.destroy)
        self.window.set_title("Syncro NeuroCiencias")

        self.box = gtk.HBox(gtk.FALSE, 0)
        self.window.add(self.box)


        #################################################################
        #################################################################
        #################                               #################
        #################           EEG DATA            #################
        #################                               #################
        #################################################################
        #################################################################
        self.box1 = gtk.VBox(gtk.FALSE, 0)#{{{
        self.box1.set_border_width(5)
        self.box2 = gtk.HBox(gtk.FALSE, 0)
        self.box2.set_border_width(10)

        #Label de EEG
        self.label = gtk.Label("Seleccione un Archivo:")
        self.box2.pack_start(self.label, gtk.TRUE, gtk.TRUE, 0)
        self.label.show()

        #Boton para la carga del archivo BDF
        self.filechooserbutton = gtk.FileChooserButton("Abrir Archivo BDF ", None)
        self.filechooserbutton.connect("file-set", self.fileSelected)
        self.filechooserbutton.set_current_folder(getcwd()+'/data/eeg')
        filtro = gtk.FileFilter()
        filtro.set_name("BDF")
        filtro.add_pattern("*.bdf")
        self.filechooserbutton.set_filter(filtro)
        self.box2.pack_start(self.filechooserbutton, gtk.TRUE, gtk.TRUE, 0)
        self.filechooserbutton.show()
        self.box1.pack_start(self.box2, gtk.FALSE, gtk.FALSE, 0)
        self.box2.show()

        #Data de EEG
        self.box3 = gtk.HBox(gtk.FALSE, 0)
        self.box4 = gtk.VBox(gtk.FALSE, 0)
        self.box4.set_border_width(10)
        self.box5 = gtk.VBox(gtk.FALSE, 0)
        self.box5.set_border_width(10)

        self.label = gtk.Label("Startdate of recording: ")
        self.label_startRec = gtk.Label("--/--/-- --:--:--")
        self.label.set_alignment(xalign=0.0, yalign=0.5)
        self.label_startRec.set_alignment(xalign=0.0, yalign=0.5)
        self.box4.pack_start(self.label, gtk.TRUE, gtk.TRUE, 0)
        self.box5.pack_start(self.label_startRec, gtk.TRUE, gtk.TRUE, 0)
        self.label.show()
        self.label_startRec.show()

        self.label = gtk.Label("Number of data records: ")
        self.label_numRec = gtk.Label("--")
        self.label.set_alignment(xalign=0.0, yalign=0.5)
        self.label_numRec.set_alignment(xalign=0.0, yalign=0.5)
        self.box4.pack_start(self.label, gtk.TRUE, gtk.TRUE, 0)
        self.box5.pack_start(self.label_numRec, gtk.TRUE, gtk.TRUE, 0)
        self.label.show()
        self.label_numRec.show()

        self.label = gtk.Label("Duration of a data record (s): ")
        self.label_RecDur = gtk.Label("--")
        self.label.set_alignment(xalign=0.0, yalign=0.5)
        self.label_RecDur.set_alignment(xalign=0.0, yalign=0.5)
        self.box4.pack_start(self.label, gtk.TRUE, gtk.TRUE, 0)
        self.box5.pack_start(self.label_RecDur, gtk.TRUE, gtk.TRUE, 0)
        self.label.show()
        self.label_RecDur.show()

        self.label = gtk.Label("Number of EEG channels: ")
        self.label_numChan = gtk.Label("--")
        self.label.set_alignment(xalign=0.0, yalign=0.5)
        self.label_numChan.set_alignment(xalign=0.0, yalign=0.5)
        self.box4.pack_start(self.label, gtk.TRUE, gtk.TRUE, 0)
        self.box5.pack_start(self.label_numChan, gtk.TRUE, gtk.TRUE, 0)
        self.label.show()
        self.label_numChan.show()

        self.label = gtk.Label("Number of samples in each record: ")
        self.label_numSam = gtk.Label("--")
        self.label.set_alignment(xalign=0.0, yalign=0.5)
        self.label_numSam.set_alignment(xalign=0.0, yalign=0.5)
        self.box4.pack_start(self.label, gtk.TRUE, gtk.TRUE, 0)
        self.box5.pack_start(self.label_numSam, gtk.TRUE, gtk.TRUE, 0)
        self.label.show()
        self.label_numSam.show()

        self.box3.pack_start(self.box4, gtk.TRUE, gtk.TRUE, 0)
        self.box3.pack_start(self.box5, gtk.TRUE, gtk.TRUE, 0)
        self.box4.show()
        self.box5.show()
        self.box1.pack_start(self.box3, gtk.FALSE, gtk.TRUE, 0)
        self.box3.show()#}}}

        #################################################################
        #################            CANVAS             #################
        #################################################################
        global canvas
        self.box6 = gtk.HBox(gtk.FALSE, 0)#{{{
        self.box6.set_size_request(800,500)
        self.fig = plt.figure()
        self.axes = self.fig.add_subplot(111)
        #self.axes.get_xaxis().set_visible(False)
        self.axbackground = None
        canvas = FigureCanvas(self.fig)
        self.fig.subplots_adjust(left=0.1, bottom=0.04, right=0.96, top=0.96)
        self.axes.grid()
        canvas.draw()
        self.box6.pack_start(canvas)
        self.box1.pack_start(self.box6, gtk.TRUE, gtk.TRUE, 0)
        self.box6.show()#}}}

        self.box.pack_start(self.box1, gtk.TRUE, gtk.TRUE, 0)
        self.box1.show()


        #################################################################
        #################################################################
        #################                               #################
        #################          VIDEO DATA           #################
        #################                               #################
        #################################################################
        #################################################################
        self.boxv1 = gtk.VBox(gtk.FALSE, 0)#{{{
        self.boxv1.set_border_width(5)
        self.boxv2 = gtk.HBox(gtk.FALSE, 0)
        self.boxv2.set_border_width(10)

        #Label de Video
        self.label = gtk.Label("Seleccione un Archivo:")
        self.boxv2.pack_start(self.label, gtk.TRUE, gtk.TRUE, 0)
        self.label.show()

        #Boton para la carga del archivo de video
        self.videochooserbutton = gtk.FileChooserButton("Abrir Archivo Video", None)
        self.videochooserbutton.connect("file-set", self.videoSelected)
        self.videochooserbutton.set_current_folder(getcwd()+'/data/video')
        filtro = gtk.FileFilter()
        filtro.set_name("Videos")
        filtro.add_mime_type("video/mpeg")
        filtro.add_mime_type("video/x-msvideo")
        filtro.add_pattern("*.avi")
        filtro.add_pattern("*.mpg")
        filtro.add_pattern("*.mpeg")
        self.videochooserbutton.set_filter(filtro)
        self.boxv2.pack_start(self.videochooserbutton, gtk.TRUE, gtk.TRUE, 0)
        self.videochooserbutton.show()
        self.boxv1.pack_start(self.boxv2, gtk.FALSE, gtk.FALSE, 0)
        self.boxv2.show()

        self.boxv3 = gtk.HBox(gtk.FALSE, 0)
        self.boxv4 = gtk.VBox(gtk.FALSE, 0)
        self.boxv4.set_border_width(10)
        self.boxv5 = gtk.VBox(gtk.FALSE, 0)
        self.boxv5.set_border_width(10)

        self.label = gtk.Label("Width: ")
        self.label_vwidth = gtk.Label("---")
        self.label.set_alignment(xalign=0.0, yalign=0.5)
        self.label_vwidth.set_alignment(xalign=0.0, yalign=0.5)
        self.boxv4.pack_start(self.label, gtk.TRUE, gtk.TRUE, 0)
        self.boxv5.pack_start(self.label_vwidth, gtk.TRUE, gtk.TRUE, 0)
        self.label.show()
        self.label_vwidth.show()

        self.label = gtk.Label("Height: ")
        self.label_vheight = gtk.Label("---")
        self.label.set_alignment(xalign=0.0, yalign=0.5)
        self.label_vheight.set_alignment(xalign=0.0, yalign=0.5)
        self.boxv4.pack_start(self.label, gtk.TRUE, gtk.TRUE, 0)
        self.boxv5.pack_start(self.label_vheight, gtk.TRUE, gtk.TRUE, 0)
        self.label.show()
        self.label_vheight.show()

        self.label = gtk.Label("Number of Frames: ")
        self.label_vlength = gtk.Label("---")
        self.label.set_alignment(xalign=0.0, yalign=0.5)
        self.label_vlength.set_alignment(xalign=0.0, yalign=0.5)
        self.boxv4.pack_start(self.label, gtk.TRUE, gtk.TRUE, 0)
        self.boxv5.pack_start(self.label_vlength, gtk.TRUE, gtk.TRUE, 0)
        self.label.show()
        self.label_vlength.show()

        self.label = gtk.Label("Fps: ")
        self.label_vfps = gtk.Label("---")
        self.label.set_alignment(xalign=0.0, yalign=0.5)
        self.label_vfps.set_alignment(xalign=0.0, yalign=0.5)
        self.boxv4.pack_start(self.label, gtk.TRUE, gtk.TRUE, 0)
        self.boxv5.pack_start(self.label_vfps, gtk.TRUE, gtk.TRUE, 0)
        self.label.show()
        self.label_vfps.show()

        self.label = gtk.Label("Duration: ")
        self.label_vdur = gtk.Label("---")
        self.label.set_alignment(xalign=0.0, yalign=0.5)
        self.label_vdur.set_alignment(xalign=0.0, yalign=0.5)
        self.boxv4.pack_start(self.label, gtk.TRUE, gtk.TRUE, 0)
        self.boxv5.pack_start(self.label_vdur, gtk.TRUE, gtk.TRUE, 0)
        self.label.show()
        self.label_vdur.show()

        self.boxv3.pack_start(self.boxv4, gtk.TRUE, gtk.TRUE, 0)
        self.boxv3.pack_start(self.boxv5, gtk.TRUE, gtk.TRUE, 0)
        self.boxv4.show()
        self.boxv5.show()
        self.boxv1.pack_start(self.boxv3, gtk.FALSE, gtk.TRUE, 0)
        self.boxv3.show()#}}}

        #################################################################
        #################        CONTROL DISPLAY        #################
        #################################################################
        #Label de Display Video#{{{
        self.label = gtk.Label("Controles de display:")
        self.label.set_alignment(xalign=0.05, yalign=0.5)
        self.boxv1.pack_start(self.label, gtk.FALSE, gtk.TRUE, 0)
        self.label.show()

        self.bbox = gtk.HBox(False,2)
        self.bbox.show()

        # crear varias imagenes con datos de archivos y cargarlos
        image = gtk.Image()
        image.set_from_file("./Images/FullFastRewind.png")
        image.show()
        # un boton que cotenga el control de imagen
        self.ffrbutton = gtk.Button()
        self.ffrbutton.add(image)
        self.ffrbutton.show()
        self.bbox.pack_start(self.ffrbutton, False, False, 0)
        self.ffrbutton.connect("clicked", self.ffr_clicked, "2")

        # crear varias imagenes con datos de archivos y cargarlos
        image = gtk.Image()
        image.set_from_file("./Images/FastRewind.png")
        image.show()
        # un boton que cotenga el control de imagen
        self.frbutton = gtk.Button()
        self.frbutton.add(image)
        self.frbutton.show()
        self.bbox.pack_start(self.frbutton, False, False, 0)
        self.frbutton.connect("clicked", self.fr_clicked, "2")

        # crear varias imagenes con datos de archivos y cargarlos
        image = gtk.Image()
        image.set_from_file("./Images/Play.png")
        image.show()
        # un boton que cotenga el control de imagen
        self.playbutton = gtk.Button()
        self.playbutton.add(image)
        self.playbutton.show()
        self.bbox.pack_start(self.playbutton, False, False, 0)
        self.playbutton.connect("clicked", self.play_clicked, "2")

        # crear varias imagenes con datos de archivos y cargarlos
        image = gtk.Image()
        image.set_from_file("./Images/Pause.png")
        image.show()
        # un boton que cotenga el control de imagen
        self.pausebutton = gtk.Button()
        self.pausebutton.add(image)
        self.pausebutton.show()
        self.bbox.pack_start(self.pausebutton, False, False, 0)
        self.pausebutton.connect("clicked", self.pause_clicked, "2")

        # crear varias imagenes con datos de archivos y cargarlos
        image = gtk.Image()
        image.set_from_file("./Images/FastForward.png")
        image.show()
        # un boton que cotenga el control de imagen
        self.ffbutton = gtk.Button()
        self.ffbutton.add(image)
        self.ffbutton.show()
        self.bbox.pack_start(self.ffbutton, False, False, 0)
        self.ffbutton.connect("clicked", self.ff_clicked, "2")

        # crear varias imagenes con datos de archivos y cargarlos
        image = gtk.Image()
        image.set_from_file("./Images/FullFastForward.png")
        image.show()
        # un boton que cotenga el control de imagen
        self.fffbutton = gtk.Button()
        self.fffbutton.add(image)
        self.fffbutton.show()
        self.bbox.pack_start(self.fffbutton, False, False, 0)
        self.fffbutton.connect("clicked", self.fff_clicked, "2")
        self.boxv1.pack_start(self.bbox, gtk.FALSE, gtk.TRUE, 2)

        #Label de Velocidad
        self.hsbox = gtk.HBox(gtk.FALSE, 0)
        self.label = gtk.Label("Velocidad:")
        self.label.set_alignment(xalign=0.05, yalign=0.5)
        self.boxv1.pack_start(self.label, gtk.FALSE, gtk.TRUE, 0)
        self.label.show()
        adj1 = gtk.Adjustment(10, 1, 101, 1, 1.0, 1.0)
        adj1.connect("value_changed", self.update_cnt)
        self.hscale = gtk.HScale(adj1)
        self.hscale.set_size_request(200, 30)
        self.hscale.set_update_policy(gtk.UPDATE_CONTINUOUS)
        self.hscale.set_digits(0)
        self.hscale.set_value_pos(gtk.POS_TOP)
        self.hscale.set_draw_value(gtk.TRUE)
        self.hsbox.pack_start(self.hscale, gtk.TRUE, gtk.TRUE, 0)
        self.hscale.show()
        self.boxv1.pack_start(self.hsbox, gtk.FALSE, gtk.TRUE, 0)
        self.hsbox.show()

        #Boton para las opciones de visualizacion del EEG
        self.box2 = gtk.HBox(gtk.FALSE, 0)
        self.box2.set_border_width(15)
        self.button = gtk.Button("Options")
        self.button.connect("clicked", self.optionClick, None)
        self.box2.pack_start(self.button, gtk.TRUE, gtk.TRUE, 0)
        self.button.show()
        self.boxv1.pack_start(self.box2, gtk.FALSE, gtk.TRUE, 0)
        self.box2.show()


        self.cfbox = gtk.HBox(gtk.FALSE, 0)
        self.cf1box = gtk.HBox(gtk.FALSE, 0)
        self.label = gtk.Label("Current Frame:")
        self.label.set_alignment(xalign=0.05, yalign=0.5)
        self.cf2box = gtk.HBox(gtk.FALSE, 0)
        self.cflabel = gtk.Label("--")
        self.cflabel.set_alignment(xalign=0.05, yalign=0.5)
        self.cf1box.pack_start(self.label, gtk.TRUE, gtk.TRUE, 0)
        self.cf2box.pack_start(self.cflabel, gtk.TRUE, gtk.TRUE, 0)
        self.cfbox.pack_start(self.cf1box, gtk.TRUE, gtk.TRUE, 0)
        self.cfbox.pack_start(self.cf2box, gtk.TRUE, gtk.TRUE, 0)
        self.cf1box.show()
        self.cf2box.show()
        self.boxv1.pack_start(self.cfbox, gtk.TRUE, gtk.TRUE, 0)
        self.cfbox.show()

        self.video = gtk.Image()
        self.boxv6 = gtk.HBox(gtk.FALSE, 0)
        self.boxv6.set_size_request(400,300)
        self.boxv6.pack_start(self.video)
        self.video.show()
        self.boxv1.pack_start(self.boxv6, gtk.FALSE, gtk.TRUE, 0)
        self.boxv6.show()

        self.box.pack_start(self.boxv1, gtk.TRUE, gtk.TRUE, 0)
        self.boxv1.show() #}}}

        # add the hbox to the window
        self.window.show_all()

    def main(self):
        gtk.main()

    def destroy(self, widget, data=None):
        gtk.main_quit()

    def optionClick(self, widget, data=None):
        global validlines#{{{
        if self.BDF_file.isEmpty():
            return
        options = OptionsWindow()
        box1 = gtk.HBox(gtk.FALSE, 0)
        box2 = gtk.VBox(gtk.FALSE, 0)
        box2.set_border_width(15)
        for i in range(0,self.BDF_file.numChan/2+1):
            button = gtk.CheckButton(str(i) + '- ' + str(self.BDF_file.labels[i]))
            button.set_active(validlines[i])
            button.connect("toggled", self.chequed, i)
            box2.pack_start(button, gtk.TRUE, gtk.TRUE, 0)
            button.show()
        box1.pack_start(box2, gtk.FALSE, gtk.FALSE, 0)
        box2.show()
        box3 = gtk.VBox(gtk.FALSE, 0)
        box3.set_border_width(15)
        for i in range(self.BDF_file.numChan/2+1,self.BDF_file.numChan):
            button = gtk.CheckButton(str(i) + '- ' + str(self.BDF_file.labels[i]))
            button.set_active(validlines[i])
            button.connect("toggled", self.chequed, i)
            box3.pack_start(button, gtk.TRUE, gtk.TRUE, 0)
            button.show()
        box1.pack_start(box3, gtk.FALSE, gtk.FALSE, 0)
        box3.show()

        options.window.add(box1)
        box1.show()#}}}

    def chequed(self, widget, data=None):
        global validlines#{{{
        validlines[data] = (False, True)[widget.get_active()]
        self.BDF_file.setMData(validlines)
        self.axes.set_ylim(self.BDF_file.Mmin,self.BDF_file.Mmax)#}}}

    def fileSelected(self,widget):
        global lines#{{{
        global validlines
        global canvas

        self.BDF_file = bdf_reader(widget.get_filename())
        self.label_startRec.set_text(self.BDF_file.startRec)
        self.label_numRec.set_text(str(self.BDF_file.numRec))
        self.label_RecDur.set_text(str(self.BDF_file.RecDur))
        self.label_numChan.set_text(str(self.BDF_file.numChan))
        self.label_numSam.set_text(str(self.BDF_file.numSam))

        self.axes.set_ylim(self.BDF_file.Mmin,self.BDF_file.Mmax)
        #self.axes.set_xlim(self.BDF_file.cnt_now-self.BDF_file.numSam/20,self.BDF_file.numSam/5+self.BDF_file.cnt_now-self.BDF_file.numSam/20)

        x = np.linspace(0,0.25,self.BDF_file.numSam/5)
        for i in range(0,self.BDF_file.numChan):
            line, = self.axes.plot(x, self.BDF_file.Mdata[i][0:self.BDF_file.numSam/5], animated=True, lw=1)
            lines.append(line)
            validlines.append(True)

        canvas.mpl_connect('draw_event', self.start_anim)

        canvas.draw()
        #}}}

    def videoSelected(self, widget):
        global videofile#{{{
        videofile = Video_File(widget.get_filename())
        self.label_vwidth.set_text(str(videofile.width))
        self.label_vheight.set_text(str(videofile.height))
        self.label_vlength.set_text(str(videofile.length))
        self.label_vfps.set_text(str(videofile.fps))
        self.label_vdur.set_text(str(videofile.dur))
        self.video.set_from_pixbuf(videofile.getFrameAsPixbuf())
        self.video.set_from_pixbuf(videofile.getFrameAsPixbuf())
        self.cflabel.set_text(str(videofile.currentFrame()))#}}}

    def ff_clicked(self, widget, data=None):
        global videofile#{{{
        frame = videofile.getFrameAsPixbuf()
        if frame:
            self.video.set_from_pixbuf(frame)
        inx = np.where(self.BDF_file.events[self.BDF_file.cnt_now:] == 251)
        if inx[0].size:
            self.BDF_file.cnt_now += inx[0][1]
        self.cflabel.set_text(str(videofile.cur))
        self.ff_eeg()#}}}

    def fff_clicked(self, widget, data=None):
        global videofile#{{{
        videofile.fullForwardFrame()
        frame = videofile.getFrameAsPixbuf()
        if frame:
            self.video.set_from_pixbuf(frame)
        inx = np.where(self.BDF_file.events[self.BDF_file.cnt_now:] == 251)
        if inx[0].size:
            self.BDF_file.cnt_now += inx[0][inx[0].size-1]
        self.cflabel.set_text(str(videofile.cur))
        self.ff_eeg()#}}}

    def ff_eeg(self):
        global lines#{{{
        global canvas
        global validlines

        if self.axbackground is None:
            self.axbackground = canvas.copy_from_bbox(self.axes.get_figure().bbox)

        # restore the clean slate background
        canvas.restore_region(self.axbackground)

        # update the data
        self.axes.hold(True)
        for i in range(0,self.BDF_file.numChan):
            if validlines[i]:
                lines[i].set_ydata(self.BDF_file.Mdata[i][self.BDF_file.cnt_now-self.BDF_file.numSam/20:self.BDF_file.numSam/5+self.BDF_file.cnt_now-self.BDF_file.numSam/20])
                #lines[i].set_xdata(np.arange(self.BDF_file.cnt_now-self.BDF_file.numSam/20,self.BDF_file.numSam/5+self.BDF_file.cnt_now-self.BDF_file.numSam/20))
                # just draw the animated artist
                self.axes.draw_artist(lines[i])

        self.axes.hold(False)

        #if np.where(self.BDF_file.events[self.BDF_file.cnt_now:(self.BDF_file.cnt_now+self.BDF_file.inc)] == 251)[0].size:
        #    frame = videofile.getFrameAsPixbuf()
        #    if frame:
        #        self.video.set_from_pixbuf(frame)

        #just redraw the axes
        canvas.blit(self.axes.bbox)

        #self.axes.set_xlim(self.BDF_file.cnt_now-self.BDF_file.numSam/20,self.BDF_file.numSam/5+self.BDF_file.cnt_now-self.BDF_file.numSam/20)
        #canvas.draw()#}}}

    def fr_clicked(self, widget, data=None):
        global videofile#{{{
        videofile.rewindFrame()
        self.video.set_from_pixbuf(videofile.getFrameAsPixbuf())
        inx = np.where(self.BDF_file.events[:self.BDF_file.cnt_now] == 251)
        if inx[0].size:
            self.BDF_file.cnt_now = inx[0][inx[0].size-1]
        self.cflabel.set_text(str(videofile.cur))
        self.fr_eeg()#}}}

    def ffr_clicked(self, widget, data=None):
        global videofile#{{{
        videofile.fullRewindFrame()
        self.video.set_from_pixbuf(videofile.getFrameAsPixbuf())
        self.video.set_from_pixbuf(videofile.getFrameAsPixbuf())
        inx = np.where(self.BDF_file.events[:self.BDF_file.cnt_now] == 251)
        if inx[0].size:
            self.BDF_file.cnt_now = inx[0][0]
        self.cflabel.set_text(str(videofile.cur))
        self.fr_eeg()#}}}

    def fr_eeg(self):
        global lines#{{{
        global canvas
        global validlines

        if self.axbackground is None:
            self.axbackground = canvas.copy_from_bbox(self.axes.get_figure().bbox)

        # restore the clean slate background
        canvas.restore_region(self.axbackground)

        # update the data
        self.axes.hold(True)
        for i in range(0,self.BDF_file.numChan):
            if validlines[i]:
                lines[i].set_ydata(self.BDF_file.Mdata[i][self.BDF_file.cnt_now-self.BDF_file.numSam/20:self.BDF_file.numSam/5+self.BDF_file.cnt_now-self.BDF_file.numSam/20])
                #lines[i].set_xdata(np.arange(self.BDF_file.cnt_now-self.BDF_file.numSam/20,self.BDF_file.numSam/5+self.BDF_file.cnt_now-self.BDF_file.numSam/20))
                # just draw the animated artist
                self.axes.draw_artist(lines[i])

        self.axes.hold(False)

        #if np.where(self.BDF_file.events[self.BDF_file.cnt_now:(self.BDF_file.cnt_now+self.BDF_file.inc)] == 251)[0].size:
        #    frame = videofile.getFrameAsPixbuf()
        #    if frame:
        #        self.video.set_from_pixbuf(frame)

        #just redraw the axes
        canvas.blit(self.axes.bbox)
        #self.axes.set_xlim(self.BDF_file.cnt_now-self.BDF_file.numSam/20,self.BDF_file.numSam/5+self.BDF_file.cnt_now-self.BDF_file.numSam/20)
        #canvas.draw()
        #}}}

    def play_clicked(self, widget, data=None):
        global StopEvent#{{{
        global canvas
        StopEvent = False
        canvas.draw()
        #}}}

    def pause_clicked(self, widget, data=None):
        global StopEvent#{{{
        global canvas
        StopEvent = True
        #}}}

    def update_cnt(self, adj):
        self.BDF_file.setIncrement(int(adj.value))#{{{
        #}}}

    def start_anim(self,event):
        gobject.idle_add(self.run)

    def run(self):
        global videofile#{{{
        global StopEvent
        global lines
        global canvas
        global validlines
        global elines
        global evalidlines

        if StopEvent:
            return True

        if self.axbackground is None:
            self.axbackground = canvas.copy_from_bbox(self.axes.get_figure().bbox)

        # restore the clean slate background
        canvas.restore_region(self.axbackground)

        # update the data
        self.axes.hold(True)
        for i in range(0,self.BDF_file.numChan):
            if validlines[i]:
                lines[i].set_ydata(self.BDF_file.Mdata[i][self.BDF_file.cnt_now-self.BDF_file.numSam/20:self.BDF_file.numSam/5+self.BDF_file.cnt_now-self.BDF_file.numSam/20])
                # just draw the animated artist
                self.axes.draw_artist(lines[i])

        self.axes.hold(False)

        if np.where(self.BDF_file.events[self.BDF_file.cnt_now:(self.BDF_file.cnt_now+self.BDF_file.inc)] == 251)[0].size:
            frame = videofile.getFrameAsPixbuf()
            if frame:
                self.video.set_from_pixbuf(frame)

        self.BDF_file.cnt_now += self.BDF_file.inc
        self.cflabel.set_text(str(videofile.cur))

        #just redraw the axes
        canvas.blit(self.axes.bbox)

        return True
        #}}}


if __name__ == "__main__":
    principal = MainWindow()
    principal.main()
