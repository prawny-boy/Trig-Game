import pygame, sys, random, time

pygame.init()
game_clock = pygame.time.Clock()
game_font = pygame.font.SysFont('calibri', 24)

def create_game_window():
  pygame.display.set_caption('I dont know this')
  window_width = 900
  window_height = 500
  window_dimensions = (window_width, window_height)
  display_surface = pygame.display.set_mode(window_dimensions)
  display_surface_rect = display_surface.get_rect()
  return display_surface, display_surface_rect

def update_game_window():
  pygame.display.update()
  game_clock.tick(30)

def create_the_ground(display_surf_rect):
  ground_height = 100
  ground_dimensions = (display_surf_rect.width, ground_height)
  ground_surface = pygame.Surface(ground_dimensions)
  ground_surface_rect = ground_surface.get_rect()
  ground_surface_rect.bottomleft = display_surf_rect.bottomleft
  ground_surface.fill('green2')
  return ground_surface, ground_surface_rect

def create_the_dino(ground_surf_rect):
  dino_width = 80
  dino_height = 85
  dino_dimensions = (dino_width, dino_height)
  dino_surface = pygame.Surface(dino_dimensions)
  dino_surface_rect = dino_surface.get_rect()
  dino_surface_rect.bottomleft = ground_surf_rect.topleft
  dino_img = pygame.image.load('OneDrive - education.wa.edu.au/Documents/School/Y8/Maths/CAT/Testing/dino.png').convert()
  dino_surface.blit(dino_img, (0,0))
  return dino_surface, dino_surface_rect

def move_the_dino(ground_surf_rect, pressed_keys, dino_surf_rect, list_of_several_cacti):
  movement_increment = 10
  if pressed_keys[pygame.K_RIGHT] and dino_surf_rect.right < ground_surf_rect.right:
    dino_surf_rect.left += movement_increment
  if pressed_keys[pygame.K_LEFT] and dino_surf_rect.left > ground_surf_rect.left:
    dino_surf_rect.left -= movement_increment
  
  for cactus_dict in list_of_several_cacti:
    if dino_surf_rect.colliderect(cactus_dict['rect']):
      pygame.display.set_caption('GAME OVER... QUITTING...')
      time.sleep(2)
      pygame.quit()
      sys.exit()

def make_dino_jump(ground_surf_rect, pressed_keys):
  if pressed_keys[pygame.K_SPACE] and dino_surf_rect.bottom == ground_surf_rect.top:
    jumping_variables['amount'] = 30
  
  jumping_variables['amount'] -= jumping_variables['gravity']
  dino_surf_rect.top -= jumping_variables['amount']
  if dino_surf_rect.bottom >= ground_surf_rect.top:
    dino_surf_rect.bottom = ground_surf_rect.top


def create_one_cactus (ground_surf_rect):
  cactus_width = 60
  cactus_height = 72
  cactus_dimensions = (cactus_width, cactus_height)
  cactus_surface = pygame.Surface(cactus_dimensions)
  cactus_surface_rect = cactus_surface.get_rect() 
  cactus_surface_rect.bottomright = ground_surf_rect.topright
  cactus_img = pygame.image.load('OneDrive - education.wa.edu.au/Documents/School/Y8/Maths/CAT/Testing/cactus.png').convert()
  cactus_surface.blit(cactus_img, (0,0))
  return cactus_surface, cactus_surface_rect

def move_the_cactus(cactus_surface_rect, level):
  movement_increment = -4 * level
  cactus_surface_rect.left += movement_increment
  return cactus_surface_rect


def create_several_cacti (number, ground_surf_rect): 
  list_of_cacti = []
  start_x_coord = ground_surf_rect.width / 2
  for i in range(number):
    current_cactus = {}
    x_coord = start_x_coord + random.randint(200, 400)
    cactus_surf, cactus_surf_rect = create_one_cactus(ground_surf_rect)
    cactus_surf_rect.left = x_coord
    current_cactus['surf'] = cactus_surf
    current_cactus['rect'] = cactus_surf_rect
    list_of_cacti.append(current_cactus)
    start_x_coord = x_coord
  return list_of_cacti

# main program
  
display_surf, display_surf_rect = create_game_window()
background_colour = 'white'

ground_surf, ground_surf_rect = create_the_ground(display_surf_rect)
dino_surf, dino_surf_rect = create_the_dino(ground_surf_rect)

list_of_several_cacti = create_several_cacti(5, ground_surf_rect)

jumping_variables = {'amount': 0, 'gravity': 2}

score = 0
score_increment = 1
score_colour = 'black'
level = 1
game_is_running = True

while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()
  display_surf.fill(background_colour)

  pressed_keys = pygame.key.get_pressed()

  move_the_dino(ground_surf_rect, pressed_keys, dino_surf_rect, list_of_several_cacti)
  make_dino_jump(ground_surf_rect, pressed_keys)

  for cactus in list_of_several_cacti:
    move_the_cactus(cactus['rect'], level)

  score_string = 'Level: '+str(score)+'      Score: '+str(score)
  score_string_surf = game_font.render(score_string, True, score_colour, background_colour)
  display_surf.blit(score_string_surf, (10, 10))

  for i in range(len(list_of_several_cacti)):
    if list_of_several_cacti[i]['rect'].right <display_surf_rect.left: 
      score += score_increment
      del(list_of_several_cacti[i])
      break

  if len(list_of_several_cacti) == 0:
    list_of_several_cacti = create_several_cacti(5, ground_surf_rect)
    score_increment += 1
    level += 1


  display_surf.blit(dino_surf, dino_surf_rect)
  display_surf.blit(ground_surf, ground_surf_rect)

  for cactus in list_of_several_cacti:
    display_surf.blit(cactus['surf'], cactus['rect'])
  
  update_game_window()