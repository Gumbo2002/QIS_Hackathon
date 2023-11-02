import pygame as pg

#Class containing methods and variables defining game pieces
class pieceSprite(pg.sprite.Sprite):
    def __init__(self, image, rectangle, x, y, value):
        pg.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = rectangle
        self.rect.center = (x, y)
        self.value = value
        self.stage = 0

    #handle events
    def update(self, events, image, value = -1):
        if self.stage == 0:
            transmute(self, image, value) #pass in superposition image
            self.stage = 1
        if self.stage != 0:
            transmute(self, image, value) #pass in collapsed image and corresponding value
            self.stage = 0

    #Change qubit states visually
    def transmute(self, image, value):
        self.image = image
        self.rect = rectangle #Will this method work
        self.value = value

