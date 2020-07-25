from tkinter import *
import tkinter as tk
from tkinter import ttk

class LABEL_WITH_ENTRY:
    def __init__(self,window,label,entry_label,width):
        self.window = window
        self.label = label
        self.entry_label = entry_label
        self.width = width
        self.create()

    def create(self):
        index_row = 0
        index_column = 0

        self.frame = ttk.Frame(self.window)
        self.label = Label(self.frame, text=self.label).grid(row=index_row,column=index_column,sticky='NSEW')
        index_column+=1

        self.entry = ttk.Entry(self.frame, width=self.width, textvariable=str)
        self.entry.grid(row=index_row,column=index_column,sticky='NSEW')
        self.entry.insert(0,self.entry_label)

        for i in range(index_row+1):
            self.frame.grid_rowconfigure(i, weight=1)

        for i in range(index_column+1):
            self.frame.grid_columnconfigure(i, weight=1)



    def pack(self):
        self.frame.pack()

class LABEL_WITH_BUTTON:
    def __init__(self,window,label,button_label,command):
        self.window = window
        self.label = label
        self.button_label = button_label
        self.command = command
        self.create()

    def create(self):
        index_row = 0
        index_column = 0

        self.frame = ttk.Frame(self.window)

        if self.label != '':
            self.label = Label(self.frame, text=self.label).grid(row=index_row,column=index_column,sticky='NSEW')
            index_column+=1
            index_row+=1


        self.button = tk.Button(self.frame,
                                text=self.button_label,
                                width=15,
                                command=self.command)

        self.button.grid(row=index_row,column=index_column,sticky='NSEW')
        index_row += 1

        for i in range(index_row+1):
            self.frame.grid_rowconfigure(i, weight=1)

        for i in range(index_column+1):
            self.frame.grid_columnconfigure(i, weight=1)


    def pack(self):
        self.frame.pack()


#
# class LABEL_WITH_DROPDOWN:
#     def __init__(self,window,label,initial_var,item_list):
#         self.window = window
#         self.label = label
#         self.item_list = item_list
#         self.string_var = tk.StringVar(self.window)
#         self.string_var.set(initial_var)
#         self.create()
#
#     def create(self):
#         self.frame = ttk.Frame(self.window)
#         self.label = Label(self.frame, text=self.label).grid(row=0)
#
#         self.dropdown = tk.OptionMenu(self.frame,self.string_var,*self.item_list)
#         self.dropdown.grid(row=0,column=1)
#
#     def pack(self):
#         self.frame.pack()