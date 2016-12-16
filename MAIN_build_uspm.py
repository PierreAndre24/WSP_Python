import h5py
import numpy as np
import MultiDimExperiment, ExperimentFileManager

XP = MultiDimExperiment.MultiDimExperiment()
FM = ExperimentFileManager.ExperimentFileManager(XP)

filepath = '/Users/pierre-andremortemousque/Documents/Research/2014-15_Neel/Experimental/Ratatouille/Ratatouille32CD8f3'
filename = 'stat8_1444'
#FM.Read_Experiment_File(filepath = filepath, filename = filename + '.lvm')
#FM.Write_Experiment_to_h5(group_name = 'raw_data')
FM.Read_Experiment_File(filepath = filepath, filename = filename + '.h5', group_name = 'raw_data')

regions = [[25,38],\
           [55,70]]

final_shape = XP.ExperimentalData['dimensions']
final_shape[1] = len(regions)
locdata = np.zeros(final_shape)

for i1,ri in enumerate(regions):
    locdata[:,i1,:,:,:] = np.sum(XP.ExperimentalData['data'][:,ri[0]:ri[1],:,:,:], axis = 1, keepdims = False)

XP.ExperimentalData['dimensions'][1] = final_shape[1]
XP.ExperimentalData['data'] = locdata

FM.Write_Experiment_to_h5(group_name = 'uspm')
