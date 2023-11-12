# QIS_Hackathon : Nine Qubit Morris
Nine Qubit Morris is a pygame based application based on the classical game of Nine Men Morris. The differences lie in how the pieces are treated as quantum objects allowing for quantum phenomena to change how players score points. Additionally, other rules are made variable to allow for players to player longer or shorter games with different rules for manipulating the qubit pieces.

### Game board
![Game board](/data/canvas.png)

### Pieces
INCLUDE PICTURES OF THE PIECES AND EXPLAIN HOW THEY WORK

### Rules
Controls required: 
- Mouse
- Computer capable of running python programs

Conventionally, Nine Men Morris rules are as follows: 
1_0.    Each player starts in an initial phase with nine marbles which they can place on the board at any unoccoupied position. 
1_1.    During this phase, it is possible to **score** by placing three of your marbles in a row, known colloquially as a **MILL**.
1_2.    A mill allows players to remove an opponents piece from the board. **THE GOAL** of the game is to remove enough pieces from the board until your opponent cannot form a **MILL**
1_3.    This initial phase ends after all pieces are on the board.
2_0.    The second phase consists of players moving marbles around the board to attempt to form more **MILLS**. Mills cannot be formed on the same row or column twice per player.
3_0.    After enough points have been scored so as to leave the opponent unable to score a **MILL** or your opponent is unable to move a piece, you win!

The difference between Nine Men Morris and Nine Qubit Morris lies within how turns are played out:
1-1_3. Same rules, but **MILLS** must be formed from pieces that are both belonging to a player AND in the same spin state (1 or 0).
1_4.   The game starts with each player having pieces either totally in the 1 or 0 state. There is also a superposition state that players cannot score off of.
2_0.   Each turn has extra rules:
2_1.   At the beginning of a turn, both players can remove pieces depending on whether the qubits collapsed favorably to form a **MILL**. 
2_2.   Then, players are allowed to entangle any piece on the board. This will place those qubits into a bell state instantaneously thus collapsing them.
2_3.   Upon the formation of a **MILL**, all qubits will be put into a superposition and the entanglements will be cleared from the board.
3_0.   After a set amount of points is reached, specified within the settings, the game will be over.

### Running the application
After downloading the master branch, in a terminal, type:
```
python3 NMMBoard.py
```
or 
```
python NMMBoard.py
```
OR run the file in an IDE.

This will open a menu with three options, "Play", "Rules", and "Settings". 

Clicking on Settings allows you to adjust relevant parameters: pointsToWin, numPieces, and numEntangle. the first parameter controls the number of points needed to force a game win. The number of pieces allows players to play with 3-9 pieces depending on preference. the final parameter controls how many qubits can be entangled with the maximum number being 8. 

Click on rules to display the rules within the game.

Clicking on play starts a game! Make sure to sit down with a friend and enjoy!

### DISCLAIMER
The game is not in working order. The current issues are: 
- inability to entangle
- inability to check score
- inability to move pieces around board POST-initial phase
- inability to measure qubits and change states

Project is still under development...
