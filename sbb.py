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

# load the balls
ball_imgs = [pygame.image.load(f'./images/balloon{i}.png') for i in range(1,5)]
ball_sizes = [i.get_rect().size for i in ball_imgs]
# ball speeds. Larger faster
ball_speed_y = [i for i in range(-18, -8, 4)]
balls = []
# the first ball
balls.append({
    'x': 50, # x position
    'y': 50,
    'img_idx': 0, # imgage index
    'to_x': 3, # x direction
    'to_y': -6, 
    'init_spd_y': ball_speed_y[0]
})


# eventloop
running = True
while running:
    # set the frame rate
    delta = clock.tick(frame_rate)
    # for the weapon cooldown
    current_time = pygame.time.get_ticks()

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
        w[1] -= weapon_speed
    # remove projectiles when it hits the ceiling
    weapons = [w for w in weapons if w[1] > 0]

    # prevent the character from leaving the screen
    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width
    
    # adjust balls' positions
    for b in balls:
        ball_width = ball_sizes[b.get('img_idx')][0]
        ball_height = ball_sizes[b.get('img_idx')][1]
        # bounce the ball on x axis when it hits the walls
        if b.get('x') < 0 or b.get('x') > screen_width - ball_width:
            b['to_x'] *= -1
        # bounce the ball on y axis when it hits the stage
        if b.get('y') >= screen_height - stage_height - ball_height:
            b['to_y'] = b.get('init_spd_y')
        # apply the gravity
        else:
            b['to_y'] += 0.5
        # adjust the position of the ball
        b['x'] += b.get('to_x')
        b['y'] += b.get('to_y')

    
    screen.blit(background, (0, 0)) # draw the background
    # draw projectiles
    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon, (weapon_x_pos, weapon_y_pos))
    # draw balls
    for b in balls:
        screen.blit(ball_imgs[b.get('img_idx')], (b.get('x'), b.get('y')))
    screen.blit(stage, (0, screen_height-stage_height)) # draw the stage
    screen.blit(character, (character_x_pos, character_y_pos))
    pygame.display.update() # refresh the background

# end the game
pygame.quit()
