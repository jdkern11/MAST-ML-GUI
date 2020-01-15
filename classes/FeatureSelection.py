class FeatureSelection:

    def __init__(self): 
        self.combobox_options = {"RFEestimatorCB": None,
                                 "SequentialFeatureSelectorestimatorCB": None,
                                 "RFECVestimatorCB": None, "RFECVcvCB": None,
                                 "SelectFromModelestimatorCB": None,
                                 "MASTMLFeatureSelectorestimatorCB": None, "MASTMLFeatureSelectorcvCB": None}

        self.vars ={"GenericUnivariateSelect": None,
                    "SelectPercentile": None,
                    "SelectKBest": None,
                    "SelectFpr": None,
                    "SelectFdr": None,
                    "SelectFwe": None,
                    # Estimator needs to match an entry in models (_selectRFE appended)
                    "RFE": { "estimatorCB" : None, "n_features_to_select" : 5, "step" : 1},
                    # Estimator needs to match an entry in models (_selectSFS appended)
                    "SequentialFeatureSelector": { "estimatorCB" : None, "k_features" : 5},
                    # Estimator needs to match an entry in models (_selectRFECV appended)
                    # CV needs to match an entry in datasplits (_selectRFECV appended)
                    "RFECV": { "estimatorCB" : None, "step" : 1, "cvCB" : None, "min_features_to_select" : 1},
                    # Estimator needs to match an entry in models (_selectfrommodel appended)
                    "SelectFromModel": { "estimatorCB" : None, "max_features" : 5},
                    "VarianceThreshold": { "threshold" : 0},
                    "PCA": { "n_components" : 5},
                    # Estimator needs to match an entry in models (_selectMASTML appended)
                    # CV needs to match an entry in Datasplits (_selectMASTML appended)
                    "MASTMLFeatureSelector": { "estimatorCB" : None, "n_features_to_select" : 5, "cvCB" : None}}
                    
    # This method initializes the combobox_options based on user choices
    #
    # Variables: self, option ("model" or "ds"), tf (true false list for choices), names (names of the options for comboboxes)
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