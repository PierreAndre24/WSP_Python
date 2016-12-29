import h5py
import numpy as np
import plot_miscellaneous as plot_misc
import MultiDimExperiment, ExperimentFileManager
import matplotlib.pyplot as plt

XP = MultiDimExperiment.MultiDimExperiment()
FM = ExperimentFileManager.ExperimentFileManager(XP)

filepath = '/Users/pierre-andremortemousque/Documents/Research/2014-15_Neel/Experimental/Ratatouille/Ratatouille32CD8f2'
filename = 'stat8_1428'
group_name = 'uspm_diff'
FM.Read_Experiment_File(filepath = filepath, filename = filename + '.h5', group_name = group_name)

qpc_list = [0,1,2,3]


fig = plt.figure()
for i,qpc in enumerate(qpc_list):
    subfigsize = plot_misc.OptimalSubFig(len(qpc_list))
    fig.add_subplot(subfigsize[0], subfigsize[1], i+1)

    data = XP.ExperimentalData['data'][qpc,0,-1,:,0]
    #n, bins, patches = plt.hist(data, 50, normed=1, facecolor='green', alpha=0.75)
    n, bins, patches = plt.hist(data, 50, facecolor='green', alpha=0.75)
    plt.xlabel('Current')
    plt.ylabel('Counts')

    #plt.title(r'$\mathrm{Histogram\ of\ :}\ \mu=100,\ \sigma=15$')
    #plt.axis([40, 160, 0, 0.03])
    plt.grid(True)

plt.show()
