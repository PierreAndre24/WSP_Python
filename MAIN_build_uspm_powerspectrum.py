import h5py
import numpy as np
from scipy import signal
import MultiDimExperiment, ExperimentFileManager
import matplotlib.pyplot as plt

XP = MultiDimExperiment.MultiDimExperiment()
FM = ExperimentFileManager.ExperimentFileManager(XP)

filepath = '/Users/pierre-andremortemousque/Documents/Research/GitHub/Data'
filename = 'stat8_1229_uspm'

FM.Read_Experiment_File(filepath = filepath, filename = filename + '.h5', group_name = 'raw_data')

# regions = [[25,40],[55,70]]
regions = [[25,40],[55,70]]

original_data = XP.ExperimentalData['data'][:]

for i1,ri in enumerate(regions):
    final_shape = XP.ExperimentalData['dimensions']
    final_shape[1] = len(signal.periodogram(original_data[0,ri[0]:ri[1],0,0,0])[1])
    locdata = np.zeros(final_shape)

    for i0 in range(final_shape[0]):
        for i2 in range(final_shape[2]):
            for i3 in range(final_shape[3]):
                for i4 in range(final_shape[4]):
                    #print str(i0) + ' ' + str(i2) + ' ' + str(i3) + ' ' + str(i4)
                    f, Pxx_den = signal.periodogram(original_data[i0,ri[0]:ri[1],i2,i3,i4],\
                                                    return_onesided = True)
                    locdata[i0,:,i2,i3,i4] = Pxx_den
    XP.ExperimentalData['dimensions'][1] = final_shape[1]
    XP.ExperimentalData['data'] = locdata

    FM.Write_Experiment_to_h5(group_name = 'p_uspm_powerspectrum_' + str(i1))
