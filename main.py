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
        self.pivot_x = 0
        self.pivot_y = 0
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
        self.canvas.bind("<Motion>", self.updateCoords)
        # self.img_handle = 0

        prev_button = Button(self, text='prev', command=self.prevImg)
        prev_button.grid(row=0, column=0, sticky=N+S)
        next_button = Button(self, text='next', command=self.nextImg)
        next_button.grid(row=0, column=2, sticky=N+S)

        # creating a status bar instance
        status_frame = Frame(self.master)
        status_frame.pack(fill=BOTH)
        self.status = StringVar()
        status_bar = Label(status_frame, textvariable=self.status)
        self.status.set('Status Bar')
        status_bar.pack(side=RIGHT)
        self.coords = StringVar()
        self.coords.set('Coordinates Bar')
        coords_bar = Label(status_frame, textvariable=self.coords)
        coords_bar.pack(side=LEFT)

    def rescale(self, event):
        if(len(self.img_list) == 0):
            return
        self.showImg()

    def updateCoords(self, event):
        if(len(self.img_list) == 0):
            return
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        x_offset = x - self.pivot_x
        y_offset = y - self.pivot_y
        if(x_offset < 0 or y_offset < 0):
            return
        rescale_x = x_offset // self.scale
        rescale_y = y_offset // self.scale
        self.coords.set("{}, {}".format(rescale_x, rescale_y))
        # print("self.pivot_x :{} self.pivot_y :{}".format(self.pivot_x, self.pivot_y))
        # print("canvas_x :{} canvas_y :{}".format(x, y))
        # print("x_offset :{} y_offset :{}".format(x_offset, y_offset))
        # print("rescale_x :{} rescale_y :{}".format(rescale_x, rescale_y))
        
    def update_status(self):
        basename, filename = os.path.split(self.img_list[self.cur_index])
        self.status.set(filename)

    def prevImg(self):
        if(len(self.img_list) == 0):
            return
        if(self.cur_index > 0):
            self.cur_index -= 1
        self.showImg()

    def nextImg(self):
        if(len(self.img_list) == 0):
            return
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
        self.scale = min(canvas_w/orig_w, canvas_h/orig_h)
        if(self.scale < 1):
            self.img = self.img.resize((int(orig_w*self.scale), int(orig_h*self.scale)), Image.ANTIALIAS)
        else:
            self.scale = 1
        self.pivot_x = (canvas_w-self.img.size[0])//2
        self.pivot_y = (canvas_h-self.img.size[1])//2
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
