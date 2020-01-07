from tkinter import *
import tkinter as tk
from tkinter import ttk
import tkinter.filedialog as fd
import pandas as pd
import math
import os

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
                     "not_input_features": None, "grouping_feature": None, "validation_columns": None}
        self.metrics = ['root_mean_squared_error', 'mean_absolute_error']
    
    
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

    def save_gen(self):
        for val in self.vars["input_features"]:
            print(val.get())
    #TODO
    
    # This method returns the current value of a combobox. Returns -1 if no value found
    #
    # variables: list (list of values to search through), value (value being searched for)
    def find_combobox_indx(self,list,value):
        indx = 0
        for i in self.vars[list]:
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
        genframe.columnconfigure(0, weight = 1)
        genframe.rowconfigure(0, weight = 1)
        genframe.pack(pady = 100, padx = 100)

        
        # input features
        input_features = self.gen_scroll_canvas(genframe,2,1,"headers","input_features",5,2)
        
        # Create labels for the various genneral settings
        gen_l = [Label(genframe,text="General"),Label(genframe,text="input_features"),
        Label(genframe,text="target_feature"),Label(genframe,text="randomizer"),
        Label(genframe,text="metrics"),Label(genframe,text="not_input_features"),
        Label(genframe,text="grouping_feature"),Label(genframe,text="validation_columns")]
        
        # Add labels to grid
        r = 1
        for label in gen_l:
            label.grid(row=r, column=0)
            if (r != 1):
                r = r+2
            else:
                r = r+1

        # target feature choice
        target_feature_combobox = ttk.Combobox(genframe, values=self.vars["headers"])
        indx = self.find_combobox_indx("headers","target_feature")
        if (indx != -1):
            target_feature_combobox.current(indx)
        #target_feature_combobox.grid(row=4, column=1)
        
        # randomizer choice
        randomizer_checkbox = Checkbutton(genframe,variable=self.vars["randomizer"],anchor='w')
        #randomizer_checkbox.grid(row=6, column=1) 
        
        # metrics
        metric_checkbuttons = list()
        c = 1
        for i in self.metrics:
            metric_checkbuttons.append(Checkbutton(genframe,text=i,variable=self.vars["metrics"][c-1]))
            metric_checkbuttons[c-1].grid(row=8, column=c)
            c = c + 1
        
        # not input features
        not_input_features_canvas = self.gen_scroll_canvas(genframe,10,1,"headers","not_input_features",5,2)
        
        # grouping_feature
        grouping_feature_combobox = ttk.Combobox(genframe, values=self.vars["headers"])
        indx = self.find_combobox_indx("headers","grouping_feature")
        if (indx != -1):
            grouping_feature_combobox.current(indx)
        grouping_feature_combobox.grid(row=12, column=1)
        
        # validation_columns
        validation_columns_canvas = self.gen_scroll_canvas(genframe,14,1,"headers","validation_columns",5,2)
        
                
        def exit_btn():
            self.vars["target_feature"] = target_feature_combobox.get()
            self.vars["grouping_feature"] = grouping_feature_combobox.get()
            gen_root.destroy()
            gen_root.update()
        
        save_b = tk.Button(genframe, 
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
        for i in range(0,num_cols):
            i_f.append(IntVar())
            n_i_f.append(IntVar())
            v_c.append(IntVar())
        m = list()
        for i in range(0,2):
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

root.mainloop()