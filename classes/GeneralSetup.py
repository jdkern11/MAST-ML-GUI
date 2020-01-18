from tkinter import IntVar

class GeneralSetup:

    def __init__(self):
        
        self.metrics = ['root_mean_squared_error', 'mean_absolute_error']
        
        met = list()
        for metric in self.metrics:
            met.append(IntVar())
        
        self.vars = {"input_features": {"Auto": IntVar(), "features": list()}, 
                      "input_target": "---", 
                      "randomizer": IntVar(),
                      "metrics": {"Auto": IntVar(), "tf": met},
                      "input_testdata": list(),
                      "input_grouping": "---", 
                      "input_other": list()}