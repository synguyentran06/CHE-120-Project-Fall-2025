"""
HN: Haris Nasir {21184089
SNT: Sy Nguyen Tran (21120268)
HGT: Haogang (Hugo) Tang (21139238)
"""

"""
Note to Hugo and Haris
In order for this to work on Spyder, make sure that you type in on the bottom right window
pip install freegames

Note to future revision:
Confirm whether pacman.y + 10 shift the pacman up 10 in the context of the games or not
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
tiles = [
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


def offset(point):
    """Return offset of point in tiles."""
    """
    SNT:
    This function essentially takes in the pixel position of any object and convert it into one of the tiles, whose values can be searched
    up in the list "tiles".
    """
    x = (floor(point.x, 20) + 200) / 20
    y = (180 - floor(point.y, 20)) / 20
    """
    SNT:
    Each tiles is essentially 20x20 pixels. The floor(point.x, 20) and floor (point.y, 20)
    return a value which is an interger multples of 20 (ex: -40, -20, 0, 20, et.c) from the x and y positions of any input "point".
    When this value is divided by 20, it returned an integer (not int type, but like "math integer") which represent (x, y) position
    in the list "tiles" when represented as grid.
    On line 85, the 200 is the horizontal offset that the entire world is created in, so needed to be accounted for here.
    On line 86, the 180 is the vertical offset that the entire world is created in, so needed to be accounted here.
    Furthermore, on line 86, floor(point.y, 20) is subtracted since pixel increases in value as we go up vertically. However, the index in list "tiles"
    increases in value as we go down. Therefore, subtracting floor(point.y, 20) accounted for subtracting
    """
    index = int(x + y * 20)
    """
    SNT:
    Instead of storing the index as (x, y) where x is the x-th column of the list "tiles" and y as the y-th row of the lits "tiles",
    index is stored essentially as one ordinal the list "tiles" 
    To convert (x, y) to an ordinal, we noticed that every row has 20 entries. To skip down 3 rows, we add 3*20.
    To move sideways by 4 entries, we simply add 4.
    As such the general formula to convert (x, y) to an ordinal numbers is:
    (x, y) -> x + y * (number of entries per row) where 20 is the number of entries per row 
    """
    return index


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


def world():
    """Draw world using path."""
    bgcolor('black') #SNT: Set background color to black
    path.color('blue') #SNT: Set "path" colour to blue

    for index in range(len(tiles)): 
        """
        SNT:
        This for loop goes through each values of the list "tiles", and for each of the value, it draws a corresponding square tiles in pixles for us to view.
        If value of a tile in the list "tiles" is greater than zero, it draws a square using the square() function aboves.
        If the value is 1, the turtle "path" is lifted from the page and shift up 10 and horizontally 10, and white dot of 2 pixle is drawn, creating those coins that the pac man can eat.
        In the context of this game, 0 is wall, 1 is untraveled path, 2 is traveled path.
        """
        tile = tiles[index] 

        if tile > 0:
            x = (index % 20) * 20 - 200 #SNT: Convert the corresponding values from the list "tiles" to an actual tiles that hte user can see, refer to square()'s commenting for more information as they are the same thing.
            y = 180 - (index // 20) * 20 #SNT: Similar to the above
            square(x, y) #SNT: Draw the actual tiles

            if tile == 1:
                path.up() #SNT: If tile == 1, then the tutle "path" is lifted of the page, shifted and draw a dot acting as "coins" for the pac man to eat.
                path.goto(x + 10, y + 10) #SNT: To be noted, when the tile is drawn, it's always draw on the grid line. So when we shifted 10 up and 10 right, the "coins" is draw in center of the tiles
                path.dot(2, 'white')


def move():
    """Move pacman and all ghosts."""
    """
    SNT:
    The main purpose of this function is to move the pac man and the ghost around.
    However, some of the code here makes little sense out of the context which it is used.
    """
    writer.undo() #SNT: Undo the what the previous turtle "writer" wrote.
    """
    SNT:
    In the context in which move() is called, a few line above, the turtle "writer" is commanded to write out the score.
    As such writer.undo() erased any previously written out score
    """
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
        """
        SNT:
        This function checks if the pacman can moves to a certain place.
        Understanding that "pacman" and "aims" are both vectors, pactman + aim is essentially the position vector of where the pacman intends to go.
        valid(pacman + aim) check if the points are valid for the pacman to move into.
        pacman.move(aim) essentially moves pacman by aim. 
        """

    index = offset(pacman) #SNT: Locates the location of pacman on the pixel coordinates and returns its index in the list "tiles"

    if tiles[index] == 1:
        """
        SNT:
        This if statement check if the current location of the pacman is in an untraveled path. This allows the games to tally score
        This is accomplished if the tile's stored value at index in the list "tiles" is 1.
        If it is, the tile's stored value is changed to 2. And a score is added
        In the context of the game, 1 is untraveled path, 2 is travelled path.
        As such, if tiles has already been traveled, its value is 2 so this if statement won't be triggered, and no new points is added.
        """
        tiles[index] = 2 #SNT: Update the tile's stored value to 2, so the program knows we traveled over this tiles.

        state['score'] += 1 #SNT: The user score is increase by 1.
        x = (index % 20) * 20 - 200 #SNT: The next three line redraw the tiles, this time without the "coins" in the middle
        y = 180 - (index // 20) * 20
        square(x, y)

    """
    SNT:
    The next three line moves the turtle up and make it goes to a location 10 upward and 10 horizontally from the pacman vector.
    To be noted, within the context of this game, a position vector for pacman or ghost lays on gridlinnes, while their actual appearances needed to be in center of the tiles.
    As such, when pacman is drawn, the drawing coodinates is shifted up 10 and horizontally 10.
    """
    up()
    goto(pacman.x + 10, pacman.y + 10)
    dot(20, 'yellow')

    for point, course in ghosts:
        """
        SNT:
        This for loop go through each index of the list "ghost". Each time, it accessed and assigned first vector in the sublist in "point" and the second vector in the sublist in "course".
        "point" is essentially the position vectors of each ghosts.
        "course" is essentially the velocity vector's of each ghosts.
        """

        if valid(point + course): #check if the positions where the ghost is aheaded is a valid desitnation
            point.move(course)
            """
            SNT:
            In this portion of the if statement, valid(point + course) check if the new destination of the ghost is a valid point to move to.
            If it is, it will move there.
            """
        else:
            """
            SNT:
            This portion of the if statements would be activated if the ghost can't move according to its inset velocity vector since said its destination isn't a valid block.
            Instead, choice() is used to pick one of the random cardinal velocity vector stored in options, and replace the ghost's velocity vector.
            """
            options = [ #SNT: Initialized a list "options", which contains 4 different cardinal velocity vectors
                vector(5, 0),
                vector(-5, 0),
                vector(0, 5),
                vector(0, -5),
            ]
            plan = choice(options) #SNT: A random cardinal velocity vector is picked from "options" and assigned to plan
            course.x = plan.x #SNT: The course vector is changed into the planned vector.
            course.y = plan.y
            """
            SNT:
            In the context of this game, this function is called multiples time a game. If the ghost can't move in this turn, its velocity is randomly changed.
            The next time this function is called, the function re-elevaluate if that velocity vector would create a valid motion (aka: don't enter a wall). This keep occuring until a valid direction is picked.
            """
        """
        SNT:
        The next three lines of code essentially drawa the ghost as a red dot in the center of the square.
        For similar reasons the pac man describe above, the drawing location is 10 pixels up and horizontal.
        """
        up()
        goto(point.x + 10, point.y + 10) #SNT: Centered the turtle before drawing the red dot, marking the ghost.
        dot(20, 'red')
        

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


def change(x, y):
    """Change pacman aim if valid."""
    if valid(pacman + vector(x, y)):
        aim.x = x
        aim.y = y


setup(420, 420, 370, 0)
hideturtle()
tracer(False)
writer.goto(160, 160)
writer.color('white')
writer.write(state['score'])
listen()
onkey(lambda: change(5, 0), 'Right')
onkey(lambda: change(-5, 0), 'Left')
onkey(lambda: change(0, 5), 'Up')
onkey(lambda: change(0, -5), 'Down')
world()
move()
done()