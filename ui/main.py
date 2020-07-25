from tkinter import *
import os
from environment.variable import CONFIG_PATH
import pickle
import ui as Ui

class Main:
    def __init__(self):
        self.create_config_file()
        self.init_window()
        self.init_components()
        self.run()

    def init_window(self):
        self.window = Tk()
        self.window.protocol("WM_DELETE_WINDOW", self.event_close)

    def create_config_file(self):
        if not os.path.exists(CONFIG_PATH):
            config ={'Sampling Rate':4,
                     'Camera Width':1280 ,
                     'Camera Height':720,
                     'Frames In One Sample':29,
                     'Name Dataset':'dataset1',
                     'Number Of Workers': '2',
                     'Name Class':'alfa'}
            f = open(CONFIG_PATH, "wb")
            pickle.dump(config, f)
            f.close()

    def init_components(self):

        index_row = 0
        index_column = 0

        self.ui_recorder = Ui.LABEL_WITH_BUTTON(self.window,
                                                  '',
                                                  '[Record]',
                                                  self.ui_recorder_command)
        self.ui_recorder.frame.grid(row=index_row,padx=70,pady=10,sticky='NSEW')
        index_row +=1


        self.ui_configuration = Ui.LABEL_WITH_BUTTON(self.window,
                                                  '',
                                                  '[Configuration]',
                                                  self.ui_configuration_command)
        self.ui_configuration.frame.grid(row=index_row,padx=70,pady=10,sticky='NSEW')
        index_row +=1

        self.ui_manager = Ui.LABEL_WITH_BUTTON(self.window,
                                                  '',
                                                  '[Dataset Manager]',
                                                  self.ui_manager_command)
        self.ui_manager.frame.grid(row=index_row,padx=70,pady=10,sticky='NSEW')
        index_row +=1

        for i in range(index_row + 1):
            self.window.grid_rowconfigure(i, weight=1)

        for i in range(index_column + 1):
            self.window.grid_columnconfigure(i, weight=1)


    def event_close(self):
        self.window.destroy()
        self.window.quit()
        del self

    def ui_manager_command(self):
        self.window.destroy()
        Ui.Manager()
        del self

    def ui_configuration_command(self):
        self.window.destroy()
        Ui.Configuration()
        del self

    def ui_recorder_command(self):
        self.window.destroy()
        Ui.Recorder()
        del self

    def run(self):
        self.window.mainloop()