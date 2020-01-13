class LearningCurve:
    def __init__(self):
        self.vars = {"estimator": None, "cv": None, "scoring": "root_mean_squared_error",
                     "n_features_to_select": 5, "selector_name": selector_name}