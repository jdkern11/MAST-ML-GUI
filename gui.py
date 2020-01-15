from tkinter import *
import tkinter as tk
from tkinter import ttk
import pandas as pd
import math
import os
import time
from classes.LearningCurve import LearningCurve as LC
from classes.DataSplits import DataSplits as DS
from classes.DataCleaning import DataCleaning as DC
from classes.Clustering import Clustering as Cl
from classes.FeatureSelection import FeatureSelection as FS
from classes.FeatureGeneration import FeatureGeneration as FG
from classes.FeatureNormalization import FeatureNormalization as FN
from classes.PlotSettings import PlotSettings as PS
from classes.GeneralSetup import GeneralSetup as GS
from classes.Models import Models as Mo
import tkinter.filedialog as fd
from sys import platform

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
        self.vars = {"headers": None, "csv_loc": None, "conf_loc": None, "result_loc": os.getcwd(), "driver": None,
                     "cl": None, "fg": None, "fn": None, "mo": None, "ds": None, "fs": None, "lc": None, "ps": None}
                     
        # General variable creations
        # empty values will all be set to headers for easier saving later one
        self.input_features = None
        self.not_input_features = None
        self.validation_columns = None
        self.gs = GS()
        self.metrics = self.gs.metrics
        
        
        # Cleaning methods variables
        self.dc = DC()
        self.cleaning_methods = self.dc.cleaning_methods
        self.imputation_strategy = self.dc.imputation_strategy
        
        # Clustering variables
        self.cl = Cl()
        cluster = list()
        for key in self.cl.vars:
            cluster.append(IntVar())
        self.vars["cl"] = cluster
                                        
        # Make list for feature generation vars  
        self.fg = FG()
        self.feature_types = self.fg.feature_types
        # feature generation checkbox lists
        fgl = list()
        for key in self.fg.vars:
            fgl.append(IntVar())
        self.vars["fg"] = fgl
        
        # Make list of feature normalizationvars
        # Add combolist for output_distribution later probably
        self.fn = FN()
        fnl = list()
        for i in range(0,len(self.fn.vars)):
            fnl.append(IntVar())
        self.vars["fn"] = fnl        
        
        # Create an DataSplits instance and make checkbox vars to choose algos later
        self.ds = DS()
        dsl = list()
        for i in range(0,len(self.ds.vars)):
            dsl.append(IntVar())
        self.vars["ds"] = dsl
        
        # Create an FeatureSelection instance and make checkbox vars to choose algos later 
        self.fs = FS()
        fsl = list()
        for i in range(0,len(self.fs.vars)):
            fsl.append(IntVar())
        self.vars["fs"] = fsl
        
        # Create an LearningCurve instance and make checkbox vars to choose algos later 
        self.lc = LC()
        lcl = list()
        for i in range(0,len(self.lc.vars)):
            lcl.append(IntVar())
        self.vars["lc"] = lcl
        
        # Create an PlotSettings instance and make checkbox vars to choose algos later 
        self.ps = PS()
        psl = list()
        for i in range(0,len(self.ps.vars)):
            psl.append(IntVar())
        self.vars["ps"] = psl
        
        
        self.mo = Mo()
        models = list()
        for i in range(0,len(self.mo.vars)):
            models.append(IntVar())
        self.vars["mo"] = models
                            
        
    
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
        for i in list or []:
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
                    indx = indx + 1
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
                    
                # make changable entry if a number value or if a string
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
        gen_widgets[0] = self.gen_y_scroll_canvas(genframe,2,1,self.vars["headers"],self.gs.vars["input_features"],4,5)
        gen_widgets[0].grid_remove()
        # target feature choice, widget 1
        gen_widgets[1] = ttk.Combobox(genframe, values=self.vars["headers"])
        indx = self.find_combobox_indx(self.vars["headers"],self.gs.vars["target_feature"])
        if (indx != -1):
            gen_widgets[1].current(indx)
        # randomizer choice, widget 2
        gen_widgets[2] = Checkbutton(genframe,variable=self.gs.vars["randomizer"],anchor='w')
        # metrics choices, widget 3
        metric_checkbuttons = list()
        c = 1
        for i in self.gs.metrics:
            metric_checkbuttons.append(Checkbutton(genframe,text=i,variable=self.gs.vars["metrics"][c-1]))
            c = c + 1   
        gen_widgets[3] = metric_checkbuttons
        # not_input_features, widget 4
        gen_widgets[4] = self.gen_y_scroll_canvas(genframe,2,1,self.vars["headers"],self.gs.vars["not_input_features"],4,5)
        gen_widgets[4].grid_remove()
        # grouping_feature, widget 5
        gen_widgets[5] = ttk.Combobox(genframe, values=self.vars["headers"])
        indx = self.find_combobox_indx(self.vars["headers"],self.gs.vars["grouping_feature"])
        if (indx != -1):
            gen_widgets[5].current(indx)
        # validation_columns_canvas, widget 6
        gen_widgets[6] = self.gen_y_scroll_canvas(genframe,2,1,self.vars["headers"],self.gs.vars["validation_columns"],4,5)
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
            self.gs.vars["target_feature"] = gen_widgets[1].get()
            self.gs.vars["grouping_feature"] = gen_widgets[5].get()
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
        indx = self.find_combobox_indx(self.imputation_strategy,self.dc.vars["imputation_strategy"])
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
        data_clean_widgets[0] = ttk.Combobox(data_cleanframe,values=self.dc.cleaning_methods)
        data_clean_widgets[0].bind('<<ComboboxSelected>>', on_field_change)
        indx = self.find_combobox_indx(self.cleaning_methods,self.dc.vars["cleaning_method"])
        if (indx != -1):
            data_clean_widgets[0].current(indx)
            if (indx == 1):
                data_clean_widgets[1].grid(row=2, column=1)
                data_clean_l[1].grid(row=2, column=0)               
        data_clean_widgets[0].grid(row = 1, column = 1)     
       
        # exit button to save choices
        def exit_btn():
            self.dc.vars["cleaning_method"] = data_clean_widgets[0].get()
            self.dc.vars["imputation_strategy"] = data_clean_widgets[1].get()
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
        indx = 0
        c = 0
        for key in self.cl.vars:
            Checkbutton(clusteringframe,text=key,variable=self.vars["cl"][indx]).grid(row=1,column=c)
            indx = indx+1
            c = c + 1
        user_choices = self.generate_user_options(clusteringframe,2,0,self.cl.vars, self.cl.combobox_options) 
        #exit button to save choices
        def exit_btn():
            # save changes
            for key in self.cl.vars:
                for key2 in self.cl.vars[key] or []:
                    if (self.is_number(user_choices[(key+key2)].get())):
                        self.cl.vars[key][key2] = user_choices[(key+key2)].get()
                    elif (key+key2) in self.cl.combobox_options:
                        self.cl.vars[key][key2] = user_choices[(key+key2)].get()
                    # this is a stipulation according to scikit-learn, so I will be nice an ensure it.
                    if (key == 'AgglomerativeClustering' and key2 == 'linkage' and self.cl.vars[key][key2] == 'ward'):
                        self.cl.vars[key]['affinity'] = 'euclidean'
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
        indx = 0
        fg_label = Label(fgframe, text="Feature Generation Methods").grid(row=2,column=0)
        for i in self.fg.vars:
            Checkbutton(fgframe,text=i,variable=self.vars["fg"][indx]).grid(row = 2, column = indx+1)
            indx = indx + 1
        
        user_choices = self.generate_user_options(fgframe,3,1,self.fg.vars, self.fg.combobox_options)
        # Add the other options
        #exit button to save choices
        def exit_btn():
            for key in self.fg.vars:
                for key2 in self.fg.vars[key] or []:
                    if (isinstance(self.fg.vars[key][key2],list) or isinstance(self.fg.vars[key][key2],IntVar)):
                        # do nothing if list
                        pass
                    elif (self.fg.vars[key][key2] == None or self.is_number(self.fg.vars[key][key2]) or isinstance(self.fg.vars[key][key2],str)):
                        if (key2 == "degree"):
                            if (self.is_number(user_choices[key+key2].get())):
                                self.fg.vars[key][key2] = user_choices[key+key2].get()
                        else:
                            self.fg.vars[key][key2] = user_choices[key+key2].get()
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
    
        # make a list of fn checkbuttons
        fn_checkbuttons = list()
        indx = 0
        fg_label = Label(fnframe, text="Feature Normalization Methods")
        fg_label.grid(row=1, column=0)
        for i in self.fn.vars:
            fn_checkbuttons.append(Checkbutton(fnframe,text=i,variable=self.vars["fn"][indx]))
            fn_checkbuttons[indx].grid(row = 1, column = indx+1)
            indx = indx + 1
        
        user_choices = self.generate_user_options(fnframe,2,1,self.fn.vars,None)
        
        # Add the other options
        #exit button to save choices
        def exit_btn():
            for key in self.fn.vars:
                for key2 in self.fn.vars[key] or []:
                    if (isinstance(self.fn.vars[key][key2],list) or isinstance(self.fn.vars[key][key2],IntVar)):
                        # do nothing if list
                        pass
                    elif (self.is_number(self.fn.vars[key][key2]) or isinstance(self.fn.vars[key][key2],str)):
                        # manually check to see if the value should be a number
                        if (key2 == "mean" or key2 == "stdev" or key2 == "n_quantiles" or key2 == "norm" or key2 == "threshold"):
                            if (self.is_number(user_choices[key+key2].get())):
                                self.fn.vars[key][key2] = user_choices[key+key2].get()
                        else:
                            self.fn.vars[key][key2] = user_choices[key+key2].get()
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
        
        scroll_canvas = self.gen_x_scroll_canvas(modelframe,1,1,self.mo.vars,self.vars["mo"],5,1,900)
        scroll_canvas[0].grid_propagate(True)
        user_choices = self.generate_user_options(scroll_canvas[2],1,0,self.mo.vars, None)
        #scroll_canvas[1].config(scrollregion=scroll_canvas[1].bbox("all"))
        
        #exit button to save choices
        def exit_btn():
            for key in self.mo.vars:
                for key2 in self.mo.vars[key] or []:
                    if (isinstance(self.mo.vars[key][key2],list) or isinstance(self.mo.vars[key][key2],IntVar)):
                        # do nothing if list
                        pass
                    elif (self.is_number(self.mo.vars[key][key2]) or isinstance(self.mo.vars[key][key2],str)):
                        self.mo.vars[key][key2] = user_choices[key+key2].get()
            # Add models to feature selection options
            self.fs.combobox_initialization("model",self.vars["mo"],self.mo.vars)
            # Add models to learning curve options
            self.lc.combobox_initialization("model",self.vars["mo"],self.mo.vars)
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
            # Add datasplits to feature selection options
            self.fs.combobox_initialization("ds",self.vars["ds"],self.ds.vars)
            # Add datasplits to learning curve options
            self.lc.combobox_initialization("ds",self.vars["ds"],self.ds.vars)
            ds_root.destroy()
            ds_root.update()
            
        save_b = tk.Button(dsframe, 
                       text="Save and Close", 
                       fg="red",
                       command=exit_btn)
        save_b.pack(side=TOP)    
    
    
    # This method will allow a user to perform feature selection
    def fs_btn(self):
        # create new window
        fs_root = Toplevel()
        fsframe = tk.Frame(fs_root)
        fsframe.grid(column=0,row=0, sticky=(N,W,E,S) )
        fsframe.columnconfigure(0, weight = 1)
        fsframe.rowconfigure(0, weight = 1)
        fsframe.pack(pady = 200, padx = 200)   
        
        scroll_canvas = self.gen_x_scroll_canvas(fsframe,1,1,self.fs.vars,self.vars["fs"],5,1,300)  
        user_choices = self.generate_user_options(scroll_canvas[2],1,0,self.fs.vars, self.fs.combobox_options)        

        #exit button to save choices
        def exit_btn():
            for key in self.fs.vars:
                for key2 in self.fs.vars[key] or []:
                    if (isinstance(self.fs.vars[key][key2],list) or isinstance(self.fs.vars[key][key2],IntVar)):
                        # do nothing if list
                        pass
                    elif (self.fs.vars[key][key2] == None or self.is_number(self.fs.vars[key][key2]) or isinstance(self.fs.vars[key][key2],str)):
                        self.fs.vars[key][key2] = user_choices[key+key2].get()
            # save changes
            # Add feature selection to learning curve options
            self.lc.combobox_initialization("fs",self.vars["fs"],self.fs.vars)
            fs_root.destroy()
            fs_root.update()
            
        save_b = tk.Button(fsframe, 
                       text="Save and Close", 
                       fg="red",
                       command=exit_btn)
        save_b.pack(side=TOP)    
    
    # This method will allow a user to choose learning curve options
    def lc_btn(self):
        # create new window
        lc_root = Toplevel()
        lcframe = tk.Frame(lc_root)
        lcframe.grid(column=0,row=0, sticky=(N,W,E,S) )
        lcframe.columnconfigure(0, weight = 1)
        lcframe.rowconfigure(0, weight = 1)
        lcframe.pack(pady = 200, padx = 200)   
        
        scroll_canvas = self.gen_x_scroll_canvas(lcframe,1,1,self.lc.vars,self.vars["lc"],5,1,0)  
        user_choices = self.generate_user_options(scroll_canvas[2],1,0,self.lc.vars, self.lc.combobox_options)        

        #exit button to save choices
        def exit_btn():
            for key in self.lc.vars:
                for key2 in self.lc.vars[key] or []:
                    if (isinstance(self.lc.vars[key][key2],list) or isinstance(self.lc.vars[key][key2],IntVar)):
                        # do nothing if list
                        pass
                    elif (self.lc.vars[key][key2] == None or self.is_number(self.lc.vars[key][key2]) or isinstance(self.lc.vars[key][key2],str)):
                        self.lc.vars[key][key2] = user_choices[key+key2].get()
            # save changes
            lc_root.destroy()
            lc_root.update()
            
        save_b = tk.Button(lcframe, 
                       text="Save and Close", 
                       fg="red",
                       command=exit_btn)
        save_b.pack(side=TOP)        
        
    # This method will allow a user to choose plot settings
    def ps_btn(self):
        # create new window
        ps_root = Toplevel()
        psframe = tk.Frame(ps_root)
        psframe.grid(column=0,row=0, sticky=(N,W,E,S) )
        psframe.columnconfigure(0, weight = 1)
        psframe.rowconfigure(0, weight = 1)
        psframe.pack(pady = 200, padx = 200)   
        
        label = Label(psframe,text="Plot Settings")
        label.grid(row=1,column=0)
        user_choices = self.generate_user_options(psframe,2,0,self.ps.vars, None)        

        #exit button to save choices
        def exit_btn():
            ps_root.destroy()
            ps_root.update()
            
        save_b = tk.Button(psframe, 
                       text="Save and Close", 
                       fg="red",
                       command=exit_btn)
        save_b.grid(row=0,column=0)        
        
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
        # for easier saving
        self.input_features = headers
        self.not_input_features = headers
        self.validation_columns = headers
        
        i_f = list()
        n_i_f = list()
        v_c = list()
        for i in range(0,num_cols):
            i_f.append(IntVar())
            n_i_f.append(IntVar())
            v_c.append(IntVar())
            
        self.gs.vars["input_features"] =  i_f
        self.gs.vars["not_input_features"] = n_i_f
        self.gs.vars["validation_columns"] = v_c       
        self.ds.combobox_initialization(headers)
        self.fg.combobox_initialization(headers)


    def load_driver(self):
        self.vars["driver"] = fd.askopenfilename()
    
    # Make button to load .conf file
    def load_conf(self):
        print("todo")
        #TODO
    
    
    def result_folder(self):
        result_dir = fd.askdirectory()
        self.vars["result_loc"] = result_dir
        
    # This method will help expedite saving
    #
    # Variables: vars (vars to be saved), file (file to be written to), nl (new line character)
    def save_helper(self,vars,file,nl):
        for key in vars:
            # see if list has dictionaries that need to be iterated through
            if (isinstance(vars[key],dict)):
                for key2 in vars[key]:
                    file.write("    ")
                    if (key2[-2:] == "CB"):
                        file.write(key2[:-2])
                    else:
                        file.write(key2)
                    file.write(" = ")
                    if (vars[key][key2] == None):
                        pass
                    # IntVar write
                    elif (isinstance(vars[key][key2],IntVar)):
                        if (vars[key][key2].get() == 1):
                            file.write("True")
                        else:
                            file.write("False")
                    # write strings automatically
                    elif (isinstance(vars[key][key2], str)):
                        file.write(vars[key][key2])
                        
                    # write checklists
                    elif (isinstance(vars[key][key2],list)):
                        indx = 0
                        first_write = 0
                        for i in getattr(self,key2):
                            if (vars[key][key2][indx].get() == 1):
                                if(first_write == 0):
                                    first_write = 1
                                else:
                                    file.write(", ")
                                file.write(i)
                            indx = indx + 1
                    file.write(nl)
            # Useful for general features
            else:
                file.write("    ")
                if (key[-2:] == "CB"):
                    file.write(key[:-2])
                else:
                    file.write(key)
                file.write(" = ")
                if (vars[key] == None):
                    pass
                # IntVar write
                elif (isinstance(vars[key],IntVar)):
                    if (vars[key].get() == 1):
                        file.write("True")
                    else:
                        file.write("False")
                # write strings automatically
                elif (isinstance(vars[key], str)):
                    file.write(vars[key])
                    
                # write checklists
                elif (isinstance(vars[key],list)):
                    indx = 0
                    first_write = 0
                    for i in getattr(self,key):
                        if (vars[key][indx].get() == 1):
                            if(first_write == 0):
                                first_write = 1
                            else:
                                file.write(", ")
                            file.write(i)
                        indx = indx + 1
                file.write(nl)
                
    # This method will help write classes that contain [[]] vars
    #
    # variables vars (features to be written), tf (whether features will be written), file (file to write to), nl (new line character)
    def write_double_brackets(self,vars,tf,file,nl):
        for key,val in zip(vars,tf):
            if (val.get() == 1):
                file.write("    [[")
                if (key[-2:] == "CB"):
                    file.write(key[:-2])
                else:
                    file.write(key)
                file.write("]]")
                file.write(nl)
                for key2 in vars[key] or []:
                    file.write("        ")
                    file.write(key2)
                    file.write(" = ")
                    if (vars[key][key2] == None):
                        pass
                    # IntVar write
                    elif (isinstance(vars[key][key2],IntVar)):
                        if (vars[key][key2].get() == 1):
                            file.write("True")
                        else:
                            file.write("False")
                    # write strings automatically
                    elif (isinstance(vars[key][key2], str)):
                        file.write(vars[key][key2])
                        
                    # write checklists
                    elif (isinstance(vars[key][key2],list)):
                        indx = 0
                        first_write = 0
                        for i in getattr(self,key2):
                            if (vars[key][key2][indx].get() == 1):
                                if(first_write == 0):
                                    first_write = 1
                                else:
                                    file.write(", ")
                                file.write(i)
                            indx = indx + 1
                    file.write(nl)
        
    def save(self):
        save_name = os.path.join(self.vars["result_loc"], "conf_file.conf")
        f = open(save_name, "w+")
        # new line variable different depending on platform
        nl = "\n"
        
        # Write general setting
        f.write("[GeneralSetup]")
        f.write(nl)
        self.save_helper(self.gs.vars,f,nl)        
        f.write(nl)
        f.write(nl)
        
        # Write DataCleaning setting
        f.write("[DataCleaning]")
        f.write(nl)
        for key in self.dc.vars:
            if (key != None):
                if (key != 'imputation_strategy'):
                    f.write("    ")
                    if (key[-2:] == "CB"):
                        f.write(key[:-2])
                    else:
                        f.write(key)
                    f.write(' = ')
                    if (self.dc.vars[key] != None):
                        f.write(self.dc.vars[key])
                else:
                    if (self.dc.vars['cleaning_method'] == 'imputation'):
                        f.write("    ")
                        f.write(key)
                        f.write(' = ')
                        if (self.dc.vars[key] != None):
                            f.write(self.dc.vars[key])
            f.write(nl)
        f.write(nl)
        f.write(nl)
        
        # Write Clustering setting
        f.write("[Clustering]")
        f.write(nl)
        self.write_double_brackets(self.cl.vars,self.vars['cl'],f,nl)        
        f.write(nl)
        f.write(nl)
        
        # Write FeatureGeneration setting
        f.write("[FeatureGeneration]")
        f.write(nl)
        self.write_double_brackets(self.fg.vars,self.vars['fg'],f,nl)               
        f.write(nl)
        f.write(nl)
        
        # Write FeatureNormalization setting
        f.write("[FeatureNormalization]")
        f.write(nl)
        self.write_double_brackets(self.fn.vars,self.vars['fn'],f,nl)         
        f.write(nl)
        f.write(nl)
        
        # Write LearningCurve setting
        f.write("[LearningCurve]")
        f.write(nl)
        self.save_helper(self.lc.vars,f,nl)        
        f.write(nl)
        f.write(nl)
        
        # Write FeatureSelection setting
        # Need to edit this
        f.write("[FeatureSelection]")
        f.write(nl)
        self.write_double_brackets(self.fn.vars,self.vars['fs'],f,nl)       
        f.write(nl)
        f.write(nl)
        
        # Write DataSplits setting
        f.write("[DataSplits]")
        f.write(nl)
        self.write_double_brackets(self.ds.vars,self.vars['ds'],f,nl)         
        f.write(nl)
        f.write(nl)
        
        # Write Models setting
        f.write("[Models]")
        f.write(nl)
        self.write_double_brackets(self.mo.vars,self.vars['mo'],f,nl)       
        f.write(nl)
        f.write(nl)
        
        # Write PlotSettings setting
        f.write("[PlotSettings]")
        f.write(nl)
        self.save_helper(self.ps.vars,f,nl)      
        f.write(nl)
        
        f.close()
        self.vars["conf_loc"] = save_name
    
    def run(self):
        command = "python3 -m "
        command = command + self.vars["conf_loc"] + " " + self.vars["csv_loc"] + " -o " + self.vars["result_loc"]
        os.system(command)
    

    

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
                   command=lambda : gui.load_conf())
load_conf_b.grid(row=0, column=2)

# will choose the result folder for the mastml files to be saved to
result_b = tk.Button(mainframe,
                   text="Choose Result Folder",
                   command=lambda : gui.result_folder())
result_b.grid(row=0, column=3)

# allows user to find the driver location
result_b = tk.Button(mainframe,
                   text="Load Driver Location",
                   command=lambda : gui.load_driver())
result_b.grid(row=0, column=4)

# save the conf file
result_b = tk.Button(mainframe,
                   text="Save",
                   command=lambda : gui.save())
result_b.grid(row=0, column=5)

# will run the conf file
result_b = tk.Button(mainframe,
                   text="Run",
                   command=lambda : gui.run())
result_b.grid(row=0, column=6)

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

gen_b = tk.Button(mainframe, 
                   text="Learning Curve", 
                   command=lambda : gui.lc_btn())
gen_b.grid(row=9, column=0)

gen_b = tk.Button(mainframe, 
                   text="Plot Settings", 
                   command=lambda : gui.ps_btn())
gen_b.grid(row=10, column=0)

root.mainloop()