"""
HN: Haris Nasir {21184089
SNT: Sy Nguyen Tran (21120268)
HGT: Haogang (Hugo) Tang (21139238)
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

# fmt: on


def square(x, y):
    """Draw square using path at (x, y)."""
    
    
    path.up() #SNT: allows the turtle "path" (which is a drawing pen, essentially) to lift up from the page and draw nothing
    path.goto(x, y) #SNT: moves the turtle "path" to the position (x, y) which is inputed into the 
    path.color('blue') #SNT Updated: Added
    path.down() #SNT: This essentially put the turle "pen" down onto the page to begin to draw
    path.begin_fill() #SNT: This intializes the starting point of the shape that about to be draw by the turle "path"

    for count in range(4): #SNT: Allows this entire block to run a total of four times
        
        
        path.forward(20)
        path.left(90)

    path.end_fill() #SNT: This ends and fill the shape intialized on line 65 with color


def offset(point):
    """Return offset of point in tiles."""
    
    
    x = (floor(point.x, 20) + 200) / 20
    y = (180 - floor(point.y, 20)) / 20
    
    
    index = int(x + y * 20)
    
    return index


def valid(point):
    """Return True if point is valid in tiles."""
    #SNT: This function should only be given pixel coordinates.
    
    index = offset(point) #SNT: Index is assigned the index in the list "tiles" in which "point" reside.
    
    #SNT: Essentially, we captured the current location of the input "point".

    if tiles[index] == 0: 
        return False #SNT: If the tile in which "point" reside in correspond to a 0 in the list "tiles", then it's not valid. AKA, "point" is in a wall. 

    index = offset(point + 19)
    

    if tiles[index] == 0:
        return False
        
    #SNT: Here, we checked if this new position is also a wall.
    #SNT: This extra step essentially check if there's any collision at the "point" current location, and 19 pixels around it.

    return point.x % 20 == 0 or point.y % 20 == 0
    


def world():
    """Draw world using path."""
    bgcolor('black') #SNT: Set background color to black
    path.color('blue') #SNT: Set "path" colour to blue

    for index in range(len(tiles)): 
        
        
        tile = tiles[index] 

        if tile > 0:
            x = (index % 20) * 20 - 200 #SNT: Convert the corresponding values from the list "tiles" to an actual tiles that hte user can see, refer to square()'s commenting for more information as they are the same thing.
            y = 180 - (index // 20) * 20 #SNT: Similar to the above
            square(x, y) #SNT: Draw the actual tiles

            if tile == 1:
                path.up() #SNT: If tile == 1, then the tutle "path" is lifted of the page, shifted and draw a dot acting as "coins" for the pac man to eat.
                path.goto(x + 10, y + 10) #SNT: To be noted, when the tile is drawn, it's always draw on the grid line. So when we shifted 10 up and 10 right, the "coins" is draw in center of the tiles
                path.dot(2, 'white')
"""
SNT: (Modified game rules)
I copied and paste the square() function but tweak it a bit so it draw a black squares.
This is done so that the wall appears.
"""
def square_black(x, y):
    """Draw a black square using path at (x, y)."""
    """
    SNT: This functions esentially draw a square
    However, as will later be seen in world(), each time a tile is drawn, square() is called.
    This makes each a tile 20x20.
    """
    
    path.up() #SNT: allows the turtle "path" (which is a drawing pen, essentially) to lift up from the page and draw nothing
    path.goto(x, y) #SNT: moves the turtle "path" to the position (x, y) which is inputed into the 
    path.color('black')
    path.down() #SNT: This essentially put the turle "pen" down onto the page to begin to draw
    path.begin_fill() #SNT: This intializes the starting point of the shape that about to be draw by the turle "path"

    for count in range(4): #SNT: Allows this entire block to run a total of four times
        """
        SNT: The entire block essentially makes the turtle "path" goes straight 20 times, turns 90 degree left
        After completing this 4 times, the turle "path" essentially drew a square
        """
        
        path.forward(20)
        path.left(90)

    path.end_fill() #SNT: This ends and fill the shape intialized on with color
    #SNT: Since this function change the color of the path I added, an extra line in the square function to set the path color back to blue.















"""
SNT: (Modified Game Rule)
We decided to make a new feature where the pacman can't traveled on twice on a path it already traversed. This makes the player more comprehensive when moving around.
This is accomplished, by changing the stored tile's value as 0 when the pacman encountered a travel tiles, which is 2.
However, if we have it so that the game will change the path as the pacman goes, then the pacman just becomes immobolized. As such we have a set timer, that makes it so the game updated every so often.
However, the the old path will become block when pacman ate a coin. This is intentional to avoid blocking the user too early.
"""
traveled = [] #SNT Updated: Initialized an empty list that would keep track of which path the pacman travelled in.
def modified_game_rules():
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
            square_black(x, y)
    
















def move():
    """Move pacman and all ghosts."""
    
    
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
            return #SNT: Interupt the game
    ontimer(move, 100)
    


def change(x, y):
    """Change pacman aim if valid."""
   
    if valid(pacman + vector(x, y)): #SNT: Check if the pacman could move x horixzontally and y vertically.
        aim.x = x #SNT: If it could, the pacman's aim vector is changed.
        aim.y = y


setup(420, 420, 370, 0) #SNT: This function opens and position the graphic windows which we can see the games with.
hideturtle() #SNT: This hides the turtle while it's drawing, allowing the graphic to appear smoother.
tracer(False) #SNT: If this is turns off, we can see the motion of the turtle drawing out each and every tiles and scores, and while it's very helpful to see what's the code is doing its not aesthetic.


writer.goto(160, 160)
writer.color('white')
writer.write(state['score'])



listen() #SNT: A turtle function that listen to any input into the module.

onkey(lambda: change(5, 0), 'Right')  #SNT: When the right arrow is pressed, the pacman turns right
onkey(lambda: change(-5, 0), 'Left') #SNT: When the left arrow is pressed, the pacman turns left
onkey(lambda: change(0, 5), 'Up') #SNT: When the up arrow is pressed, the pacman goes up
onkey(lambda: change(0, -5), 'Down') #SNT: When the down arrow is pressed, the pacman goes down

world() #SNT: Intialized the coordinates

move()

done()

