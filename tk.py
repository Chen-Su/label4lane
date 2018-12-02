from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import glob


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
        self.pack(fill=BOTH, expand=1)

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

        # create the file object
        edit = Menu(menu)

        # adds a command to the edit option, calling it undo
        edit.add_command(label="Show Img", command=self.showImg)
        edit.add_command(label="Show Text", command=self.showText)

        menu.add_cascade(label="Edit", menu=edit)

        # creating a button instance
        quitButton = Button(self.master, text="Quit", command=self.client_exit)

        # placing the button on my window
        quitButton.place(x=0, y=0)


    # open images directory and show first image.
    def open_dir(self):
        imgs_path = filedialog.askdirectory()
        self.img_list += glob.glob(imgs_path+'/*.png')
        self.img_list += glob.glob(imgs_path+'/*.PNG')
        self.img_list += glob.glob(imgs_path+'/*.jpg')
        self.img_list += glob.glob(imgs_path+'/*.JPG')
        self.showImg(self.img_list[self.cur_img])
        self.cur_img += 1


    def showImg(self, img_path):
        print(img_path)
        load = Image.open(img_path)
        render = ImageTk.PhotoImage(load)
        # labels can be text or images
        img = Label(self, image=render)
        img.image = render
        img.place(x=0, y=0)


    def showText(self):
        text = Label(self, text="Hey there good lookin!")
        text.pack()


    def client_exit(self):
        exit()
    

root = Tk()

# size of the window
root.geometry("400x300")

app = Window(root)

root.mainloop()