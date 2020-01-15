from tkinter import IntVar

class GeneralSetup:

    def __init__(self):
        
        self.metrics = ['root_mean_squared_error', 'mean_absolute_error']
        
        met = list()
        for metric in self.metrics:
            met.append(IntVar())
        
        self.vars = {"input_features": None, 
                      "target_feature": None, 
                      "randomizer": IntVar(),
                      "metrics": met,
                      "not_input_features": None,
                      "grouping_feature": None, 
                      "validation_columns": None}