import h5py
import numpy as np
import MultiDimExperiment, ExperimentFileManager
import matplotlib.pyplot as plt

XP = MultiDimExperiment.MultiDimExperiment()
FM = ExperimentFileManager.ExperimentFileManager(XP)

filepath = '/Users/pierre-andremortemousque/Documents/Research/GitHub/Data'
filename = 'stat8_1229_uspm'
group_name = 'p_uspm_powerspectrum_1'
FM.Read_Experiment_File(filepath = filepath, filename = filename + '.h5', group_name = group_name)

loc_data = XP.ExperimentalData['data'][:]
qpc = 1
print XP.ExperimentalData['data'][qpc,:,:,:,:].shape
y = np.mean(XP.ExperimentalData['data'][qpc,:,:,:,:], axis = (1,2,3), keepdims = False)

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
plt.plot(y)
plt.show()
