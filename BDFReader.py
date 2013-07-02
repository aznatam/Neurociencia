import sys
import struct
import operator
import numpy as np

def  bdf_reader(filename):
    #print 'Loading BDF file "' + filename + '"...'#{{{
    try:
        f = open(filename, 'r')
    except IOError:
        print 'File Not Found'
        sys.exit(0)

    file = BDF_File()

    #Startdate of recording
    f.seek(168)
    file.startRec = f.read(8).strip().replace('.','/') + ' ' + f.read(8).strip().replace('.',':')
    #print 'Startdate of recording: ' + file.startRec

    #number of data records
    f.seek(236)
    file.numRec = int(f.read(8).strip())
    #print 'number of data records: ' + str(file.numRec)

    #duration of a data record, sec
    file.RecDur = int(f.read(8).strip())
    #print 'duration of a data record (s): ' + str(file.RecDur)

    #number of EEG channels
    file.numChan = int(f.read(4).strip())
    #print 'number of EEG channels: ' + str(file.numChan)

    #number of samples in each record
    f.seek(256+file.numChan*216)
    file.numSam = int(f.read(4).strip())
    #print 'number of samples in each record: ' + str(file.numSam)

    #labels
    f.seek(256)
    labels = []
    for j in range(0,file.numChan):
        labels.append(f.read(16).strip())
    file.labels = labels
    #print 'labels: ' + str(file.labels)

    #positions the pointer to the beginning of data
    f.seek(256*(file.numChan+1))
    data = []
    for j in range(0,file.numChan):
            data.append([])
    for i in range(0,file.numRec):
        for j in range(0,file.numChan-1):
            f.seek(256*(file.numChan+1)+3*(i*(file.numChan*file.numSam)+j*(file.numSam)))
            for k in range(0, file.numSam):
                dato = f.read(3)
                data[j].append(struct.unpack("<i", dato + ('\0' if dato[2] < '\x80' else '\xff'))[0])
        f.seek(256*(file.numChan+1)+3*(i*(file.numChan*file.numSam)+(file.numChan-1)*(file.numSam)))
        for k in range(0, file.numSam):
            dato = f.read(3)
            data[file.numChan-1].append(struct.unpack("<i", dato + ('\0' if dato[2] < '\x80' else '\xff'))[0])
    file.data = data

    f.close()

    file.setEvents()
    file.setMData()

    return file#}}}

class BDF_File:

    def __init__(self, record=None, duration=None, channels=None, samples=None, digital_min=None, digital_max=None, physical_min=None, physical_max=None, labels=None, data=None):
        self.numRec = record#{{{
        self.RecDur = duration
        self.numChan = channels
        self.numSam = samples
        self.Dmin = digital_min
        self.Dmax = digital_max
        self.Pmin = physical_min
        self.Pmax = physical_max
        self.labels = labels
        self.data = data
        self.Mdata = None
        self.Mmax = 0
        self.Mmin = 0
        self.startRec = ''
        self.events = None
        self.cnt_start = 0
        self.cnt_end = 0
        self.cnt_now = 0
        self.inc = 10
        #}}}

    def setTime(self,time):
        self.startRec = time

    def setIncrement(self,inc):
        self.inc = inc

    def isEmpty(self):
        if self.numRec == None:#{{{
            return True
        else:
            return False#}}}

    def setEvents(self):
        thiscode = 0#{{{
        events = []
        recSize = len(self.data[self.numChan-1])
        for i in range(0,recSize):
            prevcode = thiscode
            thiscode = operator.mod(self.data[self.numChan-1][i],65536)
            if (thiscode != 0 and prevcode != thiscode) :
                events.append(thiscode)
            else:
                events.append(0)
        events = np.array(events)
        self.cnt_start = np.where(events == 221)[0][0]
        self.cnt_now = self.cnt_start
        aux = np.where(events == 2)
        self.cnt_end = aux[0][len(aux[0])-1]
        self.events = events#}}}

    def setMData(self, validlines=None):
        datos = []#{{{
        if validlines == None:
            size = self.numChan
            validlines = [True]*size
        else:
            size = validlines.count(True)
        coef = np.linspace(-size/2,size/2+1,size)
        j = 0
        for i in range(0,self.numChan-1):
            if validlines[i]:
                datos.append(np.array(self.data[i])-np.average(self.data[i])+coef[j]*30000)
                j += 1
            else:
                datos.append(np.array(self.data[i])-np.array(self.data[i]))

        print validlines

        self.Mdata = np.array(datos)
        self.Mmax = np.amax(np.array(datos))
        self.Mmin = np.amin(np.array(datos))#}}}

    def printAll(self):
        print 'Startdate of recording: ' + self.startRec
        print 'Number of data records: ' + str(self.numRec)
        print 'Duration of a data record (s): ' + str(self.RecDur)
        print 'Number of EEG channels: ' + str(self.numChan)
        print 'Number of samples in each record: ' + str(self.numSam)
        print 'Labels: ' + str(self.labels)
        inx = np.where(self.events != 0)
        print 'Number of events: ' + str(inx[0].size)

