#Goals:
#0: Make menu IN PROGRESS
#1: Get graphical representaiton of board DONE
#2: Get sprites for the qubit states and gates NEXT
    #Spin 1, Spin 0, Bell state qubits; Hadamard gates, controlled not gates, bit flip gates, etc.
#3: Encode for events for:
    #3a: moving marbles
    #3b: placing gates
    #3c: progressing a turn and checking the board for good matches (How would the pieces be encoded on the board to allow for recognition of a win state)?
    #3d: removing marbles
    #3e: win state
    #3f: Text popups

#Clerical details:
#Add more type hints
#Add more comments breaking down the code
import pygame as pg
import numpy as np
import os

pg.init()
screen = pg.display.set_mode((800, 800))
main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, "data")
pg.display.set_caption("Quantum Nine Men Morris")
font = pg.font.Font(os.path.join(data_dir, "SpongeboyMeBob.ttf"), 20)

def initializeBoard(): #INITIALIZED FOR SURFACES AND NOT RECTANGLES
    coords = np.zeros((18,2))
    for i in range(1,19):
        if i <= 9:
            coords[i-1] = [10, i*50]
        else:
            coords[i-1] = [765, (i-9)*50]
    return coords

#INSERT FUNCTION FOR CHECKING BOARD STATE


def load_image(name, colorkey=None, scale=1): #from pygame website
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

def load_sound(name): #from pygame website
    class NoneSound:
        def play(self):
            pass

    if not pg.mixer or not pg.mixer.get_init():
        return NoneSound()

    fullname = os.path.join(data_dir, name)
    sound = pg.mixer.Sound(fullname)

    return sound

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
captureSound = load_sound("capture.wav")
placementSound = load_sound("placement.mp3")

pieceCoords = initializeBoard()
score = [0,0]

clock = pg.time.Clock()

#TODO: Initialize game values
#TODO: Make menu
menu = True
while menu: #menu loop
    screen.blit(menuImg[0], (0,0))
    play = screen.blit(playButton[0], [50, 720])
    rules = screen.blit(rulesButton[0], [300, 720])
    settings = screen.blit(settingsButton[0], [550, 720])
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit(0)

        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            pos = pg.mouse.get_pos()
            if play.collidepoint(pos): #event for clicking "PLAY!!!" button
                menu = False #EXIT WHILE LOOP
                break #EXIT FOR LOOP
            '''
            if rules.collidepoint(pos): #event for clicking "Rules" button
                rulesDisplay = True
                rules = []
                text_num = 0
                with f as open(os.path.join(data_dir, "rules.txt"), 'r'):
                    for i in f:
                        rules.append(f.readline())

                while rulesDisplay:
                    screen.blit(background[0], (0,0))
                    text = font.render(text[text_num], True, (0,0,0))
                    textRect = text.getRect()
                    textRect.center = (400, 400)
                    screen.blit(text, textRect)
                    mButton = screen.blit(menuButton, [550, 720])
                    for event in pg.event.get():
                        if event.type = pg.MOUSEBUTTONDOWN and event.button == 1:
                            pass #TODO: Finish the rules display
                    pg.display.update()
                    clock.tick(20)
            '''
            if settings.collidepoint(pos): #event for clicking "Settings" button
                settingsDisplay = True
                while settingsDisplay:
                    pass
            else:
                pass
    pg.display.update()
    clock.tick(20)

#TODO: Clear entities from screen
#TODO: Increase calls for events in while loop
while True: #game loop
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit(0)

    screen.blit(board_surface[0], (0,0)) #place board on screen
    for i in range(0, 18): #TEST: PLACING PIECES; need to initialize with rectangle
        if i <= 8:
            screen.blit(white_piece[0], pieceCoords[i]) #Need to store entities in an array
        else:
            screen.blit(black_piece[0], pieceCoords[i])
    pg.display.update()
    clock.tick(20)
