"""
HN: Haris Nasir {21184089
SNT: Sy Nguyen Tran (21120268)
HGT: Haogang (Hugo) Tang (21139238)
"""

"""
Note to Hugo and Haris
In order for this to work on Spyder, make sure that you type in on the bottom right window
pip install freegames
"""

from random import choice #SNT: Import from random module choice
from turtle import * #SNT: Import turtle module, which is responsible for setting up the games

from freegames import floor, vector #SNT: Import neccessary functions, to make the function works

state = {'score': 0} #SNT: Initialize the score board, as a dictionary
path = Turtle(visible=False) #SNT: Create an object called path, with the class of Turtle, whose visibility is turned off. This turtle is responsible to draw the world.
writer = Turtle(visible=False) #SNT: Create an object called writer, with the class of Turtle, whose visibility is turned off. This turtle is responsible for drawing pacman and ghosts.
aim = vector(5, 0) #SNT: Create an aiming vector with the value of [5, 0], which in the context of this games, is pointing to the right.
pacman = vector(-40, -80) #SNT: Create a pacman vector with the value of [-40, -80]
ghosts = [
    [vector(-180, 160), vector(5, 0)],
    [vector(-180, -160), vector(0, 5)],
    [vector(100, 160), vector(0, -5)],
    [vector(100, -160), vector(-5, 0)],
 ]
"""
 SNT:
 The variable "ghosts" stores 4 new ghosts as sublist, each having two vectors associating to it. The first vector of each sublist is the position vector, the second vector is the velocity vector
 In the context of this game:
 (5, 0) go right
 (0, 5) go up
 (0, -5) go down
 (-5, 0) go left
 """

# fmt: off
from collections import defaultdict
import random

# tiles_map: key = (gx, gy) grid coords (integers), value:
# 0 = wall, 1 = normal dot (uneaten), 2 = eaten/no dot, 3 = GROW tile, 4 = SHRINK tile
tiles_map = {}  # dynamic map storage

# snake-like pacman body variables
body = []            # list of vector positions (head first)
length = 1           # initial length (number of segments)
grow_amount = 3      # when eating a GROW tile, length += grow_amount
shrink_amount = 2    # when eating a SHRINK tile, length -= shrink_amount (min 1)

# helper: convert original tiles list (if any) into tiles_map for initial area.
# To preserve your original layout, we'll paste the old 400-values into this function.
original_tiles_list = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0,
    0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
]

def init_tiles_map():
    """Initialize tiles_map from original_tiles_list in a 20x20 area with coords (0..19,0..19)."""
    for i, val in enumerate(original_tiles_list):
        gx = i % 20
        gy = i // 20
        tiles_map[(gx, gy)] = val

# procedural generator for tiles in previously-unseen grid coords
def generate_tile(gx, gy):
    rnd = random.random()
    if rnd < 0.10:
        return 0  # wall
    if rnd < 0.13:
        return 3  # grow tile
    if rnd < 0.16:
        return 4  # shrink tile
    return 1      # normal dot

# initialize map with original layout as seed
init_tiles_map()

"""
SNT: Creat a map of the game, where 1 is an untraveled path, 2 is a traveled path and walls is 0
To be noted, the grid itself is presented as essentially a 2D matrix. However, in actuality, it's actually juat one list, but with an enter every 20 entries to appear like a grid.
"""
# fmt: on


def square(x, y):
    """Draw square using path at (x, y)."""
    """
    SNT: This functions esentially draw a square
    However, as will later be seen in world(), each time a tile is drawn, square() is called.
    This makes each a tile 20x20.
    """
    
    path.up() #SNT: allows the turtle "path" (which is a drawing pen, essentially) to lift up from the page and draw nothing
    path.goto(x, y) #SNT: moves the turtle "path" to the position (x, y) which is inputed into the 
    path.down() #SNT: This essentially put the turle "pen" down onto the page to begin to draw
    path.begin_fill() #SNT: This intializes the starting point of the shape that about to be draw by the turle "path"

    for count in range(4): #SNT: Allows this entire block to run a total of four times
        """
        SNT: The entire block essentially makes the turtle "path" goes straight 20 times, turns 90 degree left
        After completing this 4 times, the turle "path" essentially drew a square
        """
        
        path.forward(20)
        path.left(90)

    path.end_fill() #SNT: This ends and fill the shape intialized on line 65 with color


def offset(point):    """Return offset of point in tiles."""
    """
    SNT:
    This function essentially takes in the pixel position of any object and convert it into one of the tiles, whose values can be searched
    up in the list "tiles".
    """
    
    gx = int(floor(point.x, 20) + 200) / 20
    gy = int(180 - floor(point.y, 20)) / 20
    
    
    return (gx , gy)


def valid(point):    """Return True if point is valid (not wall) in tiles_map."""
    gx, gy = offset(point)

    # Ensure tile exists; if not, generate it on demand
    if (gx, gy) not in tiles_map:
        tiles_map[(gx, gy)] = generate_tile(gx, gy)

    # If current tile is wall -> invalid
    if tiles_map[(gx, gy)] == 0:
        return False

    # Check the top-right corner of the bounding box (point + 19)
    gx2, gy2 = offset(point + 19)
    if (gx2, gy2) not in tiles_map:
        tiles_map[(gx2, gy2)] = generate_tile(gx2, gy2)
    if tiles_map[(gx2, gy2)] == 0:
        return False

    # Ensure movement is along grid lines
    return point.x % 20 == 0 or point.y % 20 == 0



def valid(point):
    """Return True if point is valid in tiles."""
    #SNT: This function should only be given pixel coordinates.
    
    index = offset(point) #SNT: Index is assigned the index in the list "tiles" in which "point" reside.
    
    #SNT: Essentially, we captured the current location of the input "point".

    if tiles[index] == 0: 
        return False #SNT: If the tile in which "point" reside in correspond to a 0 in the list "tiles", then it's not valid. AKA, "point" is in a wall. 

    index = offset(point + 19)
    
    """
    SNT:
    Recalling that each tiles is only 20x20.
    When "point" + 19, it is moved 19 pixels up and right.
    If and only if the "point" is originally on the very bottom left corner of the tiles, after being shifted, it would remained in the same tiles.
    Other wise, it would be moved to another tiles.
    """

    if tiles[index] == 0:
        return False
        
    #SNT: Here, we checked if this new position is also a wall.
    #SNT: This extra step essentially check if there's any collision at the "point" current location, and 19 pixels around it.

    return point.x % 20 == 0 or point.y % 20 == 0
    
    """
    SNT:
    point.x % 20 and point.y % 20 checked if this the "point" is on the edge of a tiles.
    If either of this is true, then True is returned.
    This ensure "point" is on a grid line, which for this games are like track that pac man and ghost can travel.
    """


def world(view_radius = 10):
    """Draw world using path."""
    bgcolor('black') #SNT: Set background color to black
    path.color('blue') #SNT: Set "path" colour to blue

    center_gx, center_gy = offset(pacman)

    # iterate over a square region around center
    for dy in range(-view_radius, view_radius + 1):
        for dx in range(-view_radius, view_radius + 1):
            gx = center_gx + dx
            gy = center_gy + dy

            # ensure tile exists
            if (gx, gy) not in tiles_map:
                tiles_map[(gx, gy)] = generate_tile(gx, gy)

            tile = tiles_map[(gx, gy)]
            # convert grid (gx,gy) back to pixel coords with same origin as before
            x = gx * 20 - 200
            y = 180 - gy * 20

            if tile > 0:
                square(x, y)
                path.up()
                path.goto(x + 10, y + 10)
                # draw dot for normal bean
                if tile == 1:
                    path.dot(2, 'white')
                elif tile == 3:
                    path.dot(6, 'green')
                elif tile == 4:
                    path.dot(6, 'magenta')

def move():
    """Move pacman and all ghosts."""
    """
    SNT:
    The main purpose of this function is to move the pac man and the ghost around.
    However, some of the code here makes little sense out of the context which it is used.
    """
    
    writer.undo() #SNT: Undo the what the previous turtle "writer" wrote.
    
    writer.write(state['score']) #SNT: Use the turtle "writer" to write out the new score of the game.

    clear()
    """
    SNT:
    This functions clear previous drawing done by the turtles.
    Without this function, when the ghosts and pacman moves, its creates a trail.
    We intends to use this functions to create an extra feature in the games.
    """

    if valid(pacman + aim):
        pacman.move(aim)
        
    head = vector(pacman.x, pacman.y)
    body.insert(0, head)
    while len(body) > length:
        body.pop()

    gx, gy = offset(pacman)
    if (gx,gy) not in tiles_map:
        tiles_map[(gx,gy)] = generate_tile(gx,gy)
    tile = tiles_map[(gx,gy)]

    if tile == 1:
        tiles_map[(gx,gy)] = 2
        state['score'] += 1
    elif tile == 3:
        tiles_map[(gx,gy)] = 2
        length += grow_amount
        state['score'] += 5
    elif tile == 4:
        tiles_map[(gx,gy)] = 2
        length = max(1, length - shrink_amount)
        state['score'] = max(0, state['score'] - 2)

    # redraw empty
    if tile in (1,3,4):
        x = gx*20 - 200
        y = 180 - gy*20
        square(x,y)

    # draw body
    for segment in body[1:]:
        up()
        goto(segment.x+10, segment.y+10)
        dot(18,'orange')

    # draw head
    up()
    goto(pacman.x+10, pacman.y+10)
    dot(20,'yellow')

    # ghost logic
    for point, course in ghosts:
        if valid(point + course):
            point.move(course)
        else:
            new = choice([vector(5,0),vector(-5,0),vector(0,5),vector(0,-5)])
            course.x, course.y = new.x, new.y

        up()
        goto(point.x+10, point.y+10)
        dot(20,'red')

    update() #SNT: This function essentially forces the game to redraw everthing to do the most updated versions. 

    for point, course in ghosts:
        """
        SNT:
        This for loop essentially check if the pacman had collided with a ghost. The for loop essentially check for each and every ghost
        In this game, each pac man and ghost is drawn as a circle of diameter of 20 pixles, or radius of 1o.
        As such when the distance between them is less than 20, it means they have colided.
        When this happens the function is interupted, and the game stops
        """
        if abs(pacman - point) < 20: #SNT: abs(pacman-point) is the distance between ghost and pacman, which is used to determine collisions.
            return #SNT: Interupt the game

    ontimer(move, 100)
    """
    SNT:
    ontimer() is turtle function which takes in a function with no arguments for its first argument. In this case this is the function move(), which is the same function it is in.
    The second arguments is the time intervals before the function in the first interval is re-called.
    What this does is essentially after move() has been called, move() would carries out all its task and called itself again every 100 ticks of the computers, and keep repeating.
    """


def change(x, y):
    """Change pacman aim if valid."""
    """
    SNT:
    this function takes in two arguments, and convert does two arguments into a vector.
    If then see if the pacman could validly moves x horizontally and y vertically, by using the if statment.
    If it could, it changes the aim vector of the pacman
    """
    if valid(pacman + vector(x, y)): #SNT: Check if the pacman could move x horixzontally and y vertically.
        aim.x = x #SNT: If it could, the pacman's aim vector is changed.
        aim.y = y


setup(420, 420, 370, 0) #SNT: This function opens and position the graphic windows which we can see the games with.
hideturtle() #SNT: This hides the turtle while it's drawing, allowing the graphic to appear smoother.
tracer(False) #SNT: If this is turns off, we can see the motion of the turtle drawing out each and every tiles and scores, and while it's very helpful to see what's the code is doing its not aesthetic.

"""
SNT:
The code block below essentially moves the turtle "writer" to where the games wants to write out the score.
This code block is needed to initialized the turtle "writer". Afterward, the function move() will be called and will call itself continously.
move() is also responsible to keep writing the score, so the code block doesn't need to be looped or rewrittern.
"""
writer.goto(160, 160)
writer.color('white')
writer.write(state['score'])



listen() #SNT: A turtle function that listen to any input into the module.
"""
SNT:
The turtle function onkey() takes in a function as its first arguement and a key press as its second arguement.
Here, the turtle changes the aim of the pacman according to which ever key is pressed.
As previously mentioned above, in the context of the game:
(5, 0) go right
(0, 5) go up
(0, -5) go down
(-5, 0) go left
"""
onkey(lambda: change(5, 0), 'Right')  #SNT: When the right arrow is pressed, the pacman turns right
onkey(lambda: change(-5, 0), 'Left') #SNT: When the left arrow is pressed, the pacman turns left
onkey(lambda: change(0, 5), 'Up') #SNT: When the up arrow is pressed, the pacman goes up
onkey(lambda: change(0, -5), 'Down') #SNT: When the down arrow is pressed, the pacman goes down

world() #SNT: Intialized the coordinates

"""
SNT:
move() is called.
As mentioned above and within the definition of move(): once move() is called, it will call itself again continously.
Apart from that, move() will write out the score, ensure the pacman moves in the direction choosen, the ghosts moves rnadomly, update tiles and "coins" eaten, and check for collision between pac man and ghost.
"""
move()


"""
SNT:
While at first, it appears weird that the game could play continously when done() is literally mentioned right after move().
However, since move() call itself upon being called, the code isn't actually being read beyond move(). Only when the pacman and the ghost collides, the functions returns and the progress to done() stopping the game.
done() actually stops the turtle programing that responsive for the game's graphic, but doesn't close the window. This allows the viewer to keep viewing.
"""
done()


