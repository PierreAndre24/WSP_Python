import os
import LVMManager, MultiDimExperiment

class ExperimentFileManager():

    def __init__(self,XP):
        self.XP = XP

    def Read_Experiment_File(self,filepath = os.getcwd(),filename = 'file.lvm'):
        if filename[-3:] == 'lvm':
            self.CurrentFileIO = LVMManager.LVM_IO()
        filepathname = filepath + os.sep + filename
        self.CurrentFileIO.Read_header(filepathname, self.XP)
        self.CurrentFileIO.Read_FastSequence()

    def Write_Experiment_to_h5(self,\
            filepath = os.getcwd(),\
            filename = 'file.h5',\
            group = 'raw_data'):
        pass

if __name__ == "__main__":
    XP = MultiDimExperiment.MultiDimExperiment()
    FM = ExperimentFileManager(XP)
    FM.Read_Experiment_File(filepath = '/Users/pierre-andremortemousque/Documents/Research/GitHub/Data',\
                            filename = "stat8_1124.lvm")
    FM.Write_Experiment_to_h5(filepath = '/Users/pierre-andremortemousque/Documents/Research/GitHub/Data',\
                              filename = "stat8_1124.h5",\
                              group = 'raw_data')

    print XP.FileInfo
    print XP.ExperimentData
    print XP.ExperimentParameters
