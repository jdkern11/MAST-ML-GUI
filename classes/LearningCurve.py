class LearningCurve:
    def __init__(self):
    
        self.combobox_options = {"LearningCurveestimatorCB": ['---'],
                                 "LearningCurvecvCB": ['---'],
                                 "LearningCurveselector_nameCB": ['---'],
                                 "LearningCurvescoringCB": ["root_mean_squared_error"]}
        # Estimator needs to match an entry in models (_learn appended)
        # CV needs to match an entry in datasplits (_learn appended)
        # selector_name needs to match featureselection entry
        self.vars = {"LearningCurve": {"estimatorCB": "---", 
                                       "cvCB": "---", 
                                       "scoringCB": "root_mean_squared_error",
                                       "n_features_to_select": 5, 
                                       "selector_nameCB": "---"}}
                                       
                                       
   # This method initializes the combobox_options based on user choices
    #
    # Variables: self, option ("model" or "ds" or "fs"), tf (true false list for choices), names (names of the options for comboboxes)
    def combobox_initialization(self, option, tf, names):
        name_list = list()
        for val,name in zip(tf,names):
            if (val.get() == 1):
                name_list.append(name)
                
        if (option == "model"):
            for option in self.combobox_options:
                if (option.find("estimatorCB") != -1):
                    self.combobox_options[option] = name_list
        
        
        elif (option == "ds"):
            for option in self.combobox_options:
                if (option.find("cvCB") != -1):
                    self.combobox_options[option] = name_list
                    
        elif (option == "fs"):
            for option in self.combobox_options:
                if (option.find("nameCB") != -1):
                    self.combobox_options[option] = name_list