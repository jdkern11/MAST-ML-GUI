from tkinter import *
import tkinter as tk
from tkinter import ttk
import pandas as pd
import math
import os
import time
from classes.LearningCurve import LearningCurve as LC
from classes.DataSplits import DataSplits as DS
import tkinter.filedialog as fd

#--------------------------------------------------------
# Create a Graphic User Interface for MAST-ML
#
# (C) 2020 Joseph Kern, Univeristy of Wisnconsin-Madison.
# All code can be used or modified as people see fit.
# email: jkern3@wisc.edu
#--------------------------------------------------------

class GUI:
    def __init__(self):
        # Make lists of variables that will be altered based on user choices
        self.vars = {"headers": None, "csv_loc": None, "conf_loc": None, "result_loc": os.getcwd(),
                     "randomizer": IntVar(), "input_features": None, "target_feature": None, "metrics": None, 
                     "not_input_features": None, "grouping_feature": None, "validation_columns": None,
                     "cleaning_method": None, "imputation_strategy": None, "clustering": None, 
                     "FeatureGeneration": None, "composition_feature": None, "FeatureNormalization": None,
                     "models": None, "ds": None}
                     
        # General variable creations
        self.metrics = ['root_mean_squared_error', 'mean_absolute_error']                   
        met = list()
        for i in range(0,2):
            met.append(IntVar())
        self.vars["metrics"] = met
        
        
        # Cleaning methods variables
        self.cleaning_methods = ['remove', 'imputation', 'ppca']
        self.imputation_strategy = ['mean','median']
        
        # Clustering variables
        self.clustering = ['AffinityPropagation','AgglomerativeClustering','Birch','DBSCAN',
                           'KMeans','MiniBatchKMeans','MeanShift','SpectralClustering']                   
        # make a separate list of cluster variables
        # TODO find what other strings possible
        self.c_vars = {"headers": self.clustering, "AffinityPropagation": {'damping': 0.5, 'max_iter': 200, 'convergence_iter': 15, 'affinity': 'euclidean'}, 
                      "AgglomerativeClustering": {'n_clusters': 2, 'affinity': 'euclidean', 'compute_full_tree': 'auto', 'linkage': 'ward'},
                      "Birch": {'threshold': 0.5, 'branching_factor': 50, 'n_clusters': 3}, 
                      "DBSCAN": {'eps': 0.5, 'min_samples':5, 'metric': 'euclidean', 'algorithm': 'auto', 'leaf_size': 30}, 
                      "KMeans": {'n_clusters': 8, 'n_init': 10, 'max_iter': 300, 'tol': 0.0001},
                      "MiniBatchKMeans": {'n_clusters': 8, 'max_iter': 100, 'batch_size': 100}, 
                      "MeanShift": None,
                      "SpectralClustering": {'n_clusters': 8, 'n_init': 10, 'gamma': 1.0, 'affinity': 'rbf'}}
        # create list of possible values string choices in clustering
        self.affinity_propagation_affinity = ['euclidean','precomputed']
        # if ward, must be euclidean
        self.agglomerative_clustering_affinity = ['euclidean', 'l1', 'l2', 'manhattan', 'cosine', 'precomputed']
        self.compute_full_tree = ['auto', 'True', 'False']
        self.linkage = ['ward', 'complete', 'average', 'single']
        # TODO, add options for this. There are so thinks to note for it
        self.DBSCAN_metric = ['euclidean']
        self.DBSCAN_algorithm = ['auto','ball_tree','kd_tree','brute']
        # TODO there may be other pairwise kernels that can be added
        self.spectral_clustering_affinity = ['rbf','nearest_neighbors','precomputed','precomputed_nearest_neighbors']
        self.c_vars_combobox_options = {"AffinityPropagationaffinity":self.affinity_propagation_affinity,
                                        "AgglomerativeClusteringaffinity":self.agglomerative_clustering_affinity,
                                        "AgglomerativeClusteringcompute_full_tree":self.compute_full_tree,
                                        "AgglomerativeClusteringlinkage":self.linkage,
                                        "DBSCANmetric":self.DBSCAN_metric,
                                        "DBSCANalgorithm":self.DBSCAN_algorithm,
                                        "SpectralClusteringaffinity":self.spectral_clustering_affinity}
        # Cluster checkbox list
        cluster = list()
        for i in range(0,len(self.clustering)):
            cluster.append(IntVar())
        self.vars["clustering"] = cluster
                                        
        # Make list for feature generation vars     
        self.feature_types = ["composition_avg","arithmetic_avg","max","min","difference","elements"]
        feature_types_binary = list()
        for i in self.feature_types:
            feature_types_binary.append(IntVar())
        self.fg_vars = {"Magpie": {"feature_types": feature_types_binary},
                        "MaterialsProject":{"api_key": "fill in"},
                        "Citrine": {"api_key": "fill in"},
                        "ContainsElement": {"all_elements": IntVar(), "element": "Ex: Al", "new_name": "Ex: has_Al"},
                        "PolynomialFeatures": {"degree": 2, "interaction_only": IntVar(), "include_bias": IntVar()}}
        # feature generation checkbox lists
        fg = list()
        for i in range(0,len(self.fg_vars)):
            fg.append(IntVar())
        self.vars["FeatureGeneration"] = fg 
        
        # Make list of feature normalizationvars
        # Add combolist for output_distribution later probably
        self.fn_vars = {"Binarizer": {"threshold": 0.0},
                        "MaxAbsScaler": None,
                        "MinMaxScaler": None,
                        "Normalizer": {"norm": 12},
                        "QuantileTransformer": {"n_quantiles": 1000, "output_distribution": "uniform"},
                        "RobustScaler": {"with_centering": IntVar(), "with_scaling": IntVar()},
                        "StandardScaler": None,
                        "MeanStdevScaler": {"mean": 0, "stdev": 1}}
        fn = list()
        for i in range(0,len(self.fn_vars)):
            fn.append(IntVar())
        self.vars["FeatureNormalization"] = fn
        self.ds = DS()
        
        dsl = list()
        for i in range(0,len(self.ds.vars)):
            dsl.append(IntVar())
        self.vars["ds"] = dsl
        
        
        # Make combolists for these variables
        self.model_vars = {"AdaBoostClassifier": { "n_estimators" : 50, "learning_rate" : 1.0},
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
        models = list()
        for i in range(0,len(self.model_vars)):
            models.append(IntVar())
        self.vars["models"] = models
        
        # Todo: Finish later
        self.fs_vars = {"GenericUnivariateSelect": None,
                        "SelectPercentile": None,
                        "SelectKBest": None,
                        "SelectFpr": None,
                        "SelectFdr": None,
                        "SelectFwe":None,
                        "RFE": None}
                            
        
    
    # adapted from Josselin, “tkinter Canvas Scrollbar with Grid?,” Stack Overflow, 01-May-1967. [Online]. Available: https://stackoverflow.com/questions/43731784/tkinter-canvas-scrollbar-with-grid. [Accessed: 03-Jan-2020].
    # generates scrollable canvas to store data in
    # 
    # variables: frame, gr (grid row), gc (grid column), texts (text for checkbuttons), tf (true false vars for checkbuttons)
    #            w (width, number of check buttons per row), h (height, number of check buttons per column)
    def gen_y_scroll_canvas(self,frame,gr,gc,texts,tf,w,h):
        frame_canvas = tk.Frame(frame)
        frame_canvas.grid(row=gr, column=gc, pady=(w, 0), sticky='nw')
        frame_canvas.grid_rowconfigure(0, weight=1)
        frame_canvas.grid_columnconfigure(0, weight=1)
        # Set grid_propagate to False to allow w-by-h buttons resizing later
        frame_canvas.grid_propagate(False)
        canvas = tk.Canvas(frame_canvas, bg="yellow")
        canvas.grid(row=0, column=0, sticky="news")

        # Link a scrollbar to the canvas
        vsb = tk.Scrollbar(frame_canvas, orient="vertical", command=canvas.yview)
        vsb.grid(row=0, column=1, sticky='ns')
        canvas.configure(yscrollcommand=vsb.set)
        
        frame_buttons = tk.Frame(canvas, bg="blue")
        canvas.create_window((0, 0), window=frame_buttons, anchor='nw')
        
        # generate the list of check buttons
        r = 0
        c = 0
        indx = 0
        features_list = list()
        for feature in texts:
            features_list.append(Checkbutton(frame_buttons,text=texts[indx],variable=tf[indx]))
            features_list[indx].grid(row=r, column=c, sticky='news')
            indx = indx + 1
            c = c+1
            if (c == w):
                c = 0
                r = r + 1

        # resize buttons and find width and height of this canvas
        frame_buttons.update_idletasks()        
        firstWcolumns_width = sum([features_list[j].winfo_width() for j in range(0, w)])
        firstHrows_height = sum([features_list[i*w].winfo_height() for i in range(0, h)])

        frame_canvas.config(width=firstWcolumns_width + vsb.winfo_width(),
                        height=firstHrows_height)
        canvas.config(scrollregion=canvas.bbox("all"))
        return (frame_canvas)
        
    # Need to figure out what is wrong with this. I did a hardcode fix, but would prefer it to work fully
    def gen_x_scroll_canvas(self,frame,gr,gc,texts,tf,w,h,pad):
        frame_canvas = tk.Frame(frame)
        frame_canvas.pack(side=BOTTOM)
        #frame_canvas.grid(row=gr, column=gc, pady=(w, 0), sticky='nw')
        #frame_canvas.grid_rowconfigure(0, weight=1)
        #frame_canvas.grid_columnconfigure(0, weight=1)
        # Set grid_propagate to False to allow w-by-h buttons resizing later
        #frame_canvas.grid_propagate(False)
        canvas = tk.Canvas(frame_canvas)
        #canvas.grid(row=1, column=0, sticky="news")
        canvas.pack(side=BOTTOM,fill=BOTH,expand=True)

        # Link a scrollbar to the canvas
        vsb = tk.Scrollbar(frame, orient="horizontal", command=canvas.xview)
        #vsb.grid(row=0, column=0, sticky='ns')
        vsb.pack(side=TOP,fill=BOTH)
        canvas.configure(xscrollcommand=vsb.set)
        
        frame_buttons = tk.Frame(canvas)
        canvas.create_window((4, 4), window=frame_buttons, anchor='nw')
        
        # generate the list of check buttons
        r = 0
        c = 0
        indx = 0
        features_list = list()
        # Make one row
        for feature in texts:
            features_list.append(Checkbutton(frame_buttons,text=feature,variable=tf[indx]))
            features_list[indx].grid(row=r, column=c)
            indx = indx + 1
            c = c+1
        # resize buttons
        frame_buttons.update_idletasks()
        #canvas.config(scrollregion=canvas.bbox("all"))
        canvas.config(scrollregion=(4,4,frame_buttons.winfo_reqwidth()+pad,50))
        canvases = list()
        canvases.append(frame_canvas)
        canvases.append(canvas)
        canvases.append(frame_buttons)
        return (canvases)
    
    # Method to determine if a value is a number
    #
    # variables: s (string)
    def is_number(self,s):
        try:
            float(s)
            return True
        except ValueError:
            return False
    
    # This method returns the current value of a combobox. Returns -1 if no value found
    #
    # variables: list (list of values to search through), value (value being searched for)
    def find_combobox_indx(self,list,value):
        indx = 0
        for i in list:
            if (i == value):
                return (indx)
            indx = indx + 1  
        return (-1)
        
    # Method to generate and return list of various tkinter user options
    #
    # variables:frame, sr (start row), sc (start column), vars (variables to be generated) 
    def generate_user_options(self,frame,sr,sc,vars,combobox_vars):
        labels = list()
        vars_dict = {}
        c = sc
        indx = 0
        for key in vars:
            r = sr
            # or [] gets rid of NoneType not iterable exception
            for key2 in vars[key] or []:
                #pass if none and no combbox available
                if (vars[key][key2] == None and combobox_vars == None):
                    pass
                    
                # add combobox
                elif (key2[-2:] == 'CB'):
                    # -2: to ignore the CB I added as a marker for combobox variables
                    labels.append(Label(frame,text=key2[:-2]))
                    labels[indx].grid(row=r,column=c)
                    r = r+1
                    vars_dict[(key+key2)] = ttk.Combobox(frame, values=combobox_vars[(key+key2)])
                    combo_indx = self.find_combobox_indx(combobox_vars[(key+key2)], vars[key][key2])
                    if (combo_indx != -1):
                        vars_dict[(key+key2)].current(combo_indx)
                    vars_dict[(key+key2)].grid(row=r,column=c)
                    r = r+1
                    
                # if it is a list, it will be a checkbox type
                elif(isinstance(vars[key][key2], list)):
                    labels.append(Label(frame,text=key2))
                    labels[indx].grid(row=r,column=c)
                    r = r+1
                    indx = indx+1
                    temp = list()
                    indx2 = 0
                    for i in getattr(self,key2):
                        temp.append(Checkbutton(frame,text=i,variable=vars[key][key2][indx2]))
                        temp[indx2].grid(row=r,column=c)
                        r = r + 1
                        indx2 = indx2+1
                    vars_dict[(key+key2)] = temp
                      
                elif(isinstance(vars[key][key2], IntVar)):
                    vars_dict[(key+key2)] = Checkbutton(frame,text=key2,variable=vars[key][key2])
                    vars_dict[(key+key2)].grid(row=r, column=c)
                    r = r+1
                    
                # make changable entry if a number value or if a string == ---
                elif(self.is_number(vars[key][key2]) or isinstance(vars[key][key2], str)):
                    labels.append(Label(frame,text=key2))
                    labels[indx].grid(row=r,column=c)
                    r = r+1
                    indx = indx+1
                    vars_dict[(key+key2)] = Entry(frame)
                    vars_dict[(key+key2)].insert(0,vars[key][key2])
                    vars_dict[(key+key2)].grid(row=r,column=c)
                    r = r + 1                
            c = c + 1
        return vars_dict
        
    
    # This method creates a new window to determine the general settings of the conf file
    # Changes will automatically save as attributes of the gui class 
    def general(self):                    
        # create new window
        gen_root = Toplevel()
        genframe = tk.Frame(gen_root)
        genframe.grid(column=0,row=0, sticky=(N,W,E,S) )
        genframe.columnconfigure(2, weight = 1)
        genframe.rowconfigure(0, weight = 1)
        genframe.pack(pady = 100, padx = 100)
        
        gen_widgets = [0]*7
        # input features, widget 0
        gen_widgets[0] = self.gen_y_scroll_canvas(genframe,2,1,self.vars["headers"],self.vars["input_features"],4,5)
        gen_widgets[0].grid_remove()
        # target feature choice, widget 1
        gen_widgets[1] = ttk.Combobox(genframe, values=self.vars["headers"])
        indx = self.find_combobox_indx(self.vars["headers"],self.vars["target_feature"])
        if (indx != -1):
            gen_widgets[1].current(indx)
        # randomizer choice, widget 2
        gen_widgets[2] = Checkbutton(genframe,variable=self.vars["randomizer"],anchor='w')
        # metrics choices, widget 3
        metric_checkbuttons = list()
        c = 1
        for i in self.metrics:
            metric_checkbuttons.append(Checkbutton(genframe,text=i,variable=self.vars["metrics"][c-1]))
            c = c + 1   
        gen_widgets[3] = metric_checkbuttons
        # not_input_features, widget 4
        gen_widgets[4] = self.gen_y_scroll_canvas(genframe,2,1,self.vars["headers"],self.vars["not_input_features"],4,5)
        gen_widgets[4].grid_remove()
        # grouping_feature, widget 5
        gen_widgets[5] = ttk.Combobox(genframe, values=self.vars["headers"])
        indx = self.find_combobox_indx(self.vars["headers"],self.vars["grouping_feature"])
        if (indx != -1):
            gen_widgets[5].current(indx)
        # validation_columns_canvas, widget 6
        gen_widgets[6] = self.gen_y_scroll_canvas(genframe,2,1,self.vars["headers"],self.vars["validation_columns"],4,5)
        gen_widgets[6].grid_remove()
        
        # create 0 array to see if widgets active
        active = [0]*7
        # remove widget from frame if a new button is pressed
        def remove():
            for i in range(0,7):
                if (active[i] == 1):
                    active[i] = 0
                    if (i != 3):
                        gen_widgets[i].grid_remove()
                    else:
                        for x in gen_widgets[i]:
                            x.grid_remove()

        # Generate buttons to show various widgets
        def input_features_btn():
            remove()
            gen_widgets[0].grid(row=2,column=1)
            active[0] = 1
            
        def target_feature_btn():
            remove()
            gen_widgets[1].grid(row=3,column=1)
            active[1] = 1
            
            
        def randomizer_btn():
            remove()
            gen_widgets[2].grid(row=4,column=1)
            active[2] = 1
        
        def metrics_btn():
            remove()
            c = 1
            for x in gen_widgets[3]:
                x.grid(row=5,column=c)
                c = c + 1
            active[3] = 1
        
        def not_input_features_btn():
            remove()
            gen_widgets[4].grid(row=6,column=1)
            active[4] = 1
            
        def grouping_feature_btn():
            remove()
            gen_widgets[5].grid(row=7,column=1)
            active[5] = 1
        
        def validation_columns_btn():
            remove()
            gen_widgets[6].grid(row=8,column=1)
            active[6] = 1
            
        def exit_btn():
            self.vars["target_feature"] = gen_widgets[1].get()
            self.vars["grouping_feature"] = gen_widgets[5].get()
            gen_root.destroy()
            gen_root.update()
        
        # Create labels and buttons for the various genneral settings
        gen_l = [Label(genframe,text="General"),tk.Button(genframe,text="input_features",command=input_features_btn),
        tk.Button(genframe,text="target_feature",command=target_feature_btn),tk.Button(genframe,text="randomizer",command=randomizer_btn),
        tk.Button(genframe,text="metrics",command=metrics_btn),tk.Button(genframe,text="not_input_features",command=not_input_features_btn),
        tk.Button(genframe,text="grouping_feature",command=grouping_feature_btn),tk.Button(genframe,text="validation_columns",command=validation_columns_btn)]
        
        # Add labels to grid
        r = 1
        for label in gen_l:
            label.grid(row=r, column=0)
            r = r + 1


        
        save_b = tk.Button(genframe, 
                       text="Save and Close", 
                       fg="red",
                       command=exit_btn)
        save_b.grid(row=0, column=0)
        
        
    # This method allows the user to fill out the data cleaning section of the conf file
    def data_cleaning(self):
        # create new window
        data_clean_root = Toplevel()
        data_cleanframe = tk.Frame(data_clean_root)
        data_cleanframe.grid(column=0,row=0, sticky=(N,W,E,S) )
        data_cleanframe.columnconfigure(2, weight = 1)
        data_cleanframe.rowconfigure(0, weight = 1)
        data_cleanframe.pack(pady = 100, padx = 100)
        
        data_clean_l = [Label(data_cleanframe,text="cleaning_method"),Label(data_cleanframe,text="imputation_strategy")]
        r = 1
        for label in data_clean_l:
            # ignore imputation strategy but leave this way incase more data cleaning options added in the future
            if (r != 2):
                label.grid(row=r, column=0)
            r = r + 1
        # will need to change if more options added to data_clean section
        data_clean_widgets = [0]*2
        
        # imputation strategy widget, widget 1
        data_clean_widgets[1] = ttk.Combobox(data_cleanframe, values=self.imputation_strategy)
        indx = self.find_combobox_indx(self.imputation_strategy,self.vars["imputation_strategy"])
        if (indx != -1):
            data_clean_widgets[1].current(indx)
                        
        # Method derived from following resource:
        # F. Segers, “Intercept event when combobox edited,” Stack Overflow, 01-Dec-2011. [Online]. Available: https://stackoverflow.com/questions/8432419/intercept-event-when-combobox-edited. [Accessed: 07-Jan-2020].
        # Only show the data imputation options if data imputation is chosen as the cleaning method
        def on_field_change(event):
            data_clean_widgets[1].grid_remove()
            data_clean_l[1].grid_remove()
            if (data_clean_widgets[0].current() == 1):
                data_clean_widgets[1].grid(row = 2, column = 1)
                data_clean_l[1].grid(row=2, column=0)
        
        # cleaning method widget, widget 0
        data_clean_widgets[0] = ttk.Combobox(data_cleanframe,values=self.cleaning_methods)
        data_clean_widgets[0].bind('<<ComboboxSelected>>', on_field_change)
        indx = self.find_combobox_indx(self.cleaning_methods,self.vars["cleaning_method"])
        if (indx != -1):
            data_clean_widgets[0].current(indx)
            if (indx == 1):
                data_clean_widgets[1].grid(row=2, column=1)
                data_clean_l[1].grid(row=2, column=0)               
        data_clean_widgets[0].grid(row = 1, column = 1)     
       
        # exit button to save choices
        def exit_btn():
            self.vars["cleaning_method"] = data_clean_widgets[0].get()
            self.vars["imputation_strategy"] = data_clean_widgets[1].get()
            data_clean_root.destroy()
            data_clean_root.update()
            
        save_b = tk.Button(data_cleanframe, 
                       text="Save and Close", 
                       fg="red",
                       command=exit_btn)
        save_b.grid(row=0, column=0)
        
    # This method will allow a user to choose clustering options
    def clustering_btn(self):
        # create new window
        clustering_root = Toplevel()
        clusteringframe = tk.Frame(clustering_root)
        clusteringframe.grid(column=0,row=0, sticky=(N,W,E,S) )
        clusteringframe.columnconfigure(2, weight = 1)
        clusteringframe.rowconfigure(0, weight = 1)
        clusteringframe.pack(pady = 100, padx = 100)
        
        # make a list of clustering check buttons
        c = 1
        cluster_checkbuttons = list()
        indx = 0
        indx2 = 0
        cluster_labels = list()
        combobox_keys = list()
        c_vars_dict = {}
        for x in self.clustering:
            cluster_checkbuttons.append(Checkbutton(clusteringframe,text=x,variable=self.vars["clustering"][indx2]))
            cluster_checkbuttons[indx2].grid(row=1,column=c)
            indx2 = indx2 + 1
            # Access the dictionaries in c_vars
            for key in self.c_vars:
                # if it is the current clustering option, add that options fields to the gui
                if (key == x):
                    r = 2
                    # or [] gets rid of NoneType not iterable exception
                    for key2 in self.c_vars[key] or []:
                        # add labels
                        cluster_labels.append(Label(clusteringframe,text=key2))
                        cluster_labels[indx].grid(row=r,column=c)
                        indx = indx + 1
                        # make changable entry if a number value
                        if(self.is_number(self.c_vars[key][key2])):
                            c_vars_dict[(key+key2)] = Entry(clusteringframe)
                            c_vars_dict[(key+key2)].insert(0,self.c_vars[key][key2])
                            c_vars_dict[(key+key2)].grid(row=r+1,column=c)
                        # add combobox for option if it is an option that has a discrete number of string options
                        else:
                            c_vars_dict[(key+key2)] = ttk.Combobox(clusteringframe, values=self.c_vars_combobox_options[(key+key2)])
                            combobox_keys.append(key+key2)
                            indx3 = self.find_combobox_indx(self.c_vars_combobox_options[(key+key2)],self.c_vars[key][key2])
                            if (indx3 != -1):
                                c_vars_dict[(key+key2)].current(indx3)
                            c_vars_dict[(key+key2)].grid(row=r+1,column=c)
                            
                        r = r + 2                  
            c = c + 1
            
        #exit button to save choices
        def exit_btn():
            # save changes
            for x in self.clustering:
                for key in self.c_vars:
                    if (key == x):
                        for key2 in self.c_vars[key] or []:
                            if (self.is_number(c_vars_dict[(key+key2)].get())):
                                self.c_vars[key][key2] = c_vars_dict[(key+key2)].get()
                            elif (key+key2) in combobox_keys:
                                self.c_vars[key][key2] = c_vars_dict[(key+key2)].get()
                            # this is a stipulation according to scikit-learn, so I will be nice an ensure it.
                            if (key == 'AgglomerativeClustering' and key2 == 'linkage' and self.c_vars[key][key2] == 'ward'):
                                self.c_vars[key]['affinity'] = 'euclidean'
            clustering_root.destroy()
            clustering_root.update()
            
        save_b = tk.Button(clusteringframe, 
                       text="Save and Close", 
                       fg="red",
                       command=exit_btn)
        save_b.grid(row=0, column=0)

    # This method will allow a user to choose feature generation options
    def fg_btn(self):
        # create new window
        fg_root = Toplevel()
        fgframe = tk.Frame(fg_root)
        fgframe.grid(column=0,row=0, sticky=(N,W,E,S) )
        fgframe.columnconfigure(2, weight = 1)
        fgframe.rowconfigure(0, weight = 1)
        fgframe.pack(pady = 100, padx = 100)
        
        # make a list of fg checkbuttons
        fg_checkbuttons = list()
        indx = 0
        fg_label = Label(fgframe, text="Feature Generation Methods")
        fg_label.grid(row=2, column=0)
        for i in self.fg_vars:
            fg_checkbuttons.append(Checkbutton(fgframe,text=i,variable=self.vars["FeatureGeneration"][indx]))
            fg_checkbuttons[indx].grid(row = 2, column = indx+1)
            indx = indx + 1
        
        # Choose composition feature
        cf = ttk.Combobox(fgframe, values=self.vars["headers"])
        cf_label = Label(fgframe, text="Composition Feature")
        cf_label.grid(row=1, column=0)
        indx = self.find_combobox_indx(self.vars["headers"],self.vars["composition_feature"])
        if (indx != -1):
            cf.current(indx)
        cf.grid(row=1, column = 1)
        
        user_choices = self.generate_user_options(fgframe,3,1,self.fg_vars, None)
        # Add the other options
        #exit button to save choices
        def exit_btn():
            self.vars['composition_feature'] = cf.get()
            for key in self.fg_vars:
                for key2 in self.fg_vars[key] or []:
                    if (isinstance(self.fg_vars[key][key2],list) or isinstance(self.fg_vars[key][key2],IntVar)):
                        # do nothing if list
                        pass
                    elif (self.is_number(self.fg_vars[key][key2]) or isinstance(self.fg_vars[key][key2],str)):
                        if (key2 == "degree"):
                            if (self.is_number(user_choices[key+key2].get())):
                                self.fg_vars[key][key2] = user_choices[key+key2].get()
                        else:
                            self.fg_vars[key][key2] = user_choices[key+key2].get()
            # save changes
            fg_root.destroy()
            fg_root.update()
            
        save_b = tk.Button(fgframe, 
                       text="Save and Close", 
                       fg="red",
                       command=exit_btn)
        save_b.grid(row=0, column=0)
    
    # This method will allow a user to choose feature normalization options
    def fn_btn(self):
        # create new window
        fn_root = Toplevel()
        fnframe = tk.Frame(fn_root)
        fnframe.grid(column=0,row=0, sticky=(N,W,E,S) )
        fnframe.columnconfigure(2, weight = 1)
        fnframe.rowconfigure(0, weight = 1)
        fnframe.pack(pady = 100, padx = 100)
    
        # make a list of fg checkbuttons
        fn_checkbuttons = list()
        indx = 0
        fg_label = Label(fnframe, text="Feature Normalization Methods")
        fg_label.grid(row=1, column=0)
        for i in self.fn_vars:
            fn_checkbuttons.append(Checkbutton(fnframe,text=i,variable=self.vars["FeatureNormalization"][indx]))
            fn_checkbuttons[indx].grid(row = 1, column = indx+1)
            indx = indx + 1
        
        user_choices = self.generate_user_options(fnframe,2,1,self.fn_vars,None)
        
        # Add the other options
        #exit button to save choices
        def exit_btn():
            for key in self.fn_vars:
                for key2 in self.fn_vars[key] or []:
                    if (isinstance(self.fn_vars[key][key2],list) or isinstance(self.fn_vars[key][key2],IntVar)):
                        # do nothing if list
                        pass
                    elif (self.is_number(self.fn_vars[key][key2]) or isinstance(self.fn_vars[key][key2],str)):
                        # manually check to see if the value should be a number
                        if (key2 == "mean" or key2 == "stdev" or key2 == "n_quantiles" or key2 == "norm" or key2 == "threshold"):
                            if (self.is_number(user_choices[key+key2].get())):
                                self.fn_vars[key][key2] = user_choices[key+key2].get()
                        else:
                            self.fn_vars[key][key2] = user_choices[key+key2].get()
            # save changes
            fn_root.destroy()
            fn_root.update()
            
        save_b = tk.Button(fnframe, 
                       text="Save and Close", 
                       fg="red",
                       command=exit_btn)
        save_b.grid(row=0, column=0)
    
    # This method will allow a user to select the models
    def model_btn(self):
        # create new window
        model_root = Toplevel()
        modelframe = tk.Frame(model_root)
        modelframe.grid(column=0,row=0, sticky=(N,W,E,S) )
        modelframe.columnconfigure(0, weight = 1)
        modelframe.rowconfigure(0, weight = 1)
        modelframe.pack(pady = 200, padx = 200)    
        
        scroll_canvas = self.gen_x_scroll_canvas(modelframe,1,1,self.model_vars,self.vars["models"],5,1,900)
        scroll_canvas[0].grid_propagate(True)
        user_choices = self.generate_user_options(scroll_canvas[2],1,0,self.model_vars, None)
        #scroll_canvas[1].config(scrollregion=scroll_canvas[1].bbox("all"))
        
        #exit button to save choices
        def exit_btn():
            for key in self.model_vars:
                for key2 in self.model_vars[key] or []:
                    if (isinstance(self.model_vars[key][key2],list) or isinstance(self.model_vars[key][key2],IntVar)):
                        # do nothing if list
                        pass
                    elif (self.is_number(self.model_vars[key][key2]) or isinstance(self.model_vars[key][key2],str)):
                        self.model_vars[key][key2] = user_choices[key+key2].get()
            # save changes
            model_root.destroy()
            model_root.update()
            
        save_b = tk.Button(modelframe, 
                       text="Save and Close", 
                       fg="red",
                       command=exit_btn)
        save_b.pack(side=TOP)
        
    # This method will allow a user to select the datasplits
    def ds_btn(self):
        # create new window
        ds_root = Toplevel()
        dsframe = tk.Frame(ds_root)
        dsframe.grid(column=0,row=0, sticky=(N,W,E,S) )
        dsframe.columnconfigure(0, weight = 1)
        dsframe.rowconfigure(0, weight = 1)
        dsframe.pack(pady = 200, padx = 200)   

        scroll_canvas = self.gen_x_scroll_canvas(dsframe,1,1,self.ds.vars,self.vars["ds"],5,1,300)  
        user_choices = self.generate_user_options(scroll_canvas[2],1,0,self.ds.vars, self.ds.combobox_options)        

        #exit button to save choices
        def exit_btn():
            for key in self.ds.vars:
                for key2 in self.ds.vars[key] or []:
                    if (isinstance(self.ds.vars[key][key2],list) or isinstance(self.ds.vars[key][key2],IntVar)):
                        # do nothing if list
                        pass
                    elif (self.ds.vars[key][key2] == None or self.is_number(self.ds.vars[key][key2]) or isinstance(self.ds.vars[key][key2],str)):
                        self.ds.vars[key][key2] = user_choices[key+key2].get()
            # save changes
            ds_root.destroy()
            ds_root.update()
            
        save_b = tk.Button(dsframe, 
                       text="Save and Close", 
                       fg="red",
                       command=exit_btn)
        save_b.pack(side=TOP)    
    
    
    # This method will allow a user to perform feature selection
    def fs_btn(self):
        print("todo")
    # Make button to load csv file headers and location
    def load_csv(self, root):
        root.update()
        csv_filename = fd.askopenfilename()
        self.vars["csv_loc"] = csv_filename
        df = pd.read_csv(csv_filename)
        headers = list()
        num_cols = 0
        for col in df.columns:
            headers.append(col)
            num_cols = num_cols + 1
        self.vars["headers"] = headers
        i_f = list()
        n_i_f = list()
        v_c = list()
        for i in range(0,num_cols):
            i_f.append(IntVar())
            n_i_f.append(IntVar())
            v_c.append(IntVar())
            
        self.vars["input_features"] =  i_f
        self.vars["not_input_features"] = n_i_f
        self.vars["validation_columns"] = v_c       
        self.ds.change_combobox(headers)



    
# Make button to load .conf file
def load_conf():
    print("todo")
    #TODO
    
    
def result_folder():
    result_dir = fd.askdirectory()
    vars["result_loc"] = result_dir
    

    

# Make the grid for the gui
root = Tk()
root.title("MAST-ML GUI")
mainframe = tk.Frame(root)
mainframe.grid(column=0,row=0, sticky=(N,W,E,S) )
mainframe.columnconfigure(0, weight = 1)
mainframe.rowconfigure(0, weight = 1)
mainframe.pack(pady = 100, padx = 100)

# Create an instance of the gui class
gui = GUI()

# make control buttons
quit_b = tk.Button(mainframe, 
                   text="QUIT", 
                   fg="red",
                   command=quit)
                   
quit_b.grid(row=0, column=0)
# load csv files to obtain headers
load_data_b = tk.Button(mainframe,
                   text="Load .csv file",
                   command=lambda : gui.load_csv(root))
load_data_b.grid(row=0, column=1)

# will load conf files
load_conf_b = tk.Button(mainframe,
                   text="Load .conf file",
                   command=load_conf)
load_conf_b.grid(row=0, column=2)

# will choose the result folder for the mastml files to be saved to
result_b = tk.Button(mainframe,
                   text="Choose Result Folder",
                   command=result_folder)
result_b.grid(row=0, column=3)

# fill out the general section of the conf file
gen_b = tk.Button(mainframe, 
                   text="General", 
                   command=lambda : gui.general())
gen_b.grid(row=1, column=0)

# fill out the data cleaning section
gen_b = tk.Button(mainframe, 
                   text="Data Cleaning", 
                   command=lambda : gui.data_cleaning())
gen_b.grid(row=2, column=0)

gen_b = tk.Button(mainframe, 
                   text="Clustering", 
                   command=lambda : gui.clustering_btn())
gen_b.grid(row=3, column=0)

gen_b = tk.Button(mainframe, 
                   text="Feature Generation", 
                   command=lambda : gui.fg_btn())
gen_b.grid(row=4, column=0)

gen_b = tk.Button(mainframe, 
                   text="Feature Normalization", 
                   command=lambda : gui.fn_btn())
gen_b.grid(row=5, column=0)

gen_b = tk.Button(mainframe, 
                   text="Model Selection", 
                   command=lambda : gui.model_btn())
gen_b.grid(row=6, column=0)

gen_b = tk.Button(mainframe, 
                   text="Data Splits", 
                   command=lambda : gui.ds_btn())
gen_b.grid(row=7, column=0)

gen_b = tk.Button(mainframe, 
                   text="Feature Selection", 
                   command=lambda : gui.fs_btn())
gen_b.grid(row=8, column=0)

root.mainloop()