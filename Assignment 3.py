import turtle
import random
from functools import partial

INIT_TAIL = 5
FOOD_NUM = 5
WIDTH = 500
MOTION_H = 500
STATUS_H = 80
INTRO_H = 150
INTRO_LEFT = -210
COLOR_BODY = ("#303e2f", "#bccdba")
COLOR_HEAD = "#303e2f"
COLOR_MONSTER = "#a4031f"
FONT_STATUS = ("Arial", 16, "bold")
FONT_INTRO = ("Arial", 12, "normal")
FONT_FOOD = ("Arial", 12, "normal")
FONT_ENDGAME = ("Arial", 12, "bold")

KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT, KEY_SPACE = \
       "Up", "Down", "Left", "Right", "space"

HEADING_BY_KEY = {KEY_UP:90, KEY_DOWN:270, KEY_LEFT:180, KEY_RIGHT:0}

g_screen = None
g_snake = None
g_monster = None
g_snake_size = INIT_TAIL      # Snake is initially made with INIT_TAIL number of tails
g_intro = None
g_keypressed = KEY_SPACE      # Saves current motion. Motion is paused at start of game
g_lastkeypressed = KEY_RIGHT  # Saves previous motion. Default first motion when space is pressed at start of game.
g_status_contact = None
g_status_time = None
g_status_motion = None
g_contacts = 0
g_time_elapsed = 0
g_gamestart = False
g_gameover = False
g_snakespeed = 200
g_monsterspeed = 300
g_food = []
g_foodvisibility = [1 for _ in range(FOOD_NUM)]
g_foodeaten = [0 for _ in range(FOOD_NUM)]
g_paused = 1
g_stamp_coords = []
full_tail_length = FOOD_NUM*(FOOD_NUM+1)/2 + INIT_TAIL  # Length of fully extended snake tail


# Create a turtle with specified position, body color, and border color
def createTurtle(x, y, color="red", border="black"):
    t = turtle.Turtle("square")
    t.color(border, color)
    t.up()
    t.goto(x,y)
    return t


# Configure the screen
def configScreen():
    s = turtle.Screen()
    s.tracer(0)    # disable auto screen refresh
    s.title("Snake")
    s.setup(WIDTH+80, MOTION_H+STATUS_H+80)
    s.mode("standard")
    return s


# Configure the play area
def configPlayArea():
    # create motion border
    m = createTurtle(0,0,"","black")
    m.shapesize(MOTION_H/20, WIDTH/20, 2)
    m.goto(0, -(STATUS_H/2))

    # create status border
    s = createTurtle(0,0,"","black")
    s.shapesize(STATUS_H/20, WIDTH/20, 2)
    s.goto(0, MOTION_H/2)

    # introduction
    intro = createTurtle(INTRO_LEFT, INTRO_H-5*20)
    intro.hideturtle()
    intro.write("Welcome to the snake game!\n\n"\
                "You are going to move the snake with the 4 arrow keys.\n\n"\
                "Consume all the food items before the monster catches you.\n\n"\
                "Click anywhere to start the game.", \
                font=FONT_INTRO)
    
    # contact status
    status_contact = createTurtle(0,0,"","black")
    status_contact.hideturtle()
    status_contact.goto(-210,s.ycor()-10) 

    # time status
    status_time = createTurtle(0,0,"","black")
    status_time.hideturtle()
    status_time.goto(-210+150,s.ycor()-10) 

    # motion status
    status_motion = createTurtle(0,0,"","black")
    status_motion.hideturtle()
    status_motion.goto(-210+265,s.ycor()-10) 

    return intro, status_contact, status_time, status_motion


# Set snake heading based on the key pressed
def setSnakeHeading(key):
    if key in HEADING_BY_KEY.keys():
        g_snake.setheading( HEADING_BY_KEY[key] )


# Updates the contacts status bar
def updateContactStatus():
    g_status_contact.clear()
    g_status_contact.write(f"Contacts: {g_contacts}", font=FONT_STATUS)
    g_screen.update()


# Updates the motion status bar
def updateMotionStatus():
    g_status_motion.clear()
    if g_keypressed == KEY_SPACE:
        motion = "Paused"  # Paused motion
    else:
        motion = g_keypressed
    
    g_status_motion.write(f"Motion: {motion}", font=FONT_STATUS)
    g_screen.update()


# Updates the time status bar
def onTimerTime():
    global g_time_elapsed

    if g_gameover:
        return
    
    if not g_gamestart:
        g_status_time.write(f"Time: {g_time_elapsed}", font=FONT_STATUS)
        g_screen.update()
        return
    
    g_time_elapsed += 1

    g_status_time.clear()
    g_status_time.write(f"Time: {g_time_elapsed}", font=FONT_STATUS)
    g_screen.update()

    g_screen.ontimer(onTimerTime, 1000)  # Refresh every 1 second, stops when game is over


# Update snake heading and key pressed status if motion is valid
def onArrowKeyPressed(key):
    global g_keypressed, g_lastkeypressed, g_paused

    # Reject user input if the motion is invalid
    if checkCollision(key):
        key = g_lastkeypressed

    # Update current motion and previous motion status
    g_keypressed = key
    if key != KEY_SPACE:
        g_paused = 0
        g_lastkeypressed = key
    else:
        g_paused = (g_paused + 1) % 2
        if g_paused == 0:
            g_keypressed = g_lastkeypressed  # Resume previous motion
    
    setSnakeHeading(key)
    updateMotionStatus()


# Check collision with motion border and tail
def checkCollision(key):
    # Check collision with motion border
    if ( (key == KEY_LEFT and g_snake.xcor()-20 <= (-WIDTH/2)) or
            (key == KEY_RIGHT and g_snake.xcor()+20 >= (WIDTH/2)) or
            (key == KEY_DOWN and g_snake.ycor()-20 <= (-MOTION_H/2 - STATUS_H/2)) or
            (key == KEY_UP and g_snake.ycor()+20 >= (MOTION_H/2 - STATUS_H/2)) ):
        return True
    
    # Check collision with snake's tail
    for tail in g_stamp_coords:
        if ( (key == KEY_LEFT and abs(g_snake.ycor()-tail[1]) < 0.1 and abs(g_snake.xcor()-20-tail[0]) < 0.1) or
                (key == KEY_RIGHT and abs(g_snake.ycor()-tail[1]) < 0.1 and abs(g_snake.xcor()+20-tail[0]) < 0.1) or
                (key == KEY_DOWN and abs(g_snake.xcor()-tail[0]) < 0.1 and abs(g_snake.ycor()-20-tail[1]) < 0.1) or
                (key == KEY_UP and abs(g_snake.xcor()-tail[0]) < 0.1 and abs(g_snake.ycor()+20-tail[1]) < 0.1) ):
            return True
    
    return False


# Check if game is over
def checkGameOver():
    global g_gameover

    # Check if snake is fully extended
    if len(g_stamp_coords) == full_tail_length:
        g_gameover = True
        if g_snake.xcor() < -WIDTH/4:
            g_snake.write("     Winner!!!", align="left", font=FONT_ENDGAME)
        else:
            g_snake.write("Winner!!!    ", align="right", font=FONT_ENDGAME)
        return
    
    # Check if monster catches snake
    if abs(g_monster.xcor()-g_snake.xcor()) < 11 and abs(g_monster.ycor()-g_snake.ycor()) < 11:
        g_gameover = True
        if g_monster.xcor() < -WIDTH/4:
            g_monster.write("     Game over!!!", align="left", font=FONT_ENDGAME)
        else:
            g_monster.write("Game over!!!    ", align="right", font=FONT_ENDGAME)
        return
    

# Unbind arrow and space keys from action
def unbindKeys():
    g_screen.onkey(None, KEY_DOWN)
    g_screen.onkey(None, KEY_UP)
    g_screen.onkey(None, KEY_LEFT)
    g_screen.onkey(None, KEY_RIGHT)
    g_screen.onkey(None, KEY_SPACE)


# Update the snake's moves
def onTimerSnake():
    global g_snakespeed, g_snake_size, g_foodvisibility, g_gameover

    checkGameOver()
    
    # Stop snake's movement if game is over
    if g_gameover:
        unbindKeys()
        return
    
    # Stop movement if game has not started, snake is paused, or snake collides with border or its tail
    if g_keypressed == None or g_paused == 1 or checkCollision(g_keypressed):
        g_screen.ontimer(onTimerSnake, g_snakespeed)
        return

    # Clone the head as body
    g_snake.color(*COLOR_BODY)
    g_snake.stamp()
    g_snake.color(COLOR_HEAD)
    if len(g_stamp_coords) > 0 and len(g_stamp_coords) > g_snake_size-1:
        g_stamp_coords.pop(0)
    g_stamp_coords.append(g_snake.pos())

    # Advance snake
    g_snake.forward(20)

    # Shifting or extending the tail, remove the last square on Shifting.
    # Slow down the snake when extending.
    if len(g_snake.stampItems) > g_snake_size:
        g_snakespeed = 200
        g_snake.clearstamps(1)
    else:
        g_snakespeed = 300
    
    # Check if snake eats food
    for i in range(FOOD_NUM):
        if (g_foodvisibility[i] == 1 and g_foodeaten[i] == 0 and g_snake.distance(g_food[i]) < 10):
            g_foodvisibility[i] = 0
            g_foodeaten[i] = 1
            g_food[i].clear()
            g_snake_size += i+1
    
    g_screen.update()
    g_screen.ontimer(onTimerSnake, g_snakespeed)


# Update the monster's move
def onTimerMonster():
    global g_contacts

    checkGameOver()

    # Stop monster's movement if game is over
    if g_gameover:
        unbindKeys()
        return
    
    # Get random speed for the monster
    monsterspeed = list(range(180, 381, 20))
    g_monsterspeed = random.choice(monsterspeed)
    
    # Change the monster's direction to get closer to the snake
    if abs(g_monster.xcor()-g_snake.xcor()) > abs(g_monster.ycor()-g_snake.ycor()):
        if g_monster.xcor()+10 < g_snake.xcor():
            g_monster.setheading(0)
        elif g_monster.xcor()-10 > g_snake.xcor():
            g_monster.setheading(180)
    else:
        if g_monster.ycor()+10 < g_snake.ycor():
            g_monster.setheading(90)
        elif g_monster.ycor()-10 > g_snake.ycor():
            g_monster.setheading(270)

    # Advance monster
    g_monster.forward(20)

    # Check for contact with snake's body
    for tail in g_stamp_coords:
        if g_monster.distance(tail) < 15:
            g_contacts += 1
            break
    
    updateContactStatus()
    
    g_screen.update()
    g_screen.ontimer(onTimerMonster, g_monsterspeed)


# Controls the visibility of food
def ontimerFood():
    global g_foodvisibility
    
    if g_gameover or g_foodeaten.count(0) <= 0:
        return

    # Get one random uneaten food
    uneaten_food = []
    for i in range(len(g_foodeaten)):
        if g_foodeaten[i] == 0:
            uneaten_food.append(i)
    
    target_idx = random.choice(uneaten_food)

    # Change its state, show if hidden, hide if shown
    if g_foodvisibility[target_idx] == 1:
        g_foodvisibility[target_idx] = 0
    else:
        g_foodvisibility[target_idx] = 1

    for i in range(FOOD_NUM):
        if g_foodvisibility[i] == 0:
            g_food[i].clear()
        else:
            g_food[i].write(f" {i+1}", align="center", font=FONT_FOOD)

    g_screen.update()
    g_screen.ontimer(ontimerFood, 5000)  # Refresh every 5 seconds


# Initiate the game
def startGame(x,y):
    global g_gamestart

    g_gamestart = True
    g_screen.onscreenclick(None)  # Remove onclick function
    g_intro.clear()  # Remove introduction text

    # Bind keys with actions
    g_screen.onkey(partial(onArrowKeyPressed,KEY_UP), KEY_UP)
    g_screen.onkey(partial(onArrowKeyPressed,KEY_DOWN), KEY_DOWN)
    g_screen.onkey(partial(onArrowKeyPressed,KEY_LEFT), KEY_LEFT)
    g_screen.onkey(partial(onArrowKeyPressed,KEY_RIGHT), KEY_RIGHT)
    g_screen.onkey(partial(onArrowKeyPressed,KEY_SPACE), KEY_SPACE)

    # Show all food items
    for i in range(len(g_food)):
        g_food[i].write(f" {i+1}", align="center", font=FONT_FOOD)

    # Start timers
    g_screen.ontimer(onTimerTime, 1000)
    g_screen.ontimer(ontimerFood, 5000)
    g_screen.ontimer(onTimerSnake, g_snakespeed)
    g_screen.ontimer(onTimerMonster, g_monsterspeed)


if __name__ == "__main__":
    g_screen = configScreen()
    g_intro, g_status_contact, g_status_time, g_status_motion = configPlayArea()

    # Start display status texts
    updateContactStatus()
    onTimerTime()
    updateMotionStatus()

    # Create food items at random positions with fair distance between each food item and initial snake position
    food_pos = []
    x_pos_list_f = list(range(int(-WIDTH/2)+10, int(WIDTH/2)-10+1, 20))
    y_pos_list_f = list(range(int(-MOTION_H/2)-38, int(MOTION_H/2)-58+1, 20))
    for i in range(FOOD_NUM):
        validpos = False
        while not validpos:
            x_pos_f = random.choice(x_pos_list_f)
            y_pos_f = random.choice(y_pos_list_f)
            # Condition for the first food item
            if (len(food_pos) < 1 and 
                    (abs(x_pos_f) > g_snake_size*20) and        # Keeps fair distance from initial snake position
                    (abs(y_pos_f) > g_snake_size*20)):
                break
            # Condition for the second to the rest of the food items
            for pos in food_pos:
                dist = ((x_pos_f-pos[0])**2 + (y_pos_f-pos[1])**2)**0.5
                if (dist > 50 and                               # Keeps fair distance between each food item
                        (abs(x_pos_f) > g_snake_size*20) and    # Keeps fair distance from initial snake position
                        (abs(y_pos_f) > g_snake_size*20)):       
                    validpos = True
                else:
                    validpos = False
                    break
        food_pos.append((x_pos_f, y_pos_f))
        f = createTurtle(x_pos_f, y_pos_f, "black")
        f.hideturtle()
        g_food.append(f)

    # Get a random starting position for the monster
    x_pos_list_m = list(range(int(-WIDTH/2)+20, int(WIDTH/2)-20+1, 20))
    y_pos_list_m = list(range(int(-MOTION_H/2)-20, 0, 20))
    while True:
        x_pos_m = random.choice(x_pos_list_m)
        y_pos_m = random.choice(y_pos_list_m)
        dist = (x_pos_m**2 + y_pos_m**2)**0.5
        if dist > 150 and dist < 250:  # Limit monster's initial relative position to snake to between 150-250.
            break
    
    # Create the snake and monster
    g_snake = createTurtle(0, 0, COLOR_HEAD, COLOR_HEAD)
    g_monster = createTurtle(x_pos_m, y_pos_m, COLOR_MONSTER, COLOR_MONSTER)

    # Start the game when screen is clicked
    g_screen.onscreenclick(startGame)

    g_screen.update()
    g_screen.listen()
    g_screen.mainloop()
