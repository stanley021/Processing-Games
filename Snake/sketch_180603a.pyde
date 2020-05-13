#snake variables
grid = []
s = 20
tx = 120
ty = 0
mode = 0
n = 14
difficulty = 'normal'
chosenbackground = 0
move= RIGHT
num= 4
num2= 8
play=0
x=18
y=18
dx = 1
dy = 0
snake = [[16,18],[17,18],[18,18]]
point_1= 0
points = 0
  


def setup():
    global map1, map2, map3, n, map5 , map4, chosenbackground, file, game
    size (800, 600)
    map1 = loadImage("thoe.png")
    map2 = loadImage("images.jpg")
    map3 = loadImage("scroll.jpg")
    map4 = loadImage("powow.jpg")
    map5 = loadImage("pokemon.png")


            
def draw():
    global mode,ty,tx, n
    frameRate(n)
    
    #setting different modes for different screens and parts of the game
    #main menu of the snake game.
    if mode == 0:
        image (map2,0,0)
        fill(255)
        textSize(100)
        text("Snake",50,90,10)
        rect(635,25,50,50)
        map5.resize(50,50)
        image(map5,635,22)
        rect(55,175,680,118)
        rect(55,451,680,118)
        rect(55,313,680,118)
        fill(0)
        text("Play", 300,540,10)
        text("Instructions", 130,400,10)
        text("Difficulty", 170,270,10)
        textSize(40)
        fill(255)
        text("Made by Stanley Chen", 54,147,10)
    
    
        #The menu for the instructions guiding new players on how to play the game properly
    elif mode == 1: 
        fill(0)
        image(map3,0,0)
        textSize(45)
        text("Press b to go back to menu", 10,40,10)
        textSize(20)
        text("Snake is a common name for a game where you grow \n in length after eating a certain object. The primary \nobjective is to eat as much as you can and stay \ninside of the borders. To play the game you can \n use (W,A,S,D) or the arrow keys to move. \n(W to move up, D to move right, A to move left and \n S to move down) \n Enjoy! ",104,160,10) 
    
    #The difficulty option for the game to give the players a bit of a challenge if the need it. Increases the speed of the snake depending on the level they chose to play at.
    elif mode == 'Difficulty':
        background(0)
        textSize(45)
        fill(255)
        text("Press b to go back to menu", 10,40,10)
        text("Difficulty set to:",15,96,10)
        text(difficulty, 377,96,10)
        fill(0,255,0)
        rect(223,200,350,100)
        fill(255,255,0)
        rect(223,314,350,100)
        fill(255,0,0)
        rect(223,426,350,100)
        fill(0)
        text("Easy", 330,280, 20)
        text("Medium", 315,386,5)
        text("Hard", 330 , 490,5)
        
                
    #the main part of the game, where everyone spends their time.
    elif mode == 2:
        background(0)
        
        global play, x, y, mode,num,r,s,num2, dx, dy, chance,up, points, move,key,point_1, map1, chosenbackground
        
        #changes the background if pokemon was clicked
        if chosenbackground == 0:
            image(map1,0,0)
        elif chosenbackground == 1:
            image(map4,0,0)
        textSize(25)
        fill(255)
        text("Press b to go back to menu", 50,43,10)
        
        #food
        fill(0,255,100)
        rect(num*20,num2*20,20,20)
        
        #BORDERS
        if y >= 32:
            mode = 3
        elif y < 0:
            mode = 3
        if x >= 43:
            mode = 3
            print "nut"
        elif x < 0:
            mode = 3
            print "nut"
            
        
        #CONTROLS
        if  (key == 'a' or key == 'A' or keyCode == LEFT) and move != RIGHT:
            move = LEFT
        if  (key == 'd' or key == 'D' or keyCode == RIGHT) and move !=LEFT :
            move = RIGHT
        if (key == 'w' or key == 'W' or keyCode== UP) and move != DOWN:
            move = UP
        if  (key == 's' or key == 'S' or keyCode == DOWN) and move != UP:
            move = DOWN
        #THE MOVEMENT IS DETERMINED WITH WHAT KEY YOU CLICK, it will add 1 to going up, down, left or right
        if move == LEFT:
            dx= -1
            dy=0
        if move == RIGHT:
            dx=+1
            dy=0
        if move== UP:
            dy=-1
            dx=0
        if move == DOWN:
            dy=+1
            dx=0
        
        #Depending on the points you achieve the game will get harder and harder
        if points >= 5:
            frameRate(n + 3)
        if points >= 10:
            frameRate(n + 6)
        if points >= 15:
            frameRate(n + 9)
        if points >= 20:
            frameRate(n + 12)
        if points >= 25:
            frameRate(n + 13)
        
        y = y + dy
        x = x + dx 
        print(x,y)
        snake.append((x,y))
        snake.pop(0)
        
        
        # eating food
        food = True
        if snake[len(snake)-1][0] == num and snake[len(snake)-1][1] ==num2:
            print "EATING FOOD"
            
            food = False
        
        for square in range(len(snake)-2):
            if snake[square] == snake[len(snake)-1]:
                mode =3
        
        # contant point counter,
        fill(255)
        textSize(25)
        text("Points:",50,70)
        text(points,150,70)      
        text("High Score:", 50, 100)
        text(point_1, 210,100)
        
        
        if food == False:
            points += 1
            num = int(random(30)) #food_x
            num2 = int(random(30))
            print points
            snake.append((x,y))
        
        #FOLLOWING SNAKE 
        for square in snake :
            if square == snake[-1]:
                fill(100,0,255)
                rect(square[0]*20, square[1]*20,20,20)
            else:
                fill(255)
                rect(square[0]*20, square[1]*20,20,20)
        
        
        
        #DEATH OF THE SNAKE SWITCHING THE SCREEN TO A GAME OVER SCREEN GIVING THE OPTION OF RESTARTING TEH GAME
        if mode == 3:
            global point_1, chosenbackground
            if chosenbackground == 0:
                image(map1,0,0)
            elif chosenbackground == 1:
                image(map4,0,0)
            fill(255,53,200)
            rect(315,315, 160,70)
        #play button
            textSize(60)
            fill(255)
            text("Game Over", 189,124,60)
            textSize(30)
            text("Restart", 330,360,60)
            text("HighScore:", 200,200,60)
            fill(255)
            text("Press b to go back to menu", 50,43,10)
            
            if points > point_1:
                point_1 = points
            
            text(point_1, 380,200,60)


def mousePressed():
    global mode,play, x, y, mode,num,r,s,num2, dx, dy, chance,up, points, move,key,point_1,snake,n, difficulty, chosenbackground,file2
    
    #choses the difficulty for the game
    if mode == 'Difficulty' and mousePressed and 224 < mouseX < 571 and 200 < mouseY < 298:
        difficulty = 'Easy'
        n = 12
    if mode == 'Difficulty' and mousePressed and 224 < mouseX < 571 and 316 < mouseY < 412:
        difficulty = 'Medium'
        n = 14
    if mode == 'Difficulty' and mousePressed and 224 < mouseX < 571 and 427 < mouseY < 526:
        difficulty = 'Hard'
        n = 16
    
    #difficulty menu
    if mode == 0 and mousePressed and 56 < mouseX < 734 and 177 < mouseY < 291:
        mode = 'Difficulty'
    
    if mode == 0 and mousePressed and 634 < mouseX < 686 and 23 < mouseY < 74:
        chosenbackground = 1
        
    if mode == 0 and mousePressed and 56 < mouseX < 734 and 314 < mouseY < 430:
        mode = 1
    
    if mode == 0 and mousePressed and 53 < mouseX < 736 and 450 < mouseY < 570:
        mode = 2
        
    if mode == 3 and mousePressed and 260 < mouseX < 419  and 315 < mouseY < 384:
        mode = 2
        
        move= RIGHT
        num= 4
        num2= 8
        play=0
        x=18
        y=18
        dx = 1
        dy = 0
        snake = [[16,18],[17,18],[18,18]]
        points=0
        chosenbackground = 0

def keyPressed():
    global mode
    if key == "b" and mode == "Difficulty" :
        mode = 0
    
    if key == "b" and mode == 1 :
        mode = 0
        
    if key == "b" and mode == 2 :
        mode = 0
        
    if key == "b" and mode == 3 :
        mode = 0
        
