import turtle

# Define constants
SCREEN_WIDTH = 560
SCREEN_HEIGHT = 610
SHAPE_WIDTH = 3  # Scale for shape width (width = SHAPE_WIDTH*20px)
SPACING = 10  # Gap between trackers
COLS = 8
ROWS = 8    
COLOR_1 = '#95C623'  # Color for player 1
COLOR_2 = '#445E93'  # Color for player 2
COLOR_OUTLINE = '#F93943'  # Outline color for 4-in-a-row balls
COLOR_BAR = 'black'  # Tracker fill color
OUTLINE_WIDTH = 5
REFRESH_RATE = 100


# Define global variables
g_cursor_x = -999  # Cursor's x position
g_column_trackers = []  # Stores the turtle object of each column tracker
g_game = [[] for _ in range(COLS)]  # Stores the player who owns the token
g_game_turtle = [[] for _ in range(COLS)]  # Stores the turtle object of each token
player = 0  # Current player
scn = turtle.Screen()


# Make column trackers
def init_rectangle(x, y):
    scn.tracer(0)  # Turn off auto refresh
    tt = turtle.Turtle('square')  # Create a new turtle with 4-side polygon shape (rectangle)
    tt.shapesize(1, SHAPE_WIDTH)  # Set rectangle height to 1*20px and width to SHAPE_WIDTH*20px
    tt.color(COLOR_BAR)  # Set rectangle color to COLOR_BAR
    tt.penup()  # The rectangle will not make any trace while moving
    tt.goto(x, y)  # Put the rectangle on (x,y) coordinate
    scn.update()  # Refresh the screen
    g_column_trackers.append(tt)


# Make new token on specified location and color
def new_token(x, y, p_color):
    scn.tracer(0)
    scn.onclick(None)  # Turn off onclick function temporarily while putting token
    tt = turtle.Turtle('circle')
    tt.shapesize(SHAPE_WIDTH)  # Set circle diameter to SHAPE_WIDTH*20px
    tt.color(p_color)
    tt.penup()
    tt.goto(x, y)
    scn.update()
    scn.onclick(play_turn)  # Turn on onclick function again
    return tt


# Create all column trackers
def init_column_trackers():
    x = 30  # First x position
    y = 20  # First y position
    for _ in range(COLS):
        init_rectangle(x, y)  # Create a tracker on (x,y) coordinate
        x += SHAPE_WIDTH*20 + SPACING
    scn.update()


# Create outline on the turtle object
def outline(tt, p_color, p_width):
    tt.pencolor(p_color)  # Change the turtle's outline color to p_color
    tt.shapesize(outline=p_width)  # Change the turtle's outline width to p_width


# Get mouse x position
def motion(event):
    global g_cursor_x
    g_cursor_x = event.x


# Track columns and add outline to the tracker
def column_tracking():
    global g_cursor_x
    
    col = g_cursor_x // (20*SHAPE_WIDTH + SPACING)  # Determine the column number which the cursor is located
    
    # Set color according to current player
    if player == 0:
        color = COLOR_1
    else:
        color = COLOR_2
    
    # Change the outline of each tracker
    for i in range(COLS):
        tt = g_column_trackers[i]        
        if i == col:
            outline(tt, color, OUTLINE_WIDTH)  # Change the tracker's outline when mouse is hovering on top of it
        else:
            outline(tt, COLOR_BAR, 1)  # Reset the tracker's outline to default
    
    scn.update()
    scn.ontimer(column_tracking, REFRESH_RATE)

    return col


# Check whether the current player has won the game
def check_game():
    # Returns -1 if the game has not finished yet
    # Returns 0 if the game is tied
    # Returns 1 if the player has won
    
    global g_game, player
    
    # Check vertically
    for i in range(COLS):
        num_token = len(g_game[i])
        try:
            for j in range(num_token-3):
                if (g_game[i][j] == player and 
                        g_game[i][j+1] == player and 
                        g_game[i][j+2] == player and 
                        g_game[i][j+3] == player):
                    for k in range(4):
                        outline(g_game_turtle[i][j+k], COLOR_OUTLINE, OUTLINE_WIDTH)
                    return 1
        except:
            continue
    # Check horizontally
    for j in range(ROWS):
        for i in range(COLS-3):
            try:
                if (g_game[i][j] == player and
                        g_game[i+1][j] == player and
                        g_game[i+2][j] == player and
                        g_game[i+3][j] == player):
                    for k in range(4):
                        outline(g_game_turtle[i+k][j], COLOR_OUTLINE, OUTLINE_WIDTH)
                    return 1
            except:
                continue
    # Check increasing diagonal
    for i in range(COLS-3):
        for j in range(ROWS-3):
            try:
                if (g_game[i][j] == player and
                        g_game[i+1][j+1] == player and
                        g_game[i+2][j+2] == player and
                        g_game[i+3][j+3] == player):
                    for k in range(4):
                        outline(g_game_turtle[i+k][j+k], COLOR_OUTLINE, OUTLINE_WIDTH)
                    return 1
            except:
                continue
    # Check decreasing diagonal
    for i in range(COLS-3):
        for j in range(ROWS-1,2,-1):
            try:
                if (g_game[i][j] == player and
                        g_game[i+1][j-1] == player and
                        g_game[i+2][j-2] == player and
                        g_game[i+3][j-3] == player):
                    for k in range(4):
                        outline(g_game_turtle[i+k][j-k], COLOR_OUTLINE, OUTLINE_WIDTH)
                    return 1
            except:
                continue
    # Check for tie
    full_cols = 0
    for i in range(COLS):
        if len(g_game[i]) == ROWS:
            full_cols += 1
    if full_cols == COLS:
        return 0

    return -1
    

# Play the player's turn
def play_turn(x, y):
    global g_game, g_game_turtle, player
    col = column_tracking()  # The column number where the mouse click was located
    num = len(g_game[col])  # Number of tokens in that column
    
    # Reject player intention to put token on full column
    if num >= ROWS:
        print('The column is full. Please choose another column.')
        return
    
    # Set x and y coordinate for the token final position
    x = 30 + (60 + SPACING) * col
    y = 70 + (60 + SPACING) * num
    
    # Insert the new token on the selected column with specified color
    if player == 0:
        tt = new_token(x, y, COLOR_1)
    else:
        tt = new_token(x, y, COLOR_2)
    
    # Add current player and the turtle to list
    g_game[col].append(player)
    g_game_turtle[col].append(tt)
    
    # Check if the player has won the game or the game is tied
    result = check_game()
    if result == 0:
        # The game is tied
        scn.title('Game Tied !')
        scn.exitonclick()  # Exit the game on next click
    elif result > 0:
        # The current player wins
        scn.title(f'Winner ! Player {player + 1}')
        scn.exitonclick()  # Exit the game on next click

    player = (player + 1) % 2  # Update the player's turn


# Initialize the game
def init_game():
    # Initialize the screen
    scn.mode('world')
    scn.setup(SCREEN_WIDTH, SCREEN_HEIGHT)
    scn.setworldcoordinates(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
    scn.title('Connect 4 Game')
    
    scn.onclick(play_turn)  # Set onclick function to play_turn
    
    # Bind motion with mouse tracking
    canvas = turtle.getcanvas()
    canvas.bind('<Motion>', motion)
    
    init_column_trackers()  # Create the column trackers
    
    scn.ontimer(column_tracking, REFRESH_RATE)  # Call column_tracking function every REFRESH_RATE milliseconds

    scn.mainloop()  # Keep the window on


if __name__ == '__main__':
    init_game()
