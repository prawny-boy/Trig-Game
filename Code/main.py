# imports
import random, time

# define dictionaries
from Code.triples_list import *
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
  return float
def calculate_midpoint(point1, point2): # Gets two points and calculates midpoint of them. Returns a list with a coordinate.
  return list
def calculate_gradient(point1, point2): # Gets two points and calculates the gradient of their line. Returns a float with 1 decimal.
  return float
def calculate_space_buffer(point): # Calculates the space buffer of 10 units, returns two coords as a list: [[x,y],[x2,y2]]
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
