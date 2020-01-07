from tkinter import *
import tkinter as tk
from tkinter import ttk
import tkinter.filedialog as fd
import pandas as pd
import math
import os
import time

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
                     "randomizer": None, "input_features": None, "target_feature": None, "metrics": None, 
                     "not_input_features": None, "grouping_feature": None, "validation_columns": None,
                     "cleaning_method": None, "imputation_strategy": None}
        self.metrics = ['root_mean_squared_error', 'mean_absolute_error']
        self.cleaning_methods = ['remove', 'imputation', 'ppca']
        self.imputation_strategy = ['mean','median']
    
    
    # adapted from Josselin, “tkinter Canvas Scrollbar with Grid?,” Stack Overflow, 01-May-1967. [Online]. Available: https://stackoverflow.com/questions/43731784/tkinter-canvas-scrollbar-with-grid. [Accessed: 03-Jan-2020].
    # generates scrollable canvas to store data in
    # 
    # variables: frame, gr (grid row), gc (grid column), texts (text for checkbuttons), tf (true false vars for checkbuttons)
    #            w (width, number of check buttons per row), h (height, number of check buttons per column)
    def gen_scroll_canvas(self,frame,gr,gc,texts,tf,w,h):
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
        for feature in self.vars[texts]:
            features_list.append(Checkbutton(frame_buttons,text=self.vars[texts][indx],variable=self.vars[tf][indx]))
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
    
    # This method returns the current value of a combobox. Returns -1 if no value found
    #
    # variables: list (list of values to search through), value (value being searched for)
    def find_combobox_indx(self,list,value):
        indx = 0
        for i in list:
            if (i == self.vars[value]):
                return (indx)
            indx = indx + 1  
        return (-1)
        
    
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
        gen_widgets[0] = self.gen_scroll_canvas(genframe,2,1,"headers","input_features",4,5)
        gen_widgets[0].grid_remove()
        # target feature choice, widget 1
        gen_widgets[1] = ttk.Combobox(genframe, values=self.vars["headers"])
        indx = self.find_combobox_indx(self.vars["headers"],"target_feature")
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
        gen_widgets[4] = self.gen_scroll_canvas(genframe,2,1,"headers","not_input_features",4,5)
        gen_widgets[4].grid_remove()
        # grouping_feature, widget 5
        gen_widgets[5] = ttk.Combobox(genframe, values=self.vars["headers"])
        indx = self.find_combobox_indx(self.vars["headers"],"grouping_feature")
        if (indx != -1):
            gen_widgets[5].current(indx)
        # validation_columns_canvas, widget 6
        gen_widgets[6] = self.gen_scroll_canvas(genframe,2,1,"headers","validation_columns",4,5)
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
        indx = self.find_combobox_indx(self.imputation_strategy,"imputation_strategy")
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
        indx = self.find_combobox_indx(self.cleaning_methods,"cleaning_method")
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

    # Make button to load csv file headers and location
    def load_csv(self):
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
        m = list()
        for i in range(0,num_cols):
            i_f.append(IntVar())
            n_i_f.append(IntVar())
            v_c.append(IntVar())
            if (i < 2):
                m.append(IntVar())
        self.vars["input_features"] =  i_f
        self.vars["not_input_features"] = n_i_f
        self.vars["validation_columns"] = v_c
        self.vars["randomizer"] = IntVar()
        self.vars["metrics"] = m


    
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
                   command=lambda : gui.load_csv())
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

root.mainloop()