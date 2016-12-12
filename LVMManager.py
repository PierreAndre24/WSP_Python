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

    def Read_data(self, filepathname, XP):
        # Correct the dimensions
        self._lvm_confirm_scan_dimensions(filepathname, XP)
        # initialize the data array
        #convertfunc = lambda x: float(x.strip("%"))
        convertfunc = lambda x: float(re.findall("[-+]?\d+[\.]?\d*[eE]?[-+]?\d*",x)[0])

        XP.ExperimentalData['data'] = np.genfromtxt(\
                                    fname = filepathname,\
                                    comments = '#',\
                                    converters = {1: convertfunc, 2: convertfunc, 3: convertfunc, 4: convertfunc},\
                                    skip_header = self._header_size)
        XP.ExperimentalData['data'] = XP.ExperimentalData['data'][:,-XP.ExperimentalData['dimensions'][0]:]
        final_shape = XP.ExperimentalData['dimensions']#[:4]
        #final_shape.reverse()
        XP.ExperimentalData['data'] = np.reshape(XP.ExperimentalData['data'],final_shape)

    def Read_FastSequence(self, filepathname, XP):
        self.filein = open(filepathname,'r')
        self.filein_txt = self.filein.readlines()
        self.filein.close()

        self.currentlinenumber = 0
        self.currentline = string.split(self.filein_txt[self.currentlinenumber],self.newline)[-2]
        while not self.FLAG_end_of_Fastsequence:
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
        # this will go in a datasets
        # 1st col = type
        #       0 = DAC
        #       1 = Timing
        #       2 = Trigger
        #       3 = jump
        # 2nd col = DAC fastchennel only (0 else)
        # 3rd col = value
        #       DAC delta
        #       time in ms
        #       Triggers in binary:
        #           Trig1 = T -> +2
        #           Trig2 = T -> +4
        #           Trig3 = T -> +8
        #           Trig4 = T -> +16
        #           stop = T -> +32
        if self.currentline[0:len(property_text)] == property_text:
            XP.ExperimentalParameters['Fastsequence'] = []
            while not self.FLAG_end_of_Fastsequence :
                #next
                self.currentlinenumber += 1
                self.currentline = string.split(self.filein_txt[self.currentlinenumber],self.newline)[-2]

                # detect the type of fpga command
                # check for the end of the fast Sequence
                # two possible bases:
                # - no sequence, so the fast ramp starts at index = 0
                # - finite sequence. i = 0..2 -> Trig1: T; wait; Trig1: F ... do something ...
                #   Trig1: F (fast ramp: additional check of the FLAG rampmode) or jump (real time)
                self.FLAG_finite_fastsequence = False
                # Trigger
                if string.split(self.currentline,':')[1][:4] == ' Tri':
                    trigs = string.split(self.currentline,':')[2]
                    trigs = string.split(trigs)
                    for i,t in enumerate(trigs):
                        if t == 'T':
                            trigs[i] = True
                        else:
                            trigs[i] = False

                    # check if there is a fastsequence at all
                    # from the first line of the fastsequence
                    if  (len(XP.ExperimentalParameters['Fastsequence']) == 0) and\
                        trigs[0] == False:
                        # no fastsequence
                        #self.FLAG_finite_fastsequence = False #not necessary
                        self.FLAG_end_of_Fastsequence = True
                    else:
                        #self.FLAG_finite_fastsequence = True
                        self.FLAG_end_of_Fastsequence = False #not necessary

                    # check if the fast sequence in the ramp mode ends with Trig1: F
                    if  (len(XP.ExperimentalParameters['Fastsequence']) > 2) and\
                        (trigs[0] == False) and \
                        (XP.ExperimentalParameters['Info']['Rampmode'] == True):
                        # end of the fastsequence
                        #self.FLAG_finite_fastsequence = True #not necessary
                        self.FLAG_end_of_Fastsequence = True

                    # fill the fastsequence
                    trig_decimal = 0
                    for i,t in enumerate(trigs):
                        if t == True:
                            trig_decimal += 2**(i+1)
                    XP.ExperimentalParameters['Fastsequence'].append([2,0,trig_decimal])

                # Wait
                elif string.split(self.currentline,':')[1][:4] == ' wai':
                    self.currentline = re.findall("[-+]?\d+[\.]?\d*[eE]?[-+]?\d*", self.currentline)
                    # fill the fastsequence
                    XP.ExperimentalParameters['Fastsequence'].append([1,0,float(self.currentline[1])])

                # DAC
                elif string.split(self.currentline,':')[1][:4] == ' DAC':
                    self.currentline = re.findall("[-+]?\d+[\.]?\d*[eE]?[-+]?\d*", self.currentline)
                    # fill the fastsequence
                    XP.ExperimentalParameters['Fastsequence'].append([0,int(self.currentline[1]),float(self.currentline[2])])

                # Jump
                elif string.split(self.currentline,':')[1][:4] == ' jum':
                    # check if the fast sequence in the ramp mode ends with Trig1: F
                    self.currentline = re.findall("[-+]?\d+[\.]?\d*[eE]?[-+]?\d*", self.currentline)
                    if  int(self.currentline[0]) == int(self.currentline[1]):
                        # end of the fastsequence due to the infinite loop
                        #self.FLAG_finite_fastsequence = True #not necessary
                        self.FLAG_end_of_Fastsequence = True
                    else:
                        # go to the wanted step of the fastsequence
                        # compute
                        jump_length = int(self.currentline[1]) - int(self.currentline[0])
                        # go
                        self.currentlinenumber += jump_length
                        self.currentline = string.split(self.filein_txt[self.currentlinenumber],self.newline)[-2]
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
            if self.currentline[0:len(self.endofheader_string)] == self.endofheader_string:
                FLAG_end_of_header = True
            self._header_size += 1

    def _lvm_confirm_scan_dimensions(self,filepathname,XP):
        # As the different labview programs gives more or less wrong
        # sweep dimensions, we have to check it.
        # In order to do so, we read the first sweep manually.
        self.filein = open(filepathname,'r')
        for i in range(self._header_size):
            self.filein.readline() # Go back to the end of the header
        # Finf the begining of the scan
        self.currentline = self.filein.readline()
        self.currentline = string.split(self.currentline,self.newline)
        while (self.currentline[0] == '') or (self.currentline[0][0] == '#'):
            self.currentline = self.filein.readline()
            self.currentline = string.split(self.currentline,self.newline)
        self.sweep_length = 0
        while self.currentline[0] != '':
            self.sweep_length += 1
            self.currentline = self.filein.readline()
            self.currentline = string.split(self.currentline,self.newline)
        if XP.ExperimentalData['dimensions'][1] != self.sweep_length:
            XP.ExperimentalData['dimensions'][1] = self.sweep_length
            print 'Changing the sweep length given in the header to: ' + str(self.sweep_length)
