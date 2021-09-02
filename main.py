import socket, tqdm
from tkinter import*
from threading import Thread
from tkinter import filedialog
import requests
import wget, os
from PIL import Image
from time import sleep 
from zipfile import ZipFile
#import pm_app_fxn as pm

output1 = ['']*1
list_of_sent_files = []

class main_App(Thread):
    def __init__(self):
        Thread.__init__(self)

    def browse_button(self):
        filename = filedialog.askdirectory()
        #self.filename1[0]=filename
        #print(filename)
        temp =  self.entry_path.get()
        #print(temp)
        self.entry_path.delete('0', 'end')
        self.entry_path.insert(0,filename)
        return filename

    def output(self, value):
        #value = sample_text.get(1.0, "end-1c")
        self.output_data.insert(END, value)

    def output_screen(self):
        #value = sample_text.get(1.0, "end-1c")
        value = output1[0]
        self.output(value)
        #self.entry_2.insert(1.0, value+'\n')

    def connect(self):
        filename = self.filename1[0]
        to_be_excute = "jpg_to_pdf"
        #ch = ConvertHandler( filename, to_be_excute )
        #ch.start()   

    def execute_handler(self):
        path =  self.entry_path.get()
        server_ip = self.server_ip.get()
        server_port = self.server_port.get()
        interval  = self.entry_interval.get()
        fh = file_handler(path,server_ip, server_port,interval )
        fh.start()
  
    def run(self):
        self.filename1 = ['']*1
        self.data1 = ['']*1
        self.root = Tk()
        #self.entry_0 = Text(self.root, height = 10, width = 250)
        self.entry_path = Entry(self.root, width=55)
        #self.entry_2 = Text(self.root, height = 10, width = 250)
        
        #self.root = Tk()
        self.root.geometry('900x500')
        self.root.title("File Agent - Send your files to specified server")
        # Server IP
        Label(self.root, text = "Server IP:").place(x = 100, y = 50) 
        self.server_ip = Entry(self.root, width=20)
        self.server_ip.place(x=170,y=50)
        self.server_ip.insert(0, "192.168.1.109")
        # Port Number
        Label(self.root, text = "Port No: ").place(x = 100, y = 100) 
        self.server_port = Entry(self.root, width=20)
        self.server_port.place(x=170,y=100)
        self.server_port.insert(0, "5003")
        #Connect Button
        Button(self.root, text='Connect',command = self.connect, height = 4, width=64,bg='Green',fg='white').place(x=350,y=50)
        
        # File path selector
        #Button(self.root, text='Choose path of folder where file available',command = self.browse_button, width=35,bg='brown',fg='white').place(x=90,y=150)
        self.entry_path = Entry(self.root, width=55)
        self.entry_path.place(x=350,y=150)
        #Default
        self.entry_path.insert(0, "Select Folder path")
        Label(self.root, text = "Interval: ").place(x=690,y=150) 
        self.entry_interval = Entry(self.root, width=10 )
        #Default value
        self.entry_interval.insert(0, " 5")
        self.entry_interval.place(x=740,y=150)
        Button(self.root, text='Choose path of folder where file available',command = self.browse_button, width=35,bg='brown',fg='white').place(x=90,y=150)
        
        # Action using button
        Button(self.root, text='Execute',command = self.execute_handler, height = 3, width=47,bg='blue',fg='white').place(x=90,y=200)
        #Button(self.root, text='Merge PDF',command = self.merge_pdf, width=20,bg='green',fg='white').place(x=280,y=290)
        #Button(self.root, text='SPLIT PDF',command = self.split_pdf, width=20,bg='green',fg='white').place(x=470,y=290)
        Button(self.root, text='EXIT ',command = self.root.quit, height = 3, width=47,bg='red',fg='white').place(x=470,y=200)
        # Display Logs
        # Action to download
        self.output_data = Text(self.root, height = 8, width = 90)
        self.output_data.place(x=90,y=280)
        self.root.mainloop()
        print("\nProgram Exit")


class file_handler(Thread):
    def __init__(self, path, server_ip, server_port, interval ):
        Thread.__init__(self)
        self.path = path
        self.server_ip = server_ip
        self.server_port = int(server_port)
        self.interval  = int(interval)
    def run(self):
        list_of_current_files = os.listdir(self.path)
        #print(list_of_current_files)
        #print(self.server_ip)
        #print(self.server_port)
        #print(self.interval)
        remaining_files  = list(set(list_of_current_files) -  set(list_of_sent_files))
        for file in remaining_files:
            file_path =  self.path+'/'+file
            #print(file_path)
            list_of_sent_files.append(file)
            ft = FileTransfer(file_path,self.server_ip, self.server_port )
            ft.start()
            ft.join()
        sleep(10)
        #self.run()

class FileTransfer(Thread):
    def __init__(self, path, server_ip, server_port):
        Thread.__init__(self)
        self.host = server_ip
        self.port = server_port
        self.filename = path
    def run(self):
        SEPARATOR = "<SEPARATOR>"
        BUFFER_SIZE = 4096 # send 4096 bytes each time step
        host = self.host
        port = int(self.port)
        filename = self.filename
        fl = filename.split('/')
        sp = '\\'
        filename = sp.join(fl)
        #print(filename,'\n')
        #host = "192.168.1.109"  # Server address
        #port = 5003  # Server port
        #filename = "Wall-Paper.jpeg"  # File to be send
        
        filesize = os.path.getsize(filename)   
        s = socket.socket()
        print(f"[+] Connecting to {host}:{port}")
        s.connect((host, port))
        print("[+] Connected.")
        # send the filename and filesize
        s.send(f"{filename}{SEPARATOR}{filesize}".encode())
        # start sending the file
        progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
        output1[0] =  f"Sending {filename}"
        main_App.output(client,f"Sending {filename}")
        with open(filename, "rb") as f:
            for _ in progress:
                # read the bytes from the file
                bytes_read = f.read(BUFFER_SIZE)
                if not bytes_read:
                    # file transmitting is done
                    break
                # we use sendall to assure transimission in 
                # busy networks
                s.sendall(bytes_read)
                # update the progress bar
                progress.update(len(bytes_read))
        s.close()
        sleep(3)
        #output1[0] =  f"Sending {filename}"
        main_App.output(client," - completed\n")

        
client = main_App()

client.start()
