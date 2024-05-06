import pygame
import asyncio

# initialize pygame
pygame.init()
# screen setup
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))
# frame rate
clock = pygame.time.Clock()
frame_rate = 30

async def main():
    # for game messages
    game_font = pygame.font.Font(None, 40)
    total_time = 60
    start_ticks = pygame.time.get_ticks() # start time

    # title setup
    pygame.display.set_caption('Super Buster Bros')

    

    # load the background
    background = pygame.image.load('./images/background.jpg')

    # load the character
    character  = pygame.image.load('./images/character.png')
    character_size = character.get_rect().size # rectangular shape
    character_width = character_size[0]
    character_height = character_size[1]
    # character initial position
    character_x_pos = screen_width/2 - character_width/2 
    character_y_pos = screen_height - character_height
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
    ball_speed_y = [i for i in range(-18, -8, 3)]
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
    # things need to be removed
    weapon_to_remove = -1
    ball_to_remove = -1



    # game result message
    game_result = "Game Over"
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
            if b.get('y') >= screen_height - ball_height:
                b['to_y'] = b.get('init_spd_y')
            # apply the gravity
            else:
                b['to_y'] += 0.5
            # adjust the position of the ball
            b['x'] += b.get('to_x')
            b['y'] += b.get('to_y')

        # collision check
        character_rect = character.get_rect() # update the character pos
        character_rect.left = character_x_pos
        character_rect.top = character_y_pos

        # flag to escape from the nested loop
        flag = False
        for b_idx, b in enumerate(balls):
            # update the ball pos
            b_rect = ball_imgs[b.get('img_idx')].get_rect()
            b_rect.left = b.get('x')
            b_rect.top = b.get('y')
            # the character and the ball collision check
            if character_rect.colliderect(b_rect):
                running = False
                break

            for w_idx, w in enumerate(weapons):
                # update the projectile pos
                w_rect = weapon.get_rect()
                w_rect.left = w[0]
                w_rect.top = w[1]
                # the ball and the projectile collision check
                if b_rect.colliderect(w_rect):
                    ball_to_remove = b_idx
                    weapon_to_remove = w_idx
                    # split the ball if it is not the smallest
                    if b.get('img_idx') < 3:
                        # smaller ball image index
                        sb_idx = b.get('img_idx') + 1
                        
                        # the larger ball width and height
                        lb_width = b_rect.size[0]
                        lb_height = b_rect.size[1]
                        # the smaller ball width and height
                        sb_rect_size = ball_imgs[sb_idx].get_rect().size
                        sb_width = sb_rect_size[0]
                        sb_height = sb_rect_size[1]
                        
                        # 2 smaller balls appear from the center of the larger ball
                        # left smaller ball
                        balls.append({
                            'x': b.get('x') + (lb_width/2) - (sb_width/2), # x position
                            'y': b.get('y') + (lb_height/2) - (sb_height/2),
                            'img_idx': sb_idx, # imgage index
                            'to_x': -3, # x direction
                            'to_y': -6, 
                            'init_spd_y': ball_speed_y[sb_idx]
                        })
                        # right smaller ball
                        balls.append({
                            'x': b.get('x') + (lb_width/2) - (sb_width/2), # x position
                            'y': b.get('y') + (lb_height/2) - (sb_height/2),
                            'img_idx': sb_idx, # imgage index
                            'to_x': 3, # x direction
                            'to_y': -6, 
                            'init_spd_y': ball_speed_y[sb_idx]
                        })
                    flag = True
                    break
            # when the projectile hits the ball, break the loop and remove the ball first
            if flag:
                break
        
        # remove objects that has collided
        if ball_to_remove > -1:
            del balls[ball_to_remove]
            ball_to_remove = -1
        if weapon_to_remove > -1:
            del weapons[weapon_to_remove]
            weapon_to_remove = -1
        
        # all balls eliminated
        if len(balls) == 0:
            game_result = 'Mission Complete'
            running = False

        screen.blit(background, (0, 0)) # draw the background
        # draw projectiles
        for weapon_x_pos, weapon_y_pos in weapons:
            screen.blit(weapon, (weapon_x_pos, weapon_y_pos))

        # draw balls
        for b in balls:
            screen.blit(ball_imgs[b.get('img_idx')], (b.get('x'), b.get('y')))

        # screen.blit(stage, (0, screen_height-stage_height)) # draw the stage
        screen.blit(character, (character_x_pos, character_y_pos))

        # calculate the elapsed time and draw on the screen
        elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000 # ms -> s
        timer = game_font.render("Time : {}".format(int(total_time - elapsed_time)), True, (255, 255, 255))
        screen.blit(timer, (10, 10))

        # time over
        if total_time - elapsed_time <= 0:
            game_result = "Time Over"
            running = False
        
        pygame.display.update() # refresh the background

    # draw the end of the game message
    msg = game_font.render(game_result, True, (255, 255, 0)) 
    msg_rect = msg.get_rect(center=(int(screen_width / 2), int(screen_height / 2)))
    screen.blit(msg, msg_rect)
    pygame.display.update()

    await asyncio.sleep(0)
    # end the game
    pygame.time.delay(2000) # 2000 ms
    # pygame.quit()
    

asyncio.run(main())
