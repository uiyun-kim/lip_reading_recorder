from tkinter import *
import os
from environment.variable import CONFIG_PATH,DATASET_DIR,MODEL_LIST
from tkinter import ttk
import pickle
import shutil
import ui as Ui
import paramiko


class Login:
    def __init__(self):
        self.open_session()

    def open_session(self):
        self.status = 'prompt'
        self.init_window()
        self.init_components()
        self.run()

    def init_window(self):
        self.window = Tk()
        self.window.protocol("WM_DELETE_WINDOW", self.event_close)
        self.window.bind('<Return>', self.ui_login_button_command)

    def init_components(self):
        index_row = 0
        index_column = 0
        ############################
        self.ui_ip = Ui.LABEL_WITH_ENTRY(self.window,entry_label='',label='IP',width=20)
        self.ui_ip.frame.grid(row=index_row, padx=20, pady=5,sticky='NSEW')
        index_row += 1
        ############################
        self.ui_id = Ui.LABEL_WITH_ENTRY(self.window,entry_label='',label='ID',width=20)
        self.ui_id.frame.grid(row=index_row, padx=20, pady=5,sticky='NSEW')
        index_row += 1
        ############################
        self.ui_password = Ui.LABEL_WITH_ENTRY(self.window,entry_label='',label='PW',width=20)
        self.ui_password.frame.grid(row=index_row, padx=20, pady=5,sticky='NSEW')
        index_row += 1
        ############################
        self.ui_login_button = Ui.LABEL_WITH_BUTTON(self.window,
                                            '',
                                            '[Login]',
                                            self.ui_login_button_command)
        self.ui_login_button.frame.grid(row=index_row, padx=20, pady=5,sticky='NSEW')


        for i in range(index_row+1):
            self.window.grid_rowconfigure(i, weight=1)

        for i in range(index_column+1):
            self.window.grid_columnconfigure(i, weight=1)

    def ui_login_button_command(self,event=None):
        self.credential = (self.ui_ip.entry.get(),self.ui_id.entry.get(),self.ui_password.entry.get())
        self.window.destroy()
        self.status = 'access'

    def parser(self):
        return self.status, self.credential

    def event_close(self):
        self.credential = ('','', '')
        self.window.destroy()
        self.status = 'closed'

    def run(self):
        self.window.mainloop()


