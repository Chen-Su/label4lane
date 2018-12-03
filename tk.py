from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import glob
import os


class Window(Frame):


    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()
        
        # variabels
        self.img_list = []  # list of image paths.
        self.cur_img = 0    # index of current showing image.
    

    # Creation of init_window
    def init_window(self):

        # changing the title of our master widget 
        self.master.title("GUI")
        # allowing the widget to take the full space of the root window
        self.grid()
        
        # creating a menu instance
        menu = Menu(self.master)
        self.master.config(menu=menu)
        # create the file object
        file = Menu(menu)
        # adds a command to the menu option, calling it exit, and the
        # command it runs on event is client_exit
        file.add_command(label='Open Dir', command=self.open_dir)
        file.add_command(label="Exit", command=self.client_exit)
        # added "file" to our menu
        menu.add_cascade(label="File", menu=file)

        # creating a button instance
        leftButton = Button(self.master, text="prev image", command=self.prev_image)
        leftButton.grid(row=0, column=0)

        rightButton = Button(self.master, text="next image", command=self.next_image)
        rightButton.grid(row=0, column=2)
        
        # creating a status bar instance
        self.status = StringVar()
        statusBar = Label(self.master, anchor=W, textvariable=self.status)
        self.status.set('Status Bar')
        statusBar.grid(columnspan=3, sticky=E)


    def prev_image(self):
        if(self.cur_img > 0):
            self.cur_img -= 1
        self.showImg()
        self.update_status()


    def next_image(self):
        if(self.cur_img < len(self.img_list)):
            self.cur_img += 1
        self.showImg()
        self.update_status()


    # open images directory and show first image.
    def open_dir(self):
        imgs_path = filedialog.askdirectory()
        self.img_list += glob.glob(imgs_path+'/*.png')
        self.img_list += glob.glob(imgs_path+'/*.PNG')
        self.img_list += glob.glob(imgs_path+'/*.jpg')
        self.img_list += glob.glob(imgs_path+'/*.JPG')
        self.showImg()
        self.update_status()


    def update_status(self):
        basename, filename = os.path.split(self.img_list[self.cur_img])
        self.status.set(filename)


    def showImg(self):
        img_path = self.img_list[self.cur_img]
        load = Image.open(img_path)
        render = ImageTk.PhotoImage(load)
        img = Label(self.master, image=render)
        img.image = render
        img.grid(row=0, column=1)


    def client_exit(self):
        exit()
    

root = Tk()

# size of the window
root.geometry("400x300")

app = Window(root)

root.mainloop()
