# imports
import random, time, sys, pygame

# define dictionaries
from triples_list import *
player_one = {
  "name": "one", # only used for printing the stats
  "current": [0, 0], # sets current to origin for now
  "pygame_current": None,
  "colour": None,
  "distance": 0.0,
  "gradient": 0.0,
  "midpoint": [0, 0],
  "personal": 0 # 0 for now
}
player_two = { # This dictionary can act as the npc when in npc mode.
  "name": "two", # only used for printing the stats
  "current": [0, 0], # sets current to origin for now
  "pygame_current": None,
  "colour": None,
  "distance": 0.0,
  "gradient": 0.0,
  "midpoint": [0, 0],
  "personal": 0 # 0 for now
}

destination = {
  "current": [0, 0], # sets current to origin for now
  "pygame_current": None,
  "colour": None,
  "personal": 0 # 0 for now
}

# Pygame fuctions
pygame.init()
app_clock = pygame.time.Clock()

def create_app_window(width:int, height:int): # Creates app window, input with two int.
  pygame.display.set_caption("Game")
  app_dimensions = (width + 10, height + 10)
  app_surf = pygame.display.set_mode(app_dimensions)
  app_surf_rect = app_surf.get_rect()
  return app_surf, app_surf_rect

def app_surf_update(destination, player_one, player_two): # draws plane and players
  app_surf.fill("white") # Fill the display surface with white background.
  # draw the x and y axis
  pygame.draw.line(app_surf, 'grey', (0, app_surf_rect.height / 2),(app_surf_rect.width, app_surf_rect.height / 2), width = 1)
  pygame.draw.line(app_surf, 'grey',(app_surf_rect.width/2, 0),(app_surf_rect.width/2,app_surf_rect.height),width=1)
  # draw destination
  pygame.draw.circle(app_surf, destination['colour'], destination['pygame_current'], radius = player_size, width = player_size)
  # draw player one and player two
  pygame.draw.circle(app_surf, player_one['colour'], player_one['pygame_current'], radius = player_size, width = round(player_size * (2 / 3)))
  pygame.draw.circle(app_surf, player_two['colour'], player_two['pygame_current'], radius = player_size, width = round(player_size * (2 / 3)))

def refresh_window(): # This refreshes the display
  pygame.display.update()
  app_clock.tick(30)

def conv_cartesian_to_pygame_coords(x, y):
  pygame_x = x + app_surf_rect.width / 2
  pygame_y = -y + app_surf_rect.height / 2
  return(pygame_x, pygame_y)

def make_pygame_coords():
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

def update_dicts():
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

def reset_dicts():
  # reset current coordinates
  player_one["current"] = [random.randint(-size_of_grid, size_of_grid), random.randint(-size_of_grid, size_of_grid)] # resets the random coodinates
  player_two["current"] = [random.randint(-size_of_grid, size_of_grid), random.randint(-size_of_grid, size_of_grid)] # resets the random coodinates
  destination["current"] = [random.randint(-size_of_grid, size_of_grid), random.randint(-size_of_grid, size_of_grid)] # resets the random coodinates
  # For others
  update_dicts()

def print_stats(player_dict:dict, destination_dict:bool = None): # prints the stats; PLAYER x Location, Distance to destination, Gradient with destination, Midpoint with other player
  print(f"""
PLAYER {player_dict["name"].upper()} STATS:
Location: ({player_dict["current"][0]}, {player_dict["current"][1]})
Midpoint with player {"two" if player_dict["name"] == "one" else "one"}: ({player_dict["midpoint"][0]}, {player_dict["midpoint"][1]})
Distance to destination: {player_dict["distance"]} units
Gradient with destination: {player_dict["gradient"]}""")
  if destination_dict != None:
    print(f"Destination Location: {destination_dict["current"][0]}, {destination_dict["current"][1]}.")
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

def draw_plane(): # redraws the cartesian plane with player points on top. 
  x_size = 1600 # size of the grid, -800 to 800
  y_size = 1600 # size of the grid, -800 to 800
  # something here to print cartesian plane. Pygame?

def update_coords(x_add:int, y_add:int, player_num:int): # Translates the coordinates in a certain amount of x and certain amount of y.
  if player_num == 1:
    player_one["current"] = [player_one["current"][0] + x_add, player_one["current"][1] + y_add]
  elif player_num == 2:
    player_two["current"] = [player_two["current"][0] + x_add, player_two["current"][1] + y_add]
  elif player_num == 3: # NPC update as player 3
    pass

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
    return str(random.randint(5, 800)) + " " + str(random.randint(1, 8))
  # actual movement (direction)
  if gradient >= 0: # Means quadrant 1 or 3
    if gradient >= 1: # Means direction 2 or 6
      direction = "6" if npc_x < destination_x else "2"
    else: # Means direction 1 or 5
      direction = "5" if npc_x < destination_x else "1"
  else: # Means quadrant 4 or 2
    if gradient <= -1: # Means direction 7 or 3
      direction = "3" if npc_x < destination_x else "7"
    else: # Means direction 8 or 4
      direction = "4" if npc_x < destination_x else "8"
  # actual movement (distance)
  distance = round(distance)
  if distance > size_of_grid * 2:
    distance = size_of_grid * 2
  return str(distance) + " " + direction

# testing functions
# update_dicts()
# print_stats(player_one)
# print_stats(player_two)
# update_coords(100, 0, 1)
# 
  
# ----------------- MAIN CODE -----------------
print("Hello, welcome to this math game by Sean Chan!")

# Initalise some default settings
size_of_grid = 400
colour = ["red", "blue", "black"]
distance_to_win = 10
npc_mode = False
npc_difficulty = 3
player_size = 3

# Main loop
while True:
  # quits the display, this is for replaying.
  pygame.display.quit()

  # This is the main (text based) menu of the game
  menu = True
  while menu:
    userInput = input("Enter 'start' to start the game. Enter 'help' for additional commands: ").lower().strip() # inputs a command, removing spaces and making it lowercase.
    if userInput == "start": # checks what command it is a does it.
      print("Have fun! Starting...")
      menu = False
    elif userInput == "help":
      print("""
'help'     -> Displays all commands and what they do.
'start'    -> Starts a new round of the game.
'rules'    -> Prints the rules of the game.
'quit'     -> Quits this program. This can be done at any time (any input) in the game.
'settings' -> Shows some extra options to edit gameplay.
""")
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
  -> A NPC can also be added in the menu at a certain difficulty if wanted, by using "npc".
  -> This NPC can either be selected as a third player or a second player to play with by yourself.
4. MOVEMENT
  -> You can only move along the hypothenuse of a pythagorean triple.
  -> You will move by inputting a distance and a direction in the format 'distance<space>direction'
  -> Distance is the amount of units you want to travel.
  -> Direction is a number from 1 to 8, representing the quadrants of the cartesian plane cut in half.
  -> Cartesian direction means that 0 degrees is East and the positive direction is counter-clockwise.
""")
    elif userInput == "quit":
      print("Bye!\n")
      pygame.quit()
      sys.exit()
    elif userInput == "settings":
      extraRunning = True
      while extraRunning:
        print("""
Enter a command to edit:
'npc'         -> Toggles npc or no npc.
'npc.level'   -> Selects the difficulty of the npc. It defaults to 3 (the hardest).
'rounding'    -> Changes rounding to triple, up or down. (Not completed)
'size.grid'   -> Changes the size of the grid. This also changes the player coords to be random.
'size.player' -> Changes the size of the players and destination. Defaults to 3.
'colour'      -> Changes the colours of each player and destination on the display. Default is red, blue and black.
'personal'    -> Changes the buffer to win if touching either player or destination. (Not completed)
'time'        -> Changes the timeout for a player taking too long to move. Default is 10. (Not completed)
'back'        -> Go back to previous page.
""")
        editAnswer = input("Command: ").strip().lower()
        if editAnswer == "back":
          break
        elif editAnswer == "size.grid":
          sizeSelect = True
          while sizeSelect:
            sizeAnswer = input("Select the size of the grid. (100 to 800): ").strip()
            try:
              sizeAnswer = int(sizeAnswer)
            except:
              if sizeAnswer.lower() == "quit":
                pygame.quit()
                sys.exit()
              elif sizeAnswer.lower() in ["back", ""]:
                break
              else:
                print("Has to be a whole number. Try Again.")
                continue

            if sizeAnswer > 800 or sizeAnswer < 100:
              print("From 100 to 800. Try again.")
            else:
              size_of_grid = round(sizeAnswer/2)
              # Reset coordinates
              reset_dicts()

              print(f"Size of grid has been set to {str(sizeAnswer)}.")
              break
        elif editAnswer == "colour":
          back = False
          for i in range(3): # change to 4 after implementing npc.
            while True:
              colourSelect = input(f"Select a colour for {"player 1" if i == 0 else ("player 2" if i == 1 else "destination")}: ").strip().lower()
              if colourSelect in pygame.color.THECOLORS.keys(): # Checks if it is a real colour
                print(f"Colour {colourSelect} selected.")
                colour[i] = colourSelect
                break
              elif colourSelect == "quit":
                sys.exit()
              elif colourSelect in ["back", ""]:
                back = True
                break
              else:
                print("That is not a valid colour. See pygame documentation for whole list of colours.")
            if back:
              break
        elif editAnswer == "npc":
          if npc_mode == False:
            npc_mode = True
            if input("NPC mode has been turned on. Enter to continue: ").lower().strip() == "quit":
              sys.exit()
          else:
            npc_mode = False
            if input("NPC mode has been turned off. Enter to continue: ").lower().strip() == "quit":
              sys.exit()
        elif editAnswer == "npc.level":
          while True:
            levelSelect = input("Enter new difficulty of NPC. (1-3): ").strip()
            if levelSelect == "quit":
              sys.exit()
            try:
              levelSelect = int(levelSelect)
            except:
              print("Must be a number.")
              continue
            if levelSelect >= 1 and levelSelect <= 3:
              print(f"Successfully selected difficulty to be {levelSelect}.")
              npc_difficulty = levelSelect
              break
            else:
              print("Must be a number from 1 to 3.")
        elif editAnswer == "size.player":
          while True:
            sizePlayerAnswer = input("Select the size of the players and destination. (3 to 20): ").strip()
            try:
              sizePlayerAnswer = int(sizePlayerAnswer)
            except:
              if sizePlayerAnswer.lower() == "quit":
                pygame.quit()
                sys.exit()
              elif sizePlayerAnswer.lower() in ["back", ""]:
                break
              else:
                print("Has to be a whole number. Try Again.")
                continue

            if sizePlayerAnswer > 20 or sizePlayerAnswer < 3:
              print("From 3 to 20. Try again.")
            else:
              player_size = sizePlayerAnswer
              print(f"Size of players and destination has been set to {str(sizePlayerAnswer)}.")
              break
        elif editAnswer == "quit":
          pygame.quit()
          sys.exit()
        else: # add other functions later
          print("That is not a command. See list for details:")
    else:
      print("That is invalid. Enter 'help' for commands.")
  
  # After the menu, this is the game code.
  print("If you haven't read the rules, it is recommended as you won't know how to play. (hint: type 'rules' in menu)") # print out some early texts to show players.
  print(f"Player 1, you are {colour[0]}.")
  if npc_mode == True:
    print(f"The NPC is {colour[1]}.")
  else:
    print(f"Player 2, you are {colour[1]}.")
  print("Click the screen to start the game.") # tells players to click the screen

  # restart. this is for resetting the dictionaries
  reset_dicts()

  # testing variables
  # print(colour)
  # print(player_one["colour"])

  # Initalise pygame display
  app_surf, app_surf_rect = create_app_window(size_of_grid*2,size_of_grid*2)
  make_pygame_coords()
  app_surf_update(destination, player_one, player_two) # call the function to update the app surface with the new coordinates. Send it the entities
  refresh_window()

  # Start turns
  turn = 1
  gameInProgress = True
  while gameInProgress:

    # Pygame pump
    for event in pygame.event.get():
      if event.type == pygame.QUIT:   # must have this else the user can't quit.
        pygame.quit()
        sys.exit()
      if event.type == pygame.MOUSEBUTTONDOWN:
        if npc_move == False or turn == 1:
          # Get move from player.
          inputting = True
          while inputting:
            move = input(f"Player {turn}! Make your move: ")

            if "quit" in move.lower(): # just in case player wants to quit.
              print("Bye!\n")
              sys.exit()
            
            move = move.split(" ")

            try:
              distance = int(move[0])
              direction = int(move[1])
            except:
              print("Please enter in format 'distance<space>direction' where distance and directions are numbers.")
              continue
            
            if distance < 0:
              print("The distance was negative. Please re-enter.")
            elif distance < 5: # Just in case if it is less then 5
              print("The distance was less than 5. Please re-enter.")
            elif direction > 8 or direction < 1:
              print("The direction must be 1-8. Read rules for more details.")
            elif distance > size_of_grid * 2 or distance < 0:
              print(f"Distance must be from 0 to {size_of_grid * 2}.")
            else:
              inputting = False
        else: # If it is the NPC's turn
          print("NPC turn:", end=" ")
          time.sleep(1)
          move = npc_move(player_two["distance"], player_two["gradient"], npc_difficulty, player_two["current"][0], destination["current"][0])
          print(move)
          move = move.split(" ")

        # Find triple
        isFound = False
        for num in range(100): # The 100 here is to ensure a triple is picked.
          for triple in triples: # This loops through the dictionary with triples and finds the one that has the distance with hypothenuse matching.
            if triple[2] == (distance - num): # This checks for the triple with the distance with subtracting every time it is looped.
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
          update_coords(b, a, turn)
        elif direction <= 4: # if the direction is in the 2nd quadrant, a is negative and b is positive.
          a = -abs(a)
          b = abs(b)
          update_coords(a, b, turn)
        elif direction <= 6: # if the direction is in the 3rd quadrant, a and b are both negative
          a = -abs(a)
          b = -abs(b)
          update_coords(b, a, turn)
        elif direction <= 8: # if the direction is in the 4th quadrant, a is positive and b is negative.
          a = abs(a)
          b = -abs(b)
          update_coords(a, b, turn)

        # Update dictionaries and stats
        update_dicts()
        
        # Check for win and submit to variables and print accordingly.
        destinationWin = False
        playerWin = False
        if turn == 1: # prints the stats of the player.
          print_stats(player_one, destination)
          destinationWin = check_destination_win(player_one) # Check if the player won.
          playerWin = check_player_win(player_one, player_two)
        elif turn == 2:
          print_stats(player_two, destination)
          destinationWin = check_destination_win(player_two) # Check if the player won.
          playerWin = check_player_win(player_two, player_one)
        
        # Refresh screen
        make_pygame_coords()
        app_surf_update(destination, player_one, player_two) # call the function to update the app surface with the new coordinates. Send it the entities
        refresh_window()

        # Check if the player won
        if destinationWin: # Win by getting near destination
          if turn == 1: # Checks which player won.
            print_stats(player_two)
            lastInput = input("Player 1 won because they ended up near the destination! Enter to go back to menu.")
            if lastInput.lower().strip() == "quit": # Just in case they want to exit.
              pygame.quit()
              sys.exit()
            else:
              gameInProgress = False
              break
          elif turn == 2:
            print_stats(player_one)
            lastInput = input(f"{"Player 2" if npc_mode == False else "The NPC"} won because {"they" if npc_mode == False else "it"} ended up near the destination! Enter to go back to menu.")
            if lastInput.lower().strip() == "quit": # Just in case they want to exit.
              pygame.quit()
              sys.exit()
            else:
              gameInProgress = False
              break
        elif playerWin: # Win by getting near player
          if turn == 1: # Checks which player won.
            print_stats(player_two)
            lastInput = input(f"Player 1 won because they ended up near {"player 2" if npc_mode == False else "the NPC"}! Enter to go back to menu. ")
            if lastInput.lower().strip() == "quit": # Just in case they want to exit.
              pygame.quit()
              sys.exit()
            else:
              gameInProgress = False
              break
          elif turn == 2:
            print_stats(player_one)
            lastInput = input(f"{"Player 2" if npc_mode == False else "The NPC"} won because {"they" if npc_mode == False else "it"} ended up near player 1! Enter to go back to menu. ")
            if lastInput.lower().strip() == "quit": # Just in case they want to exit.
              pygame.quit()
              sys.exit()
            else:
              gameInProgress = False
              break
        
        
        # Change the turn 
        turn = 2 if turn == 1 else 1 # This changes the turns between 1 and 2.

        # Print the player whose turn it is and tell them to click
        if npc_mode == False or turn == 1:
          print(f"Player {turn}, click the screen to move. Close the display to quit.")
        else:
          print("It's the NPC's turn! Click to continue.")

    make_pygame_coords()
    app_surf_update(destination, player_one, player_two) # call the function to update the app surface with the new coordinates. Send it the entities
    refresh_window()
