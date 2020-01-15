from tkinter import IntVar

class PlotSettings:

    def __init__(self):
        
        self.vars = {"PlotSettings": {"target_histogram": IntVar(),
                                      "train_test_plots": IntVar(),
                                      "predicted_vs_true": IntVar(),
                                      "predicted_vs_true_bars": IntVar(),
                                      "best_worst_per_point": IntVar(),
                                      "feature_vs_target": IntVar(),
                                      "average_normalized_errors": IntVar()}}