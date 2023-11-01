#Goals:
#0: Make menu -> IN PROGRESS
    #Get play button working -> DONE
    #Get rules working -> DONE
    #Get settings working -> IN PROGRESS
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
import Circuit_Builder as cb #used to simulate quantum circuit


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

#INSERT FUNCTION FOR CHECKING BOARD STATE

#TODO: finish comments -> indicate the type of sound in def
def load_image(name: str): #modified from pygame website
    fullname = os.path.join(data_dir, name)
    image = pg.image.load(fullname)
    image = image.convert_alpha()

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

def canMove(rect): #checks if desired spot is empty
    pos = rectToMatrix(rect)
    return (positions[pos[1]][pos[0]] == 0)

def validMoves(piece):
    moves = [] #list to store the end positions of all valid moves
    clostestX, clostestY = 0, 0 #nearest neighbor distance in x and y directions
    pos = rectToMatrix(piece) #converts center of rect object into matrix coords
    
    #Determines the nearest neighbor distance based on the position of piece
    if(pos[0]==0 or pos[0]==6): clostestY = 3
    elif(pos[0]==1 or pos[0]==5): clostestY = 2
    else: clostestY = 1
    
    if(pos[1]==0 or pos[1]==6): clostestX = 3
    elif(pos[1]==1 or pos[1]==5): clostestX = 2
    else: clostestX = 1
    
    #these loops iterate through all relavent empty spaces and determines the closest ones to the piece
    #Valid X moves
    i, dist = 0, 0
    for x in positions[pos[1]]:
        if(x == 0 and i != pos[0]): #skips all spaces that are full, invalid, or the space of the piece
            dist = abs(pos[0]-i) #find the distance between empty spot and piece
            if(dist == clostestX):
                moves.append((i, pos[1])) #store all spaces that are empty and the right distance away
        i += 1   
         
    #Valid Y Moves 
    j, dist = 0, 0
    for y in positions:
        if(y[pos[0]] == 0 and j != pos[1]):
            dist = abs(pos[1]-j)
            if(dist == clostestY):
                moves.append((pos[0], j))
        j += 1
                    
    #Convert moves to rect coords     
    rectMoves = []   
    for m in moves: rectMoves.append(matrixToCenter(m[0], m[1]))
        
#    return rectMoves   #rectangle coords
    return moves    #matrix coords

#Converts from rect coordinate system to matrix coord system
def rectToMatrix(rect):
    cent = rect.center
    x, y = round((cent[0]/100)-1), round((cent[1]/100)-1)
    return (x, y)

def rectToMatrix(tup):
    x, y = round((tup[0]/100)-1), round((tup[1]/100)-1)
    return (x, y)

#Converts matrix coords to rect coords
def matrixToCenter(x, y):
    centX, centY = (x+1)*100, (y+1)*100
    return (centX, centY)

def matrixToCenter(tup):
    centX, centY = (tup[0]+1)*100, (tup[1]+1)*100
    return (centX, centY)

#TODO: Finish
''''
def createCircuit(numPieces, maxGates, boolGates):
    template = np.zeros((numPieces, maxGates))
    for i in boolGates:
        for j in i:

    return fullTemplate
'''
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
positions = [[0, -1, -1, 0, -1, -1, 0],
             [-1, 0, -1, 0, -1, 0, -1], #0 = empty
             [-1, -1, 0, 0, 0, -1, -1], #1 = white
             [ 0, 0, 0, -1, 0,  0,  0], #2 = black
             [-1, -1, 0, 0, 0, -1, -1], #else = invalid space
             [-1, 0, -1, 0, -1, 0, -1], #so, to get index (x, y) pos[y][x]
             [0, -1, -1, 0, -1, -1, 0]]
#Might need to load these individually
'''
P1_0 = load_image("P1_0.png")
P1_1 = load_image("P1_1.png")
P2_0 = load_image("P2_0.png")
P2_1 = load_image("P2_1.png")
P1_sup = load_image("P1_sup.png")
P2_sup = load_image("P2_sup.png")
'''
captureSound = load_sound("capture.wav")
placementSound = load_sound("placement.mp3")

score: list[int] = [0,0]

clock = pg.time.Clock()

#TODO: Initialize game parameters in settings

P1_sprites = pg.sprite.Group()  # Create a sprite group for P1
P2_sprites = pg.sprite.Group()  # Create a sprite group for P2

# Create and add sprites to the sprite groups
for i in range(1,10):
    #P1_1[1].move(30, i*75)
    #P1_sprite = pieceSprite(P1_1[0], P1_1[1], 30, i*75, 1)
    P1Temp = load_image("P1_1.png")
    P1_sprite = pieceSprite(P1Temp[0], P1Temp[1], 30, i*75, 1)
    P1_sprites.add(P1_sprite)

    #P2_0[1].move(770, i*75)
    #P2_sprite = pieceSprite(P2_0[0], P2_0[1], 770, i*75, 0)
    P2Temp = load_image("P2_0.png")
    P2_sprite = pieceSprite(P2Temp[0], P2Temp[1], 770, i*75, 1)
    P2_sprites.add(P2_sprite)
    
Sprite_group_initial = [P1_sprites, P2_sprites]

turn = [True, False] #Determines turn order
activateMenu = True
menuButton[1].center = (800/2, 770)
while True: #game loop
    if activateMenu:
        P1_sprites = Sprite_group_initial[0]
        P2_sprites = Sprite_group_initial[1]
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
                        for event1 in pg.event.get():
                            if(event1.type == pg.MOUSEBUTTONDOWN):
                                i.rect.center = pg.mouse.get_pos()
                                if(canMove(i.rect.center)):
                                    i.rect.center = matrixToCenter(rectToMatrix(i.rect.center))
                                    P1_sprites.draw(screen)
                                    movePiece = False
                                    turn = [False, True]
                                else: print("NO")


        elif (event.type == pg.MOUSEBUTTONDOWN and turn[1]):
            pos1 = pg.mouse.get_pos()

            for j in P2_sprites.sprites():
                if j.rect.collidepoint(pos1):
                    movePiece = True
                    while movePiece:
                        for event1 in pg.event.get():
                            if(event1.type == pg.MOUSEBUTTONDOWN):
                                j.rect.center = pg.mouse.get_pos()
                                if(canMove(j.rect.center)):
                                    j.rect.center = matrixToCenter(rectToMatrix(j.rect.center))
                                    P2_sprites.draw(screen)
                                    movePiece = False
                                    turn = [True, False]
                                else: print("NO")

    screen.blit(board_surface[0], (0,0)) #place board on screen
    mButton = screen.blit(menuButton[0], menuButton[1])

    P1_sprites.draw(screen)
    P2_sprites.draw(screen)

    pg.display.flip()
    clock.tick(20)
