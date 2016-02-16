"""+==========================+========-========*========-========+==========================+
   ||                         WRITING AN AI FOR THE GAME OF OTHELLO                         ||
   ||       (For an electronic copy, go to http://academics.tjhsst.edu/compsci/ai/.)        ||
   ||                           by M. Stueben (December 19, 2012)                           ||
   +==========================+========-========*========-========+==========================+

                   QUESTION: How should computer code be written?
                   ANSWER: So that others can read it in minimal time.


ASSIGNMENT: Given a working game of Othello, write a strategy to allow the computer usually to
            choose a strong (or at least not weak) move.

THE GAME OTHELLO. Othello (aka Reversi) is a game played by two players on a board with 8 rows and 8
columns and a set of pieces that can change color during the game. The pieces (aka stones and tiles)
are white on one side and black on the other side. Players alternate placing pieces of their color
on an 8 x 8 board. The Human (BLACK) moves first vs. Computer (WHITE).

   If a row, column, or diagonal of consecutive pieces (no blanks) all of the same color becomes
flanked (touched on both sides) by two pieces of the opposite color (by a piece just played), then
the pieces in between are turned over and all become pieces of the boundary color. Hence, the
original name "Reversi." In fact, every legal move MUST turn the color of some of the opponent's
pieces. Below White makes a legal move and turns three black pieces into three white pieces.

                    ..........         ..........         ..........
                    ..BBBWBW..    -->  .WBBBWBW..    -->  .WWWWWBW..
                    ..........         ..........         ..........
                  White to move        White moves         Result

   If one of the three left-most black pieces was replaced by an empty   +----------------------+
cell, White's move would have been illegal, because no black piece      1|.  .  .  .  .  .  .  .|
would have changed color. If a player cannot legally move, he or she    2|.  .  .  .  .  .  .  .|
must  pass the move to the opponent. The game ends when neither         3|.  .  .  =  .  .  .  .|
player can legally move. This usually occurs because the board fills    4|.  .  =  W  B  .  .  .|
up.                                                                     5|.  .  .  B  W  =  .  .|
                                                                        6|.  .  .  .  =  .  .  .|
   Othello has a fixed starting position, but Reversi does not. See     7|.  .  .  .  .  .  .  .|
diagram. Reversi layers use a common pool of 64 pieces, but each        8|.  .  .  .  .  .  .  .|
Othello player has his own pile of 32 pieces. If an Othello player       +----------------------+
plays his final piece--his opponent having passed he move on several      a  b  c  d  e  f  g  h
occasions--his opponent can finish making legal moves anyway he wants.
Othello is copyrighted (1973), Reversi (invented prior to 1886) is not. Otherwise the games are
identical.

   In the above diagram, it is always Black to make his first move. Since a legal move must bound
consecutive pieces of the opposite color, Black has only four legal moves: c4, d3, e6, and f5. These
positions are indicated by equal signs. In fact, these four moves all lead to the same geometric
position either mirrored, or rotated 180 degrees, or both. So Black's first move is already known by
his opponent.

   Traditionally, and required for this assignment, the board is dark green and the pieces are
circles of black and white. The background will be GREY30 (not the British "GRAY.") I will save you
some time by giving you a working game in this handout.

ASSIGNMENT AGAIN: Your job is to write a strategy for the computer's moves. In particular, write the
makeComputerReply2() function, and then remove the 2 in the function name. (But change the name of
the other function to avoid two functions of the same name.) My makeComputerReply() has a simple
strategy. It always grabs a corner if possible. If not possible it chooses a cell that maximizes the
pieces to be turned over. See Wikipedia for more details about the game and some simple strategy.
Try to make your strategy almost unbeatable by beginners. Shouldn't there be some advice on how to
do this on the Internet? For some reason I never looked.

   Here is a common (and good) idea. For each candidate computer move, find the best human reply and
subtract the human's gain from the computer's gain. Then choose the computer move that maximizes
this difference. If looking two moves forward is a good idea, why not look four moves forward? The
answer is that the computer will likely take too much time to calculate a move. Although I have not
tried this. This look-ahead strategy is not the only strategy one can use. And the look-ahead
strategy might be combined with other tricks to make it even stronger. For instance, some squares
are generally to be avoided, no matter how many pieces get turned over. Other squares--like the
corners--are generally to be taken when possible, even if you turn over only one piece. What are
these other good squares? What are the almost-always bad squares? Thinking this out is part of the
assignment. Good luck.

P.S. 1) The command exit() seems to cause errors in Tk graphics.
     2) Tk commands with syntax errors often do NOT stop the program from running.
"""
#########################################<START OF PROGRAM>#########################################
def setUpCanvas(root): # These are the REQUIRED magic lines to enter graphics mode.
    root.title("A Tk/Python Graphics Program") # Your screen size may be different from 1270 x 780.
    canvas = Canvas(root, width = 1270, height = 780, bg = 'GREY30')
    canvas.pack(expand = YES, fill = BOTH)
    return canvas
#---------------------------------------------------------------------------------------------------

def createMatrix(): # = the initial position, with Black = 1, and white = -1.
    M = [ [0, 0, 0, 0, 0, 0, 0, 0,],
          [0, 0, 0, 0, 0, 0, 0, 0,],
          [0, 0, 0, 0, 0, 0, 0, 0,],
          [0, 0, 0,-1, 1, 0, 0, 0,], # The matrix M is global.
          [0, 0, 0, 1,-1, 0, 0, 0,],
          [0, 0, 0, 0, 0, 0, 0, 0,],
          [0, 0, 0, 0, 0, 0, 0, 0,],
          [0, 0, 0, 0, 0, 0, 0, 0,],]

##    M = [ [ 0, 1, 0, 0, 1, 0, 0, 1,], # Practice matrix 1
##          [ 0, 0,-1, 0,-1, 0,-1, 0,],
##          [ 0, 0, 0,-1,-1,-1, 0, 0,],
##          [ 1,-1,-1,-1, 0,-1,-1, 1,],
##          [ 0, 0, 0,-1,-1,-1, 0, 0,],
##          [ 0, 0,-1, 0,-1, 0,-1, 0,],
##          [ 0,-1, 0, 0,-1, 0, 0, 1,],
##          [ 1, 0, 0, 0, 1, 0,-1, 1,],]

##    M = [ [1, 1, 1, 1, 1, 1, 1, 0,], # Practice matrix 2
##          [1, 1, 1, 1, 1, 1,-1, 1,],
##          [0, 1,-1, 1, 1, 1, 1, 1,],
##          [1, 1, 1, 1, 1, 1, 1, 1,],
##          [0, 1, 1, 1, 1, 1,-1, 1,],
##          [1, 1, 1, 1, 1,-1, 1, 1,],
##          [1,-1, 1, 1, 1, 1, 1, 1,],
##          [0, 1, 1, 1, 1, 1, 1, 0,],]

    return M
#---------------------------------------------------------------------------------------------------

def copyMatrixToScreen():
    ch = chr(9679) # = a solid disk shape
    canvas.create_text(30,30, text="x", fill = 'BLACK', font = ('Helvetica',1))
    for r in range (8):
       for c in range (8):
        if M[r][c] ==  1:
           sx = c*70 + 85
           sy = r*70 + 99
           canvas.create_text(sx, sy, text = ch, fill = 'BLACK', font = ('Helvetica', 90, 'bold') )
        if M[r][c] == -1:
           sx = c*70 + 85
           sy = r*70 + 99
           canvas.create_text(sx, sy, text = ch, fill = 'WHITE', font = ('Helvetica', 90, 'bold') )
    canvas.update()
#---------------------------------------------------------------------------------------------------

def copyOldBoardToScreenInMiniturizedForm(cc, rr):
 #--erase previous miniture board
    canvas.create_rectangle(650, 400, 821, 567, width = 5, fill    = 'GREY30')
    ch = chr(9679)
    for r in range (8):
       for c in range (8):
        sx = c*20 + 665
        sy = r*20 + 412
        if M[r][c] ==  1:
           canvas.create_text(sx, sy, text = ch, fill = 'BLACK', font = ('Helvetica', 20, 'bold') )
        if M[r][c] == -1:
           canvas.create_text(sx, sy, text = ch, fill = 'WHITE', font = ('Helvetica', 20, 'bold') )

    canvas.create_text(cc*20 + 665, rr*20 + 413, text = 'B', fill = 'BLACK', \
                             font = ('Helvetica', 9, 'bold') )
    canvas.update()      # make all previous changes to the canvas
#---------------------------------------------------------------------------------------------------

def score(): # returns the number of black and white disks.
    whiteTotal = 0; blackTotal = 0
    for r in range(8):
      for c in range (8):
        if M[r][c] ==  1: blackTotal += 1
        if M[r][c] == -1: whiteTotal += 1
    return (blackTotal, whiteTotal)
#---------------------------------------------------------------------------------------------------

def printMatrix(M, msg = "Matrix M:"): # <-- Useful for debugging.
    print("\n", msg)
    print ("     0  1  2  3  4  5  6  7")
    print ("  +--------------------------+")
    for r in range(8):
      print (r, "|", end = "")
      for c in range (8):
         if M[r][c] == 1: ch = '#'
         if M[r][c] ==-1: ch = 'O'
         if M[r][c] == 0: ch = '-'
         print ("%3s"%ch, end = "")
      print ("  |")
    print ("  +--------------------------+")
    print ("   human    = # = BLACK  =  1 ")
    print ("   computer = O = WHITE  = -1 ")
#---------------------------------------------------------------------------------------------------

def LocateTurnedPieces(r, c, player): # The pieces turned over are of -player's color
    if M[r][c] != 0: return []  # A zero in a matrix M cell means an empty cell.
    totalFlipped =   []
 #--case 1 (move right)
    flipped = []
    if c < 6 and M[r][c+1] == -player:
        for n in range(1, 9):
            if c+n > 7 or M[r][c+n] == 0:
                flipped = []
                break
            if M[r][c+n] == player: break
            flipped += ((r,c+n,),)
    totalFlipped += flipped

 #--case 2 (move down)
    flipped = []
    if r < 6 and M[r+1][c] == -player:
        for n in range(1, 9):
            if r+n > 7 or M[r+n][c] == 0:
                flipped = []
                break
            if M[r+n][c] == player: break
            flipped += ((r+n,c,),)
    totalFlipped += flipped

 #--case 3 (move up)
    flipped = []
    if r > 1 and M[r-1][c  ] == -player:
        for n in range(1, 9):
            if r-n < 0 or M[r-n][c] == 0:
                flipped = []
                break
            if M[r-n][c] == player: break
            flipped += ((r-n,c,),)
    totalFlipped += flipped

 #--case 4 (move left)
    flipped = []
    if c > 1 and M[r][c-1] == -player:
        for n in range(1, 9):
            if c-n < 0 or M[r][c-n] == 0:
                flipped = []
                break
            if M[r][c-n] == player: break
            flipped += ((r,c-n,),)
    totalFlipped += flipped

 #--case 5 (move down and right)
    flipped = []
    if r < 6 and c < 6 and M[r+1][c+1] == -player:
        for n in range(1, 9):
            if (r+n) > 7 or (c+n) > 7 or M[r+n][c+n] == 0:
                flipped = []
                break
            if M[r+n][c+n] == player: break
            flipped += ((r+n,c+n,),)
    totalFlipped += flipped

 #--case 6 (move up and left)
    flipped = []
    if r > 0 and c > 0 and M[r-1][c-1] == -player:
        for n in range(1, 9):
            if (r-n) < 0 or (c-n) < 0 or M[r-n][c-n] == 0:
                flipped = []
                break
            if M[r-n][c-n] == player: break
            flipped += ((r-n,c-n,),)
    totalFlipped += flipped

#--case 7 (move up and right)
    flipped = []
    if r > 1 and c < 6 and M[r-1][c+1] == -player:
        for n in range(1, 9):
            if (r-n) < 0 or (c+n) > 7 or M[r-n][c+n] == 0:
                flipped = []
                break
            if M[r-n][c+n] == player: break
            flipped += ((r-n,c+n,),)
    totalFlipped += flipped

 #--case 8 (move down and left)
    flipped = []
    if r < 6 and c > 1 and M[r+1][c-1] == -player:
        for n in range(1, 9):
            if (r+n) > 7 or (c-n) < 0 or M[r+n][c-n] == 0:
                flipped = []
                break
            if M[r+n][c-n] == player: break
            flipped += ((r+n,c-n,),)
    totalFlipped += flipped

    return totalFlipped
#---------------------------------------------------------------------------------------------------

def setUpInitialBoard(canvas):
    global M; ch = chr(9679)

 #--print title
    canvas.create_text(330, 50, text = "OTHELLO with AI", \
                       fill = 'WHITE',  font = ('Helvetica', 20, 'bold'))
 #--print directions
    stng = "DIRECTIONS:\n1) Black (human) moves first. Click on any unoccupied cell.\n\
2) If a player cannot move, play passes to the opponent. \n3) Game ends when \
no legal move is possible.\n4) The player with the most colors on the board \
wins.\n5) A legal move MUST cause some pieces to turn color."
    canvas.create_text(810, 100, text = stng,  \
                       fill = 'WHITE',  font = ('Helvetica', 10, 'bold'))
 #--draw outer box, with red border
    canvas.create_rectangle(50, 70, 610,630, width = 1, fill    = 'DARKGREEN')
    canvas.create_rectangle(47, 67, 612,632, width = 5, outline = 'RED'  )

 #--Draw 7 horizontal and 7 vertical lines to make the cells
    for n in range (1, 8): # draw horizontal lines
       canvas.create_line(50, 70+70*n, 610, 70+70*n, width = 2, fill = 'BLACK')
    for n in range (1, 8):# draw vertical lines
       canvas.create_line(50+70*n,  70, 50+70*n, 630, width = 2, fill = 'BLACK')

 #--Place letters at bottom
    tab = " " * 7
    stng = 'a' + tab + 'b' + tab + 'c' + tab + 'd' + tab + 'e' + \
                 tab + 'f' + tab + 'g' + tab + 'h'
    canvas.create_text(325, 647, text = stng, fill = 'DARKBLUE',  font = ('Helvetica', 20, 'bold'))

 #--Place digits on left side
    for n in range (1,9):
        canvas.create_text(30, 35 + n * 70, text = str(n),
                       fill = 'DARKBLUE',  font = ('Helvetica', 20, 'bold'))

 #--copy matrix to screen.
    copyMatrixToScreen()

 #--Place score on screen
##    canvas.create_rectangle(800, 200, 960,350, width = 5, fill    = 'GREY30')
    (BLACK, WHITE) = score()
    stng = 'BLACK = ' + str(BLACK) + '\nWHITE  = ' + str(WHITE)
    canvas.create_text(800, 200, text = stng, fill = 'WHITE',  font = ('Helvetica', 20, 'bold'))
    stng = "Suggested reply (col, row): (c, 4)"
    canvas.create_text     (755,350,text = stng, fill = 'GREEN',  font = ('Helvetica', 10, 'bold'))
#---------------------------------------------------------------------------------------------------

def illegalClick(x, y):
    player = 1 # player = Black
    if x < 52 or x > 609:
        print("Error 1. Mouse is to left or right of board.")
        return True # = mouse position is off the board

    if y < 62 or y > 632:
        print("Error 2.Mouse is above or below the board.")
        return True # = mouse position is off the board

 #--Calculate matrix position
    c = (x-50)//70
    r = (y-70)//70

    if M[r][c] != 0:
        print("ERROR 3: Cell is occupied at r =", r, " c =", c)
        return True      # = cell is occupied

 #--Not next to cell of opposite color
    flag = 0
    if c < 7 and           M[r  ][c+1] == -player: return False
    if r < 7 and           M[r+1][c  ] == -player: return False
    if r > 0 and           M[r-1][c  ] == -player: return False
    if c > 0 and           M[r  ][c-1] == -player: return False
    if r < 7 and c < 7 and M[r+1][c+1] == -player: return False
    if r > 0 and c > 0 and M[r-1][c-1] == -player: return False
    if r > 0 and c < 7 and M[r-1][c+1] == -player: return False
    if r < 7 and c > 0 and M[r+1][c-1] == -player: return False
    print("ERROR 4: no opposite colored neighbors at r =", r, " c =", c)
    return True # = illegal move
#---------------------------------------------------------------------------------------------------

def legalMove(player):
    print('LEGAL MOVE NOW BEING CHECKED.') # <--Used only for debugging.
    pieces = []
    for r in range(8):
        for c in range(8):
           pieces += LocateTurnedPieces(r, c, player)
           if pieces != []: break
        if pieces != []: break
    if pieces ==[]:
       person = 'WHITE'
       if player == 1: person = 'BLACK'
       stng = 'There is no legal move for ' + person
       canvas.create_rectangle(655,260,957,307, width = 0, fill = 'GREY30')
       canvas.create_text     (800,280,text = stng, fill = 'RED',  font = ('Helvetica', 10, 'bold'))
       return False
    return True
#---------------------------------------------------------------------------------------------------

def printBestPotentialReply(player): # <--Optional feature
    printMatrix(M)

#-- Search for the BEST (flips the most pieces) reply move.
    max = 0; # max = the most filpped pieces obtained by a future move in the position.
    r = -1; c = -1
    for r in range(8):
        for c in range(8):
            if M[r][c] == 0:
               LL = len(LocateTurnedPieces(r, c, -player)) # = the number of to-be-flipped pieces.
               if LL > max:
                  max = LL
                  x   = c
                  y   = r

 #--print best reply on screen.
    canvas.create_rectangle(650, 330, 930, 390, width = 0, fill = 'GREY30')
    if max == 0:
          stng = "NO LEGAL MOVE FOUND."
    else: stng = "Suggested reply (col, row): ("+ chr(x+97)+ ", "+ str(y+1)+ ") = "+ \
                  str(max) +" piece(s)"
    canvas.create_text (790, 350, text = stng, fill = 'GREEN',  font = ('Helvetica', 10, 'bold'))
#---------------------------------------------------------------------------------------------------

def makeMove(c, r, pieces, player):
    global M

 #--make the player's legal move in matrix
    M[r][c] = player

 #--flip pieces to same color as the player
    for elt in pieces:
        M[elt[0]][elt[1]] = player

#--update the screen
    copyMatrixToScreen()

 #--erase old score and previous move
    canvas.create_rectangle(650, 160,960,310, width = 5, fill    = 'GREY30')

 #--print new score
    (BLACK, WHITE) = score()
    stng = 'BLACK = ' + str(BLACK) + '\nWHITE  = ' + str(WHITE)
    canvas.create_text(800, 200, text = stng, \
                       fill = 'WHITE',  font = ('Helvetica', 20, 'bold'))

 #--print previous move on miniture board
    position = "previous move: "+ str(chr(c + 97))+str(r+1)
    canvas.create_text(800, 250, text = position, \
                       fill = 'WHITE',  font = ('Helvetica', 20, 'bold'))

    if player == computer:
       canvas.create_text(c*20 + 665, r*20 + 413, text = 'W', fill = 'WHITE', \
                             font = ('Helvetica', 9, 'bold') )
#---------------------------------------------------------------------------------------------------

def quit():
    canvas.create_text(330, 350, text = "GAME OVER", \
                       fill = 'RED',  font = ('Helvetica', 40, 'bold'))
    stng = 'THERE ARE NO LEGAL MOVES FOR EITHER PLAYER.'
    canvas.create_rectangle(655, 260, 955, 300, width = 0, fill = 'GREY30')
    canvas.create_text(805, 280, text = stng, fill = 'GOLD',  font = ('Helvetica', 9, 'bold'))
#---------------------------------------------------------------------------------------------------

def makeComputerReply2(): # <--THIS IS THE KEY FUNCTION YOU MUST REWRITE IN THE NEXT FUNCTION.
 #--Move into upper left corner (0,0) if possible.
    pieces = LocateTurnedPieces (0, 0, computer)
    if pieces != []:
       makeMove(0, 0, pieces, computer)
       printBestPotentialReply(computer) # <--Optional feature
       return

 #--Move into lower right corner (7,7) if possible.
    pieces = LocateTurnedPieces(7, 7, computer)
    if pieces != []:
       makeMove(7, 7, pieces, computer)
       printBestPotentialReply(computer) # <--Optional feature
       return

 #--Move into lower left corner (0,7) if possible.
    pieces = LocateTurnedPieces(0, 7, computer)
    if pieces != []:
       makeMove(7, 0, pieces, computer)
       printBestPotentialReply(computer) # <--Optional feature
       return

 #--Move into upper right corner (7,0) if possible.
    pieces = LocateTurnedPieces(7, 0, computer)
    if pieces != []:
       makeMove(0, 7, pieces, computer)
       printBestPotentialReply(computer) # <--Optional feature
       return

#--Make a move that turns over the maximum number of pieces.
    max = 0
    for r in range(8):
        for c in range(8):
           if M[r][c] == 0:
              pieces = LocateTurnedPieces(r, c, computer)
              L = len(pieces)
              if L > max:
                 finalPieces = pieces
                 x = c
                 y = r
                 max = L
    makeMove(x, y, finalPieces, computer)
    printBestPotentialReply(computer) # <--Optional feature
#---------------------------------------------------------------------------------------------------

def makeComputerReply():
    P = [ [10, 1, 6, 6, 6, 6, 1, 10,],
          [ 1, 1, 2, 2, 2, 2, 1, 1,],
          [ 6, 2, 4, 4, 4, 4, 2, 6,],
          [ 6, 2, 4, 0, 0, 4, 2, 6,], # The matrix M is global.
          [ 6, 2, 4, 0, 0, 4, 2, 6,],
          [ 6, 2, 4, 4, 4, 4, 2, 6,],
          [ 1, 1, 2, 2, 2, 2, 2, 1,],
          [10, 1, 6, 6, 6, 6, 1,10,],]
    #--Make a move that turns over the maximum number of pieces.
    max = 0
    for r in range(8):
        for c in range(8):
           if M[r][c] == 0:
              pieces = LocateTurnedPieces(r, c, computer)
              if len(pieces) != 0:
                print(r,' ', c)
                badMove(r,c)
                L = len(pieces) + P[r][c]
                if L > max:
                    finalPieces = pieces
                    x = c
                    y = r
                    max = L
    makeMove(x, y, finalPieces, computer)
    printBestPotentialReply(computer) # <--Optional feature
    # Place your AI here. Remove the 2 in the name and append it to the previous function.
#---------------------------------------------------------------------------------------------------
def badMove(x,y):
    horiz = horizontalCheck(x,y)
    print('Horiz: ', horiz)
    vert = verticalCheck(x,y)
    print('Vert: ', vert)
    dia1 = diagonal1Check(x,y)
    dia2 = diagonal2Check(x,y)
    return horiz and vert and dia1 and dia2
#---------------------------------------------------------------------------------------------------
def horizontalCheck(x,y):
    side1 = True
    side2 = True
    for i in range(y, 8):
        if M[x][i] == 0 and i != y:
           # print('sdfs',i)
            break
        elif M[x][i] == 1:
            side1 = False
           # print('sasss',i)
            break
    for i in range(y,0):
        print(i)
        if M[x][i] == 0 and i != y:
            break
        elif M[x][i] == 1:
            side2 = False
            break
    if side1 and M[x][7] == -1:
        return True
    elif side2 and M[x][0] == -1:
        return True
    elif (side1 and side2) or (side1 == True and side2 == False) or (side1 == False and side2 == True):
        return True
    else: return False
def verticalCheck(x,y):
    side1 = True
    side2 = True
    for i in range(x, 8):
        if M[i][y] == 0 and i != x:
            #print('sdfs',i)
            break
        elif M[i][y] == 1:
            side1 = False
           # print('sasss',i)
            break
    for i in range(x,0):
        print(i)
        if M[i][y] == 0 and i != x:
            break
        elif M[i][y] == 1:
            side2 = False
            break
    if side1 and M[7][y] == -1:
        return True
    elif side2 and M[0][y] == -1:
        return True
    elif (side1 and side2) or (side1 == True and side2 == False) or (side1 == False and side2 == True):
        return True
    else: return False
def diagonal1Check(x,y):
    side1 = True
    side2 = True

def diagonal2Check(x,y):
    pass
#---------------------------------------------------------------------------------------------------

def click(evt): # Human (= 1 = Black) legal move is guaranteed to exist.
 #--If move is off board, or cell full, or no opp. neighbor, then CLICK AGAIN.
    if illegalClick(evt.x, evt.y):
        canvas.create_rectangle(660, 270, 940,300, width = 0, fill = 'GREY30')
        stng = 'Your last mouse click was an ILLEGAL MOVE.'
        canvas.create_text(800, 280, text = stng, fill = 'RED',  font = ('Helvetica', 9, 'bold'))
        return

 #--Find matrix coordinates (c,r) in terms of mouse coordinates (evt.x, evt.y).
    c = (evt.x-50)//70
    r = (evt.y-70)//70
    print('Mouse screen coordinates =', c,r)

 #--if none of the computer's pieces will be turned, then CLICK AGAIN.
    pieces     = LocateTurnedPieces(r, c, human)
    if pieces == []:
       canvas.create_rectangle(660, 270, 940,300, width = 0, fill = 'GREY30')
       stng = 'Your last mouse click did NOT turn a piece.'
       canvas.create_text(800, 280, text = stng, fill = 'ORANGE',  font = ('Helvetica', 9, 'bold'))
       return

 #--Make human move(s) and computer reply/replies.
    copyOldBoardToScreenInMiniturizedForm(c,r)
    makeMove(c, r, pieces, human)
    canvas.create_rectangle(655, 330, 870,370, width = 0, fill = 'grey30')
    if legalMove(human) and not legalMove(computer): return

 #--Make computer reply/replies (1 = BLACK = human, -1 = computer = WHITE)
    if legalMove(computer): makeComputerReply() # <--This is the computer's strategy (IMPORTANT!).
    while legalMove(computer) and not legalMove(human):
        makeComputerReply()

    if not legalMove(human) and not legalMove(computer): quit()
 #-- Note: legal move for human must now necessarily exist.
    return

#==============================<GLOBAL CONSTANTS and GLOBAL IMPORTS>================================
# Global Variables should be avoided. But in Python this is impossible with graphics.
from tkinter  import *   # <-- Use Tkinter in Python 2.x
root     =  Tk()
canvas   =  setUpCanvas(root)
M        =  createMatrix()
human    =  1 # = Black
computer = -1 # = White
#===============================================<MAIN>==============================================

def main():
    global root, canvas
    root.bind('<Button-1>', click)
    setUpInitialBoard(canvas)
    root.mainloop()
#---------------------------------------------------------------------------------------------------
if __name__ == '__main__':  main()
