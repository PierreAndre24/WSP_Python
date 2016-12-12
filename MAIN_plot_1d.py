import h5py
import numpy as np
import MultiDimExperiment, ExperimentFileManager
import matplotlib.pyplot as plt

XP = MultiDimExperiment.MultiDimExperiment()
FM = ExperimentFileManager.ExperimentFileManager(XP)

filepath = '/Users/pierre-andremortemousque/Documents/Research/GitHub/Data'
filename = 'stat8_1325_2.h5'
FM.Read_Experiment_File(filepath = filepath,\
                        filename = filename,\
                        group_name = 'raw_data')

#print XP.ExperimentalData['data'].shape

fig = plt.figure()
ax = fig.add_subplot(2, 2, 1)
plt.plot(XP.ExperimentalData['data'][0,:,55,900,0])
ax = fig.add_subplot(2, 2, 2)
plt.plot(XP.ExperimentalData['data'][1,:,55,900,0])
ax = fig.add_subplot(2, 2, 3)
plt.plot(XP.ExperimentalData['data'][2,:,55,900,0])
ax = fig.add_subplot(2, 2, 4)
plt.plot(XP.ExperimentalData['data'][3,:,55,900,0])
ax.set_title(filename)
plt.show()
