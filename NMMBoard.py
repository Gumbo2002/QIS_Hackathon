#Goals:
#0: Make menu -> IN PROGRESS
    #Get play button working -> DONE
    #Get rules working -> DONE
    #Get settings working -> DONE
#1: Get graphical representaiton of board -> DONE
#2: Get sprites for the qubit states and gates -> IN PROGRESS
    #Spin 1, Spin 0, Bell state qubits; Hadamard gates, controlled not gates, bit flip gates, etc.
#3: Encode for events for:
    #3a: moving marbles -> NEXT
    #3b: placing gates -> NEXT
    #3c: progressing a turn and checking the board for good matches (How would the pieces be encoded on the board to allow for recognition of a win state)? -> MICHAEL
    #3d: removing marbles -> NEXT
    #3e: win state -> NEXT
    #3f: Text popups -> DANIEL

#Clerical details:
#Add more type hints
#Add more comments breaking down the code
import pygame as pg
import numpy as np
import os
import csv
import typing
from piece import pieceSprite

pg.init()                                                               #Initialize the game engine
screen = pg.display.set_mode((800, 800))                                #Initialize the
main_dir = os.path.split(os.path.abspath(__file__))[0]                  # VVV
data_dir = os.path.join(main_dir, "data")                               # > Get data directory
pg.display.set_caption("Quantum Nine Men Morris")                       #Set caption
FONT = pg.font.Font(os.path.join(data_dir, "SpongeboyMeBob.ttf"), 25)   #initialize font


#method obtained from this source: https://www.pygame.org/wiki/TextWrap
#function which handles drawing the text for the rules.

def menu():
    while True: #menu loop
        screen.blit(menuImg[0], (0,0))                        # These functions put the following objects on the screen at
        play = screen.blit(playButton[0], [40, 720])          # specified coordinates.
        rules = screen.blit(rulesButton[0], [290, 720])       #
        settings = screen.blit(settingsButton[0], [540, 720]) #
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit(0)

            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                pos = pg.mouse.get_pos()
                if play.collidepoint(pos): #event for clicking "PLAY!!!" button
                    return 0

                if rules.collidepoint(pos): #event for clicking "Rules" button
                    handleRules()
                    break

                if settings.collidepoint(pos): #event for clicking "Settings" button
                    settingsDisplay: bool = True
                    while settingsDisplay:
                        pass
                else:
                    pass
        pg.display.update()
        clock.tick(20)

def drawText(surface, text, color, rect, font, aa=False, bkg=None) -> None:
    y = rect.top
    lineSpacing = -2

    # get the height of the font
    fontHeight = font.size("Tg")[1]

    while text:
        i = 1

        # determine if the row of text will be outside our area
        if y + fontHeight > rect.bottom:
            break

        # determine maximum width of line
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1

        # if we've wrapped the text, then adjust the wrap to the last word
        if i < len(text):
            i = text.rfind(" ", 0, i) + 1

        # render the line and blit it to the surface
        if bkg:
            image = font.render(text[:i], 1, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(text[:i], aa, color)

        surface.blit(image, (rect.left, y))
        y += fontHeight + lineSpacing

        # remove the text we just blitted
        text = text[i:]

#handles the display of the rules; text is fed through the drawText function above.
def handleRules()  -> None:
    rules = []
    text_num = 0
    path = os.path.join(data_dir, "rules.txt")
    textBox = pg.Rect(50, 50, 650, 650)
    with open(path, 'r') as f:
        for i in f:
            if i != "\n":
                rules.append(i)

    while True:
        screen.blit(background[0], (0,0))
        drawText(screen, rules[text_num], (247, 227, 176), textBox, FONT)
        if text_num != len(rules) - 1:
            nButton = screen.blit(nextButton[0], [550, 720])

        else:
            mButton = screen.blit(menuButton[0], [550, 720])

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit(0)

            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and text_num != len(rules)-1:
                pos = pg.mouse.get_pos()
                if nButton.collidepoint(pos): #Handle pressing of the next button
                    text_num += 1
                    break

            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and text_num == len(rules)-1:
                pos = pg.mouse.get_pos()
                if mButton.collidepoint(pos): #Handle pressing of the menu button
                    return 0

            pg.display.update()
            clock.tick(20)

def initializeBoard() -> list[int]:
    coords = np.zeros((18,2))
    for i in range(1,19):
        if i <= 9:
            coords[i-1] = [10, i*50]

        else:
            coords[i-1] = [765, (i-9)*50]

    return coords

#INSERT FUNCTION FOR CHECKING BOARD STATE

#TODO: finish comments -> indicate the type of sound in def
def load_image(name: str, colorkey=None, scale=1): #from pygame website
    fullname = os.path.join(data_dir, name)
    image = pg.image.load(fullname)

    size = image.get_size()
    size = (size[0] * scale, size[1] * scale)
    image = pg.transform.scale(image, size)

    image = image.convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pg.RLEACCEL)
    return image, image.get_rect()

#TODO: finish comments -> indicate the type of sound in def
def load_sound(name: str): #from pygame website
    class NoneSound:
        def play(self):
            pass

    if not pg.mixer or not pg.mixer.get_init():
        return NoneSound()

    fullname = os.path.join(data_dir, name)
    sound = pg.mixer.Sound(fullname)

    return sound

#TODO: Finish

'''
def checkMove(pos1: tuple(int), pos2: tuple(int)) -> tuple(bool, int):
#check for the intersection of the mouse with the spaces; check for illegal moves based on the initial position of the mouse when picking up the piece
#check for the intersection of a piece sprite with an open space. If there is an illegal move, move the piece back to its original space
#TODO: Encode events for getting piece sprites close to the following coords:
    #top left: (100, 100)
    #top middle: (400, 100)
    #top right: (700, 100)
    #outer mid left: (100, 400)
    #outer mid right: (700, 400)
    #bottom left: (100, 700)
    #bottom right: (700, 700)
    #bottom middle: (400, 700)
    #mid top: (400, 200)
    #mid right: (600, 400)
    #mid right corner: (600, 200)
    #mid left corner: (200, 200)
    #mid left: (200, 400)
    #mid bottom left: (200, 600)
    #mid bottom right: (600, 600)
    #mid bottom: (400, 600)
    #inner right: (500, 400)
    #inner top right: (500, 300)
    #inner top: (400, 300)
    #inner top left: (300, 300)
    #inner left: (300, 400)
    #inner bottom right: (500, 500)
    #inner bottom left: (300, 500)
    #inner bottom: (400, 500)
    return (checkBool, checkInt)
'''

playButton = load_image("playButton.png")
rulesButton = load_image("rulesButton.png")
settingsButton = load_image("settingsButton.png")
nextButton = load_image("nextButton.png")
menuButton = load_image("menuButton.png")
menuImg = load_image("menu.png")
background = load_image("gameBacking.png") #TODO Use somewhere
clubLogo = load_image("QIS.png") #TODO Use somewhere; maybe at the end when the game is over
board_surface = load_image("canvas.png")
white_piece = load_image("WhitePiece.png")
black_piece = load_image("BlackPiece.png")
P1_0 = load_image("P1_0.png")
P1_1 = load_image("P1_1.png")
P2_0 = load_image("P2_0.png")
P2_1 = load_image("P2_1.png")
captureSound = load_sound("capture.wav")
placementSound = load_sound("placement.mp3")

pieceCoords: list[int] = initializeBoard()
score: list[int] = [0,0]

clock = pg.time.Clock()

#TODO: Initialize game parameters in settings

P1_sprites = pg.sprite.Group()
P2_sprites = pg.sprite.Group()
for i in range(9):
    P1_sprites.add(pieceSprite(P1_1[0].convert(), P1_1[1], 30, i*75, 1))
    P2_sprites.add(pieceSprite(P2_0[0].convert(), P2_0[1], 770, i*75, 0))


turn = [True, False] #Determines turn order
activateMenu = True
menuButton[1].center = (800/2, 770)
while True: #game loop
    if activateMenu:
        menu()
        activateMenu = False

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit(0)

        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if mButton.collidepoint(pg.mouse.get_pos()):
                activateMenu = True
                break

    #method for draggin sprites
        #TODO: Finish block of code which handles the turns
        if (event.type == pg.MOUSEBUTTONDOWN and turn[0]):
            pos1 = pg.mouse.get_pos()

            for i in P1_sprites.sprites():
                if i.rect.collidepoint(pos1):
                    movePiece = True
                    while movePiece:
                        for event in pg.event.get():
                            i.rect.center = pg.mouse.get_pos()
                            P1_sprites.draw(screen)
                            if event.type == pg.MOUSEBUTTONUP:
                                i.rect.center = pg.mouse.get_pos()
                                movePiece = False
                                turn = [False, True]


        elif (event.type == pg.MOUSEBUTTONDOWN and turn[1]):
            pos1 = pg.mouse.get_pos()

            for j in P2_sprites.sprites():
                if j.rect.collidepoint(pos1):
                    movePiece = True
                    while movePiece:
                        for event in pg.event.get():
                            j.rect.center = pg.mouse.get_pos()
                            P2_sprites.draw(screen)
                            if event.type == pg.MOUSEBUTTONUP:
                                j.rect.center = pg.mouse.get_pos()
                                movePiece = False
                                turn = [True, False]

    screen.blit(board_surface[0], (0,0)) #place board on screen
    mButton = screen.blit(menuButton[0], menuButton[1])
    P1_sprites.draw(screen)
    P2_sprites.draw(screen)
    pg.display.update()
    clock.tick(20)
