import h5py, os
import numpy as np
import MultiDimExperiment, ExperimentFileManager

XP = MultiDimExperiment.MultiDimExperiment()
FM = ExperimentFileManager.ExperimentFileManager(XP)

FM.Read_Experiment_File(filepath = '/Users/pierre-andremortemousque/Documents/Research/2014-15_Neel/Experimental/Ratatouille/Ratatouille32CD8f2',\
                        filename = "stat8_1428_00000.lvm",\
                        read_multiple_files = True)
FM.Write_Experiment_to_h5(filename = "stat8_1428.h5", group_name = 'raw_data', force_overwrite = True)

# filepath = '/Users/pierre-andremortemousque/Documents/Research/2014-15_Neel/Experimental/Ratatouille/Ratatouille32CD8f2'
# filename = 'stat8_1428_00000.lvm'
# filein = open(filepath + os.sep + filename,'r')
# filein_txt = filein.readlines()
# filein.close()

# locdata = np.genfromtxt(filepath + os.sep + filename, dtype = float, skip_header = 81)
#
# print locdata[81:81+10]
