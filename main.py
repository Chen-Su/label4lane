from tkinter import Tk, Canvas, Frame, Menu, Label
from tkinter import StringVar
from tkinter import BOTH, NW, LEFT, RIGHT, ALL, N, S, E, W
from tkinter import filedialog
from tkinter.ttk import Button, Style
from PIL import Image, ImageTk
import glob
import os


class App(Frame):
    def __init__(self):
        super().__init__()
        self.cur_index = 0
        self.img_list = []
        self.initUI()

    def initUI(self):
        self.master.title("Labeltools")
        self.pack(fill=BOTH, expand=1)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        open_dir = Menu(self.master)
        open_dir.add_command(label="Open Dir", command=self.openDir)
        open_dir.add_command(label="Exit", command=self.quit)
        self.master.config(menu=open_dir)

        self.canvas = Canvas(self, width=640, height=480, bg='black')
        self.canvas.grid(row=0, column=1, sticky=N+S+E+W)
        self.canvas.bind("<Configure>", self.rescale)
        # self.img_handle = 0

        prev_button = Button(self, text='prev', command=self.prevImg)
        prev_button.grid(row=0, column=0, sticky=N+S)
        next_button = Button(self, text='next', command=self.nextImg)
        next_button.grid(row=0, column=2, sticky=N+S)

        # creating a status bar instance
        self.status = StringVar()
        statusBar = Label(self.master, anchor=W, textvariable=self.status)
        self.status.set('Status Bar')
        statusBar.pack(side=RIGHT)

    def rescale(self, event):
        self.showImg()

    def update_status(self):
        basename, filename = os.path.split(self.img_list[self.cur_index])
        self.status.set(filename)

    def prevImg(self):
        if(self.cur_index > 0):
            self.cur_index -= 1
        self.showImg()

    def nextImg(self):
        if(self.cur_index < len(self.img_list)-1):
            self.cur_index += 1
        self.showImg()

    def openDir(self):
        self.base_path = filedialog.askdirectory()
        self.img_list += glob.glob(self.base_path+'/*.png')
        self.img_list += glob.glob(self.base_path+'/*.PNG')
        self.img_list += glob.glob(self.base_path+'/*.jpg')
        self.img_list += glob.glob(self.base_path+'/*.JPG')
        self.img_list.sort()
        self.showImg()

    def showImg(self):
        if(len(self.img_list) == 0):
            return
        canvas_w = self.canvas.winfo_width()
        canvas_h = self.canvas.winfo_height()
        img_path = self.img_list[self.cur_index]
        self.img = Image.open(img_path)
        orig_w, orig_h = self.img.size
        scale = min(canvas_w/orig_w, canvas_h/orig_h)
        if(scale < 1):
            self.img = self.img.resize((int(orig_w*scale), int(orig_h*scale)), Image.ANTIALIAS)
        self.pil_img = ImageTk.PhotoImage(self.img)
        self.canvas.delete(ALL)
        self.canvas.create_image(canvas_w//2, canvas_h//2, anchor='center', image=self.pil_img)
        self.update_status()


def main():

    root = Tk()
    app = App()
    app.mainloop()


if __name__ == '__main__':
    main()
