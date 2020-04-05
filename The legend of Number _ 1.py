# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 17:59:24 2020

@author: Kiryonn
"""

from biblio import *
from tkinter import Tk, Frame, Canvas, Button, Label
from tkinter.font import Font

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
        Frame.__init__(self, master, bg="black")
        fontTitle = Font(family="Arial", size=40)
        fontNormal = Font(family="Arial", size=20)
        Label(self, text="The Legends of Number :", fg="green", bg="black", font=fontTitle).grid(sticky="nsew", padx=WIDTH//4-20, pady=(30, 0))
        Label(self, text="1", fg="green", bg="black", font=fontTitle).grid(padx=WIDTH//2-20, sticky="nsew")
        self.text = Label(self, text="Appuyez sur Entrer pour jouer", font=fontNormal, fg="white", bg="black")
        self.text.grid(pady=(HEIGHT//2-20,HEIGHT))
        self.flash()
        master.bind('<Return>', self.startCommand)

    def startCommand(self, event):
        self.master.unbind("<Return>")
        self.isflashing = False
        self.master.switch_frame(SelectMenu)

    def flash(self):
        if self.state:
            self.text.config(state="disabled")
            self.state = False
        else:
            self.text.config(state=("normal"))
            self.state = True
        if self.isflashing:
            self.after(400, self.flash)

class SelectMenu(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.cnv = Canvas(self, width=WIDTH, height=HEIGHT, bg="black")
        self.cnv.pack()
        points = ((43,40), (WIDTH-43, 40), (WIDTH-40, 43), (WIDTH-40, HEIGHT-43), (WIDTH-43, HEIGHT-40), (43, HEIGHT-40), (40, HEIGHT-43), (40, 43))
        self.cnv.create_polygon(points, outline="white")
        self.file1 = ButtonMainMenu(self.cnv, WIDTH//4, 100, WIDTH//2, 75, index=1)
        self.file2 = ButtonMainMenu(self.cnv, WIDTH//4, 200, WIDTH//2, 75, index=2)
        self.file3 = ButtonMainMenu(self.cnv, WIDTH//4, 300, WIDTH//2, 75, index=3)
        self.file1.draw()
        self.file2.draw()
        self.file3.draw()

    def transition(self):
        pass

class ButtonMainMenu(object):
    def __init__(self, canvas, x, y, width, height, marge=5, index=0):
        self.cnv = canvas
        self.marge = marge
        self.points = [(x+marge,y), (x+width-marge, y), (x+width, y+marge), (x+width, y+height-marge), (x+width-marge, y+height), (x+marge, y+height), (x, y+height-marge), (x, y+marge)]
        self.x = x
        self.y = y
        self.w = width
        self.h = height
        self.text = "Pas de sauvegarde"
        self.font = Font(family="Arial", size=20)

    def draw(self):
        self.cnv.create_polygon(self.points, outline="white")
        self.cnv.create_text(self.x+self.w//4, self.y+self.h//2, text=self.text, font=self.font, fill="white")


WIDTH = 1000
HEIGHT = WIDTH * 9 // 14
app = App()
app.mainloop()
