import h5py, os
import numpy as np
import MultiDimExperiment, ExperimentFileManager

XP = MultiDimExperiment.MultiDimExperiment()
FM = ExperimentFileManager.ExperimentFileManager(XP)

FM.Read_Experiment_File(filepath = '/Users/pierre-andremortemousque/Documents/Research/2014-15_Neel/Experimental/Ratatouille/Ratatouille32CD8f3',\
                        filename = 'stat8_1444.lvm',\
                        read_multiple_files = False)

FM.Write_Experiment_to_h5(filename = "stat8_1444.h5", group_name = 'raw_data', force_overwrite = True)
