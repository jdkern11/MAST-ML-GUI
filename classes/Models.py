class Models:
    def __init__(self):
        # Make combolists for these variables
        self.vars = {"AdaBoostClassifier": { "n_estimators" : 50, "learning_rate" : 1.0},
                           "AdaBoostRegressor": { "n_estimators" : 50, "learning_rate" : 1.0},
                           "BaggingClassifier": { "n_estimators" : 50, "maxamples" : 1.0, "max_features" : 1.0},
                           "BaggingRegressor": { "n_estimators" : 50, "maxamples" : 1.0, "max_features" : 1.0},
                           "ExtraTreesClassifier": { "n_estimators" : 50, "criterion" : "gini", "minamples_split" : 2, "min_samples_leaf" : 1},
                           "ExtraTreesRegressor": { "n_estimators" : 50, "criterion" : "mse", "minamples_split" : 2, "min_samples_leaf" : 1},
                           "GradientBoostingClassifier": { "loss" : "deviance", "learning_rate" : 1.0, "n_estimators" : 100, "subsample" : 1.0, "criterion" : "friedman_mse", "minamples_split" : 2, "min_samples_leaf" : 1},
                           "GradientBoostingRegressor": { "loss" : "ls", "learning_rate" : 0.1, "n_estimators" : 100, "subsample" : 1.0, "criterion" : "friedman_mse", "minamples_split" : 2, "min_samples_leaf" : 1},
                           "RandomForestClassifier": { "n_estimators" : 10, "criterion" : "gini", "minamples_leaf" : 1, "min_samples_split" : 2},
                           "RandomForestRegressor": { "n_estimators" : 10, "criterion" : "mse", "minamples_leaf" : 1, "min_samples_split" : 2},
                           "KernelRidge": { "alpha" : 1, "kernel" : "linear"},
                           "KernelRidgeelectMASTML": { "alpha" : 1, "kernel" : "linear"},
                           "KernelRidge_learn": { "alpha" : 1, "kernel" : "linear"},
                           "ARDRegression": { "n_iter" : 300},
                           "BayesianRidge": { "n_iter" : 300},
                           "ElasticNet": { "alpha" : 1.0},
                           "HuberRegressor": { "epsilon" : 1.35, "max_iter" : 100},
                           "Lars": None,
                           "Lasso": { "alpha" : 1.0},
                           "LassoLars": { "alpha" : 1.0, "max_iter" : 500},
                           "LassoLarsIC": { "criterion" : "aic", "max_iter" : 500},
                           "LinearRegression": None,
                           "LogisticRegression": { "penalty" : 12, "C" : 1.0},
                           "Perceptron": { "alpha" : 0.0001},
                           "Ridge": { "alpha" : 1.0},
                           "RidgeClassifier": { "alpha" : 1.0},
                           "SGDClassifier": { "loss" : "hinge", "penalty" : 12, "alpha" : 0.0001},
                           "SGDRegressor": { "loss" : "squared_loss", "penalty" : 12, "alpha" : 0.0001},
                           "MLPClassifier": { "hidden_layerizes" : 100, "activation" : "relu", "solver" : "adam", "alpha" : 0.0001, "batch_size" : "auto", "learning_rate" : "constant"},
                           "MLPRegressor": { "hidden_layerizes" : 100, "activation" : "relu", "solver" : "adam", "alpha" : 0.0001, "batch_size" : "auto", "learning_rate" : "constant"},
                           "LinearSVC": { "penalty" : 12, "loss" : "squared_hinge", "tol" : 0.0001, "C" : 1.0},
                           "LinearSVR": { "epsilon" : 0.1, "loss" : "epsilon_insensitive", "tol" : 0.0001, "C" : 1.0},
                           "NuSVC": { "nu" : 0.5, "kernel" : "rbf", "degree" : 3},
                           "NuSVR": { "nu" : 0.5, "C" : 1.0, "kernel" : "rbf", "degree" : 3},
                           "SVC": { "C" : 1.0, "kernel" : "rbf", "degree" : 3},
                           "SVR": { "C" : 1.0, "kernel" : "rbf", "degree" : 3},
                           "DecisionTreeClassifier": { "criterion" : "gini", "splitter" : "best", "minamples_split" : 2, "min_samples_leaf" : 1},
                           "DecisionTreeRegressor": { "criterion" : "mse", "splitter" : "best", "minamples_split" : 2, "min_samples_leaf" : 1},
                           "ExtraTreeClassifier": { "criterion" : "gini", "splitter" : "random", "minamples_split" : 2, "min_samples_leaf" : 1},
                           "ExtraTreeRegressor": { "criterion" : "mse", "splitter" : "random", "minamples_split" : 2, "min_samples_leaf" : 1}}