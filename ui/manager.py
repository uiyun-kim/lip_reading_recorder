from tkinter import *

import os
from environment.variable import CONFIG_PATH,DATASET_DIR,MODEL_LIST
from tkinter import ttk
import pickle
import shutil
import ui as Ui
import zipfile
import paramiko
from zipfile import ZipFile
from contextlib import closing
from zipfile import ZipFile, ZIP_DEFLATED
import pickle
import time
class Manager:
    def __init__(self):
        if self.login_prompt():
            self.init_window()
            self.load_configuration()
            self.init_components()
            self.run()

    def login_prompt(self):
        session = Ui.Login()
        status, self.credential = session.parser()

        if status == 'closed':
            Ui.Main()
            del self
            return False

        elif status == 'access':

            return True

    def load_configuration(self):
        self.info_text = StringVar()
        self.configuration = pickle.load(open(CONFIG_PATH, "rb"))

        self.sftp_client = SftpClient(self.credential[0], self.credential[1], self.credential[2])


    def init_window(self):

        self.window = Tk()

        self.window.protocol("WM_DELETE_WINDOW", self.event_close)


    def refresh_list(self):

        self.ui_local_dataset_listbox.delete(0, 'end')
        self.ui_remote_dataset_listbox.delete(0, 'end')

        self.local_dataset_list = []
        self.remote_dataset_list = []

        if os.path.exists(DATASET_DIR):
            for i, dataset in enumerate(os.listdir(DATASET_DIR)):
                self.ui_local_dataset_listbox.insert(i, dataset)
                self.local_dataset_list.append(dataset)

        remote_list,remote_dict = self.sftp_client.get_dataset_list()
        for i, dataset in enumerate(remote_list):
            if 'properties' in dataset:
                continue
            self.ui_remote_dataset_listbox.insert(i, dataset.split('.')[0])
            self.remote_dataset_list.append(dataset.split('.')[0])

        self.dataset_dict =remote_dict
        print(remote_dict)

    def ui_remote_dataset_listbox_select_command(self,event):
        w = event.widget
        if w.curselection():
            index = int(w.curselection()[0])
            value = w.get(index)
            self.ui_download_author.entry.delete(0,END)
            self.ui_download_description_entry.delete(1.0,END)
            self.ui_download_author.entry.insert(0,self.dataset_dict[value]['author'])
            self.ui_download_description_entry.insert(1.0, self.dataset_dict[value]['description'])


    def init_components(self):

        index_row = 0
        index_column = 0

        self.ui_local_label = Label(self.window, text='Local Dataset')
        self.ui_local_label.grid(row=0, column=0, sticky='NSEW')

        self.ui_remote_label = Label(self.window, text='Server Dataset')
        self.ui_remote_label.grid(row=0, column=1, sticky='NSEW')
        ############################
        self.ui_local_dataset_listbox = Listbox(self.window, height=10)
        self.ui_remote_dataset_listbox = Listbox(self.window, height=10)

        self.ui_local_dataset_listbox.grid(row=1, column=0, padx=50, pady=20, sticky='NSEW')
        index_row+=1

        self.ui_remote_dataset_listbox.grid(row=1, column=1, padx=50, pady=20, sticky='NSEW')
        self.ui_remote_dataset_listbox.bind('<<ListboxSelect>>', self.ui_remote_dataset_listbox_select_command)
        self.refresh_list()
        ############################


        self.ui_local_delete_button = Ui.LABEL_WITH_BUTTON(self.window,
                                                     '',
                                                     '[Delete Local]',
                                                     self.ui_local_delete_button_command)
        self.ui_local_delete_button.frame.grid(row=2, column=0, padx=20, pady=5, sticky='NSEW')
        index_column += 1
        ############################
        self.ui_remote_delete_button = Ui.LABEL_WITH_BUTTON(self.window,
                                                     '',
                                                     '[Delete Server]',
                                                     self.ui_remote_delete_button_command)
        self.ui_remote_delete_button.frame.grid(row=2, column=1, padx=20, pady=5, sticky='NSEW')
        index_column += 1
        ############################
        self.ui_upload_button = Ui.LABEL_WITH_BUTTON(self.window,
                                                     '',
                                                     '[Upload]',
                                                     self.ui_upload_button_command)
        self.ui_upload_button.frame.grid(row=3, column=0, padx=20, pady=5, sticky='NSEW')
        index_column += 1


        ############################

        self.ui_download_button = Ui.LABEL_WITH_BUTTON(self.window,
                                                       '',
                                                       '[Download]',
                                                       self.ui_download_button_command)
        self.ui_download_button.frame.grid(row=3, column=1, padx=20, pady=5, sticky='NSEW')
        index_column += 1
        ############################
        self.ui_upload_author = Ui.LABEL_WITH_ENTRY(self.window,entry_label='',label='Author',width=20)
        self.ui_upload_author.frame.grid(row=4,column=0, padx=20, pady=5,sticky='NSEW')
        index_row += 1
        ############################
        self.ui_upload_description = ttk.Frame(self.window)
        self.ui_upload_description_label = Label(self.ui_upload_description, text='Description')
        self.ui_upload_description_label.grid(row=0, column=0, sticky='NSEW')
        self.ui_upload_description_entry = Text(self.ui_upload_description, width=20,height=5)
        self.ui_upload_description_entry.grid(row=0, column=1, sticky='NSEW', ipady=30)
        self.ui_upload_description.grid(row=5,column=0, padx=20, pady=5,sticky='NSEW')
        ############################
        self.ui_download_author = Ui.LABEL_WITH_ENTRY(self.window,entry_label='',label='Author',width=20)
        self.ui_download_author.frame.grid(row=4,column=1, padx=20, pady=5,sticky='NSEW')
        #self.ui_download_author.entry.config(state='readonly')
        index_row += 1
        ############################
        self.ui_download_description = ttk.Frame(self.window)
        self.ui_download_description_label = Label(self.ui_download_description, text='Description')
        self.ui_download_description_label.grid(row=0, column=0, sticky='NSEW')
        self.ui_download_description_entry = Text(self.ui_download_description, width=20,height=5)
        self.ui_download_description_entry.grid(row=0, column=1, sticky='NSEW', ipady=30)
        self.ui_download_description.grid(row=5,column=1, padx=20, pady=5,sticky='NSEW')
        #self.ui_download_description_entry.config(state=DISABLED)
        ############################
        self.info_label = Label(self.window,textvariable=self.info_text)
        self.info_label.grid(row=6,column=1, sticky='NSEW')

        self.info_text.set("Status")
        index_row += 1

    def ui_remote_delete_button_command(self):
        dataset = self.ui_remote_dataset_listbox.get(ACTIVE)


        self.sftp_client.remove(dataset)
        del self.dataset_dict[dataset]
        self.sftp_client.update_properties(self.dataset_dict)
        self.ui_download_author.entry.delete(0, END)
        self.ui_download_description_entry.delete(1.0, END)
        self.refresh_list()
        self.info_text.set("[" + dataset +']' +'Deleted from server')

    def ui_download_button_command(self):
        dataset = self.ui_remote_dataset_listbox.get(ACTIVE)
        if dataset in self.local_dataset_list:
            self.info_text.set("[" + dataset + '] Exist')
            return

        self.sftp_client.download(dataset)
        self.refresh_list()
        self.info_text.set("[" + dataset + ']'+'Downloaded')

    def ui_local_delete_button_command(self):
        dataset = self.ui_local_dataset_listbox.get(ACTIVE)
        path = os.path.join(DATASET_DIR,dataset)
        if os.path.exists(path):
            shutil.rmtree(path)
        self.refresh_list()
        self.info_text.set("[" + dataset +']' +'Deleted from local computer')
        pass
    def ui_upload_button_command(self):
        dataset =  self.ui_local_dataset_listbox.get(ACTIVE)

        if dataset in self.remote_dataset_list:
            self.info_text.set("[" + dataset + '] Exist')
            return

        dataset_property = {dataset:{'author':self.ui_upload_author.entry.get() , 'description':self.ui_upload_description_entry.get(1.0,END)}}
        self.dataset_dict.update(dataset_property)

        self.sftp_client.upload(dataset)
        self.sftp_client.update_properties(self.dataset_dict)
        self.refresh_list()
        self.info_text.set("[" + dataset + '] Uploaded')

    def event_close(self):
        self.window.destroy()
        Ui.Main()
        del self

    def run(self):
        self.window.mainloop()


class SftpClient:
    def __init__(self,ip,id,password):
        self.host = ip
        self.username = id
        self.password = password

        self.sftpURL = self.host
        self.sftpUser = self.username
        self.sftpPass = self.password
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(self.sftpURL, username=self.sftpUser, password=self.sftpPass)
        self.ftp = self.ssh.open_sftp()

    def get_dataset_list(self):

        files = self.ftp.listdir('upload')
        self.ftp.get('upload/properties.pickle', 'properties.pickle')

        with open('properties.pickle', 'rb') as handle:
            dict = pickle.load(handle)

        os.remove('properties.pickle')
        return files,dict

    def zipdir(self,basedir, archivename):
        assert os.path.isdir(basedir)
        with closing(ZipFile(archivename, "w", ZIP_DEFLATED)) as z:
            for root, dirs, files in os.walk(basedir):
                for fn in files:
                    absfn = os.path.join(root, fn)
                    zfn = absfn[len(basedir) + len(os.sep):]
                    z.write(absfn, zfn)

    def update_properties(self,new_properties):

        with open('properties.pickle', 'wb') as handle:
            pickle.dump(new_properties, handle, protocol=pickle.HIGHEST_PROTOCOL)

        self.ftp.put('properties.pickle', 'upload/properties.pickle')

        os.remove('properties.pickle')
    def upload(self,dataset):

        dataset_path = os.path.join(DATASET_DIR,dataset)
        self.zipdir(dataset_path,dataset+'.zip')

        path = 'upload/'+dataset+'.zip'
        localpath = dataset+'.zip'
        self.ftp.put(localpath, path)

        os.remove(localpath)


    def remove(self,dataset):

        path = 'upload/'+dataset +'.zip'

        self.ftp.remove(path)

    def download(self,dataset):

        path = 'upload/'+dataset +'.zip'
        localpath = dataset+'.zip'
        self.ftp.get(path, localpath)
        dataset_path = os.path.join(DATASET_DIR,dataset)

        fantasy_zip = zipfile.ZipFile(localpath)
        fantasy_zip.extractall(dataset_path)
        fantasy_zip.close()

        os.remove(localpath)



if __name__ == '__main__':
    SftpClient()