import os, h5py
import numpy as np
import h5Manager, LVMManager, MultiDimExperiment

class ExperimentFileManager():

    def __init__(self,XP):
        self.XP = XP
        self.compression_type = 'gzip'
        self.compression_level = 9
        self.fileversion = 1.0

    def Read_Experiment_File(self,\
                             filepath = os.getcwd(),\
                             filename = 'file.lvm',\
                             group_name = '',\
                             read_fstsq = True,\
                             read_multiple_files = False):

        if filename[-3:] == 'lvm':

            self.CurrentFileIO = LVMManager.LVM_IO(read_fstsq)

            # save the path to reuse eventually in the writing
            # we do it here to simply remove the filename extension
            self.filepath = filepath
            self.filename = filename[:-4]

            # read the main file
            self.CurrentFileIO.Read_header(filepath, filename, self.XP, read_multiple_files)
            self.CurrentFileIO.Read_data(filepath, filename, self.XP, read_multiple_files)

            # read the fast sequence file if it exists
            self.CurrentFileIO.Read_FastSequence(filepath, filename, self.XP, read_multiple_files)

        elif filename[-2:] == 'h5':
            self.CurrentFileIO = h5Manager.h5_IO(read_fstsq)

            # save the path to reause eventually in the writing
            # we do it here to simply remove the filename extension
            self.filepath = filepath
            self.filename = filename[:-3]

            # read the main file
            self.CurrentFileIO.Read_header(filepath, filename, self.XP, group_name)
            self.CurrentFileIO.Read_data(filepath, filename, self.XP, group_name)

            # read the fast sequence file if it exists
            self.CurrentFileIO.Read_FastSequence(filepath, filename, self.XP, group_name)

    def Write_Experiment_to_h5(self,\
            filepath = '',\
            filename = '',\
            group_name = 'raw_data'):

        #File name
        if filepath == '':
            filepath = self.filepath # recall the path of the original file
        if filename == '':
            filename = self.filename + '.h5'# recall the name of the original file minus extension
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

        # Write the FileInfo entries as attributes of the group "group_name"
        for e in self.XP.FileInfo.keys():
            group.attrs[e] = self.XP.FileInfo[e]

        # Create the parameters and data datasets

        # ExperimentalData
        chunkSize = [1]*len(self.XP.ExperimentalData['dimensions'])
        chunkSize[0] = self.XP.ExperimentalData['dimensions'][0]
        chunkSize[1] = self.XP.ExperimentalData['dimensions'][1]
        #chunkSize[2] = self.XP.ExperimentalData['dimensions'][2]

        # ExperimentalDataSet abbreviated as ExpD
        self.ExpDExceptions = []
        self.ExpDExceptions.append('data')
        ExpD = f.create_dataset(\
                group_name + "/ExperimentalData", \
                shape = tuple(self.XP.ExperimentalData['dimensions']), \
                chunks = True,\
                compression = self.compression_type, \
                compression_opts = self.compression_level)
        ExpD[:] = self.XP.ExperimentalData['data']

        # Save the Info entries as attributes of the data
        for e in self.XP.ExperimentalData.keys():
            if e not in self.ExpDExceptions:
                ExpD.attrs[e] = self.XP.ExperimentalData[e]

        # ExperimentalParameters group as ExpP
        ExpP = f.create_group(group_name + '/ExperimentalParameters')

        # Write the Info entries as attributes of the group "ExperimentalParameters"

        # Start with the dictionaries and DS
        self.ExpPInfoExceptions = []
        # Save the Fastsequence as a dataset to be more or less in agreement with the labview 1.13 h5 version
        chunkSize = [len(self.XP.ExperimentalParameters['Fastsequence']), 3]
        ExpPFastS = f.create_dataset(\
                group_name + "/ExperimentalParameters/Fastsequence", \
                tuple(chunkSize), \
                compression = self.compression_type, \
                compression_opts = self.compression_level)
        ExpPFastS[:] = np.asarray(self.XP.ExperimentalParameters['Fastsequence'])

        # Save all parameters as DS
        # First write the the name of all moving parameters
        all_moving_parameters = []
        loc_dict_of_ExpP_MP = {}
        for k in self.XP.ExperimentalParameters['moving_parameters'].keys():
            if k != 'dimensions':
                all_moving_parameters.append(k)
                loc_dict_of_ExpP_MP[k] = f.create_dataset(\
                        group_name + "/ExperimentalParameters/" + k,\
                        tuple(self.XP.ExperimentalParameters['moving_parameters'][k]['dimensions']),\
                        chunks = True,\
                        compression = self.compression_type,\
                        compression_opts = self.compression_level)

                loc_dict_of_ExpP_MP[k][:] = self.XP.ExperimentalParameters['moving_parameters'][k]['values']
                loc_dict_of_ExpP_MP[k].attrs['dimensions'] = self.XP.ExperimentalParameters['moving_parameters'][k]['dimensions']
                loc_dict_of_ExpP_MP[k].attrs['unit'] = self.XP.ExperimentalParameters['moving_parameters'][k]['unit']
                loc_dict_of_ExpP_MP[k].attrs['type'] = self.XP.ExperimentalParameters['moving_parameters'][k]['type']
                if 'DAC' in XP.ExperimentalParameters['moving_parameters'][k]['type']:
                    loc_dict_of_ExpP_MP[k].attrs['DAC_row'] = self.XP.ExperimentalParameters['moving_parameters'][k]['DAC_row']
                    loc_dict_of_ExpP_MP[k].attrs['DAC_column'] = self.XP.ExperimentalParameters['moving_parameters'][k]['DAC_column']
                if 'fast' in XP.ExperimentalParameters['moving_parameters'][k]['type']:
                    loc_dict_of_ExpP_MP[k].attrs['slot'] = self.XP.ExperimentalParameters['moving_parameters'][k]['slot']
        ExpP.attrs['all_moving_parameters'] = all_moving_parameters

        # Save the Fastchannels dictionary
        if 'Fastchannels' in self.XP.ExperimentalParameters['Info'].keys():
            Fastchannels = []
            self.ExpPInfoExceptions.append('Fastchannels')
            for e in self.XP.ExperimentalParameters['Info']['Fastchannels']:
                index = e
                DAC_column = self.XP.ExperimentalParameters['Info']['Fastchannels'][e][0]
                DAC_row = self.XP.ExperimentalParameters['Info']['Fastchannels'][e][1]
                Fastchannels.append([index,DAC_column,DAC_row])
            ExpPFastS.attrs['Fastchannels'] = np.asarray(Fastchannels)

        # Save the rest
        for e in self.XP.ExperimentalParameters['Info'].keys():
            if e not in self.ExpPInfoExceptions:
                ExpP.attrs[e] = self.XP.ExperimentalParameters['Info'][e]




if __name__ == "__main__":
    XP = MultiDimExperiment.MultiDimExperiment()
    FM = ExperimentFileManager(XP)
    FM.Read_Experiment_File(filepath = '/Users/pierre-andremortemousque/Documents/Research/GitHub/Data',\
                            filename = "stat8_1124.lvm",\
                            read_multiple_files = False)
    FM.Write_Experiment_to_h5()

    FM.Read_Experiment_File(filepath = '/Users/pierre-andremortemousque/Documents/Research/GitHub/Data',\
                            filename = "stat8_1124.h5",\
                            group_name = 'raw_data')

    print XP.ExperimentalData['dimensions']
