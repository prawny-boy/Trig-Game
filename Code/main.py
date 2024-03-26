# imports
import random, time, sys

# define dictionaries
from triples_list import *
player_one = {
  "name": "one",
  "current": [random.randint(0,0), random.randint(0,0)], # randomises player location
  "distance": 0.0,
  "gradient": 0.0,
  "midpoint": [0, 0],
  "personal": [[0,0],[0,0]] # sets two coordinates that are going to be the top left and bottom right of the personal space buffer.
}
player_two = {
  "name": "two",
  "current": [random.randint(-800, 800), random.randint(-800, 800)], # randomises player location
  "distance": 0.0,
  "gradient": 0.0,
  "midpoint": [0, 0],
  "personal": [[0,0],[0,0]] # sets two coordinates that are going to be the top left and bottom right of the personal space buffer.
}
destination = {
  "current": [random.randint(-800, 800), random.randint(-800, 800)], # randomises player location
  "personal": [[0,0],[0,0]] # sets two coordinates that are going to be the top left and bottom right of the personal space buffer.
}

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

def calculate_space_buffer(point:list) -> list: # Calculates the space buffer of 10 units, returns two coords as a list: [[x,y],[x2,y2]] being top left and bottom right.
  buffer_side = 5
  return list

def update_dicts():
  # player 1 update
  player_one["distance"] = calculate_distance(destination["current"], player_one["current"])
  player_one["gradient"] = calculate_gradient(destination["current"], player_one["current"])
  player_one["midpoint"] = calculate_midpoint(player_one["current"], player_two["current"])
  player_one["personal"] = [[0,0],[0,0]] # change later
  # player 2 update
  player_two["distance"] = calculate_distance(destination["current"], player_two["current"])
  player_two["gradient"] = calculate_gradient(destination["current"], player_two["current"])
  player_two["midpoint"] = calculate_midpoint(player_two["current"], player_one["current"])
  player_two["personal"] = [[0,0],[0,0]] # change later

def print_stats(player_dict:dict): # prints the stats; PLAYER x Location, Distance to destination, Gradient with destination, Midpoint with other player
  print(f"""
PLAYER {player_dict["name"].upper()} STATS:
Location: ({player_dict["current"][0]}, {player_dict["current"][1]})
Midpoint with player {"two" if player_dict["name"] == "one" else "one"}: ({player_dict["midpoint"][0]}, {player_dict["midpoint"][1]})
Distance to destination: {player_dict["distance"]} units
Gradient with destination: {player_dict["gradient"]}
""")

def check_destination_win(player_dict:dict) -> bool: # Gets a player_dict and checks if that player won by reaching the destination. returns a boolean.
  return bool

def check_player_win(player_dict:dict) -> bool: # Gets a player_dict and checks if that player won through getting into another player's space. returns a boolean.
  return bool

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

# testing functions
# update_dicts()
# print_stats(player_one)
# print_stats(player_two)

# Main loop
print("Hello, welcome to this math game by Sean Chan!")
while True:

  # This is the main (text based) menu of the game
  menu = True
  while menu:
    userInput = input("Enter 'start' to start the game. Enter 'help' for additional commands: ").lower().strip() # inputs a command, removing spaces and making it lowercase.
    if userInput == "start": # checks what command it is a does it.
      print("Have fun! Starting...")
      menu = False
    elif userInput == "help":
      print("""
'help' -> Displays all commands and what they do.
'start' -> Starts a new round of the game.
'rules' -> Prints the rules of the game.
'quit' -> Quits this program.
'npc' -> adds a npc with a certain difficulty. You are also able to select 3 player or 2 player mode with this.
""")
    elif userInput == "rules": # Instructions on the game.
      print("""
RULES:
1. SETUP
  -> This is a 2 player game.
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
      sys.exit()
    elif userInput == "npc":
      print("That has not been completed yet. Please try again in later versions.")
    else:
      print("That is invalid. Enter 'help' for commands.")
  
  # After the menu, this is the game code.
  input("If you haven't read the rules, it is recommended as you won't know how to play. ")
  turn = 1
  gameInProgress = True
  while gameInProgress:

    # Get move from player.
    move = input(f"Player {turn}! Make your move: ")
    if "quit" in move.lower(): # just in case player wants to quit.
      print("Bye!\n")
      sys.exit()
    move = move.split(" ")
    distance = int(move[0])
    direction = int(move[1])

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
    
    turn += 1 if turn != 2 else 1 # This changes the turns between 1 and 2.