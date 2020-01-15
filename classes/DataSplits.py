from tkinter import IntVar

class DataSplits:
    def __init__(self):
    
        self.combobox_options = {"LeaveOneGroupOutgrouping_columnCB": None}
        
        # Grouping column of leavonegroupout will be headers
        self.vars ={"NoSplit": None,
                    "KFold": { "shuffle" : IntVar(), "n_splits" : 10},
                    "RepeatedKFold": { "n_splits" : 5, "n_repeats" : 10},
                    "GroupKFold": { "n_splits" : 3},
                    "LeaveOneOut": None,
                    "LeavePOut": { "p" : 10},
                    "RepeatedStratifiedKFold": { "n_splits" : 5, "n_repeats" : 10},
                    "StratifiedKFold": { "n_splits" : 3},
                    "ShuffleSplit": { "n_splits" : 10},
                    "StratifiedShuffleSplit": { "n_splits" : 10},
                    "LeaveOneGroupOut": { "grouping_columnCB" : None}}
                    
    def combobox_initialization(self, names):
        self.combobox_options["LeaveOneGroupOutgrouping_columnCB"] = names
                    