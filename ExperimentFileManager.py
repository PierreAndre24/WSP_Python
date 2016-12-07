import os
import LVMManager, MultiDimExperiment

class ExperimentFileManager():

    def __init__(self,XP):
        self.CurrentFileIO = LVMManager.LVM_IO()
        self.XP = XP

    def Read_LVM(self,filepath = os.getcwd(),filename = 'file.lvm'):
        filepathname = filepath + os.sep + filename
        filein = open(filepathname,'r')
        # L1list = filein.readline()
        self.CurrentFileIO.Read_header(filein, self.XP)


if __name__ == "__main__":
    XP = MultiDimExperiment.MultiDimExperiment()
    FM = ExperimentFileManager(XP)
    FM.Read_LVM(filename = "stat8_1032.lvm")
    print XP.fileversion
