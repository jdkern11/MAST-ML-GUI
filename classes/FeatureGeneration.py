from tkinter import IntVar

class FeatureGeneration:
    def __init__(self):
        # Make list for feature generation vars     
        self.feature_types = ["composition_avg","arithmetic_avg","max","min","difference","elements"]
        feature_types_binary = list()
        for i in self.feature_types:
            feature_types_binary.append(IntVar())
        self.vars ={"Magpie": {"composition_featureCB": None, "feature_types": feature_types_binary},
                    "MaterialsProject":{"composition_featureCB": None, "api_key": "fill in"},
                    "Citrine": {"composition_featureCB": None, "api_key": "fill in"},
                    "ContainsElement": {"composition_featureCB": None, "all_elements": IntVar(), "element": "Ex: Al", "new_name": "Ex: has_Al"},
                    "PolynomialFeatures": {"degree": 2, "interaction_only": IntVar(), "include_bias": IntVar()}}
                    
        self.combobox_options = {"Magpiecomposition_featureCB": None,
                                 "MaterialsProjectcomposition_featureCB": None,
                                 "Citrinecomposition_featureCB": None,
                                 "ContainsElementcomposition_featureCB": None}

    def combobox_initialization(self, names):
        for key in self.combobox_options:
            self.combobox_options[key] = names
