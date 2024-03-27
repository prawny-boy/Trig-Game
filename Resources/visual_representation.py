### PLACE THE IDE WINDOW (VS Code or PyCharm) SIDE BY SIDE WITH THE APP WINDOW THAT OPENS WHEN YOU HIT RUN. ###
# that way you can see the commands you are typing and their effect on the screen
# click the window once to select it, then click it again with left or right mouse button to make a move.

# if you improve my code in a way that you are really proud of, share it back with me :)

import pygame                       # Engine for visual Mathematical Modeling
import sys                          # so that we can exit the app
import random                       # to generate coordinates

pygame.init()                       # initialise the engine
app_clock = pygame.time.Clock()     # allows us to set the refresh rate in frames per second

def create_app_window(width, height):
    print(f'\nWelcome. The plane goes from -{width/2} to {width/2} in both the x and y directions')
    pygame.display.set_caption("<App Name> TBD")           # Email me with a suggestion of what we should name this app/game. 
    app_dimensions = (width + 10, height + 10)             # to give a bit of margin. -400 to 400 both ways
    app_surf = pygame.display.set_mode(app_dimensions)     # create the main display surface for us to draw on
    app_surf_rect = app_surf.get_rect()                    # get a rectangle with important coordinates of the display surface.
    return app_surf, app_surf_rect # so that they can be used outside the function. At the moment they are local variables

def app_surf_update(destination, player_one, player_two):
    app_surf.fill('white') # fill the display surface with white background colour

    # draw the x-axis and the y-axis
    # pygame.draw.line() needs the display surfaceto draw on, colour of the line, starting coordinates and ending coordinates
    pygame.draw.line(app_surf, 'grey',(0,app_surf_rect.height/2),(app_surf_rect.width,app_surf_rect.height/2),width=1)
    pygame.draw.line(app_surf, 'grey',(app_surf_rect.width/2, 0),(app_surf_rect.width/2,app_surf_rect.height),width=1)
    
    # draw destination
    # pygame.draw.circle() needs the surface to draw on, colour, coordinates, circle radius and line width
    pygame.draw.circle(app_surf, 'black',destination['pygame_coords'], radius = 3, width = 3)

    # draw player one and player two
    pygame.draw.circle(app_surf, player_one['colour'], player_one['pygame_coords'], radius = 3, width = 2)
    pygame.draw.circle(app_surf, player_two['colour'], player_two['pygame_coords'], radius = 3, width = 2)

def refresh_window():
    pygame.display.update() # refresh the screen with what we drew inside the app_surf_update() function
    app_clock.tick(24)      # tell pygame to refresh the screen 24 times per second

def conv_cartesian_to_pygame_coords(x,y):
    # pygame's coordinate system has the origin at the top left corner which is weird (they have good reasons for this)
    # x values increase to the right and y values increase going DOWN which is backwards!
    # we need to move the x coordinate to the center which is easy - just add half a window width
    # for the y coordinate, we need to first negate it, then move it down half a window height
    pygame_x = x + app_surf_rect.width / 2
    pygame_y = -y + app_surf_rect.height /2
    return(pygame_x, pygame_y)              # return the 'weird' coordinates that pygame can use

def initialise_entities():
    # initially set the requested coordinates to random values
    # each time you call randint() you get new random coords
    p1_rand_x, p1_rand_y = random.randint(-400,400), random.randint(-400,400)
    player_one['cartesian_coords'] = (p1_rand_x, p1_rand_y)     # store the random cartesian coordinates
    player_one['pygame_coords'] = conv_cartesian_to_pygame_coords(p1_rand_x, p1_rand_y) # convert and store pygame coordinates

    p2_rand_x, p2_rand_y = random.randint(-400,400), random.randint(-400,400)
    player_two['cartesian_coords'] = (p2_rand_x, p2_rand_y)
    player_two['pygame_coords'] = conv_cartesian_to_pygame_coords(p2_rand_x, p2_rand_y)

    dest_rand_x, dest_rand_y = random.randint(-400,400), random.randint(-400,400)
    destination['cartesian_coords'] = (dest_rand_x, dest_rand_y)
    destination['pygame_coords'] = conv_cartesian_to_pygame_coords(dest_rand_x, dest_rand_y)
    # no need to return entities. They are dictionaries so the function can modify them directly (see the Python Functions tutorial on Connect Notices)


# ********** MAIN PROGRAM ************* #
player_one={
    'name': 'Player One',
    'cartesian_coords':None, # not set yet. 'None' is special in Python.
    'pygame_coords':None,
    'colour':'red',
}

# you need to store the distance and gradient to destination as well as midpoint to the other player.

player_two={
    'name': 'Player Two',
    'cartesian_coords':None, 
    'pygame_coords':None,
    'colour':'blue',
}

destination={
    'name': 'Destination',
    'cartesian_coords':None,
    'pygame_coords':None,
    'colour':'black',
}

# create the app window
app_surf, app_surf_rect = create_app_window(800, 800)
# these two are now global variables that everyone can access

initialise_entities()

print('\nThree entities initialised... here is a raw printout of their dictionaries')
print(destination)
print(player_one)
print(player_two)
print('\nLEFT click inside the window to make player ONE move')
print('RIGHT click inside the window to make player TWO move')
print('You might need to first click the window to select it, then L/R click to make a move')

# GAME LOOP #
while True:                             # The gameplay happens in here. Infinite loop until the user quits or a player wins"
    for event in pygame.event.get():    # scan through all 'events' happening to the window such as mouse clicks and key presses
        if event.type == pygame.QUIT:   # must have this else the user can't quit!
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:    # if a mouse button is down
            left_button, middle_button, right_button = pygame.mouse.get_pressed()   # get the state of the mouse buttons
            if left_button == True:     # if the left button was pressed, ask for player 1 new coordinates (for you, you must ask for distance and direction!)
                requested_x, requested_y = input("Enter new coordinates for Player ONE: e.g. 60, -155: ").split(",") # You neeed to ask for distance and direction
                requested_x = int(requested_x)
                requested_y = int(requested_y)
                player_one['cartesian_coords'] = (requested_x, requested_y)
                player_one['pygame_coords'] = conv_cartesian_to_pygame_coords(requested_x, requested_y)
            if right_button == True:    # if the right buttom was pressed, as for player two's request (you must has for distance and direction)
                requested_x, requested_y = input("Enter new coordinates for Player TWO: e.g. 60, -155: ").split(",") # You need to ask for distance and direction
                requested_x = int(requested_x)
                requested_y = int(requested_y)
                player_two['cartesian_coords'] = (requested_x, requested_y)
                player_two['pygame_coords'] = conv_cartesian_to_pygame_coords(requested_x, requested_y)
                # If you plan to use some or all of my code in your investigation, email me with the subject line of you want to name the game. Be creative :)
            
    app_surf_update(destination, player_one, player_two)    # call the function to update the app surface with the new coordinates. Send it the entities
    refresh_window()            # now refresh the window so that our changes are visible. Loop back to while True.