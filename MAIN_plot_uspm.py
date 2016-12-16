import h5py
import numpy as np
import plot_miscellaneous as plot_misc
import MultiDimExperiment, ExperimentFileManager
import matplotlib.pyplot as plt

XP = MultiDimExperiment.MultiDimExperiment()
FM = ExperimentFileManager.ExperimentFileManager(XP)

filepath = '/Users/pierre-andremortemousque/Documents/Research/2014-15_Neel/Experimental/Ratatouille/Ratatouille32CD8f3'
filename = 'stat8_1444'
group_name = 'uspm_diff'
FM.Read_Experiment_File(filepath = filepath, filename = filename + '.h5', group_name = group_name)

qpc_list = [0,1,2,3]
fig = plt.figure()
for i,qpc in enumerate(qpc_list):
    subfigsize = plot_misc.OptimalSubFig(len(qpc_list))
    fig.add_subplot(subfigsize[0], subfigsize[1], i+1)
    z = XP.ExperimentalData['data'][qpc,0,:,:,0]
    p = plt.imshow(z, interpolation='none')
    plt.clim()   # clamp the color limits
    plt.title("us pulse map of " + filename)

plt.show()
