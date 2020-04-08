# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 17:59:24 2020

@author: Kiryonn
"""

from biblio import *
from tkinter import Tk, Frame, Canvas, PhotoImage
from tkinter.font import Font
from pathlib import Path
from random import randrange

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
    """
    Ecran d'acceuil
    """
    def __init__(self, master):
        Frame.__init__(self, master)
        fontTitle = Font(family="Arial", size=40)
        fontNormal = Font(family="Arial", size=20)
        self.master = master

        # existe principalement pour éviter un messge d'erreur du a la fonction récurssive flash
        self.isflashing = True

        # state : True: montre le texte, False : desactive le texte
        self.state = True

        # création du canvas
        self.color = "#ff0000"
        self.cnv = Canvas(self, width=WIDTH, height=HEIGHT, bg=self.color)
        self.cnv.pack()

        # création de l'arriere plan
        self.bgImage = PhotoImage(file="img/default.png")
        self.cnv.create_image(WIDTH//2, HEIGHT//2, image=self.bgImage, anchor="center")
        self.cnv.bgImage = self.bgImage

        # ajout du titre du jeu
        self.title = self.cnv.create_text(WIDTH//2, 100, text="The Legends of Number :\n1", fill="green", font=fontTitle, justify="center")

        # ajout de text informatif
        self.text = self.cnv.create_text(WIDTH//2, HEIGHT*3//4, text="Appuyez sur Entrée pour jouer", disabledfill="#888888", fill="white", font=fontNormal)

        # lancement de l'animation
        self.flash()
        self.animation()

        # évenements
        master.bind('<Return>', self.startCommand)

    def startCommand(self, event):
        self.master.unbind("<Return>") # par sécurité
        self.isflashing = False # pour éviter un message d'erreur
        self.master.switch_frame(SelectMenu)

    def flash(self):
        if self.state:
            self.cnv.itemconfig(self.text, state="disabled")
            self.state = False
        else:
            self.cnv.itemconfig(self.text, state=("normal"))
            self.state = True
        if self.isflashing: # seulement si on ne se prépare pas a quitter l'écran pour éviter un message d'erreur
            self.after(400, self.flash)

    def animation(self):
        red, green, blue = hex_to_rgb(self.color[1:])
        if red == 255 :
            if blue == 0 and green != 0:
                green -= 1
            elif blue != 255:
                blue += 1
            else:
                red -= 1
        elif blue == 255:
            if green == 0 and red != 0:
                red -= 1
            elif green != 255:
                green += 1
            else:
                blue -= 1
        else:
            if red == 0 and blue != 0:
                blue -= 1
            elif red != 255:
                red += 1
            else:
                green -= 1
        self.color = "#" + rgb_to_hex((red,green,blue))
        color = "#" + rgb_to_hex((255-red, 255-green, 255-blue))
        self.cnv.configure(bg=self.color)
        self.cnv.itemconfig(self.title, fill=color)
        if self.isflashing:
            self.after(30, self.animation)

class SelectMenu(Frame):
    """
    Menu de selection/création de la partie
    """
    def __init__(self, master):
        Frame.__init__(self, master)

        # création du canvas
        self.cnv = Canvas(self, width=WIDTH, height=HEIGHT, bg="white")
        self.cnv.pack()

        # ajout des images
        bgImage = PhotoImage(file="img/default.png")
        img = PhotoImage(file="img/select.png")
        self.cnv.create_image(WIDTH//2, HEIGHT//2, image=bgImage, anchor="center")
        self.cnv.create_image(WIDTH//2, HEIGHT//2, image=img, anchor="center")
        self.cnv.bgImage = bgImage
        self.cnv.image = img

        # récupération des infos des joueurs de chaques parties si existante
        self.infosFile1 = self.getFileInfo("saves/file1.txt")
        self.infosFile2 = self.getFileInfo("saves/file2.txt")
        self.infosFile3 = self.getFileInfo("saves/file3.txt")

        # création des boutons
        self.b1 = Button(self.cnv, WIDTH//4, 100, WIDTH//2, 75, text="Pas de sauvegarde" if self.infosFile1 == None else self.infosFile1["charaName"])
        self.b2 = Button(self.cnv, WIDTH//4, 200, WIDTH//2, 75, text="Pas de sauvegarde" if self.infosFile2 == None else self.infosFile2["charaName"])
        self.b3 = Button(self.cnv, WIDTH//4, 300, WIDTH//2, 75, text="Pas de sauvegarde" if self.infosFile3 == None else self.infosFile3["charaName"])
        self.back = None
        self.play = None

        # affichage des boutons
        self.b1.draw()
        self.b2.draw()
        self.b3.draw()

        # création des évenements
        # clique gauche
        self.b1.bind("<Button-1>", lambda e: self.func(e, 1))
        self.b2.bind("<Button-1>", lambda e: self.func(e, 2))
        self.b3.bind("<Button-1>", lambda e: self.func(e, 3))

        # souris au dessus de l'objet
        self.b1.bind("<Enter>", self.b1.mouseOver)
        self.b2.bind("<Enter>", self.b2.mouseOver)
        self.b3.bind("<Enter>", self.b3.mouseOver)

        # souris quitte le dessus de l'objet
        self.b1.bind("<Leave>", self.b1.mouseQuit)
        self.b2.bind("<Leave>", self.b2.mouseQuit)
        self.b3.bind("<Leave>", self.b3.mouseQuit)

    def getFileInfo(self, filepath):
        """
        E : le chemin d'acces d'un fichier
        S : None : ssi pas d'infos sur la partie
            infos(dico) : les infos de la partie ssi existantes
        """
        infos = {
            "charaName" : "",
            "map" : (0, 0),
            "life" : 300,
            "maxLife" : 300}
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
            Path("saves").mkdir(parents=True, exist_ok=True) # création du dossier si non existant
            return None
        except ValueError:
            return None

    def func(self, event, index):
        if index in [1,2,3]:
            self.transition1(index, 80)
        else:
            print("this should not happen")

    def transition1(self, index, cpt, dt=1):
        # cpt : compteur
        # index : le numérau du bouton cliqué
        # dt (détransition) : 1 si transition -1 si détransition
        if cpt == 0:
            if dt == -1:
                self.b1.rebind()
                self.b2.rebind()
                self.b3.rebind()
            else:
                self.transition2(index, 10 if index==2 else 20)
        else:
            if index == 1:
                self.b2.changePos(-10*dt, 0)
                self.b3.changePos(10*dt, 0)
            elif index == 2:
                self.b1.changePos(-10*dt, 0)
                self.b3.changePos(10*dt, 0)
            else:
                self.b1.changePos(-10*dt, 0)
                self.b2.changePos(10*dt, 0)
            self.after(10, lambda:self.transition1(index, cpt-1, dt=dt))

    def transition2(self, index, cpt, dt=1):
        # cpt : compteur
        # index : le numérau du bouton cliqué
        # dt (détransition) : 1 si transition -1 si détransition
        if cpt == 0 or index == 1:
            if dt == -1:
                self.transition1(index, 80, dt=-1)
            else:
                self.back = Button(self.cnv, WIDTH//7, -40, 90, 40, text="Retour")
                self.play = Button(self.cnv, WIDTH//7, HEIGHT+40, 90, 40, text="Play")
                self.b1.unbind()
                self.transition3(index, 16)
        else:
            if index == 2:
                self.b2.changePos(0, -10*dt)
            else:
                self.b3.changePos(0, -10*dt)
            self.after(10, lambda:self.transition2(index, cpt-1, dt=dt))

    def transition3(self, index, cpt, dt=1):
        # cpt : compteur
        # index : le numérau du bouton cliqué
        # dt (détransition) : si vrai applique l'inverse de la transition
        if cpt == 0:
            if dt == -1:
                self.transition2(index, 10 if index == 2 else 20, dt=-1)
                self.back.destroy()
                self.play.destroy()
            else:
                self.back.bind("<Button-1>", lambda e: self.detransition(index, e))
                self.back.bind("<Enter>", self.back.mouseOver)
                self.back.bind("<Leave>", self.back.mouseQuit)
                self.showFileMenu(index)
        else:
            self.back.changePos(0, 10*dt)
            self.play.changePos(0, -10*dt)
            self.after(10, lambda:self.transition3(index, cpt-1, dt=dt))

    def detransition(self, index, event):
        self.transition3(index, 10 if index==2 else 20, dt=-1)

    def showFileMenu(self, index):
        pass

    def createFile(self, filepath):
        pass


class Button(object):
    """
    Boutons custom
    """
    def __init__(self, canvas, x, y, width, height, marge=5, text="", font=None):
        self.cnv = canvas
        self.marge = marge
        self.points = [(x+marge,y), (x+width-marge, y), (x+width, y+marge), (x+width, y+height-marge), (x+width-marge, y+height), (x+marge, y+height), (x, y+height-marge), (x, y+marge)]
        self.x = x
        self.y = y
        self.w = width
        self.h = height
        self.text = text
        self.font = Font(family="Arial", size=20) if font==None else font
        self.polygon = None
        self.label = None
        self.events = []

    def draw(self):
        self.polygon = self.cnv.create_polygon(self.points, outline="white", fill='')
        self.label = self.cnv.create_text(self.x + self.w//2, self.y+self.h//2, text=self.text, font=self.font, fill="white")

    def hide(self):
        self.cnv.itemconfigure(self.polygon, state="hidden")
        self.cnv.itemconfigure(self.label, state="hidden")

    def show(self):
        self.cnv.itemconfigure(self.polygon, state="normal")
        self.cnv.itemconfigure(self.label, state="normal")

    def destroy(self):
        self.cnv.delete(self.polygon)
        self.cnv.delete(self.label)

    def changePos(self, x, y):
        self.x += x
        self.y += y
        self.points = [(self.x+self.marge, self.y), (self.x+self.w-self.marge, self.y), (self.x+self.w, self.y+self.marge), (self.x+self.w, self.y+self.h-self.marge), (self.x+self.w-self.marge, self.y+self.h), (self.x+self.marge, self.y+self.h), (self.x, self.y+self.h-self.marge), (self.x, self.y+self.marge)]
        self.cnv.delete(self.polygon)
        self.cnv.delete(self.label)
        self.polygon = self.cnv.create_polygon(self.points, outline="white", fill='')
        self.label = self.cnv.create_text(self.x + self.w//2, self.y+self.h//2, text=self.text, font=self.font, fill="white")

    def centerLabel(self):
        self.cnv.delete(self.label)
        self.label = self.cnv.create_text(self.x+self.w//2, self.y+self.h//2, text=self.text, font=self.font, fill="white")

    def bind(self, event, func):
            self.cnv.tag_bind(self.polygon, event, func)
            self.cnv.tag_bind(self.label, event, func)
            self.events.append((event, func))

    def unbind(self):
        for event, func in self.events:
            self.cnv.tag_unbind(self.polygon, event)
            self.cnv.tag_unbind(self.label, event)

    def rebind(self):
        """
        apres le changement de pos le bouton n'est plus bind.
        pour palier a cela la fonction rebind permet de redonner les evenements au bouton
        """
        for event, func in self.events:
            self.cnv.tag_bind(self.polygon, event, func)
            self.cnv.tag_bind(self.label, event, func)

    def mouseOver(self, event):
        self.cnv.itemconfig(self.polygon, fill="#888888")

    def mouseQuit(self, event):
        self.cnv.itemconfig(self.polygon, fill='')

if __name__ == "__main__":
    WIDTH = 1000
    HEIGHT = WIDTH * 9 // 14
    app = App()
    app.mainloop()
