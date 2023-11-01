import pygame as pg
import numpy as np

#functions to determine valid moves for any chosen piece

            #y denotes the row we work with, x denotes the element in y
positions = [[0, 9, 9, 0, 9, 9, 0],
             [9, 0, 9, 0, 9, 0, 9], #0 = empty
             [9, 9, 0, 0, 0, 9, 9], #1 = white
             [0, 0, 0, 9, 0, 0, 0], #2 = black
             [9, 9, 0, 0, 0, 9, 9], #else = invalid space
             [9, 0, 9, 0, 9, 0, 9],
             [0, 9, 9, 0, 9, 9, 0]]

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
    x, y = (int) (cent[0]/100)-1, (int) (cent[1]/100)-1
    return (x, y)

#Converts matrix coords to rect coords
def matrixToCenter(x, y):
    centX, centY = (x+1)*100, (y+1)*100
    return (centX, centY)

textBox = pg.Rect(50, 50, 650, 650)
textBox.center = (500, 400)
print(validMoves(textBox))