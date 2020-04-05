# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 15:26:35 2020

@author: Kiryonn
"""
from tkinter import PhotoImage

class Entity(object):
    def __init__(self, maxHP=300, attackDMG=2, imagePath="images/default.png"):
        """stats fixe"""
        self.maxHP = maxHP
        self.attackDMG = attackDMG
        """stats variables"""
        self.HP = maxHP
        self.image = PhotoImage(file=imagePath)
        """positionnement"""
        self.x = 0
        self.y = 0

    def attack(self):
        pass

    def takeDmg(self, dmgTaken):
        self.HP -= dmgTaken
        if self.HP <= 0:
            self.HP = 0
            self.death()

    def death(self):
        pass


class Player(Entity):
    def __init__(self, name, **kw):
        Entity.__init__(self, kw)
        self.name = name

    def raiseAtk(self, nb):
        self.attackDMG += nb


class Monster(Entity):
    def __init__(self, **kw):
        Entity.__init__(self, kw)


