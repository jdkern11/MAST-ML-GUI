from tkinter import IntVar

class HyperOpt:
    def __init__(self):
        # Make combolists for these variables
        #mse = mean square error, mae = mean absolute error
        self.combobox_options = {"GridSearchestimatorCB": ['---'], "GridSearchcvCB": ['---'],
                                "RandomizedSearchestimatorCB": ['---'], "RandomizedSearchcvCB": ['---'], 
                                "BayesianSearchestimatorCB": ['---'], "BayesianSearchcvCB": ['---']} 
        self.vars = {"GridSearch": { "estimatorCB" : "---", "cvCB" : "---", "param_names": "---", "param_values": "---", "scoring": "root_mean_squared_error"},
                     "RandomizedSearch": {"estimatorCB" : "---", "cvCB" : "---", "param_names": "---", "param_values": "---", "scoring": "root_mean_squared_error", "n_iter": 50},
                     "BayesianSearch": {"estimatorCB" : "---", "cvCB" : "---", "param_names": "---", "param_values": "---", "scoring": "root_mean_squared_error", "n_iter": 50}}
                     
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
                    