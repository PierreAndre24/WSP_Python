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
fig.add_subplot(1,1,1)



t = XP.ExperimentalParameters['moving_parameters']['timing [27]']['values'][0,0,:,0,0]

y = np.zeros(len(t))
for it in range(len(t)):
    data = XP.ExperimentalData['data'][1,0,it,:,5]
    for d in data:
        if d > 80.:
            y[it] += 1
print y
plt.plot(t,y)
plt.xlabel('Current')
plt.ylabel('Counts')
plt.title('stat8_1428_TL')

plt.grid(True)

plt.show()
