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

"""
SNT Updated Games Rules:
I created a level version of this game.
"""
levels = 1 #ST: Initialize the level at one




state = {'score': 0} #SNT: Initialize the score board, as a dictionary
path = Turtle(visible=False) #SNT: Create an object called path, with the class of Turtle, whose visibility is turned off. This turtle is responsible to draw the world.
writer = Turtle(visible=False) #SNT: Create an object called writer, with the class of Turtle, whose visibility is turned off. This turtle is responsible for drawing pacman and ghosts.

def square(x, y, color = 'blue'):
    """Draw square using path at (x, y)."""
    """
    SNT: This functions esentially draw a square
    However, as will later be seen in world(), each time a tile is drawn, square() is called.
    This makes each a tile 20x20.
    """
    
    path.up() #SNT: allows the turtle "path" (which is a drawing pen, essentially) to lift up from the page and draw nothing
    path.goto(x, y) #SNT: moves the turtle "path" to the position (x, y) which is inputed into the 
    path.color(color)
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

"""
SNT Updated Game Rules:
In order to implement a level advancement system, we must determine whether or not the player has managed to reach the "portal" to the next level
Which is just a random cell.
We also want to keep track of all the score acquired between each level, so the score won't be wiped
"""

def advanced_level(row, column):
    """
    SNT Updated Games Rules:
    If the player reaches this tiles, then their level advances.
    """
    global levels
    current_tiles = offset(pacman)
    tiles_index = column + 20 * row #SNT: Convert the grids layout to the index with the list "tiles", which is used to store the map of the game
    if tiles_index == current_tiles:
        levels += 1
        

"""
SNT Updated games rules:
This is the first level of the games, which is the unchanged version.
"""
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
"""
SNT Updated Games rUles:
This will draw a redsquare in the top left corner, indicating an exit.
21 is the index within the list "tiles" which indicates the top left corner
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

def restart_level_1():
    """
    SNT Updated Game rules,
    This function essentially stores all the intial conditions for level 1.
    When it is called it resets everything.
    
    """

    global aim, pacman, ghosts, tiles, writer
    writer.undo()
    """
    SNT:
    Since the function requires to have the restart function it is neccesary to have it here.
    """
    aim = vector(5, 0) #SNT: Create an aiming vector with the value of [5, 0], which in the context of this games, is pointing to the right.
    pacman = vector(-40, -80) #SNT: Create a pacman vector with the value of [-40, -80]
    ghosts = [
        [vector(-180, 160), vector(5, 0)],
        [vector(-180, -160), vector(0, 5)],
        [vector(100, 160), vector(0, -5)],
        [vector(100, -160), vector(-5, 0)],
    ]
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
    #SNT: This next portion of the code essentially reset everything
    world()
    writer.goto(160, 160)
    writer.color('white')
    writer.write(state['score'])
    writer.write(state['score'])
    x_1 = (21 % 20) * 20 - 200 #SNT: The next three line redraw the tiles, this time without the "coins" in the middle, 21 was used because thats the index within the list "tiles" of the 
    y_1 = 180 - (21 // 20) * 20
    square(x_1, y_1, 'red')


def move():
    """Move pacman and all ghosts."""
    """
    SNT Updated Games Rules:
    While all the other functions has been moved outside of the if statement to optimize the game, this function is so crucial to each version of the game that it must be re-intialzied.
    """
    """
    SNT:
    The main purpose of this function is to move the pac man and the ghost around.
    However, some of the code here makes little sense out of the context which it is used.
    """
    global aim, pacman, ghosts, tiles, levels, move #SNT: This added, to make sure when the game restart, it actually reset the function
    
    writer.undo() #SNT: Undo the what the previous turtle "writer" wrote.
    
    """
    SNT:
    In the context in which move() is called, a few line above, the turtle "writer" is commanded to write out the score.
    As such writer.undo() erased any previously written out score.
    Furthermore, when move() is called, in itself is a function that keeps on calling move(). As such, move is continously called again and again.
    Therefore, having writer.undo() is neccesary to erased previously written scores.
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
    SNT Updated Game Rules:
    For level 1, I decided to make the top left corner to be an exit point.
    """
    advanced_level(1, 1) #SNT:The top left actually accesible corner is (1,1)
    
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
            In the context of this game, this function (move()) is called multiples time, continously in a game. If the ghost can't move in this turn, its velocity is randomly changed.
            The next time this function is called, the function re-elevaluate if that velocity vector would create a valid motion (aka: don't enter a wall). This keep occuring until a valid direction is randomly picked.
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
            restart_level_1()

    """
    SNT Updated Games Rules:
    Previously the ontimer(move, 100) is just executed until the games ends, however, here we only want it to be excuted if the level is correct.
    """
    if levels == 1:
        ontimer(move, 100)
        """
        SNT:
        ontimer() is turtle function which takes in a function with no arguments for its first argument. In this case this is the function move(), which is the same function it is in.
        The second arguments is the time intervals before the function in the first interval is re-called.
        What this does is essentially after move() has been called, move() would carries out all its task and called itself again every 100 ticks of the computers, and keep repeating.
        """
    if levels == 2:
            
        """
        SNT:
        Due to the mechanics of turles, we can't figure out to have seperate if statements for each levels.
        This is because done() is needed to run the games, so afterward, no code after done() will ever be excuted. As such, if statement can't be placed before done.
        However, move() are continously called prior to done(), and for some reason, if we put an if statment for level 2, there the games just stops when it reaches level 2.
        We couldn't figure out how to make it works.
        The only way it works -we found after extensive searching online- is to defined within move() an if statment that would redefined move.
        Then afterward the games runs smoothly.

        Essentially, move() is a function that will call upon itself continously until the games is completed.
        It is also a function that would rewrite itself when certain conditions is met, which intialized the next level.
        We're very sorry for the convuluted code but this is the only way it works.

        """
        move = move_2 
        move() #SNT: move(), despite being rewritten, do need to be called before ontimer(move, 1000) can take over.

#SNT: Since some portion of the code should only be executed, once, we created a count function 

count = 0
traveled = [] #SNT Updated: Initialized an empty list that would keep track of which path the pacman travelled in.

def move_2():
    """Move pacman and all ghosts."""
    """
    SNT: To make it easier to integrate everybody's code, we make sure to have everything reassigned so it's easier to make sure everything works toghether.
    We have the functions nestles like dolls like this because the game just doesn't work otherwise
    """
    global aim, pacman, ghosts, tiles, count, move
    if count == 0:
        """
        When move is rewritten, we want to reintialized all variables to create a new map.
        However, we don't want it reintialized every single time, so we use an external variable called count to keep track.
        """
        restart_level_1() #SNT: Since level 1 and level 2 shares the same map, I used the same function restart_level_1()
        count += 1

    
    """
    SNT: (Modified Game Rule)
    We decided to make a new feature where the pacman can't traveled on twice on a path it already traversed. This makes the player more comprehensive when moving around.
    This is accomplished, by changing the stored tile's value as 0 when the pacman encountered a travel tiles, which is 2.
    However, if we have it so that the game will change the path as the pacman goes, then the pacman just becomes immobolized. As such we have a set timer, that makes it so the game updated every so often.
    However, the the old path will become block when pacman ate a coin. This is intentional to avoid blocking the user too early.
    """
    def modified_game_rules():
        global traveled
        just_traveled_tiles = offset(pacman) #SNT: Track the index in the list "tiles" that the pacman currently in
        traveled.append(just_traveled_tiles) #create a list that track the path the pacman traveled
        if len(traveled) > 10:
            """
            SNT:
            This if statement check if the pacman has traveled more than 5 tiles.
            If it is, the first tile the pacman traveled is turned to a wall first. And as the pacman traveled further, the if statement is retriggered, the oldest tiles start becoming walls one by one.
            This accomplished using the list.pop(0) method which extract the first entry and shift everything up.
            This allows each of the tiles traveled to turn into a wall one at a time.
            """
            if tiles[traveled[0]] == 2:
                indice = traveled.pop(0) #SNT: Extract the oldest traveled tiles, and remove it from the list
                tiles[indice] = 0        
                x = (indice % 20) * 20 - 200 #SNT: The next three line redraw the tiles
                y = 180 - (indice // 20) * 20
                square(x, y, 'black')
        

    writer.undo() #SNT: Undo the what the previous turtle "writer" wrote.
    
    
    writer.write(state['score']) #SNT: Use the turtle "writer" to write out the new score of the game.

    clear()


    if valid(pacman + aim):
        pacman.move(aim)
        


    index = offset(pacman) #SNT: Locates the location of pacman on the pixel coordinates and returns its index in the list "tiles"

    if tiles[index] == 1:
        
        tiles[index] = 2 #SNT: Update the tile's stored value to 2, so the program knows we traveled over this tiles.

        state['score'] += 1 #SNT: The user score is increase by 1.
        
        """
        SNT Modified game Rules:
        By putting the modified_game_rules here it allows the traveled tiles to turn into walls as the pacman moves into a valid cell.
        This works because move() is being called repeatedly, and as such this function will be called as well.
        """
        modified_game_rules()

        x = (index % 20) * 20 - 200 #SNT: The next three line redraw the tiles, this time without the "coins" in the middle
        y = 180 - (index // 20) * 20
        square(x, y)
    
    advanced_level(1, 1)

    up()
    goto(pacman.x + 10, pacman.y + 10)
    dot(20, 'yellow')

    for point, course in ghosts:
    

        if valid(point + course): #check if the positions where the ghost is aheaded is a valid desitnation
            point.move(course)
            
        else:
            
            options = [ #SNT: Initialized a list "options", which contains 4 different cardinal velocity vectors
                vector(5, 0),
                vector(-5, 0),
                vector(0, 5),
                vector(0, -5),
            ]
            plan = choice(options) #SNT: A random cardinal velocity vector is picked from "options" and assigned to plan
            course.x = plan.x #SNT: The course vector is changed into the planned vector.
            course.y = plan.y
            
    
        up()
        goto(point.x + 10, point.y + 10) #SNT: Centered the turtle before drawing the red dot, marking the ghost.
        dot(20, 'red')
        

    update() #SNT: This function essentially forces the game to redraw everthing to do the most updated versions. 

    for point, course in ghosts:
        
        if abs(pacman - point) < 20: #SNT: abs(pacman-point) is the distance between ghost and pacman, which is used to determine collisions.
            restart_level_1() #SNT: Since level 1 and level 2 has the same set up, I do it to make it easier
    
    if levels == 2:
        ontimer(move, 100)
    if levels == 3:
        """
        SNT: This portion of the code is only activated when move() is rewriten by move_1()
        When levels is advnaced, move() is again rewritten into move_2
        """
        count = 0 #SNT: Restart the count for the next iteration of move
        traveled = [] #SNT: Reintialized traveled for the next iteration of move 
        move = move_3
        move()


def move_3():
           
    """Move pacman and all ghosts."""

    global aim, pacman, ghosts, tiles, count, move
    
    if count == 0:
        """
        SNT:
        """
        restart_level_1

        def modified_games_rules_2(traveled):
            """
            SNT Modified Games Rules:
            This function essentially keep track of all the tiles on which the pacman had traveled.
            It then spawn a new ghost at that location, moving in the opposite direction as the pacman.
            This function is then implemanted in the move() function.
            """
            just_traveled_tiles = offset(pacman)
            if not(just_traveled_tiles in traveled): #SNT UpdatedL Only update the list if the pacman traveled to a new cell
                traveled.append(just_traveled_tiles)

            if len(traveled) > 7:

                indice = traveled[0]
                x = (indice % 20) * 20 - 200 
                y = 180 - (indice // 20) * 20
                ghosts.append([vector(x, y), -aim]) #SNT Updated: Add a new ghost in the last location the pac man travel.

        count += 1
 

    
    writer.undo() #SNT: Undo the what the previous turtle "writer" wrote.
    
    
    writer.write(state['score']) #SNT: Use the turtle "writer" to write out the new score of the game.

    clear()

    if valid(pacman + aim):
        pacman.move(aim)

    index = offset(pacman) #SNT: Locates the location of pacman on the pixel coordinates and returns its index in the list "tiles"

    if tiles[index] == 1:
        
        tiles[index] = 2 #SNT: Update the tile's stored value to 2, so the program knows we traveled over this tiles.

        """
        SNT Modified Game Rules:
        To make it fairer for the players, we make it so that only when the pacman had eaten a coins would a new ghost be spawned.
        """
        modified_games_rules_2(traveled)

        state['score'] += 1 #SNT: The user score is increase by 1.
        x = (index % 20) * 20 - 200 #SNT: The next three line redraw the tiles, this time without the "coins" in the middle
        y = 180 - (index // 20) * 20
        square(x, y)

    advanced_level(1, 1)
    
    up()
    goto(pacman.x + 10, pacman.y + 10)
    dot(20, 'yellow')


    for point, course in ghosts:

        if valid(point + course): #check if the positions where the ghost is aheaded is a valid desitnation
            point.move(course)
        
        else:
            
            options = [ #SNT: Initialized a list "options", which contains 4 different cardinal velocity vectors
                vector(5, 0),
                vector(-5, 0),
                vector(0, 5),
                vector(0, -5),
            ]
            plan = choice(options) #SNT: A random cardinal velocity vector is picked from "options" and assigned to plan
            course.x = plan.x #SNT: The course vector is changed into the planned vector.
            course.y = plan.y
            
        
        up()
        goto(point.x + 10, point.y + 10) #SNT: Centered the turtle before drawing the red dot, marking the ghost.
        dot(20, 'red')
        

    update() #SNT: This function essentially forces the game to redraw everthing to do the most updated versions. 

    for point, course in ghosts:
        
        if abs(pacman - point) < 20: #SNT: abs(pacman-point) is the distance between ghost and pacman, which is used to determine collisions.
            restart_level_1() #Since level 3 and 2 shares the same map, we used the same function to restart.

    ontimer(move, 100)
    
    


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

x_1 = (21 % 20) * 20 - 200 #SNT: The next three line redraw the tiles, this time without the "coins" in the middle
y_1 = 180 - (21 // 20) * 20
square(x_1, y_1, 'red')
"""
SNT:
move() is called.
As mentioned above and within the definition of move(): once move() is called, it will call itself again continously.
Apart from that, move() will write out the score, ensure the pacman moves in the direction choosen, the ghosts moves rnadomly, update tiles and "coins" eaten, and check for collision between pac man and ghost.
"""
move()


mainloop()


