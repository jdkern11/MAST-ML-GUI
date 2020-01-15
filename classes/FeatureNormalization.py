from tkinter import IntVar

class FeatureNormalization:
    def __init__(self):
        # Add combolist for output_distribution later probably
        self.vars ={"Binarizer": {"threshold": 0.0},
                    "MaxAbsScaler": None,
                    "MinMaxScaler": None,
                    "Normalizer": {"norm": 12},
                    "QuantileTransformer": {"n_quantiles": 1000, "output_distribution": "uniform"},
                    "RobustScaler": {"with_centering": IntVar(), "with_scaling": IntVar()},
                    "StandardScaler": None,
                    "MeanStdevScaler": {"mean": 0, "stdev": 1}}