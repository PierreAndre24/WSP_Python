import string
import re

class LVM_IO:

    def __init(self):
        self.expected_header = [ \
            ['# measurement file writer version',0], \
            ['expected number of points',0],\
            ['measured values converted in',2],\
            ['#DAC initial values (V)',64],\
            ['#Mag field initial Value',1]]
        self.endofheader_string = '#sweep'

    def Read_header(self,filein, XP):
        self.header_size = 0
        currentline = filein.readline()
        currentline = re.findall("[-+]?\d+[\.]?\d*[eE]?[-+]?\d*", currentline)
        XP.fileversion = float(currentline[0])

    def _read_header_size(self,filein):
        FLAG_end_of_header = False
        self.header_size = 0
        while not FLAG_end_of_header:
            currentline = filein.readline()
            if len(currentline) >= len(self.endofheader_string):
                if currentline[0:len(self.endofheader_string)-1] == self.endofheader_string:
                    FLAG_end_of_header = True
            self.header_size += 1
