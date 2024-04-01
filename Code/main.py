# Imports
import random, time, sys, pygame # Imports needed libraries. 
# Random for selecting random coords and a way to calculate the npc move. 
# Time for making npc typing feel more realistic and timeout of inputs.
# Sys for system exit and timed input because it needs to be printed using sys.stdout.write().
# Pygame for visual depiction of display and timeout.
from termcolor import cprint, colored # Imports the module functions that prints in colour.
from triples_list import * # Imports the triple_list.

# define dictionaries
player_one = { # Player_one dictionary (initialise, so all is set to 0 or none)
  "name": "one", # only used for printing the stats
  "current": [0, 0], # sets current to origin for now
  "pygame_current": None, # Pygame coords of the player
  "colour": None, # Colour of the player to make it changeable
  "distance": 0.0, # Distance from destination
  "gradient": 0.0, # The gradient of the player from the destination
  "midpoint": [0, 0], # The midpoint between this player and the other player
  "personal": 0 # 0 for now, personal space buffer distance
}
player_two = { # Player 2 dictionary. This dictionary can act as the npc when in npc mode.
  "name": "two", 
  "current": [0, 0], 
  "pygame_current": None, 
  "colour": None,
  "distance": 0.0,
  "gradient": 0.0,
  "midpoint": [0, 0],
  "personal": 0 
}
destination = { # Destination dictionary.
  "current": [0, 0], 
  "pygame_current": None,
  "colour": None,
  "personal": 0 
}

print_colours = { # right is print colours, left is pygame colours that correspond to them. This is for printing in colours so that it corresponds to the actual display colours.
  "black": "dark_grey",
  "red": "red",
  "green": "green",
  "yellow": "yellow",
  "blue": "blue",
  "magenta": "magenta",
  "cyan": "cyan",
  "lightgrey": "white"
}

# Pygame fuctions
pygame.init() # Initialise pygame
app_clock = pygame.time.Clock() # Defines the clock (for pygame display)

def create_app_window(width:int, height:int): # Creates app window of the pygame display. Takes two integers and returns the application surface and rectangle.
  pygame.display.set_caption("Game") # Sets the caption of the game
  app_dimensions = (width + 10, height + 10) # Sets the dimensions
  app_surf = pygame.display.set_mode(app_dimensions) # Sets the app surface size to the dimensions
  app_surf_rect = app_surf.get_rect() # Gets the rectangle of the app surface.
  return app_surf, app_surf_rect # Returns the app surface and rectangle.

def app_surf_update(destination, player_one, player_two): # draws plane and players as dot on the visual display with a white background.
  app_surf.fill("white") # Fill the display surface with white background.
  # draw the x and y axis
  pygame.draw.line(app_surf, 'grey', (0, app_surf_rect.height / 2),(app_surf_rect.width, app_surf_rect.height / 2), width = 1)
  pygame.draw.line(app_surf, 'grey',(app_surf_rect.width / 2, 0),(app_surf_rect.width / 2, app_surf_rect.height), width = 1)
  # draw destination
  pygame.draw.circle(app_surf, destination['colour'], destination['pygame_current'], radius = player_size, width = player_size)
  # draw player one and player two as circles
  pygame.draw.circle(app_surf, player_one['colour'], player_one['pygame_current'], radius = player_size, width = round(player_size * (2 / 3)))
  pygame.draw.circle(app_surf, player_two['colour'], player_two['pygame_current'], radius = player_size, width = round(player_size * (2 / 3)))

def refresh_window(): # This refreshes the display every 30 ticks
  pygame.display.update()
  app_clock.tick(30)

def conv_cartesian_to_pygame_coords(x, y): # Converts normal coords to pygame coords because pygame's 0,0 is in the top left corner.
  pygame_x = x + app_surf_rect.width / 2
  pygame_y = -y + app_surf_rect.height / 2
  return(pygame_x, pygame_y)

def make_pygame_coords(): # Updates the pygame coords for each entity using their current coordinates.
  player_one['pygame_current'] = conv_cartesian_to_pygame_coords(player_one['current'][0], player_one['current'][1])
  player_two['pygame_current'] = conv_cartesian_to_pygame_coords(player_two['current'][0], player_two['current'][1])
  destination['pygame_current'] = conv_cartesian_to_pygame_coords(destination['current'][0], destination['current'][1])

# define functions to calculate distance, midpoint, gradient, space buffer and printing
def calculate_distance(point1:list, point2:list) -> float: # Gets two points and calculates the distance. Returns a float with 1 decimal.
  x1 = point1[0]
  y1 = point1[1]
  x2 = point2[0]
  y2 = point2[1]
  distance = (((x2 - x1) ** 2) + ((y2 - y1) ** 2)) ** 0.5 # Formula √((x2 – x1)² + (y2 – y1)²), using pythagoras theorem to find distance. **0.5 is to find square root.
  return round(distance, 1) # rounds the distance variable to 1 decimal place.

def calculate_midpoint(point1:list, point2:list) -> list: # Gets two points and calculates midpoint of them. Returns a list with a coordinate.
  x1 = point1[0]
  y1 = point1[1]
  x2 = point2[0]
  y2 = point2[1]
  midpoint_x = (x1 + x2) / 2 # find x of the midpoint by using average of x1 and x2.
  midpoint_y = (y1 + y2) / 2 # find y of the midpoint by using average of y1 and y2.
  return [midpoint_x, midpoint_y]

def calculate_gradient(point1:list, point2:list) -> float: # Gets two points and calculates the gradient of their line. Returns a float with 1 decimal.
  x1 = point1[0]
  y1 = point1[1]
  x2 = point2[0]
  y2 = point2[1]
  try: # does this unless error
    gradient = (y2 - y1) / (x2 - x1) # Formula (y2-y1)/(x2-x1)
    return round(gradient, 1) # rounds the gradient variable to 1 decimal place.
  except: # if there is a error, means that it is undefined
    gradient = "undefined"
    return gradient # returns the undefined value.

def update_dicts(): # Updates the dictionaries of each entity.
  # player 1 update
  player_one["distance"] = calculate_distance(destination["current"], player_one["current"])
  player_one["gradient"] = calculate_gradient(destination["current"], player_one["current"])
  player_one["midpoint"] = calculate_midpoint(player_one["current"], player_two["current"])
  # player 2 update
  player_two["distance"] = calculate_distance(destination["current"], player_two["current"])
  player_two["gradient"] = calculate_gradient(destination["current"], player_two["current"])
  player_two["midpoint"] = calculate_midpoint(player_two["current"], player_one["current"])
  # update colours
  player_one["colour"] = colour[0] # sets the colour of each player/destination
  player_two["colour"] = colour[1] # sets the colour of each player/destination
  destination["colour"] = colour[2] # sets the colour of each player/destination
  # update the personal space buffer
  player_one["personal"] = distance_to_win # sets the distance of the personal space buffer
  player_two["personal"] = distance_to_win # sets the distance of the personal space buffer
  destination["personal"] = distance_to_win # sets the distance of the personal space buffer
  # Update name of player_two
  if npc_mode:
    player_two["name"] = "npc"
  else:
    player_two["name"] = "two"

def reset_dicts(): # resets every entities' coordinates to random. and then updates the other parts, like distance using the new coordinates
  # reset current coordinates
  player_one["current"] = [random.randint(-size_of_grid, size_of_grid), random.randint(-size_of_grid, size_of_grid)] # resets the random coodinates
  player_two["current"] = [random.randint(-size_of_grid, size_of_grid), random.randint(-size_of_grid, size_of_grid)] # resets the random coodinates
  destination["current"] = [random.randint(-size_of_grid, size_of_grid), random.randint(-size_of_grid, size_of_grid)] # resets the random coodinates
  # For others, like gradient and distance
  update_dicts()

def print_stats(player_dict:dict, destination_dict:bool = None): # prints the stats with colour; PLAYER x Location, Distance to destination, Gradient with destination, Midpoint with other player
  print("")
  cprint(f"PLAYER {player_dict["name"].upper()} STATS:", player_dict["colour"], attrs=["bold"])
  cprint("Location:", player_dict["colour"], end=" ")
  print(f"({player_dict["current"][0]}, {player_dict["current"][1]})")
  cprint(f"Midpoint with player {"two" if player_dict["name"] == "one" else "one"}:", player_dict["colour"], end=" ")
  print(f"({player_dict["midpoint"][0]}, {player_dict["midpoint"][1]})")
  cprint("Distance to destination:", player_dict["colour"], end=" ")
  print(f"{player_dict["distance"]} units")
  cprint("Gradient with destination:", player_dict["colour"], end=" ")
  print(f"{player_dict["gradient"]}")
  if destination_dict != None:
    cprint(f"Destination Location:", destination_dict["colour"], end=" ")
    print(f"{destination_dict["current"][0]}, {destination_dict["current"][1]}.")
  print("")

def check_destination_win(player_dict:dict) -> bool: # Gets a player_dict and checks if that player won by reaching the destination. returns a boolean.
  if player_dict["distance"] <= player_dict["personal"]:
    return True
  else:
    return False

def check_player_win(player_dict:dict, other_player_dict:dict) -> bool: # Gets a player_dict and checks if that player won through getting into another player's space. returns a boolean.
  if calculate_distance(player_dict["current"], other_player_dict["current"]) <= player_dict["personal"]:
    return True
  else:
    return False
  
def check_if_win() -> bool: # Uses above 2 functions to check if a player/npc won.
  # Check for winning conditions and submit to variables that store if the player won
  if turn == 1: # prints the stats of the player.
    destinationWin = check_destination_win(player_one) # Check if the player won.
    playerWin = check_player_win(player_one, player_two) # Check if the player won.
  elif turn == 2:
    destinationWin = check_destination_win(player_two) # Check if the player won.
    playerWin = check_player_win(player_two, player_one) # Check if the player won.
  
  # check the variables, if the player won, print that they did and then go back to menu for replay or quitting.
  if destinationWin: # Win by getting near destination
    if turn == 1: # Checks which player won.
      print_stats(player_two)
      print(colored("Player 1 won because they ended up near the destination!", pcolour[turn-1], attrs=["bold"])) # print who won with colour and winning condition
      return True
    elif turn == 2:
      print_stats(player_one)
      print(colored(f"{"Player 2" if npc_mode == False else "The NPC"} won because {"they" if npc_mode == False else "it"} ended up near the destination!", pcolour[turn-1], attrs=["bold"])) # print who won with colour and winning condition
      return True
  elif playerWin: # Win by getting near player
    if turn == 1: # Checks which player won.
      print_stats(player_two)
      print(colored(f"Player 1 won because they ended up near {"player 2" if npc_mode == False else "the NPC"}!", pcolour[turn-1], attrs=["bold"])) # print who won with colour and winning condition
      return True
    elif turn == 2:
      print_stats(player_one)
      print(colored(f"{"Player 2" if npc_mode == False else "The NPC"} won because {"they" if npc_mode == False else "it"} ended up near player 1!", pcolour[turn-1], attrs=["bold"])) # print who won with colour and winning condition
      return True
  else:
    return False

def translate_coords(x_add:int, y_add:int, player_num:int, boundary:bool): # Translates the coordinates in a certain amount of x and certain amount of y.
  if player_num == 1:
    player_one["current"] = [player_one["current"][0] + x_add, player_one["current"][1] + y_add]
    if boundary: # stop from going out of screen
      if player_one["current"][0] > size_of_grid:
        player_one["current"][0] = size_of_grid
      elif player_one["current"][0] < -size_of_grid:
        player_one["current"][0] = -size_of_grid
      if player_one["current"][1] > size_of_grid:
        player_one["current"][1] = size_of_grid
      elif player_one["current"][1] < -size_of_grid:
        player_one["current"][1] = -size_of_grid
  elif player_num == 2:
    player_two["current"] = [player_two["current"][0] + x_add, player_two["current"][1] + y_add]
    if boundary: # stop from going out of screen
      if player_two["current"][0] > size_of_grid:
        player_two["current"][0] = size_of_grid
      elif player_two["current"][0] < -size_of_grid:
        player_two["current"][0] = -size_of_grid
      if player_two["current"][1] > size_of_grid:
        player_two["current"][1] = size_of_grid
      elif player_two["current"][1] < -size_of_grid:
        player_two["current"][1] = -size_of_grid

def npc_move(distance:float, gradient:float, difficulty:int, npc_x, destination_x) -> str: # calculates the move for the npc and returns str in the format distance<space>direction.
  # difficulty code
  randomised = False 
  if difficulty == 1:
    if random.randint(0, 2) == 0:
      randomised = True
  elif difficulty == 2:
    if random.randint(0, 5) == 0:
      randomised = True
  if randomised == True:
    return str(random.randint(5, size_of_grid * 2)) + " " + str(random.randint(1, 8))
  # actual movement (direction)
  try:
    if gradient >= 0: # Means quadrant 1 or 3
      if gradient >= 1: # Means direction 2 or 6
        direction = "2" if npc_x < destination_x else "6"
      else: # Means direction 1 or 5
        direction = "1" if npc_x < destination_x else "5"
    else: # Means quadrant 4 or 2
      if gradient <= -1: # Means direction 7 or 3
        direction = "7" if npc_x < destination_x else "3"
      else: # Means direction 8 or 4
        direction = "8" if npc_x < destination_x else "4"
  except: # Gradient is undefined
    direction = "3"
  # actual movement (distance)
  distance = round(distance)
  if distance > size_of_grid * 2:
    distance = size_of_grid * 2
  return str(distance) + " " + direction

def print_settings(): # Prints the settings of the game out nicely with colour.
  print("")
  print(f"NPC:              {colored("Off", "red", attrs=["bold"]) if npc_mode == False else colored("On", "green", attrs=["bold"])}, difficulty is {colored(npc_difficulty, "green", attrs=["bold"]) if npc_difficulty == 1 else (colored(npc_difficulty, "yellow", attrs=["bold"]) if npc_difficulty == 2 else colored(npc_difficulty, "red", attrs=["bold"]))}.")
  print(f"Rounding:         Currently set to round {colored(rounding_type, "red", attrs=["bold"]) if rounding_type == "down" else colored(rounding_type, "green", attrs=["bold"])}.")
  print(f"Grid Size:        {colored(size_of_grid, attrs=["bold", "underline"])} units.")
  print(f"Player Size:      {colored(player_size, attrs=["bold", "underline"])} pixels wide.")
  print(f"Destination Size: {colored(player_size, attrs=["bold", "underline"])} pixels wide.")
  print(f"Colours:          Player one is {colored(colour[0], print_colours[colour[0]])}, {"player 2" if npc_mode == False else "NPC"} is {colored(colour[1], print_colours[colour[1]])}, destination is {colored(colour[2], print_colours[colour[2]])}.")
  print(f"Win Buffer:       Get {colored(distance_to_win, attrs=["bold", "underline"])} units or nearer to the other player or destination to win.")
  print(f"Turn Timeout:     {colored(timeout, attrs=["bold", "underline"])} seconds.")
  print("")
  
# ----------------- MAIN CODE -----------------
print("----------------------------------------------")
cprint("Hello, welcome to this math game by Sean Chan!", "white", attrs=["bold"]) # Prints a welcome message in bold
print("----------------------------------------------")

# Initalise some default settings, can be modified in settings.
size_of_grid = 400 # The default size of the grid.
colour = ["red", "blue", "black"] # The default colours of the players and destination
pcolour = [print_colours[colour[0]], print_colours[colour[1]], print_colours[colour[2]]] # The default print colours of the player and destination, from the colour list
distance_to_win = 10 # The default distance needed (or less) to win.
npc_mode = False # The default is that npc is turned off.
npc_difficulty = 3 # The default of the npc is the hardest: 3
player_size = 3 # The default player size is 3 pixels wide, this is for drawing the players visually in pygame
rounding_type = "down" # The default rounding to a triple if the distance selected does not exist as a hypothenuse is down.
timeout = 10 # The timeout of a turn defaults at 10 seconds to move.
boundary_mode = True

# Main loop
while True: # so you can replay
  # quits the display, this is for replaying.
  pygame.display.quit()

  # This is the main (text based) menu of the game, where the user(s) can changed settings related to gameplay. Every input is checked for user error or if the user wants to quit. Printed also in colour.
  menu = True
  while menu: # Repeats until player inputs start.
    userInput = input("Enter 'start' to start the game. Enter 'help' for additional commands: ").lower().strip() # tells the player to input a command, removing spaces and making it lowercase.
    if userInput == "start": # checks what command it is a does it.
      menu = False
    elif userInput == "help": # shows what each command does.
      cprint("""
'help'     -> Displays all commands and what they do.
'start'    -> Starts a new round of the game.
'rules'    -> Prints the rules of the game.
'quit'     -> Quits this program. This can be done at any time (any input) in the game.
'settings' -> Shows some extra options to edit gameplay.
""", "dark_grey")
    elif userInput == "rules": # Instructions on the game.
      print("""
RULES:
1. SETUP
  -> This is a 2 player game. (A NPC can be turned on for 1 player to play with.)
  -> Each player is placed on a random point on a cartesian plane. (-800 to 800 both x and y)
  -> A destination will be also placed at a random point.
2. AIM
  -> The aim is to move your player into the destination's personal area of 10 units wide
  -> Or, move your player into another player's personal space of 10 units wide.
3. TURNS
  -> Each player will take turns to move, with player 1 starting first.
  -> A NPC can also be added in the menu at a certain difficulty if wanted, by using "npc" then "npc.level" in settings.
4. MOVEMENT
  -> You can only move along the hypothenuse of a pythagorean triple.
  -> You will move by inputting a distance and a direction in the format 'distance<space>direction'
  -> Distance is the amount of units you want to travel.
  -> Direction is a number from 1 to 8, representing the quadrants of the cartesian plane cut in half.
  -> Cartesian direction means that 0 degrees is East and the positive direction is counter-clockwise.
""")
    elif userInput == "quit": # if the user wants to quit
      pygame.quit()
      sys.exit()
    elif userInput == "settings": # if the user wants to change settings.
      while True: # display settings that can be changed, if they are entered, guide the user to change them.
        cprint("""
Enter a command to edit:
'npc'         -> Toggles npc or no npc. Default is no npc.
'npc.level'   -> Selects the difficulty of the npc. Default is 3. (the hardest)
'rounding'    -> Toggles rounding to triple, up or down. Default is down.
'size.grid'   -> Changes the size of the grid. This also changes the player coords to be random. The default is 400 pixels.
'size.player' -> Changes the size of the players and destination. Default is 3 pixels.
'colour'      -> Changes the colours of each player and destination on the display. Default is red, blue and black.
'personal'    -> Changes the buffer to win if near either player or destination. Default is 10 units.
'time'        -> Changes the timeout for a player taking too long to move. Default is 10 seconds.
'boundary     -> Toggles the boundary that doesn't let you out the screen. Default is on. (Not Completed)
'print'       -> Prints the current settings.
'back'        -> Go back to previous page.
""", "dark_grey")
        editAnswer = input("Command: ").strip().lower()
        if editAnswer == "back": # back to main menu
          break
        elif editAnswer == "size.grid": 
          sizeSelect = True
          while sizeSelect: # handles user input then changes the setting
            sizeAnswer = input("Select the size of the grid. (100 to 800): ").strip()
            try:
              sizeAnswer = int(sizeAnswer)
            except:
              if sizeAnswer.lower() == "quit":
                sys.exit()
              elif sizeAnswer.lower() in ["back", ""]:
                break
              else:
                cprint("Has to be a whole number. Try Again.", "red", attrs=["underline"])
                continue

            if sizeAnswer > 800 or sizeAnswer < 100:
              cprint("From 100 to 800. Try again.", "red", attrs=["underline"])
            else:
              size_of_grid = round(sizeAnswer / 2)
              cprint(f"Size of grid has been set to {str(sizeAnswer)}.", "green", attrs=["bold"])
              break
        elif editAnswer == "colour": # handles user input then changes the setting
          back = False 
          for i in range(3): # change to 4 after implementing npc.
            while True:
              colourSelect = input(f"Select a colour for {"player 1" if i == 0 else ("player 2" if i == 1 else "destination")}: ").strip().lower()
              if colourSelect in print_colours.keys(): # Checks if it is a real colour.
                cprint(f"Colour {colourSelect} selected.", print_colours[colourSelect], attrs=["bold"])
                colour[i] = colourSelect
                break
              elif colourSelect == "list": # displays the list of colours
                print("Here is a list of colours:")
                for c in print_colours.keys():
                  print(" " + c)
                print("")
              elif colourSelect == "quit":
                sys.exit()
              elif colourSelect in ["back", ""]:
                back = True
                break
              else:
                cprint("That is not a valid colour. Enter 'list' for a list of avaliable colours.", "red", attrs=["underline"])
            if back:
              break
          pcolour = [print_colours[colour[0]], print_colours[colour[1]], print_colours[colour[2]]] # refresh the pcolor variable to sync with the colour variable
        elif editAnswer == "npc": # handles user input then changes the setting
          if npc_mode == False:
            npc_mode = True
            if input(colored("NPC mode has been turned on. Enter to continue: ", "green", attrs=["bold"])).lower().strip() == "quit":
              sys.exit()
          else:
            npc_mode = False
            if input(colored("NPC mode has been turned off. Enter to continue: ", "green", attrs=["bold"])).lower().strip() == "quit":
              sys.exit()
        elif editAnswer == "npc.level": # handles user input then changes the setting
          while True:
            levelSelect = input("Enter new difficulty of NPC. (1-3): ").strip()
            if levelSelect == "quit":
              sys.exit()
            try:
              levelSelect = int(levelSelect)
            except:
              cprint("Must be a number.", "red", attrs=["underline"])
              continue
            if levelSelect >= 1 and levelSelect <= 3:
              cprint(f"Successfully selected difficulty to be {levelSelect}.", "green", attrs=["bold"])
              npc_difficulty = levelSelect
              break
            else:
              print("Must be a number from 1 to 3.", "red", attrs=["underline"])
        elif editAnswer == "size.player": # handles user input then changes the setting
          while True:
            sizePlayerAnswer = input("Select the size of the players and destination. (3 to 20): ").strip()
            try:
              sizePlayerAnswer = int(sizePlayerAnswer)
            except:
              if sizePlayerAnswer.lower() == "quit":
                sys.exit()
              elif sizePlayerAnswer.lower() in ["back", ""]:
                break
              else:
                cprint("Has to be a whole number. Try Again.", "red", attrs=["underline"])
                continue

            if sizePlayerAnswer > 20 or sizePlayerAnswer < 3:
              cprint("From 3 to 20. Try again.", "red", attrs=["underline"])
            else:
              player_size = sizePlayerAnswer
              cprint(f"Size of players and destination has been set to {str(sizePlayerAnswer)}.", "green", attrs=["bold"])
              break
        elif editAnswer == "personal": # handles user input then changes the setting
          while True:
            personalAnswer = input("Select the distance from the destination that you need to get to win. (0 to 100): ").strip()
            try:
              personalAnswer = int(personalAnswer)
            except:
              if personalAnswer.lower() == "quit":
                pygame.quit()
                sys.exit()
              elif personalAnswer.lower() in ["back", ""]:
                break
              else:
                cprint("Has to be a whole number. Try Again.", "red", attrs=["underline"])
                continue

            if personalAnswer > 100 or personalAnswer < 0:
              cprint("From 0 to 100. Try again.", "red", attrs=["underline"])
            else:
              distance_to_win = personalAnswer
              cprint(f"The distance needed to win has been set to {personalAnswer}.", "green", attrs=["bold"])
              break
        elif editAnswer == "rounding": # handles user input then changes the setting
          if rounding_type == "down":
            rounding_type = "up"
            if input(colored("Rounding has been set to up. Enter to continue: ", "green", attrs=["bold"])).lower().strip() == "quit":
              sys.exit()
          else:
            rounding_type = "down"
            if input(colored("Rounding has been set to down. Enter to continue: ", "green", attrs=["bold"])).lower().strip() == "quit":
              sys.exit()
        elif editAnswer == "print": # prints current settings
          print_settings()
          if input(colored("Enter to continue: ", "green", attrs=["bold"])).strip().lower() == "quit":
            sys.exit()
        elif editAnswer == "time": # handles user input then changes the setting
          while True:
            timeAnswer = input("Select the timeout for moving. (1 to 100 seconds): ").strip()
            try:
              timeAnswer = int(timeAnswer)
            except:
              if timeAnswer.lower() == "quit":
                sys.exit()
              elif timeAnswer.lower() in ["back", ""]:
                break
              else:
                cprint("Has to be a whole number. Try Again.", "red", attrs=["underline"])
                continue

            if timeAnswer > 100 or timeAnswer < 1:
              cprint("From 1 to 100. Try again.", "red", attrs=["underline"])
            else:
              timeout = timeAnswer
              cprint(f"Timeout for making a move has been set to {str(timeAnswer)}.", "green", attrs=["bold"])
              break
        elif editAnswer == "boundary":
          if boundary_mode == False:
            boundary_mode = True
            if input(colored("The boundary is off. Enter to continue: ", "green", attrs=["bold"])).lower().strip() == "quit":
              sys.exit()
          else:
            boundary_mode = False
            if input(colored("The boundary is on. Enter to continue: ", "green", attrs=["bold"])).lower().strip() == "quit":
              sys.exit()
        elif editAnswer == "quit":
          sys.exit()
        else: 
          cprint("That is not a command. See list for details:", "red", attrs=["underline"])
    else:
      cprint("That is invalid. Enter 'help' for commands.", "red", attrs=["underline"])
      print("------------------------------------------------------------------------")
  
  # After the menu, this is the game code for the actual game. Printed all stats in colour, handles user input and if they want to quit.
  cprint("If you haven't read the rules, it is recommended as you won't know how to play. (hint: type 'rules' in menu)", "white", attrs=["bold"]) # print out some early texts to show players.
  cprint(f"Player 1, you are {colour[0]}.", pcolour[0])
  if npc_mode == True:
    cprint(f"The NPC is {colour[1]}.", pcolour[1])
  else:
    cprint(f"Player 2, you are {colour[1]}.", pcolour[1])
  cprint("Click the screen to start the game.", attrs=["bold"]) # tells players to click the screen
  print("")

  # Restart. this is for resetting the dictionaries
  reset_dicts()

  # Initalise pygame display
  app_surf, app_surf_rect = create_app_window(size_of_grid * 2,size_of_grid * 2)
  make_pygame_coords()
  app_surf_update(destination, player_one, player_two) # call the function to update the app surface with the new coordinates. Send it the entities
  refresh_window()

  # Start turns
  turn = 1 # a variable to store whose turn it is
  gameInProgress = True # a variable that stores if the game is running
  inputting = False # a variable that stores if a real player is entering their move, for pygame input and timeout on input.
  calculation_needed = False # Stores if a player just moved and their turn movement needs to be calculated
  user_input = "" # stores the current input from the user, this is for pygame input.
  start_time = None # Stores when the input started.

  while gameInProgress: # While the game is running

    # Pygame pump so that it doesn't say not responding
    for event in pygame.event.get():
      if event.type == pygame.QUIT: # must have this else the user can't quit.
        pygame.quit()
        sys.exit()
      if event.type == pygame.MOUSEBUTTONDOWN: # if the screen is clicked, next turn starts
        if calculation_needed == False:
          inputting = True
          move = None
          if npc_mode == False or turn == 1: # If its a player's turn
            start_time = (pygame.time.get_ticks())/1000
        # NPC turn code
        if npc_mode == True and turn == 2: # If its the npc's turn, start its turn, otherwise ignore
          print("NPC turn:", end=" ")
          update_dicts()
          move = npc_move(player_two["distance"], player_two["gradient"], npc_difficulty, player_two["current"][0], destination["current"][0])
          for char in move:
            print(char, end="")
            sys.stdout.flush()
            time.sleep(random.random() / 2)
          print("")
          move = move.split(" ")
          distance = int(move[0])
          direction = int(move[1])
          inputting = False
          calculation_needed = True
      if event.type == pygame.KEYDOWN: # If a key is pressed
        if inputting == True: # If its supposed to be inputting as a player
          if npc_mode == False or turn == 1: # if its the player's turn
            
            # Player turn code
            if event.key == pygame.K_BACKSPACE: # If a backspace is pressed
              user_input = user_input[:-1] # Remove a letter
            elif event.key == pygame.K_RETURN: # If its entered
              move = user_input # Set move to the user input
              user_input = "" # Set the user input to a empty string
              if "quit" in move.lower(): # just in case player wants to quit.
                pygame.quit()
                sys.exit()
              move = move.split(" ") # splits the str to have 2 parts, distance and direction
              try: # More user error
                distance = int(move[0]) # sets the distance and direction
                direction = int(move[1]) 
              except: # user error
                cprint("Please enter in format 'distance<space>direction' where distance and directions are numbers.\n", pcolour[turn-1], attrs=["underline"])
                continue
              if distance < 0:
                cprint("The distance was negative. Please re-enter.\n", pcolour[turn-1], attrs=["underline"])
              elif distance < 5: # Just in case if it is less then 5
                cprint("The distance was less than 5. Please re-enter.\n", pcolour[turn-1], attrs=["underline"])
              elif direction > 8 or direction < 1:
                cprint("The direction must be 1-8. Read rules for more details.\n", pcolour[turn-1], attrs=["underline"])
              elif distance > size_of_grid * 2 or distance < 0:
                cprint(f"Distance must be from 0 to {size_of_grid * 2}.\n", pcolour[turn-1], attrs=["underline"])
              else:
                inputting = False # If not user error, turn inputting off
                calculation_needed = True # means that the player has inputted, waiting for the program to move the player.
            else:
              user_input += event.unicode # If any other key is pressed, add that key to the user input

    if calculation_needed == True: # Only occurs if a turn has been just entered/made.
      # Find triple
      if rounding_type == "up" and distance > 797: # Prevent from going up when its above the highest.
        distance = 797
      
      isFound = False # isfound is set to false.
      for num in range(100): # The 100 here is to ensure a triple is picked.
        for triple in triples: # This loops through the dictionary with triples and finds the one that has the distance with hypothenuse matching.
          if rounding_type == "down": # If the type of rounding is down
            if triple[2] == (distance - num): # This checks for the triple with the distance with subtracting every time it is looped.
              a = triple[0] # if the triple is matching, save the a and b sides.
              b = triple[1]
              isFound = True # allows us to break from the second loop.
              break
          else: # If the type of rounding is up
            if triple[2] == (distance + num): # This checks for the triple with the distance with adding every time it is looped.
              a = triple[0] # if the triple is matching, save the a and b sides.
              b = triple[1]
              isFound = True # allows us to break from the second loop.
              break
        if isFound == True: # only occurs if the triple is found
          break

      # Use direction to move to a coordinate.
      if direction % 2 == 0: # if the direction is even, flip a and b.
        a, b = b, a # flips the variables so a=b and b=a
      if direction <= 2: # if the direction is in the 1st quadrant, a and b are positive.
        a = abs(a)
        b = abs(b)
        translate_coords(b, a, turn, boundary_mode) # translates the player coords
      elif direction <= 4: # if the direction is in the 2nd quadrant, a is negative and b is positive.
        a = -abs(a)
        b = abs(b)
        translate_coords(a, b, turn, boundary_mode) # translates the player coords
      elif direction <= 6: # if the direction is in the 3rd quadrant, a and b are both negative
        a = -abs(a)
        b = -abs(b)
        translate_coords(b, a, turn, boundary_mode) # translates the player coords
      elif direction <= 8: # if the direction is in the 4th quadrant, a is positive and b is negative.
        a = abs(a)
        b = -abs(b)
        translate_coords(a, b, turn, boundary_mode) # translates the player coords

      # Update dictionaries and stats
      update_dicts()

      if turn == 1:
        print_stats(player_one, destination) # print the stats of player 1 if it is their turn
      elif turn == 2:
        print_stats(player_two, destination) # Print the stats of player 2 if it is their turn

      # Check if that player won, if the did, go back to menu.
      if check_if_win():
        gameInProgress = False # leaves the current game and goes back into the main menu
        break
      
      # Change the turn 
      turn = 2 if turn == 1 else 1 # This changes the turns between 1 and 2 so it can loop back again for the next player's turn.

      # Print the player whose turn it is and tell them to click
      if npc_mode == False or turn == 1:
        cprint(f"Player {turn}, click the screen to move. Close the display to quit.", pcolour[turn-1])
      else:
        cprint("It's the NPC's turn! Click to continue.", pcolour[turn-1])
      
      # Make sure that the turn is not done 2 times
      calculation_needed = False
      start_time = None

    # If no player clicked the screen for that tick, refresh the screen
    make_pygame_coords() # Update the pygame_coords
    app_surf_update(destination, player_one, player_two) # call the function to update the app surface with the new coordinates. Send it the entities
    refresh_window() # Refreshes the window.
    
    # Simulate input
    if inputting:
      print("\033[A                                                                  \033[A") # Clear the last line and put the cursor on that line.
      print(colored(f"Player {turn}, make your move: ") + user_input) # Print that looks like "input"
    
    if start_time != None:
      if (pygame.time.get_ticks() / 1000) - start_time >= timeout: # if the time since the input started is past the timeout time
        move = str(random.randint(5, size_of_grid * 2)) + " " + str(random.randint(1, 8)) # pick random triple
        print("Timeout! Picking random triple:", move) # print that a random triple was selected
        time.sleep(1) # sleep for 1 sec before doing the turn so that the player can see what happened
        calculation_needed = True # so that the next time it loops the player moves
        inputting = False # inputting is set to false so key presses won't do anything
        move = move.split(" ") # splits move into a list
        distance = int(move[0]) # sets distance and direction
        direction = int(move[1])