import copy as Copy
class Game(): #Game controls values(modes, checkmate, winners)
    def __init__(self):
        self.total_moves = 0 #counts the total number of moves
        self.upgrade = None #Upgrade is possible or not
        self.var_check = 0 #check for which side,
        self.variable_checkmate = 0 #checks which side is in checkmate
        #display purposes
        self.alpha_coord = ["A","B","C","D","E","F","G","H"]
        #display purposes
        self.num_coord = [1,2,3,4,5,6,7,8]
        #game mode
        self.mode = 0
        #game board
        self.board = [[None,None,None,None,None,None,None,None]for n in range(8)]
        #Current player move
        self.player = 2
        #Stores the current player move when upgrading
        self.stored = 0
        #The winner text
        self.winner_string = None
        #The name the player enters
        self.name = ''
        #Whether or not the user has finished typing in their name, to submit
        self.entered = False
        #Stores history of all the players
        self.players = []
        #Stores history of all scores
        self.player_high = []
        #Highlighted piece
        self.highlight = None
        #calc value of 1 cause the game to run the calc_mvoes function once
        self.calc = 1
        #Whether or not its in check, checkmate or stalemate
        self.status = None
   
    #Method used to calculate the possible moves of each piece across the board
    def calculate_moves(self,board):
        for m in range(len(board)):
            for n in board[m]:
                if n != None:
                    #Calculates moves based on type which then calls specific method to choose moves
                    n.moves = []
                    n.in_path = []
                    if n.type == "pawn":
                        n.pawn(board)
                    if n.type == "bishop":
                        n.bishop(board)
                    if n.type == "rook":
                        n.rook(board)
                    if n.type == "knight":
                        n.knight(board)
                    if n.type == "queen":
                        n.queen(board)
                    if n.type == "king":
                        n.king(board)
                        
    #check if the king is going to get checked
    def checkmate(self,board):
        for y in range (len(board)):
            for x in board[y]:
                if x != None:
                    for (dx,dy) in x.moves:
                        n = board[dy][dx]
                        if n != None and n.type == "king" and n.side != x.side:
                            if x.side != game.player:
                                #If the king has any moves left the game shows the possible moves to move without getting checked using remove_danger
                                if self.moves_left(n.side,board) != 0:
                                    game.var_check = n.side
                                    return ("Check")
                                #If either side does not have any escape options left then game is over
                                if self.moves_left(n.side,board) == 0:
                                    game.variable_checkmate = n.side
                                    return ("Checkmate")

                        
    #checks if the move is legal
    def legal_move(self,side,board):
        for y in range (len(board)):
            for x in board[y]:
                if x != None and x.side != side and len(x.moves) != 0:
                    for (dx,dy) in x.moves:
                        n = board[dy][dx]
                        if n != None and n.type == "king" and side != x.side:
                            return False
                        
    #Creates another board to see whether the move can be made with the king
    def remove_danger(self,side,board):
        tboard = Copy.deepcopy(board)
        for y in range(len(board)):
            for x in board[y]:
                if x != None and x.side == side and len(x.moves) != 0:
                    removeable_list = []
                    for (dx,dy) in x.moves:
                        #Store original move as true(x,y)
                        truex = x.x
                        truey = x.y
                        true_destination = tboard[dy][dx]
                        tboard[dy][dx] = tboard[x.y][x.x]
                        tboard[dy][dx].x = dx
                        tboard[dy][dx].y = dy
                        tboard[x.y][x.x] = None
                        self.calculate_moves(tboard)
                        if self.legal_move(side,tboard) == False:
                            removeable_list.append((dx,dy))
                        tboard[truey][truex] = tboard[dy][dx]
                        tboard[truey][truex].x = truex
                        tboard[truey][truex].y = truey
                        tboard[dy][dx] = true_destination
                    for (dx,dy) in removeable_list:
                        x.moves.remove((dx,dy))
    #Calculates the amount of legal moves that the player has left
    def moves_left(self,side,board):
        total = 0  
        for y in range(len(board)):
            for x in board[y]:
                if x != None and x.side == side:
                    for n in range(len(x.moves)):
                        total += 1
        return total
    #If illegal moves have yet to be removed and a player simply cannot move, then it is Stalemate
    def stalemate(self):
        piece_counter = 0
        move_counter1 = 0
        move_counter2 = 0
        for m in range(len(self.board)):
            for n in self.board[m]:
                if n != None:
                    piece_counter += 1
                    for x in range(len(n.moves)):
                        if n.side == 1:
                            move_counter1 += 1
                        if n.side == 2:
                            move_counter2 += 1
        #If there are two kings left then it is stalemate
        if piece_counter == 2 or move_counter1 == 0 or move_counter2 == 0:
            return True
        
    #calcutes moves
    def Move_Calculations(self):
        #RESET STATUS VARIABLE TO 0/None FOR THE NEXT CYCLE OF MOVE_CALCULATIONS
        self.status = None
        self.var_check = 0
        #First calculates moves for 'checkmate method'
        self.calculate_moves(game.board)
        self.checkmate(game.board)
        self.variable_checkmate = 0
        #ILLEGAL CASTLING(IF PLAYER IS IN CHECK THEN CANNOT CASTLE)
        self.calculate_moves(game.board)
        #REMOVES ILLEGAL MOVES
        self.remove_danger(1,game.board)
        self.remove_danger(2,game.board)
        #SETS STATUS TO 'None', 'Check' OR 'Checkmate'
        self.status = self.checkmate(game.board)
        if self.status != 'Check' and self.status != 'Checkmate':
            if self.stalemate() == True:
                self.status = "Stalemate"
        #ENDS GAME WHEN IN CM OR SM
        if self.status == "Checkmate" or self.status == "Stalemate":
            self.player = 0
        self.calc = 0
        
    #RESETS ALL INGAME VALUES(BACK TO TITLE)
    def reset(self):
        self.mode = 0
        self.board = [[None,None,None,None,None,None,None,None]for n in range(8)]
        self.player = 2
        self.stored = 0
        self.highlight = None
        self.calc = 1
        self.status = None
        self.total_moves = 0
        self.upgrade = None
        self.var_check = 0
        self.variable_checkmate = 0
        self.current_time = 0
        self.winner_string = None
        self.name = ''
        self.entered = False
        
game = Game()
 
#MASTER CLASS FOR ALL PIECES
class all():
    def __init__(self,x,y,side,type):
        self.x = x
        self.y = y
        self.side = side
        self.type = type
        self.hl = False
        self.fm = True
        self.moves = []
    #BISHOP, ROOK AND QUEEN RECURSIVE MOVEMENT PATH
    def move_br(self,x,y,cx,cy,board):
        x += cx
        y += cy
        if onboard(x,y) == False or self.no_stack((x,y)) == False:
            return
        if board[y][x] == None:
            self.moves.append((x,y))
            self.move_br(x,y,cx,cy,board)
        if board[y][x] != None:
            if board[y][x].side == self.side:
                return
            if board[y][x].side != self.side:
                self.moves.append((x,y))
                return
    #KING AND KNIGHT ITERATIVE MOVEMENT PATH
    def move_kk(self,all_pos,board): 
        for dx,dy in all_pos:
            x = self.x+dx
            y = self.y+dy
            if self.no_stack((x,y)) == False:
                return
            if onboard(x,y) != False:
                n = board[y][x]
                if n != None and n.side != self.side or n == None:
                    self.moves.append((x,y))
    def no_stack(self,x):
        if x in self.moves:
            return False
        
class pawn(all):
    #Pawn has special attribute("special_chance")
    def __init__(self,x,y,side,type):
        all.__init__(self,x,y,side,type)
        #En passant is -1 if there is no chance, if there is chance it will be the same value as total_moves
        self.special_chance = -1
    #PAWN RECURSIVE MOVEMENT PATH & EN PASSANT
    def pawn(self,board):
        #calculates all possible moves
        if self.side == 1:
            self.pawn_move(self.x,self.y,0,1,0,board)
            self.pawn_move(self.x,self.y,1,1,0,board)
            self.pawn_move(self.x,self.y,-1,1,0,board)
            #IF REQUIREMENTS ARE MET FOR EN PASSANT OPPURTUNITY THEN EN PASSANT CAN ONLY BE EXECUTED THE FOLLOWING MOVE(CHESS RULE)
            if self.special_chance == game.total_moves:
                self.en_passant(self.x,self.y,1,board)
        if self.side == 2:
            self.pawn_move(self.x,self.y,0,-1,0,board)
            self.pawn_move(self.x,self.y,1,-1,0,board)
            self.pawn_move(self.x,self.y,-1,-1,0,board)
            if self.special_chance == game.total_moves:
                self.en_passant(self.x,self.y,-1,board)
    def pawn_move(self,x,y,dx,dy,d,board):
        x += dx
        y += dy
        d += 1
        if onboard(x,y) == False or self.no_stack((x,y)) == False:
            return
        n = board[y][x]
        #DIAGONAL JUMP KILL
        if dx != 0 and dy != 0:
            if n != None and n.side != self.side:
                self.moves.append((x,y))
            return
        elif n == None:
            #FORWARD ONCE(RECURSSION)
            if d == 1:
                self.pawn_move(x,y,dx,dy,d,board)
            if d == 2 and self.fm == False:
                return
            self.moves.append((x,y))
            return
    #CHECKS FOR POSITIONING OF PAWNS AND ENEMY PAWNS
    def en_passant(self,x,y,dy,board):
        if self.side == 1 and y != 4:
            return
        if self.side == 2 and y != 3:
            return
        if board[y][x+1] != None and board[y][x+1].side != self.side:
            self.moves.append((x+1,y+dy))
        if board[y][x-1] != None and board[y][x-1].side != self.side:
            self.moves.append((x-1,y+dy))
        
class bishop(all):    
    #ALL FOUR DIRECTION PATHS
    def bishop(self,board):
        self.move_br(self.x,self.y,1,1,board)
        self.move_br(self.x,self.y,-1,1,board)
        self.move_br(self.x,self.y,1,-1,board)
        self.move_br(self.x,self.y,-1,-1,board)
        
class rook(all):
    def rook(self,board):
        self.move_br(self.x,self.y,1,0,board)
        self.move_br(self.x,self.y,-1,0,board)
        self.move_br(self.x,self.y,0,1,board)
        self.move_br(self.x,self.y,0,-1,board)
        
class knight(all):
    def knight(self,board):
        #ALL POSSIBLE MOVES FOR KNIGHT IN LIST, THEN CHECKED FOR VALIDATION
        all_pos = [(2,1),(2,-1),(-2,-1),(-2,1),(1,2),(1,-2),(-1,2),(-1,-2)]
        self.move_kk(all_pos,board)
        
class queen(all):
    #ALL 8 DIRECTION PATHS
    def queen(self,board):
        self.move_br(self.x,self.y,1,1,board)
        self.move_br(self.x,self.y,-1,1,board)
        self.move_br(self.x,self.y,1,-1,board)
        self.move_br(self.x,self.y,-1,-1,board)
        self.move_br(self.x,self.y,1,0,board)
        self.move_br(self.x,self.y,-1,0,board)
        self.move_br(self.x,self.y,0,1,board)
        self.move_br(self.x,self.y,0,-1,board)
        
class king(all):
    def king(self,board):
        all_pos = [(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,1),(1,-1),(-1,-1)]
        self.move_kk(all_pos,board)
        #IF THE PLAYER IS NOT IN CHECK AND CONDITIONS ARE MET THEN THE PLAYER CAN CASTLE
        if game.var_check != self.side:
            self.castle(self.x,self.y,board)
    def castle(self,x,y,board):
        if self.fm != True:
            return
        check = True
        #CHECK FOR EMPTY SPACES
        for n in range(1,4):
            if not onboard(x-n,y) or board[y][x-n] != None:
                check = False
        if onboard(x-4,y) and check == True:
            n = board[y][x-4]
            if n != None and n.fm == True:
                self.moves.append((x-2,y))
        check = True
        for n in range(1,3):
            if not onboard(x+n,y) or board[y][x+n] != None:
                check = False
        if onboard(x+3,y) and check == True:
            n = board[y][x+3]
            if n != None and n.fm == True:
                self.moves.append((x+2,y))
#PLACES ALL PIECES INTO STARTING POSITIONS        
def starts():
    for y in range(len(game.board)):
        for x in range(len(game.board[y])):
            pos = None
            if y == 0 or y == 1:
                side = 1
            if y == 6 or y == 7:
                side = 2
            if y == 0 or y == 7:
                if x == 2 or x == 5:
                    pos = "bishop"
                if x == 0 or x == 7:
                    pos = "rook"
                if x == 1 or x == 6:
                    pos = "knight"
                if x == 3:
                    pos = "queen"
                if x == 4:
                    pos = "king"
            if y == 1 or y == 6:
                pos = "pawn" 
            if pos == "pawn":
                game.board[y][x] = pawn(x,y,side,pos)
            if pos == "bishop":
                game.board[y][x] = bishop(x,y,side,pos)
            if pos == "rook":
                game.board[y][x] = rook(x,y,side,pos)
            if pos == "knight":
                game.board[y][x] = knight(x,y,side,pos)
            if pos == "queen":
                game.board[y][x] = queen(x,y,side,pos)
            if pos == "king":
                game.board[y][x] = king(x,y,side,pos)


#CHECKS IF TWO PIECES ARE FROM OPPOSING SIDES
def enemy_piece(a,b):
    return a != None and b != None and a.side != b.side

#CHECKS IF PEICES IS ON THE BOARD
def onboard(x,y):
    return 0<=x<=7 and 0<=y<=7

#DISPLAYS THE UPGRADE PANEL FOR A PAWN(ABOVE BOARD OR BELOW BOARD)
def upgrade_panel(dy,c):
    rect(275,c,40,44)
    rect(315,c,40,44)
    rect(355,c,40,44)
    rect(395,c,40,44)
    copy(img,520,dy,94,95,278,c+2,30,40)
    copy(img,367,dy,94,95,322,c+2,30,40)
    copy(img,690,dy,94,95,358,c+2,30,40)
    copy(img,188,dy,94,95,398,c+2,30,40)


def upgrade_display():
    fill(255)
    #IF WHITE UPGRADE MOVE PANEL TO THE TOP AND SELECT WHITE PIECE
    if game.upgrade.side == 2:
        upgrade_panel(160,28)
    if game.upgrade.side == 1:
        upgrade_panel(19,638)

#creates a grid for the game of chess
def display_grid(n,leftx,topy):
    fill(0)
    strokeWeight(8)
    rect(leftx,topy,n*8,n*8)
    strokeWeight(3)
    for y in range(8):
        for x in range(4):
            if y % 2 == 0:
                fill(128,128,128)
                rect(leftx + n + x * 2 * n, (n * y) + topy, n, n)
                fill(255)
                rect(leftx + x * 2 * n, (n * y) + topy, n, n) 
            if y % 2 == 1:
                fill(255)
                rect(leftx + n + x * 2 * n, (n * y) + topy, n, n)
                fill(128,128,128)
                rect(leftx + x * 2 * n, (n * y) + topy, n, n) 


def mouse_Boundaries(leftx,rightx,topy,bottomy):
    return leftx <= mouseX <= rightx and topy <= mouseY <= bottomy

#DISPLAYS WINNER TEXT
def display_status():
    fill(0)
    textAlign(CENTER)
    textSize(30)
    if game.player == 0:
        text("Click Anywhere",350,680)
    text(game.status,350,50)
    if game.status == "Checkmate":
        if game.variable_checkmate == 1:
            text("White Wins",350,650)
        if game.variable_checkmate == 2:
            text("Black Wins",350,650)
#DISPLAYS WHO'S MOVE IT IS    
def display_player_move():
    textAlign(LEFT)
    textSize(50)
    if game.player == 1:
        fill(0)
        strokeWeight(150)
        text("Black Turn",15,670)
    if game.player == 2:
        fill(0)
        strokeWeight(150)
        text("White Turn",15,670)
def display_coordinate():
    fill(0)
    textSize(30)
    textLeading(50)
    for n in range(8):
        text(game.alpha_coord[n],125+64*n,90)
    for n in range(8):
        text(game.num_coord[n],73,142+64*n)

#DISPLAYS HIGHLIGHTED SQUARE AS WELL AS POSSIBLE MOVES
def display_moves():
    #Loops through draws non-selected pieces
    for m in game.board:
        for n in m:
            if n != None:
                if (n.x,n.y) != game.highlight:
                    n.hl = False
                if n.side == 1:
                    dy = 19
                if n.side == 2:
                    dy = 160
                if n.type == "pawn":
                    copy(img,860,dy,80,95,101+64*n.x,101+64*n.y,50,55)
                if n.type == "bishop":
                    copy(img,520,dy,94,95,104+64*n.x,99+64*n.y,50,58)
                if n.type == "rook":
                    copy(img,367,dy,94,95,112+64*n.x,99+64*n.y,50,58)
                if n.type == "knight":
                    copy(img,690,dy,94,95,104+64*n.x,99+64*n.y,50,58)
                if n.type == "queen":
                    copy(img,188,dy,94,95,103+64*n.x,99+64*n.y,51,58)
                if n.type == "king":
                    copy(img,25,dy,94,95,108+64*n.x,99+64*n.y,50,58)
    #Loops through and draws selected pieces
    for m in game.board:
        for n in m:
            if n != None:
                if (n.x,n.y) == game.highlight:
                    n.hl = True
                if n.side == 1:
                    dy = 19
                if n.side == 2:
                    dy = 160
                if n.hl == True:
                    fill(252,76,98,100)
                    rect(100 + n.x * 64, (64 * n.y) + 100, 64, 64)
                    fill(0, 128, 128,100)
                    for (cx,cy) in n.moves:
                        rect(100 + cx * 64, (64 * cy) + 100, 64, 64)
#IF A MOVE IS SELECTED
def move_made(n,dx,dy):
    #n.moves set to 0 so player cannot double press a spot(thus settin the move twice)
    n.moves = []
    game.board[n.y][n.x] = None
    #enpassant move
    if n.type == "pawn" and sqrt((dy-n.y)**2) == 2:
        for side in range(-1,2,2):
            if onboard(dx+side,dy):
                a = game.board[dy][dx+side]
                if enemy_piece(n,a) and a.type == "pawn":
                    #Tells the pawn object that en passant is an available move
                    a.special_chance = game.total_moves + 1
    #enpassant move is made thus kill the pawn behind it
    if n.type == "pawn" and n.y - dy != 0 and n.x - dx != 0 and game.board[dy][dx] == None:
        game.board[n.y][dx] = None
    #Castle on the right
    if n.type == "king" and n.x - dx == 2 and game.board[dy][dx] == None:
        game.board[dy][3] = game.board[dy][0]
        game.board[dy][0].x = 3
        game.board[dy][0] = None
    #Castle on the left
    if n.type == "king" and n.x - dx == -2 and game.board[dy][dx] == None:
        game.board[dy][5] = game.board[dy][7]
        game.board[dy][7].x = 5
        game.board[dy][7] = None
    #sets object coordinates to new grid and sets first move to false if true
    n.x = dx
    n.y = dy
    if n.fm == True:
        n.fm = False
    game.board[n.y][n.x] = n
    #Tells game to calculate new moves
    game.calc = 1
    #Changes the current player's turn
    if game.player == 1:
        game.player = 2
    else:
        game.player = 1
    #Adds one to the total moves made in a game
    game.total_moves += 1
    #If pawn is in position for upgrade set the player turn to zero and allow for an upgrade
    if n.y == 0 and n.side == 2 or n.y == 7 and n.side == 1:
        if n.type == "pawn":
            game.upgrade = n
            game.stored = game.player
            game.player = 0

def piece_highlight(n): #IF THE SELECTED PIECE HAS AVAILABLE MOVES
    if n.side == 2 and game.player == 2 or n.side == 1 and game.player == 1:
        if n.hl == False and len(n.moves) > 0:
            game.highlight = (n.x,n.y)
        else:
            game.highlight = None


def pawn_upgrade():#MOUSE SELECTION FOR PAWN UPGRADE PANEL
    n = game.upgrade
    game.board[n.y][n.x] = None
    if 275 <= mouseX <= 315:
        game.board[n.y][n.x] = bishop(n.x,n.y,n.side,"bishop")
    if 315 <= mouseX <= 355:
        game.board[n.y][n.x] = rook(n.x,n.y,n.side,"rook")
    if 355 <= mouseX <= 395:
        game.board[n.y][n.x] = knight(n.x,n.y,n.side,"knight")
    if 395 <= mouseX <= 435:
        game.board[n.y][n.x] = queen(n.x,n.y,n.side,"queen")
    game.upgrade = None
    game.player = game.stored
    game.calc = 1

#ENTER WINNERS NAME WHEN GAME IS OVER
def enter_name():
    if game.entered == False:
        if key == ENTER or key == RETURN:
            game.entered = True
        if key == BACKSPACE:
            game.name = game.name[0:-1]
        lk = ''
        if isinstance(key, basestring):
            if key.isalnum() or key == ' ':
                lk = key
        if len(game.name) <= 14:
            game.name = game.name +lk
    if game.entered == True:
        not_in = True
        for n in game.players:
            if game.name in n:
                n[0] += 1
                not_in = False
        if not_in == True:
            game.players.append([1,game.name])
        with open("scores.txt", "w") as out_score:
            for n in game.players:
                out_score.write(str(n[0]) + "\n")
                out_score.write("%s" % (n[1]) + "\n")
        game.players_high = quickSort(game.players)
        game.reset()
        

def display_ingame():#COMBINES IN-GAME DISPLAY FUNCTIONS
    if game.status != None:
        display_status()
    if game.status == None or game.status == "Check":
        display_player_move()
    if game.upgrade != None:
        upgrade_display()
    display_grid(64,100,100)
    display_coordinate()
    display_moves()
    if game.calc == 1:
        game.Move_Calculations()

#TITLE SCREEN DISPLAY
def display_title_screen():
    textSize(40)
    fill(255)
    fill(0)
    rect(128,180,450,70)
    fill(255)
    fill(0)
    textAlign(CENTER)
    textSize(140)
    text("Chess",350,140)
    textSize(40)

    fill(255)
    strokeWeight(2)
    text("PLAY",350,230)


def display_game_over(): #DISPLAYS THAT THE GAME IS OVER
    background(255,248,220)
    fill(0)
    textSize(40)
    textAlign(CENTER)
    if game.variable_checkmate == 1:
        game.winner_string = "WINNER: White Side"
    elif game.variable_checkmate == 2:
        game.winner_string = "WINNER: Black Side"
    else:
        game.winner_string = "Stalemate"
    text(game.winner_string,350,100)
    fill(40)
    textSize(30)
    textAlign(LEFT)
    text('(Press "Enter" to Return to Main Menu)',40,300)
    display_grid(20,280,450)
    fill(40)
    if game.winner_string != "Stalemate":
        text("Enter your name:",40,200)
        text(game.name,335,200)
        textSize(30)


def mouse_title_screen(): #TITLE SCREEN MOUSE SELECTION
    if mouse_Boundaries(127, 581,180,251):
        game.mode = 1
        starts()



def mouse_ingame(): #IN-GAME MOUSE SELECTION(PAWN UPGRADE AND PIECE SELECTION)
    if game.upgrade != None:
        if 28 <= mouseY <= 72 or 638 <= mouseY <= 682:
            if 275 <= mouseX <= 425:
                pawn_upgrade()
    for m in range(len(game.board)):
        for n in game.board[m]:
            if n != None:
                if mouse_Boundaries(100+64*n.x,100+64*(n.x+1),100+64*n.y,100 + 64*(n.y+1)):
                    piece_highlight(n)
                if n.hl == True:
                    for (dx,dy) in n.moves:
                        if mouse_Boundaries(100+64*dx,100+64*(dx+1),100+64*dy,100 + 64*(dy+1)):
                            move_made(n,dx,dy)

def setup():
    global img
    size(700,700)
    img = loadImage("pieces.png")
    
def draw():
    background(255)
    if game.mode == 0:
        display_title_screen()
    elif game.mode == 1:
        display_ingame()
    elif game.mode == 3:
        display_game_over()
        
def mousePressed():
    print(mouseX,mouseY)
    if game.mode == 0:
        mouse_title_screen()
    elif game.mode == 1:
        mouse_ingame()
        if game.status == "Checkmate" or game.status == "Stalemate":
            if mouse_Boundaries(0,700,0,700):
                game.mode = 3
                
def keyPressed():
    if game.mode == 3:
        enter_name()
