# imports
import random, time

# define dictionaries
from triples_list import *
player_one = {
  "current": [random.randint(-800, 800), random.randint(-800, 800)], # randomises player location
  "distance": 0.0,
  "gradient": 0.0,
  "midpoint": [0, 0],
  "personal": [[0,0],[0,0]] # sets two coordinates that are going to be the top left and bottom right of the personal space buffer.
}
player_two = {
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
def calculate_distance(point1, point2): # Gets two points and calculates the distance. Returns a float with 1 decimal.
  x1 = point1[0]
  y1 = point1[1]
  x2 = point2[0]
  y2 = point2[1]
  distance = (((x2 - x1) ** 2) + ((y2 - y1) ** 2)) ** 0.5 # Formula √((x2 – x1)² + (y2 – y1)²), using pythagoras theorem to find distance. **0.5 is to find square root.
  return round(distance, 1) # rounds the distance variable to 1 decimal place.

def calculate_midpoint(point1, point2): # Gets two points and calculates midpoint of them. Returns a list with a coordinate.
  x1 = point1[0]
  y1 = point1[1]
  x2 = point2[0]
  y2 = point2[1]
  midpoint_x = (x1 + x2) / 2 # find x of the midpoint by using average of x1 and x2.
  midpoint_y = (y1 + y2) / 2 # find y of the midpoint by using average of y1 and y2.
  return [midpoint_x, midpoint_y]

def calculate_gradient(point1, point2): # Gets two points and calculates the gradient of their line. Returns a float with 1 decimal.
  x1 = point1[0]
  y1 = point1[1]
  x2 = point2[0]
  y2 = point2[1]
  gradient = (y2 - y1) / (x2 - x1) # Formula (y2-y1)/(x2-x1)
  return round(gradient, 1) # rounds the gradient variable to 1 decimal place.

def calculate_space_buffer(point): # Calculates the space buffer of 10 units, returns two coords as a list: [[x,y],[x2,y2]] being top left and bottom right.
  buffer_side = 5 # Might be 10, check later
  return list

def print_stats(player_dict): # Gets a dictionary and prints the stats; PLAYER ONE Location, Distance to destination, Gradient with destination, Midpoint with other player
  print("""STATS""")

def check_if_won(player_num): # Gets an int of the player number (only 1 and 2) and checks if that player won. returns true or false.
  return bool

def draw_plane(): # redraws the cartesian plane with player points on top. 
  x_size = 1600 # size of the grid, -800 to 800
  y_size = 1600 # size of the grid, -800 to 800
  # something here to print cartesian plane. Pygame?

# Update dictionaries using the functions

# Main loop
print(calculate_distance([0,0],[0,3]))
print(calculate_midpoint([0,0],[0,3]))