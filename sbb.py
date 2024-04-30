import pygame

# initialize pygame
pygame.init()

# screen setup
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))

# title setup
pygame.display.set_caption('Super Buster Bros')

# frame rate
clock = pygame.time.Clock()
frame_rate = 60

# load the background
background = pygame.image.load('./images/background.png')

# load the stage
stage = pygame.image.load('./images/stage.png')
stage_size = stage.get_rect().size
stage_height = stage_size[1] # to put the character on the stage

# load the character
character  = pygame.image.load('./images/character.png')
character_size = character.get_rect().size # rectangular shape
character_width = character_size[0]
character_height = character_size[1]
# character initial position
character_x_pos = screen_width/2 - character_width/2 
character_y_pos = screen_height - stage_height - character_height
character_speed = 0.3

# load the weapon
weapon = pygame.image.load('./images/weapon.png')
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]
# can fire multiple projectiles
weapons = []
weapon_speed = 10
weapon_cooldown = 500
last_shot_time = 0

# # load the enemy
# enemy  = pygame.image.load('./images/enemy.png')
# character_size = character.get_rect().size # rectangular shape
# character_width = character_size[0]
# character_height = character_size[1]

# eventloop
running = True
while running:
    # set the frame rate
    delta = clock.tick(frame_rate)
    # for the weapon cooldown
    current_time = pygame.time.get_ticks()
    
    print()

    for event in pygame.event.get(): # cheking events
        if event.type == pygame.QUIT: # if the event is QUIT
            running = False

    # check for pressed keys
    keys = pygame.key.get_pressed()
    # adjust the speed according to the frame rate by multiplying with delta
    if keys[pygame.K_LEFT]:
        character_x_pos -= character_speed * delta
    if keys[pygame.K_RIGHT]:
        character_x_pos += character_speed * delta
    if keys[pygame.K_SPACE] and current_time - last_shot_time > weapon_cooldown:
        weapon_x_pos = character_x_pos + character_width/2 - weapon_width/2
        weapon_y_pos = character_y_pos 
        weapons.append([weapon_x_pos, weapon_y_pos])
        last_shot_time = current_time
    # adjust weapons' y positions
    for w in weapons:
        w[1] = w[1] - weapon_speed

    # prevent the character from leaving the screen
    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width

    screen.blit(background, (0, 0)) # draw the background
    screen.blit(stage, (0, screen_height-stage_height)) # draw the stage
    # draw weapons
    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon, (weapon_x_pos, weapon_y_pos))
    screen.blit(character, (character_x_pos, character_y_pos))
    pygame.display.update() # refresh the background

# end the game
pygame.quit()
