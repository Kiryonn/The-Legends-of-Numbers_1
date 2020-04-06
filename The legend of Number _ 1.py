# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 17:59:24 2020

@author: Kiryonn
"""

from biblio import *
from tkinter import Tk, Frame, Canvas, Button, Label
from tkinter.font import Font
from pathlib import Path

class App(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.geometry("%dx%d" % (WIDTH, HEIGHT))
        self.lift()
        self.attributes('-topmost',True)
        self.after_idle(self.attributes,'-topmost',False)
        self.focus_force()
        self.resizable(False, False)
        self.title("The Legends of Number : 1")
        self.iconbitmap("img/icone.ico")
        self._frame = None
        self.switch_frame(MainMenu)
        self.showExp = True

    def switch_frame(self, frame_class, **opt):
        new_frame = frame_class(self, **opt)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack(fill="both")

class MainMenu(Frame):
    def __init__(self, master):
        self.master = master
        self.isflashing = True
        self.state = True
        Frame.__init__(self, master)
        self.bgImage = PhotoImage(file="img/default.png")
        self.cnv = Canvas(self, width=WIDTH, height=HEIGHT, bg="black")
        self.cnv.pack()
        fontTitle = Font(family="Arial", size=40)
        fontNormal = Font(family="Arial", size=20)
        self.cnv.create_text(WIDTH//2, 100, text="The Legends of Number :\n1", fill="green", font=fontTitle, justify="center")
        self.text = self.cnv.create_text(WIDTH//2, HEIGHT*3//4, text="Appuyez sur Entrer pour jouer", disabledfill="#888888", fill="white", font=fontNormal)
        self.flash()
        master.bind('<Return>', self.startCommand)

    def startCommand(self, event):
        self.master.unbind("<Return>")
        self.isflashing = False
        self.master.switch_frame(SelectMenu)

    def flash(self):
        if self.state:
            self.cnv.itemconfig(self.text, state="disabled")
            self.state = False
        else:
            self.cnv.itemconfig(self.text, state=("normal"))
            self.state = True
        if self.isflashing:
            self.after(400, self.flash)

class SelectMenu(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.cnv = Canvas(self, width=WIDTH, height=HEIGHT, bg="black")
        self.cnv.pack()
        self.bgImage = PhotoImage(file="img/default.png")
        img = PhotoImage(file="img/select.png")
        self.cnv.create_image(WIDTH//2, HEIGHT//2, image=self.bgImage, anchor="center")
        self.cnv.create_image(WIDTH//2, HEIGHT//2, image=img, anchor="center")
        self.cnv.bgImage = self.bgImage
        self.cnv.image = img

        infosFile1 = self.getFileInfo("saves/file1.txt")
        infosFile2 = self.getFileInfo("saves/file2.txt")
        infosFile3 = self.getFileInfo("saves/file3.txt")

        # create buttons
        self.b1 = ButtonMainMenu(self.cnv, WIDTH//4, 100, WIDTH//2, 75, infos=infosFile1)
        self.b2 = ButtonMainMenu(self.cnv, WIDTH//4, 200, WIDTH//2, 75, infos=infosFile2)
        self.b3 = ButtonMainMenu(self.cnv, WIDTH//4, 300, WIDTH//2, 75, infos=infosFile3)

        # draw buttons
        self.b1.draw()
        self.b2.draw()
        self.b3.draw()

        # left click events
        self.b1.bind("<Button-1>", lambda e: self.func(e, 1))
        self.b2.bind("<Button-1>", lambda e: self.func(e, 2))
        self.b3.bind("<Button-1>", lambda e: self.func(e, 3))

        # mouse over events
        self.b1.bind("<Enter>", self.b1.mouseOver)
        self.b2.bind("<Enter>", self.b2.mouseOver)
        self.b3.bind("<Enter>", self.b3.mouseOver)

        # mouse not over anymore events
        self.b1.bind("<Leave>", self.b1.mouseQuit)
        self.b2.bind("<Leave>", self.b2.mouseQuit)
        self.b3.bind("<Leave>", self.b3.mouseQuit)

    def func(self, event, index):
        if index == 1:
            print("ok1")
        elif index == 2:
            print("ok2")
        elif index == 3:
            print("ok3")
        else:
            print("this should not happen")

    def getFileInfo(self, filepath):
        infos = {
            "charaName" : "",
            "map" : (0, 0),
            "life" : 3,
            "maxLife" : 3}
        try:
            file = open(filepath, "r")
            name = file.readline().strip('\n')
            pos = file.readline().strip('\n')
            life = file.readline().strip('\n')
            maxLife = file.readline().strip('\n')
            file.close()
            infos["charaName"] = name
            i = pos.find(',')
            infos["map"] =(int(pos[0:i]), int(pos[i+1:]))
            infos["life"] = int(life)
            infos["maxLife"] = int(maxLife)
            return infos
        except EnvironmentError:
            Path("saves").mkdir(parents=True, exist_ok=True)
            return None

class ButtonMainMenu(object):
    def __init__(self, canvas, x, y, width, height, marge=5, infos=None):
        self.cnv = canvas
        self.marge = marge
        self.points = [(x+marge,y), (x+width-marge, y), (x+width, y+marge), (x+width, y+height-marge), (x+width-marge, y+height), (x+marge, y+height), (x, y+height-marge), (x, y+marge)]
        self.x = x
        self.y = y
        self.w = width
        self.h = height
        self.text = "Pas de sauvegarde" if infos == None else infos["charaName"]
        self.life = 0 if infos == None else infos["life"]
        self.font = Font(family="Arial", size=20)
        self.polygon = None
        self.label = None

    def draw(self):
        self.polygon = self.cnv.create_polygon(self.points, outline="white", fill='')
        self.label = self.cnv.create_text(self.x+self.w//4, self.y+self.h//2, text=self.text, font=self.font, fill="white")

    def bind(self, event, func):
            self.cnv.tag_bind(self.polygon, event, func)
            self.cnv.tag_bind(self.label, event, func)

    def func(self):
        pass

    def mouseOver(self, event):
        self.cnv.itemconfig(self.polygon, fill="#888888")

    def mouseQuit(self, event):
        self.cnv.itemconfig(self.polygon, fill='')


WIDTH = 1000
HEIGHT = WIDTH * 9 // 14
app = App()
app.mainloop()
