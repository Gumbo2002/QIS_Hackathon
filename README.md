# QIS_Hackathon : Quantum Nine Men Morris

Write how the game is supposed to work in here, as well as how to run the application. A good software project has good documentation.
###TODO: 
**NOTE: Claim a task before you do it by updating the readme**
1. Fix sprite issue; only one sprite is initialized thus only displaying one piece.
   '''
   P1_sprites = pg.sprite.Group()
   P2_sprites = pg.sprite.Group()
   for i in range(9):
       P1_sprites.add(pieceSprite(P1_1[0].convert(), P1_1[1], 30, i*75, 1))
       P2_sprites.add(pieceSprite(P2_0[0].convert(), P2_0[1], 770, i*75, 0))
   '''
2. Fix drag and drop method for placing pieces on the board through one of three methods: scrap for different method (click on piece -> click on available space) or encode for snapping piece to unoccupied and legal spot on board (refer to checkMove method for relevant coordinates; look at rules section for legality based on phase of game) AND animating piece motion.
   '''
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
   '''
3. Integrate quantum program, **CircuitBuilder.py**, into the main program **NMMBoard.py**. This should be done in the following ways: upon the end of a turn, AFTER THE INITIAL PLACEMENT PHASE, all pieces for P1 or P2, depending on the turn, should be put into the |0> or |1> state. This is done with the **CircuitBuilder.py** program in a call from the **NMMBoard.py** program. the **CircuitBuilder.py** program then returns the *Classical Register* to the **NMMBoard.py** program with the indices of the array corresponding to pieces from either player. Thus, there are three objectives: find a way to, upon placement of a piece from P1 or P2, correlate that piece to a corresponding qubit FOR THE ENTIRE GAME **AND** Represent sprite visuals dynamically (switch between |0>, |1>, and Hadamard states depending on qubit state) **AND**
   
4. Encode for a mill or three pieces in a row. This involves not only detecting the mill but also handling for the player who scored to take an opponent's piece off of the board.
   
5. **MAKE GATE SPRITES AND THEIR FUNCTIONALITY WITH RESPECT TO CircuitBuilder.py**

### Game board
 
### Rules

### Running the application
```
python3 NMMBoard.py ?
```
