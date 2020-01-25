from tkinter import IntVar

class MiscSettings:

    def __init__(self):
        
        self.vars = {"MiscSettings": {"plot_target_histogram": IntVar(),
                                      "plot_train_test_plots": IntVar(),
                                      "plot_predicted_vs_true": IntVar(),
                                      "plot_predicted_vs_true_average": IntVar(),
                                      "plot_best_worst_per_point": IntVar(),
                                      "plot_each_feature_vs_target": IntVar(),
                                      "plot_error_plots": IntVar(),
                                      "rf_error_method": "stdev",
                                      "rf_error_percentile": 95,
                                      "normalize_target_feature": IntVar()}}
                                      
