import string
import re
import numpy as np

class LVM_IO:

    def __init__(self, read_fstsq = False):
        # self.expected_header = [ \
        #     [,'fileversion']], \
        #     ['expected number of points','dimensions'],\
        #     ['measured values converted in','measures'],\
        #     ['#DAC initial values (V)','DACs'],\
        #     ['#Mag field initial Value','Magnetic field']]
        # self.remaining_header = self.expected_header
        self.read_fstsq = read_fstsq
        self.endofheader_string = '#sweep'
        self.newline = '\r\n'
        self.DAC_number_of_lines = 64
        self.DAC_useful_number_of_lines = 4*8
        self.Fastchannels_number_of_lines = 16
        self.FLAG_end_of_Fastsequence = False

    def Read_FastSequence(self, filepathname, XP):
        self.filein = open(filepathname,'r')
        self.filein_txt = self.filein.readlines()
        self.filein.close()

        self.currentlinenumber = 0
        self.currentline = string.split(self.filein_txt[self.currentlinenumber],self.newline)[-2]
        while not self.FLAG_end_of_Fastsequence:
            print self.currentlinenumber, self.currentline
            self._read_fstsq_property(XP)

    def _read_fstsq_property(self, XP):
        # We start to read the property_name
        # We are trying to identify the property_name

        # Fileversion
        property_text = '#Fastsequence file version'
        if self.currentline[0:len(property_text)] == property_text:
            self.currentline = re.findall("[-+]?\d+[\.]?\d*[eE]?[-+]?\d*", self.currentline)
            XP.ExperimentalParameters['Info']['fstsq_fileversion'] = float(self.currentline[0])
            #next
            self.currentlinenumber += 1
            self.currentline = string.split(self.filein_txt[self.currentlinenumber],self.newline)[-2]


        # Fast sequence divider
        property_text = '#divider'
        if self.currentline[0:len(property_text)] == property_text:
            # Rampmode
            if self.currentline[-1] == 'T':
                XP.ExperimentalParameters['Info']['Rampmode'] = True
            elif self.currentline[-1] == 'F':
                XP.ExperimentalParameters['Info']['Rampmode'] = False
            # Fastsequence divider
            self.currentline = re.findall("[-+]?\d+[\.]?\d*[eE]?[-+]?\d*", self.currentline)
            XP.ExperimentalParameters['Info']['Fastsequence_divider'] = float(self.currentline[0])
            #next
            self.currentlinenumber += 1
            self.currentline = string.split(self.filein_txt[self.currentlinenumber],self.newline)[-2]


        # Fast channels
        property_text = '#FastChannels'
        if self.currentline[0:len(property_text)] == property_text:
            XP.ExperimentalParameters['Info']['Fastchannels'] = {}
            for i in range(self.Fastchannels_number_of_lines):
                self.currentlinenumber += 1
                self.currentline = string.split(self.filein_txt[self.currentlinenumber],self.newline)[-2]
                # check if it is a dummy fast channel.
                # F means it is NOT a dummy
                if self.currentline[-1] == 'F':
                    self.currentline = re.findall("[-+]?\d+[\.]?\d*[eE]?[-+]?\d*", self.currentline)
                    index = int(self.currentline[0])
                    DAC_column = int(self.currentline[1])
                    DAC_row = int(self.currentline[2])
                    XP.ExperimentalParameters['Info']['Fastchannels'][index] = [DAC_column,DAC_row]
            #next
            self.currentlinenumber += 1
            self.currentline = string.split(self.filein_txt[self.currentlinenumber],self.newline)[-2]

        property_text = '#Sequence'
        if self.currentline[0:len(property_text)] == property_text:
            while not self.FLAG_end_of_Fastsequence :
                #next
                self.currentlinenumber += 1
                self.currentline = string.split(self.filein_txt[self.currentlinenumber],self.newline)[-2]

                #detect the type of fpga command
                # Trigger
                if string.split(self.currentline,':')[1][:4] == ' Tri':
                    trigs = string.split(self.currentline,':')[2]
                    trigs = string.split(trigs)
                    for i,t in enumerate(trigs):
                        if t == 'T':
                            trigs[i] = True
                        else:
                            trigs[i] = False
                        print trigs
                elif string.split(self.currentline,':')[1][:4] == ' wai':
                    print self.currentline
                elif string.split(self.currentline,':')[1][:4] == ' DAC':
                    print self.currentline
                elif string.split(self.currentline,':')[1][:4] == ' jum':
                    print self.currentline
                self.FLAG_end_of_Fastsequence = True

        # while self.currentline == '\n':
        #     self.currentline = self.filein.readline()
        #     self.currentlinenumber += 1

    def Read_header(self, filepathname, XP):
        self.filein = open(filepathname,'r')
        self._read_header_size()
        self.filein.seek(0) # Go back to the begin of the file

        self.currentlinenumber = 0
        self.currentline = self.filein.readline()
        while self.currentlinenumber < self._header_size:
            self._read_header_property(XP)
        self.filein.close()

    def _read_header_property(self, XP):
        # We start to read the property_name
        # We are trying to identify the property_name

        # Fileversion
        property_text = '# measurement file writer version'
        if self.currentline[0:len(property_text)] == property_text:
            self.currentline = re.findall("[-+]?\d+[\.]?\d*[eE]?[-+]?\d*", self.currentline)
            XP.FileInfo['fileversion'] = float(self.currentline[0])

        # Dimensions
        # The lvm file store the dimensions so that : [sweep, step, step2, step3, #measures]
        # We rotate that list to [#measures, sweep, step, step2, step3]
        property_text = 'expected number of points'
        if self.currentline[0:len(property_text)] == property_text:
            self.currentline = string.split(self.currentline,':')[1]
            self.currentline = re.findall("[-+]?\d+[\.]?\d*[eE]?[-+]?\d*", self.currentline)
            XP.ExperimentalData['dimensions'] = map(int, self.currentline)
            n_measures = XP.ExperimentalData['dimensions'][-1]
            XP.ExperimentalData['dimensions'] = XP.ExperimentalData['dimensions'][0:-1]
            XP.ExperimentalData['dimensions'][:0] = [n_measures]

        # Measurement name and unit on the following line
        property_text = 'measured values converted'
        if self.currentline[0:len(property_text)] == property_text:
            XP.ExperimentalData['measures'] = []
            for i in range(XP.ExperimentalData['dimensions'][0]):
                self.currentline = string.split(self.filein.readline(),self.newline)[0]
                XP.ExperimentalData['measures'].append([self.currentline])
                self.currentlinenumber += 1
                self.currentline = string.split(self.filein.readline(),self.newline)[0]
                XP.ExperimentalData['measures'][i].append(self.currentline)
                self.currentlinenumber += 1
                # print self.currentline

        # DAC values
        # There might be more lines written in the file than that actually used ...
        property_text = '#DAC initial values (V)'
        if self.currentline[0:len(property_text)] == property_text:
            XP.ExperimentalParameters['Info']['DAC_initial_values'] = np.zeros(self.DAC_useful_number_of_lines)
            for i in range(self.DAC_number_of_lines):
                self.currentline = self.filein.readline()
                self.currentline = re.findall("[-+]?\d+[\.]?\d*[eE]?[-+]?\d*", self.currentline)
                self.currentlinenumber += 1
                if i < self.DAC_useful_number_of_lines:
                    XP.ExperimentalParameters['Info']['DAC_initial_values'][i] = self.currentline[0]

        # Magnetic field
        property_text = '#Mag field initial Value'
        n_additional_lines = 1
        if self.currentline[0:len(property_text)] == property_text:
            self.currentline = self.filein.readline()
            self.currentline = re.findall("[-+]?\d+[\.]?\d*[eE]?[-+]?\d*", self.currentline)
            self.currentlinenumber += 1
            XP.ExperimentalParameters['Info']['MagneticField_initial_values'] = np.zeros(3)
            XP.ExperimentalParameters['Info']['MagneticField_initial_values'][2] = self.currentline[0]

        # At the end of the method, a non-empty currentline should be returned.
        self.currentline = self.filein.readline()
        self.currentlinenumber += 1
        while self.currentline == '\n':
            self.currentline = self.filein.readline()
            self.currentlinenumber += 1

    def _read_header_size(self):
        FLAG_end_of_header = False
        self._header_size = 0
        while not FLAG_end_of_header: #self.header_size<100: # () or
            self.currentline = self.filein.readline()
            #print len(currentline)
            #print currentline[0:len(self.endofheader_string)] + ' -- ' + self.endofheader_string
            if self.currentline[0:len(self.endofheader_string)] == self.endofheader_string:
                FLAG_end_of_header = True
            self._header_size += 1
