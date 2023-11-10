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

from qiskit import QuantumCircuit
from qiskit import transpile 
from qiskit.providers.aer import AerSimulator

pg.init()                                                               #Initialize the game engine
screen = pg.display.set_mode((800, 800))                                #Initialize the
main_dir = os.path.split(os.path.abspath(__file__))[0]                  # VVV
data_dir = os.path.join(main_dir, "data")                               # > Get data directory
pg.display.set_caption("Quantum Nine Men Morris")                       #Set caption
FONT = pg.font.Font(os.path.join(data_dir, "SpongeboyMeBob.ttf"), 25)   #initialize font
locations = []
qubit = 0
circ = QuantumCircuit(18)
temp = 0

#method obtained from this source: https://www.pygame.org/wiki/TextWrap
#function which handles drawing the text for the rules.

def menu():
    while True: #menu loop
        settings = { #default settings; will reset everytime you return to the menu
            "pointsToWin" : 3, #number of mills to win the game (MIN = 1, MAX = 7)
            "numPieces" : 9,   #number of pieces afforded to each player (MIN = 3, MAX = 9)
            "numEntangle" : 4  #number of pairs of qubits that can be entangled per person at one time (MIN = 0, MAX = 8)
        }
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
                    return settings

                if rules.collidepoint(pos): #event for clicking "Rules" button
                    handleRules()
                    break

                if settings.collidepoint(pos): #event for clicking "Settings" button
                    settings = handleSettings()
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

            pg.display.flip()
            clock.tick(20)

def handleSettings() -> dict:
    #handles the display of the settings and passes the variables to the settings variable
    slider = load_image("WhitePiece.png")
    sliderTrack = load_image()
    while True:
        for event in pg.event.get():
            if(event == pg.MOUSEBUTTONDOWN and event.button == 1):
                pos = pg.mouse.get_pos()
                if sliderButton1.collidePoint(pos):
                    for event in pg.event.get():
                        if(event == pg.MOUSEBUTTONUP):
                            #stop the slider at the current position and initialize the concomitant value associated for pointsToWin
                            pointsToWin = sliderButton1.ge
                            break
                elif sliderButton2.collidePoint(pos):
                    for event in pg.event.get():
                        if(event == pg.MOUSEBUTTONUP):
                            #stop the slider at the current position and initialize the concomitant value associated for numPieces
                            numPieces = sliderButton2.ge
                            break
                elif sliderButton3.collidePoint(pos):
                    for event in pg.event.get():
                        if(event == pg.MOUSEBUTTONUP):
                            #stop the slider at the current position and initialize the concomitant value associated for numEntangle
                            numEntangle = sliderButton3.ge
                            break
                return {
                    "pointsToWin" : pointsToWin,
                    "numPieces" : numPieces,
                    "numEntangled" : numEntangle
                }
                #check for collision with rectangle representing slider bar
        
        menuButton = screen.blit(menuButton[0], [550, 720])
        sliderButton1 = screen.blit(slider[0], [400, 100])
        sliderButton2 = screen.blit(slider[0], [400, 300])
        sliderButton3 = screen.blit(slider[0], [400, 500])
        pg.display.flip()
        clock.tick(20)

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

def check_win():
    #Break algorithm into rings and check 4 sides, and in separate loop check 4 cross rings
    p1_win = 0
    p2_win = 0
    for i in range(3):
        triple = [0,0]
        sums = [0,0]
        for j in range(2):
            triple[0] = (get_state((i,2*j,0))==get_state((i,2*j,1)) and get_state((i,2*j,1))==get_state((i,2*j,2)))
            triple[1] = (get_state((i,0,2*j))==get_state((i,1,2*j)) and get_state((i,1,2*j))==get_state((i,2,2*j)))
            sums[0] = get_state((i,2*j,0))+get_state((i,2*j,1))+get_state((i,2*j,2))
            sums[1] = get_state((i,0,2*j))+get_state((i,1,2*j))+get_state((i,2,2*j))
            if(1 in triple):
                if(sums[triple.index(1)] > 0):
                    print("Player +1 scores")
                else:
                    print("Player -1 scores")
    #Cross ring check
    triple = [0,0]
    sums = [0,0]
    for j in range(2):
        triple[0] = (get_state((0,1,2*j))==get_state((1,1,2*j)) and get_state((1,1,2*j))==get_state((2,1,2*j)))
        triple[1] = (get_state((0,2*j,1))==get_state((1,2*j,1)) and get_state((1,2*j,1))==get_state((2,2*j,1)))
        sum[0] = get_state((0,1,2*j))+get_state((1,1,2*j))+get_state((2,1,2*j))
        sum[1] = get_state((0,2*j,1))+get_state((1,2*j,1))+get_state((2,2*j,1))
        if(1 in triple):
            if(sums[triple.index(1)] > 0):
                print("Player +1 scores")
            else:
                print("Player -1 scores")

def set_state(tup,value):
    states[tup[0],tup[1],tup[2]] = value

def get_state(tup):
    return states[tup[0],tup[1],tup[2]]

def distance(pos1, pos2):
    #print(pos1,pos2)
    return (pos1[0]-pos2[0])**2+(pos1[1]-pos2[1])**2

#Returns the index of the location in the state array
def state_index(pos):
    for i in range(3):
        for j in range(3):
            for k in range(3):
                loc = [400+(3-i)*(100*(j-1)),400+(3-i)*(100*(k-1))]
                if(distance(pos,loc)<150):
                    return (i,j,k)
    return (-1,-1,-1)
        
def index_position(tup):
    return (400+(3-tup[0])*(100*(tup[1]-1)),400+(3-tup[0])*(100*(tup[2]-1)))

def state_empty(rect):
    loc = state_index(rect)
    #print(loc)
    if(loc[0]==-1):
        return True
    return (states[loc[0]][loc[1]][loc[2]] == 0)

def measure():
    meas = QuantumCircuit(18, 18)
    meas.barrier(range(18))
    meas.measure(range(18), range(18))
    qc = meas.compose(circ, range(18), front=True)
    backend = AerSimulator()
    qc_compiled = transpile(qc, backend)
    job_sim = backend.run(qc_compiled, shots=1024)
    result_sim = job_sim.result()
    counts = result_sim.get_counts(qc_compiled)
    print(counts)
    result = max(counts, key=lambda key: counts[key])
    print(result,qubit)
    for i in range(qubit):
        print(result[-i])
        if(result[17-i]=="1"):
            if(get_state(locations[i])>0):
                set_state(locations[i],2)
                print(locations[i])
                print(index_position(locations[i]))
                #change to P1_1
                for p1 in P1_sprites.sprites(): #Check for interactions with a piece FROM PLAYER 1
                    if p1.rect.collidepoint(index_position(locations[i])):
                        P1_sprites.remove(p1)
                        P1Temp = load_image("P1_1.png")
                        P1_sprite = pieceSprite(P1Temp[0], P1Temp[1], p1.rect.center[0], p1.rect.center[1], 1)
                        P1_sprites.add(P1_sprite)
                        print("update",locations[i])
            else:
                set_state(locations[i],-2)
                print(locations[i])
                print(index_position(locations[i]))
                #change to P2_1
                for p2 in P2_sprites.sprites(): #Check for interactions with a piece FROM PLAYER 1
                    if p2.rect.collidepoint(index_position(locations[i])):
                        P2_sprites.remove(p2)
                        P2Temp = load_image("P2_1.png")
                        P2_sprite = pieceSprite(P2Temp[0], P2Temp[1], p2.rect.center[0], p2.rect.center[1], 1)
                        P2_sprites.add(P2_sprite)
                        print("update",locations[i])
        else:
            if(get_state(locations[i])>0):
                set_state(locations[i],1)
                print(locations[i])
                print(index_position(locations[i]))
                #change to P1_0
                for p1 in P1_sprites.sprites(): #Check for interactions with a piece FROM PLAYER 1
                    if p1.rect.collidepoint(index_position(locations[i])):
                        P1_sprites.remove(p1)
                        P1Temp = load_image("P1_0.png")
                        P1_sprite = pieceSprite(P1Temp[0], P1Temp[1], p1.rect.center[0], p1.rect.center[1], 1)
                        P1_sprites.add(P1_sprite)
                        print("update",locations[i])
            else:
                set_state(locations[i],-1)
                print(locations[i])
                print(index_position(locations[i]))
                #change to P2_0
                for p2 in P2_sprites.sprites(): #Check for interactions with a piece FROM PLAYER 1
                    if p2.rect.collidepoint(index_position(locations[i])):
                        P2_sprites.remove(p2)
                        P2Temp = load_image("P2_0.png")
                        P2_sprite = pieceSprite(P2Temp[0], P2Temp[1], p2.rect.center[0], p2.rect.center[1], 1)
                        P2_sprites.add(P2_sprite)
                        print("update",locations[i])

def add_gate(pos,turnNum):
    global qubit
    global temp
    print(state_index(pos))
    if(state_index(pos) not in locations):
        print("New location")
        tup = state_index(pos)
        locations.append(tup)
        if(abs(get_state(tup))==1):#Apply bit flip to +1
            circ.x(qubit)
            print("not",qubit)
        if(get_state(tup)==0):#Apply H to 0 as boundary
            circ.h(qubit)
            print("hb",qubit)
        if(turnNum%2==0):#Even qubits
            circ.h(qubit)
            print("h",qubit)
            temp = qubit
        else:#Odd qubits
            circ.cx(temp,qubit)
            print("cnot",temp,qubit)
        qubit = qubit + 1
    else:#Apply duplicate tup to existing qubit in location
        for j in range(qubit):
            if(tup==locations[j]):
                if(turnNum%2==0):
                    circ.h(j)
                    print("h",j)
                    temp = j
                else:
                    if(temp != j):
                        circ.cx(temp, j)
                        print("cnot",temp,j)

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

def matrixToCenter(rings):
    return

#draws board between turns and uses 'goodMove' to choose which message to display at the top
def displayBoard(board_surface, menuButton, screen, turn, turnBox, P1_sprites, P2_sprites, goodMove):
    screen.blit(board_surface[0], (0,0)) #place board on screen
    screen.blit(menuButton[0], menuButton[1])
    if(goodMove):
        if(turn[0]==True): drawText(screen, "Red Turn", (247, 227, 176), turnBox, FONT)
        else: drawText(screen, "Blue Turn", (247, 227, 176), turnBox, FONT)
    else: drawText(screen, "Not There! Choose an open space.", (247, 227, 176), turnBox, FONT)
    P1_sprites.draw(screen)
    P2_sprites.draw(screen)
    pg.display.flip()
    return

#Puts pieces in starting positions
def resetBoard(P1_sprites, P2_sprites):
    n=1
    for i in P1_sprites:
        i.rect.center = (30, n*75)
        n += 1
        
    m=1
    for i in P2_sprites:
        i.rect.center = (770, m*75)
        m += 1
    return

def numMils(pos):
    
    return
    
#TODO: Finish
''''
def createCircuit(numPieces, maxGates, boolGates):
    template = np.zeros((numPieces, maxGates))
    for i in boolGates:
        for j in i:

    return fullTemplate
'''
#TODO: Finish



playButton = load_image("playButton.png")
rulesButton = load_image("rulesButton.png")
settingsButton = load_image("settingsButton.png")
nextButton = load_image("nextButton.png")
menuButton = load_image("menuButton.png")
menuImg = load_image("menu.png")
background = load_image("gameBacking.png") #TODO Use somewhere
clubLogo = load_image("QIS.png") #TODO Use somewhere; maybe at the end when the game is over
board_surface = load_image("canvas.png")
states = np.zeros((3, 3, 3)) 
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

score = [0,0]
clock = pg.time.Clock()

#TODO: Initialize game parameters in settings

P1_sprites = pg.sprite.Group()  # Create a sprite group for P1
P2_sprites = pg.sprite.Group()  # Create a sprite group for P2

# Create and add sprites to the sprite groups
for i in range(1,10):
    P1Temp = load_image("P1_1.png")
    P1_sprite = pieceSprite(P1Temp[0], P1Temp[1], 30, i*75, 1)
    P1_sprites.add(P1_sprite)

    P2Temp = load_image("P2_0.png")
    P2_sprite = pieceSprite(P2Temp[0], P2Temp[1], 770, i*75, 1)
    P2_sprites.add(P2_sprite)

turn = [True, False] #Determines turn order
activateMenu = True
menuButton[1].center = (800/2, 770)
turnBox = pg.Rect(350, 0, 200, 50)
goodMove = True
points = [0, 0]
turnNum = 0
settings = None #initialized in game loop


while True: #game loop
    if activateMenu:
        settings = menu()
        activateMenu = False

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit(0)

        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if menuButton[1].collidepoint(pg.mouse.get_pos()):
                activateMenu = True
                resetBoard(P1_sprites, P2_sprites)
                break
        if(turnNum == 18):
            qubit = 0
        
        #Handle entanglement
        if(event.type == pg.MOUSEBUTTONDOWN and turnNum >= 18):
            turn = [False,False]
            pos = pg.mouse.get_pos()
            for p1 in P1_sprites.sprites():
                if p1.rect.collidepoint(pos):
                    add_gate(pos,turnNum)
                    turnNum = turnNum + 1
                    if(turnNum%2==0):
                        measure()
                    P1_sprites.draw(screen)
                    check_win()
            for p2 in P2_sprites.sprites():
                if p2.rect.collidepoint(pos):
                    add_gate(pos,turnNum)
                    turnNum = turnNum + 1
                    if(turnNum%2==0):
                        measure()
                    P2_sprites.draw(screen)
                    check_win()


        #method for draggin sprites
        #TODO: Finish block of code which handles the turns
        if (event.type == pg.MOUSEBUTTONDOWN and turn[0]):
            pos1 = pg.mouse.get_pos()
            print(pos1)
            for i in P1_sprites.sprites(): #Check for interactions with a piece FROM PLAYER 1
                if i.rect.collidepoint(pos1):
                    movePiece = True
                    while movePiece: #Movement of piece that has been clicked on
                        for event1 in pg.event.get():
                            if(event1.type == pg.MOUSEBUTTONDOWN):
                                if(turnNum < 18):
                                    #handles the initial phase; places can be placed on any unoccupied regions.
                                    tempCenter = pg.mouse.get_pos()
                                    if(canMove(tempCenter)):
                                        i.rect.center = matrixToCenter(rectToMatrix(tempCenter))
                                        set_state(state_index(tempCenter),1)
                                        P1_sprites.draw(screen)
                                        check_win()
                                        movePiece = False
                                        turnNum += 1
                                        turn = [False, True]
                                    else: 
                                        displayBoard(board_surface, menuButton, screen, turn, turnBox, P1_sprites, P2_sprites, False)

        elif (event.type == pg.MOUSEBUTTONDOWN and turn[1]):
            pos1 = pg.mouse.get_pos()
            for j in P2_sprites.sprites():
                if j.rect.collidepoint(pos1):
                    movePiece = True
                    while movePiece:
                        for event1 in pg.event.get():
                            if(event1.type == pg.MOUSEBUTTONDOWN):
                                if(turnNum < 18):
                                    tempCenter = pg.mouse.get_pos()
                                    if(canMove(tempCenter)):
                                        j.rect.center = matrixToCenter(rectToMatrix(tempCenter))
                                        set_state(state_index(tempCenter),-1)
                                        P2_sprites.draw(screen)
                                        check_win()
                                        movePiece = False
                                        turnNum += 1
                                        turn = [True, False]
                                    else: 
                                        displayBoard(board_surface, menuButton, screen, turn, turnBox, P1_sprites, P2_sprites, False)


    displayBoard(board_surface, menuButton, screen, turn, turnBox, P1_sprites, P2_sprites, True)
    clock.tick(20)
