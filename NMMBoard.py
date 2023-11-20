#--INCOMPLETE--

#Clerical details:
#Add more type hints
#Add more comments breaking down the code
import pygame as pg
import numpy as np
import os
import math
from math import floor
from piece import pieceSprite
#import Circuit_Builder as cb #used to simulate quantum circuit
from qiskit import QuantumCircuit
from qiskit import transpile 
from qiskit_aer import AerSimulator

def menu():
    settings = {                #default settings; will reset everytime you return to the menu
             "pointsToWin" : 3,     #number of mills to win the game (MIN = 1, MAX = 7)
             "numPieces" : 9,       #number of pieces afforded to each player (MIN = 3, MAX = 9)
             "numEntangle" : 4      #number of pairs of qubits that can be entangled per person at one time (MIN = 0, MAX = 8)
        }
    while True: #menu loop
        screen.blit(menuImg[0], (0,0))                        # These functions put the following objects on the screen at
        play = screen.blit(playButton[0], [40, 720])          # specified coordinates.
        rules = screen.blit(rulesButton[0], [290, 720])       #
        settings_button = screen.blit(settingsButton[0], [540, 720]) #
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit(0)

            if (event.type == pg.MOUSEBUTTONDOWN and event.button == 1):
                pos = pg.mouse.get_pos()
                if play.collidepoint(pos): #event for clicking "PLAY!!!" button
                    return settings

                if rules.collidepoint(pos): #event for clicking "Rules" button
                    handleRules()
                    break

                if settings_button.collidepoint(pos): #event for clicking "Settings" button
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

def handleSettings():
    menuImg = load_image("menuButton.png")
    #handles the display of the settings and passes the variables to the settings variable
    sliderTrack1 = load_image("sliderTrack.png") #used for the slider track
    sliderTrack2 = load_image("sliderTrack.png")
    sliderTrack3 = load_image("sliderTrack.png")
    display1 = pg.Rect(200, 70, 400, 30)
    display2 = pg.Rect(200, 270, 400, 30)
    display3 = pg.Rect(200, 470, 400, 30)
    MAX_pointsToWin = 7
    MAX_numPieces = 9
    MAX_numEntangle = 8
    MAX_params = [7, 9, 8]
    pointsToWin = 3
    numPieces = 9
    numEntangle = 4
    default = [3, 9 ,4]
    sliders = []
    activeSlider = None
    for i in range(0, 3): 
            sliders.append(pg.Rect(int((default[i]/MAX_params[i])*400)+200, 100+200*i, 25, 25))

    while True:
        screen.blit(background[0], (0,0))
        drawText(screen, "Points required for win = %d" %(MAX_pointsToWin*((sliders[0].x-200)/400)), [230, 0, 0], display1, FONT)
        drawText(screen, "Pieces per player = %d" %(MAX_numPieces*((sliders[1].x-200)/400)), [0, 230, 0], display2, FONT)
        drawText(screen, "Entangled pairs per player = %d" %(MAX_numEntangle*((sliders[2].x-200)/400)), [0, 0, 230], display3, FONT)
        menuButton2 = screen.blit(menuImg[0], [550, 720]) #drawing the menu button
        sliderT1 = screen.blit(sliderTrack1[0], (200, 100))
        sliderT2 = screen.blit(sliderTrack2[0], (200, 300))
        sliderT3 = screen.blit(sliderTrack3[0], (200, 500))
        for slider in sliders: 
            pg.draw.rect(screen, "purple", slider) #getting the sliders drawn
        for event in pg.event.get():
            if(event.type == pg.MOUSEBUTTONDOWN and event.button == 1):
                pos = pg.mouse.get_pos()
                if (menuButton2.collidepoint(pos)):
                    #END OF SETTINGS MENU
                    settings = {
                        "pointsToWin" : pointsToWin,     #number of mills to win the game (MIN = 1, MAX = 7)
                        "numPieces" : numPieces,       #number of pieces afforded to each player (MIN = 3, MAX = 9)
                        "numEntangle" : numEntangle      #number of pairs of qubits that can be entangled per person at one time (MIN = 0, MAX = 8)
                    }
                    return settings
                
                #check for collision with rectangle representing slider bar
                for i in range(0, len(sliders)):
                    if (sliders[i].collidepoint(pos)):
                        activeSlider = i

            if (event.type == pg.MOUSEMOTION and activeSlider != None):
                #animate the motion of the slider across the board
                new_pos = pg.mouse.get_pos()[0]
                if (new_pos < 200 or new_pos > 600): 
                    event.rel = [0]

                sliders[activeSlider].move_ip(event.rel[0], 0) #MOVES THE BOX
                if(activeSlider == 0):
                    drawText(screen, "Points required for win = %d" %(MAX_pointsToWin*((sliders[activeSlider].x - 200)/400)), [230, 0, 0], display1, FONT)
                elif(activeSlider == 1):
                    drawText(screen, "Pieces per player = %d" %(MAX_numPieces*((sliders[activeSlider].x - 200)/400)), [0, 230, 0], display2, FONT)
                else:
                    drawText(screen, "Entangled pairs per player = %d" %(MAX_numEntangle*((sliders[activeSlider].x - 200)/400)), [0, 0, 230], display3, FONT)
                pg.display.flip()

            if (event.type == pg.MOUSEBUTTONUP and activeSlider != None):
                        #stop the slider at the current position and initialize the concomitant value associated for numPieces
                        if (activeSlider == 0): 
                            pointsToWin = int(MAX_pointsToWin*((sliders[0].x - 200)/400))
                            #print(pointsToWin)
                        elif (activeSlider == 1): 
                            numPieces = int(MAX_numPieces*((sliders[1].x - 200)/400)) #PROBLEM!!!!!!!
                            #print(numPieces)
                        elif (activeSlider == 2): 
                            numEntangle = int(MAX_numEntangle*((sliders[2].x - 200)/400))
                            #print(numEntangle)
                        activeSlider = None
                        break
        
        pg.display.flip()
        clock.tick(20)

#TODO: finish comments -> indicate the type of image in def
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
        triple = [0,0,0,0,0,0]#Triple is a boolean that is true if three of the same states are next to each other
        sums = [0,0,0,0,0,0]#Sums contains the player information as positive or negative
        for j in range(2):
            colMill = ((i,2*j,0),(i,2*j,1),(i,2*j,2))
            rowMill = ((i,0,2*j),(i,1,2*j),(i,2,2*j))
            leftRingMillH = ((0,0,1),(1,0,1),(2,0,1))
            topRingMillV = ((0,1,0),(1,1,0),(2,1,0)) 
            rightRingMillH = ((0,2,1),(1,2,1),(2,2,1)) 
            botRingMillV = ((0,1,2),(1,1,2),(2,1,2))
        
            sums[0] = get_state(rowMill[0])*get_state(rowMill[1])*get_state(rowMill[2])
            sums[1] = get_state(colMill[0])*get_state(colMill[1])*get_state(colMill[2])
            sums[2] = get_state(leftRingMillH[0])*get_state(leftRingMillH[1])*get_state(leftRingMillH[2])
            sums[3] = get_state(rightRingMillH[0])*get_state(rightRingMillH[1])*get_state(rightRingMillH[2])
            sums[4] = get_state(topRingMillV[0])*get_state(topRingMillV[1])*get_state(topRingMillV[2])
            sums[5] = get_state(botRingMillV[0])*get_state(botRingMillV[1])*get_state(botRingMillV[2])
            
            ind=0
            for s in sums:
                if(math.floor(s ** (1/3)) ** 3 == s and s != 0):
                    print(s)
                    if(ind == 0):
                        if(s < 9 and ((rowMill[0],rowMill[1],rowMill[2]) not in pastWins[0])):
                            print("Player 1 scores")
                            pastWins[0].append((rowMill[0],rowMill[1],rowMill[2]))
                        elif((rowMill[0],rowMill[1],rowMill[2]) not in pastWins[1]):
                            print("Player 2 scores")
                            pastWins[1].append((rowMill[0],rowMill[1],rowMill[2]))  
                    if(ind == 1):
                        if(s < 9 and ((colMill[0],colMill[1],colMill[2]) not in pastWins[0])):
                            print("Player 1 scores")
                            pastWins[0].append((colMill[0],colMill[1],colMill[2]))
                        elif((colMill[0],colMill[1],colMill[2]) not in pastWins[1]):
                            print("Player 2 scores")
                            pastWins[1].append((colMill[0],colMill[1],colMill[2]))
                    if(ind == 2):
                        if(s < 9 and ((leftRingMillH[0],leftRingMillH[1],leftRingMillH[2]) not in pastWins[0])):
                            print("Player 1 scores")
                            pastWins[0].append((leftRingMillH[0],leftRingMillH[1],leftRingMillH[2]))
                        elif((leftRingMillH[0],leftRingMillH[1],leftRingMillH[2]) not in pastWins[1]):
                            print("Player 2 scores")
                            pastWins[1].append((leftRingMillH[0],leftRingMillH[1],leftRingMillH[2]))
                    if(ind == 3):
                        if(s < 9 and ((rightRingMillH[0],rightRingMillH[1],rightRingMillH[2]) not in pastWins[0])):
                            print("Player 1 scores")
                            pastWins[0].append((rightRingMillH[0],rightRingMillH[1],rightRingMillH[2]))
                        elif(rightRingMillH[0],rightRingMillH[1],rightRingMillH[2]) not in pastWins[1]:
                            print("Player 2 scores")
                            pastWins[1].append((rightRingMillH[0],rightRingMillH[1],rightRingMillH[2]))
                    if(ind == 4):
                        if(s < 9 and ((topRingMillV[0],topRingMillV[1],topRingMillV[2]) not in pastWins[0])):
                            print("Player 1 scores")
                            pastWins[0].append((topRingMillV[0],topRingMillV[1],topRingMillV[2]))
                        elif(topRingMillV[0],topRingMillV[1],topRingMillV[2]) not in pastWins[1]:
                            print("Player 2 scores")
                            pastWins[1].append((topRingMillV[0],topRingMillV[1],topRingMillV[2]))
                    if(ind == 5):
                        if(s < 9 and ((botRingMillV[0],botRingMillV[1],botRingMillV[2]) not in pastWins[0])):
                            print("Player 1 scores")
                            pastWins[0].append((botRingMillV[0],botRingMillV[1],botRingMillV[2]))
                        elif(botRingMillV[0],botRingMillV[1],botRingMillV[2]) not in pastWins[1]:
                            print("Player 2 scores")
                            pastWins[1].append((botRingMillV[0],botRingMillV[1],botRingMillV[2]))
                ind += 1
                

#State array is a 3*3*3 array that stores the states and colors of the pieces
#Red UP state is stored as 2
#Red DOWN state is stored as 1
#Empty is stored as 0
#Blue DOWN state is stored as -1
#Blue UP state is stored as -2
def set_state(tup,value):
    states[tup[0],tup[1],tup[2]] = value

def get_state(tup):
    return states[tup[0],tup[1],tup[2]]

def distance(pos1, pos2):
    return (pos1[0]-pos2[0])**2+(pos1[1]-pos2[1])**2

#Returns the index of the location in the state array
def state_index(pos):
    for i in range(3):
        for j in range(3):
            for k in range(3):
                loc = [400+(3-i)*(100*(j-1)), 400+(3-i)*(100*(k-1))]
                if(distance(pos, loc) < 150):
                    return (i,j,k) #(ring, col, row)
    return (-1,-1,-1)

#Converts a 3D tuple into an [x,y] coordinate for the board   
def index_position(tup):
    return (400+(3-tup[0])*(100*(tup[1]-1)), 400+(3-tup[0])*(100*(tup[2]-1)))

#Checks if the state is empty
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
    #print(counts)
    result = max(counts, key=lambda key: counts[key])
    #print(result,qubit)
    for i in range(qubit):
        #print(result[-i])
        if(result[17-i]=="1"):
            if(get_state(locations[i])>0):
                set_state(locations[i],2)
                #print(locations[i])
                #print(index_position(locations[i]))
                #change to P1_1
                for p1 in P1_sprites.sprites(): #Check for interactions with a piece FROM PLAYER 1
                    if p1.rect.collidepoint(index_position(locations[i])):
                        P1_sprites.remove(p1)
                        P1Temp = load_image("P1_1.png")
                        P1_sprite = pieceSprite(P1Temp[0], P1Temp[1], p1.rect.center[0], p1.rect.center[1], 1)
                        P1_sprites.add(P1_sprite)
                        #print("update",locations[i])
            else:
                set_state(locations[i],-2)
                #print(locations[i])
                #print(index_position(locations[i]))
                #change to P2_1
                for p2 in P2_sprites.sprites(): #Check for interactions with a piece FROM PLAYER 1
                    if p2.rect.collidepoint(index_position(locations[i])):
                        P2_sprites.remove(p2)
                        P2Temp = load_image("P2_1.png")
                        P2_sprite = pieceSprite(P2Temp[0], P2Temp[1], p2.rect.center[0], p2.rect.center[1], 1)
                        P2_sprites.add(P2_sprite)
                        #print("update",locations[i])
        else:
            if(get_state(locations[i])>0):
                set_state(locations[i],1)
                #print(locations[i])
                #print(index_position(locations[i]))
                #change to P1_0
                for p1 in P1_sprites.sprites(): #Check for interactions with a piece FROM PLAYER 1
                    if p1.rect.collidepoint(index_position(locations[i])):
                        P1_sprites.remove(p1)
                        P1Temp = load_image("P1_0.png")
                        P1_sprite = pieceSprite(P1Temp[0], P1Temp[1], p1.rect.center[0], p1.rect.center[1], 0)
                        P1_sprites.add(P1_sprite)
                        #print("update",locations[i])
            else:
                set_state(locations[i],-1)
                #print(locations[i])
                #print(index_position(locations[i]))
                #change to P2_0
                for p2 in P2_sprites.sprites(): #Check for interactions with a piece FROM PLAYER 1
                    if p2.rect.collidepoint(index_position(locations[i])):
                        P2_sprites.remove(p2)
                        P2Temp = load_image("P2_0.png")
                        P2_sprite = pieceSprite(P2Temp[0], P2Temp[1], p2.rect.center[0], p2.rect.center[1], 0)
                        P2_sprites.add(P2_sprite)
                        #print("update",locations[i])
                
#Recursive method which gets the positions of the relevant        
def handle_gate_helper(completeSet, sprite_group, pos1 = 0, pos2 = 0):
    if (completeSet[0] and completeSet[1]):
        return (pos1, pos2)
    
    if (completeSet[0] == False):
        while(True):
            for event1 in pg.event.get():
                            if (event1.type == pg.MOUSEBUTTONDOWN and event1.button == 1):
                                pos1 = pg.mouse.get_pos() #first qubit to entangle correlated with position of first click
                                for p in sprite_group:
                                    if (p.rect.collidepoint(pos1)):
                                        handle_gate_helper([True, False], pos1, pos2)
                            
    elif (completeSet[1] == False):
        while(True):
            for event1 in pg.event.get():
                            if (event1.type == pg.MOUSEBUTTONDOWN and event1.button == 1):
                                pos2 = pg.mouse.get_pos() #first qubit to entangle correlated with position of first click
                                for p in sprite_group:
                                    if (p.rect.collidepoint(pos2)):
                                        handle_gate_helper([True, False], pos1, pos2)
    print("GATE HELPER ERROR!")       
    return (pos1, pos2) #should not reach this point
    
def handle_gate(pos1, pos2, entangleType = 0, done = False):
    #TODO: FINISH
    #Handle the creation of entangled states
    #pos: get the corresponding qubit in the state array
    #entangleType: get the type state the player wants to create
    #recursive_var: used in recursion; handle_gate contains the WHOLE PROCESS of creatin entanglements
    if(state_index(pos1) not in locations):
        tup = state_index(pos1)
        locations.append(tup)
    else: 
        for j in range(qubit):
            if(tup==locations[j]):
                if(turnNum%2==0):
                    circ.h(j)
                    #print("h",j)
                    temp = j
                else:
                    if(temp != j):
                        circ.cx(temp, j)
                        #print("cnot",temp,j)
    return

#The general rule for adding gates is alternating between H and CNOT's, no matter what color
def add_gate(pos, parity):
    global qubit
    global temp
    #print(state_index(pos))
    tup = state_index(pos)
    if(tup not in locations):#First we check whether the selected qubit is already in the circuit
        #print("New location")
        locations.append(tup)
        if(abs(get_state(tup))==1):#Initialize down states opposite for red and blue
            circ.x(qubit)
            #print("not",qubit)
        if(get_state(tup)==0):#Apply H to 0 as a boundary condition
            circ.h(qubit)
            #print("hb",qubit)
        if(parity%2==0):#Even selected qubits get H gate, and the qubit number is stored for the next CNOT
            circ.h(qubit)
            #print("h",qubit)
            temp = qubit
        else:#Odd selected qubits get CNOT gate
            circ.cx(temp,qubit)
            #print("cnot",temp,qubit)
        qubit = qubit + 1
    else:#If the selected qubit was already in the circuit, this find's it's index and adds another gate
        for j in range(qubit):
            if(tup==locations[j]):
                if(parity%2==0):
                    circ.h(j)
                    #print("h",j)
                    temp = j
                else:
                    if(temp != j):
                        circ.cx(temp, j)
                        #print("cnot",temp,j)

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
pastWins = [[],[]]

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

captureSound = load_sound("capture.wav")
placementSound = load_sound("placement.mp3")

score = [0,0]
clock = pg.time.Clock()

#TODO: Initialize game parameters in settings

P1_sprites = pg.sprite.Group()  # Create a sprite group for P1
P2_sprites = pg.sprite.Group()  # Create a sprite group for P2
P_sprites = pg.sprite.Group()   # Create a sprite group to manipulate both P1 and P2 sprites for entanglement

turn = [True, False] #Determines turn order; Player 1 goes first
activateMenu = True
menuButton[1].center = (800/2, 770)
turnBox = pg.Rect(350, 0, 200, 50)
goodMove = True
total_points = [0, 0]
temp_points = [0, 0]
turnNum = 1     #Turn number will be separated from parity for the qubits
parity = 0      #Parity tracks whether qubit gets H or CNOT
settings = None #initialized in game loop (zero index = pointsToWin; first index = numPieces; second index = numEntangle)
once = True

while True: #game loop
    if activateMenu:
        settings = menu()
        points = [0, 0]
        once = True
        activateMenu = False

    if once: 
        #print(settings["numPieces"]) #TODO: delete later 
        #print(settings["pointsToWin"])
        #print(settings["numEntangle"])
        for i in range(1, settings["numPieces"]+1):
            P1Temp = load_image("P1_0.png")
            P1_sprite = pieceSprite(P1Temp[0], P1Temp[1], 30, i*75, 2)
            P1_sprites.add(P1_sprite)

            P2Temp = load_image("P2_1.png")
            P2_sprite = pieceSprite(P2Temp[0], P2Temp[1], 770, i*75, -3)
            P2_sprites.add(P2_sprite)
            P_sprites.add(P1_sprite)
            P_sprites.add(P2_sprite)

        once = False

    points[0] += temp_points[0]
    points[1] += temp_points[1]
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit(0)

        if (event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and menuButton[1].collidepoint(pg.mouse.get_pos())):
            activateMenu = True
            resetBoard(P1_sprites, P2_sprites)
            break
            
        '''
        if(turnNum == 18): #????
            qubit = 0
        '''
        
        #Handle GAME WINS!!! (Turn action 0.1 of 3) >>> CAN END THE GAME HERE
        '''
        if(any(x == settings["pointsToWin"] for x in    ))
        '''
        #Handle taking pieces away (Turn action 1 of 3)
        '''
        if(temp_points[0] > 0 or temp_points[1] > 0):
            
            for i in range(0, temp_points[0]):
                drawText(screen, "Blue: remove", (247, 227, 176), turnBox, FONT) #Communicate to player 1 to extract pieces from the board
                
            temp_points[0] = 0
            for i in range(0, temp_points[1]):
                drawText(screen, "Blue Turn", (247, 227, 176), turnBox, FONT) #Communicate to player 2 to extract pieces from the board
            temp_points[1] = 0
        '''  
            #Check for the points array being changed from the last turn
        #Handle Superpositions here (Turn action 2.1 of 3) >>> Should be done after every mill event
        
        #Handle entanglement (Turn action 2.2 of 3)
        #if(event.type == pg.MOUSEBUTTONDOWN and turnNum >= settings["numPieces"]*2+1): #TODO: change the condition to be dependent upon the number of pieces which is specified in the settings.
        #    if(turn[0]):
        #        drawText(screen, "Blue: click on two pieces to entangle them.", (247, 227, 176), turnBox, FONT)
        #
        #    elif(turn[1]):
        #        drawText(screen, "Red: click on two pieces to entangle them.")
                
        #    pos1, pos2 = handle_gate_helper([False, False], P_sprites)
            #entanglement_type = choose_entanglement() #finish this later; default to |00>+|11>
        #    handle_gate(pos1, pos2) #pos1, pos2 = position of qubits for entanglement > correlated with state array. 
                                    #entanglement_type = |00>+|11> or |10>+|01>
                                    #done = recursive variable

        #This is left click to entangle, it finds the sprite that was pressed and adds the gate.
        if(event.type == pg.MOUSEBUTTONDOWN and event.button == 3):
            pos = pg.mouse.get_pos()
            for p1 in P1_sprites.sprites():
                if p1.rect.collidepoint(pos):
                    add_gate(pos,parity)
                    parity = parity + 1
                    if(parity%2==0):
                        measure()
                    P1_sprites.draw(screen)
                    check_win()
            for p2 in P2_sprites.sprites():
                if p2.rect.collidepoint(pos):
                    add_gate(pos,parity)
                    parity = parity + 1
                    if(parity%2==0):
                        measure()
                    P2_sprites.draw(screen)
                    check_win()                     
        '''Michael code (modified to draw all sprites and to check in a shared group to allow for entanglements between P1 and P2 pieces)
                            if p.rect.collidepoint(pos):
                                add_gate(pos, turnNum) 
                                turnNum = turnNum + 1
                                if(turnNum%2==0):
                                    measure()
                                P_sprites.draw(screen)
                                check_win()'''
    
        #Handle moving pieces (Turn action 3 of 3)
        if (event.type == pg.MOUSEBUTTONDOWN and turn[0] and event.button == 1):
            pos1 = pg.mouse.get_pos()
            for i in P1_sprites.sprites(): #Check for interactions with a piece FROM PLAYER 1
                if i.rect.collidepoint(pos1):
                    movePiece = True
                    while movePiece: #Movement of piece that has been clicked on
                        for event1 in pg.event.get():
                            if(event1.type == pg.MOUSEBUTTONDOWN and event1.button == 1):
                                if(turnNum < settings["numPieces"]*2+1):
                                    #handles the initial phase; places can be placed on any unoccupied regions.
                                    tempCenter = pg.mouse.get_pos()
                                    if(canMove(tempCenter)):
                                        i.rect.center = matrixToCenter(rectToMatrix(tempCenter))
                                        set_state(state_index(tempCenter), 1)                       #Sets the state value at state_index(tempCenter) index (2 always)
                                        P1_sprites.draw(screen)
                                        check_win()                                                 #Checks for mills
                                        movePiece = False                                           #End turn
                                        turnNum += 1
                                        turn = [False, True]
                                    else: 
                                        displayBoard(board_surface, menuButton, screen, turn, turnBox, P1_sprites, P2_sprites, False)
                                else:
                                    tempCenter = pg.mouse.get_pos()
                                    boolMoves = [move == tempCenter for move in validMoves(i)]  #Check if the player did a valid move in post-initial phase
                                    once2 = False
                                    for checkValidMove in boolMoves:
                                        if(checkValidMove): 
                                            once2 = True
                                            i.rect.center = matrixToCenter(rectToMatrix(tempCenter))
                                            set_state(state_index(tempCenter, i.value))             #Sets the state value at state_index(tempCenter) to piece1.value
                                            P1_sprites.draw(screen)
                                            check_win()
                                            movePiece = False
                                            turnNum += 1
                                            turn = [False, True]
                                            break
                                    if(once2 != True):
                                        displayBoard(board_surface, menuButton, screen, turn, turnBox, P1_sprites, P2_sprites, False)

        elif (event.type == pg.MOUSEBUTTONDOWN and turn[1] and event.button == 1):            #Event for player 2 clicking the left mouse button
            pos1 = pg.mouse.get_pos()                                                         #MOUSE VARIABLE                                                                           
            for j in P2_sprites.sprites():
                if j.rect.collidepoint(pos1):                                                 #Use MOUSE VARIABLE to check if player 2 has clicked on a piece
                    movePiece = True
                    while movePiece:
                        for event1 in pg.event.get():
                            if(event1.type == pg.MOUSEBUTTONDOWN and event1.button == 1):
                                if(turnNum < settings["numPieces"]*2+1):                                             #Track the initial phase based on turn number
                                    tempCenter = pg.mouse.get_pos()
                                    if(canMove(tempCenter)):
                                        j.rect.center = matrixToCenter(rectToMatrix(tempCenter))
                                        set_state(state_index(tempCenter), -2)                 #Sets the state value at state_index(tempCenter) index (-3 always)
                                        P2_sprites.draw(screen)
                                        check_win()
                                        movePiece = False
                                        turnNum += 1
                                        turn = [True, False]
                                    else: 
                                        displayBoard(board_surface, menuButton, screen, turn, turnBox, P1_sprites, P2_sprites, False)
                                else: 
                                    tempCenter = pg.mouse.get_pos()
                                    boolMoves = [move == tempCenter for move in validMoves(i)]  #Check if the player did a valid move in post-initial phase
                                    once2 = False
                                    for checkValidMove in boolMoves:
                                        if(checkValidMove): 
                                            once2 = True
                                            j.rect.center = matrixToCenter(rectToMatrix(tempCenter))
                                            set_state(state_index(tempCenter, j.value))       #Sets the state value at state_index(tempCenter) index to piece2.value
                                            P2_sprites.draw(screen)
                                            check_win()
                                            movePiece = False
                                            turnNum += 1
                                            turn = [True, False]
                                            break
                                    if(once2 != True):
                                        displayBoard(board_surface, menuButton, screen, turn, turnBox, P1_sprites, P2_sprites, False)

    displayBoard(board_surface, menuButton, screen, turn, turnBox, P1_sprites, P2_sprites, True)
    clock.tick(20)
