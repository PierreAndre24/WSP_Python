import os, h5py
import numpy as np
import LVMManager, MultiDimExperiment

class ExperimentFileManager():

    def __init__(self,XP):
        self.XP = XP
        self.compression_type = 'gzip'
        self.compression_level = 9
        self.fileversion = 1.0

    def Read_Experiment_File(self,\
                             filepath = os.getcwd(),\
                             filename = 'file.lvm',\
                             read_fstsq = False):
        if filename[-3:] == 'lvm':
            self.CurrentFileIO = LVMManager.LVM_IO(read_fstsq)
            filepathname = filepath + os.sep + filename
            self.CurrentFileIO.Read_header(filepathname, self.XP)
            filepathname = filepath + os.sep + filename[:-3] + 'fstsq'
            self.CurrentFileIO.Read_FastSequence(filepathname, self.XP)

    def Write_Experiment_to_h5(self,\
            filepath = os.getcwd(),\
            filename = 'file.h5',\
            group_name = '/raw_data'):

        #File name
        filepathname = filepath + os.sep + filename

        # Create the h5 file
        f = h5py.File(filepathname,'a')

        # Give the file version
        f.attrs['fileversion'] = self.fileversion

        # Create the main group
        # If it exists already, ask the user what to do
        if group_name in f.keys():
            answer = raw_input("Do you want to replace the existing group? y/n")
            if answer == 'y':
                del f[group_name]
                group = f.create_group(group_name)
            else:
                f.close()
                return
        else:
            group = f.create_group(group_name)

        # Create the parameters and data datasets

        # ExperimentalData
        chunkSize = self.XP.ExperimentalData['dimensions']
        if len(chunkSize) > 2:
            for i in range(2,len(chunkSize)):
                chunkSize[i] = 1
        ExperimentalData = f.create_dataset(\
                group_name + "/ExperimentalData", \
                tuple(chunkSize), \
                compression = self.compression_type, \
                compression_opts = self.compression_level)

        # ExperimentalParameters
        subgroup_ep = f.create_group(group_name + '/ExperimentalParameters')
        # chunkSize = self.XP.ExperimentalParameters['Info']['dimensions']
        # if len(chunkSize) > 2:
        #     for i in range(2,len(chunkSize)):
        #         chunkSize[i] = 1
        # ExperimentalParameters = f.create_dataset(\
        #         group_name + "/ExperimentalParameters", \
        #         tuple(chunkSize), \
        #         compression = self.compression_type, \
        #         compression_opts = self.compression_level)

        # Write the FileInfo entries as attributes of the group "group_name"
        for e in self.XP.FileInfo.keys():
            group.attrs[e] = self.XP.FileInfo[e]

        # Write the Info entries as attributes of the group "Parameters"
        # Start with the dictionaries
        # Build the list of dictionaries not to take into account for the loop saving
        self._dict_list_ep = []
        # Save the Fastchannels dictionary
        if 'Fastchannels' in self.XP.ExperimentalParameters['Info'].keys():
            self._dict_list_ep.append('Fastchannels')
            Fastchannels = []
            for e in self.XP.ExperimentalParameters['Info']['Fastchannels']:
                index = e
                DAC_column = self.XP.ExperimentalParameters['Info']['Fastchannels'][e][0]
                DAC_row = self.XP.ExperimentalParameters['Info']['Fastchannels'][e][1]
                Fastchannels.append([index,DAC_column,DAC_row])
            print np.asarray(Fastchannels)
            subgroup_ep.attrs['Fastchannels'] = np.asarray(Fastchannels)

        for e in self.XP.ExperimentalParameters['Info'].keys():
            if e not in self._dict_list_ep:
                subgroup_ep.attrs[e] = self.XP.ExperimentalParameters['Info'][e]




if __name__ == "__main__":
    XP = MultiDimExperiment.MultiDimExperiment()
    FM = ExperimentFileManager(XP)
    FM.Read_Experiment_File(filepath = '/Users/pierre-andremortemousque/Documents/Research/GitHub/Data',\
                            filename = "stat8_1124.lvm",\
                            read_fstsq = True)
    FM.Write_Experiment_to_h5(filepath = '/Users/pierre-andremortemousque/Documents/Research/GitHub/Data',\
                              filename = "stat8_1124.h5",\
                              group_name = 'raw_data')
