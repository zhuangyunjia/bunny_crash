import pygame
import random
import os
from pygame.locals import *


# initialization of pygame
pygame.init()

# screen display
SCREEN_WIDTH = 370
SCREEN_HEIGHT = 760

WIN = pygame.display.set_mode((370,760))
pygame.display.set_caption('insert name')
font = pygame.font.Font('freesansbold.ttf', 16)

# graphics
stone_image = pygame.image.load(os.path.join('./assets/stone.jpg')) #75, 130
bunny_image = pygame.image.load(os.path.join('./assets/bun.png')) #65, 120
bunny_width = 65
bunny_height = 120

background = (153, 204, 255)
back = pygame.image.load(os.path.join('./assets/easter.jpg')) 

left = 0
right = SCREEN_WIDTH-75
LEFT_x, LEFT_y = 0,0 #1
RIGHT_x, RIGHT_y = right, 0 #2

# resize by BLOCK_LEFT = pygame.transform.scale(BLOCK,LEFT, (100,100))
# rotate by .transform.rotate

lst_pos = []
n = 9999

for i in range(n):
    if random.randint(1,2) == 1:
        lst_pos.append(left)
    else:
        lst_pos.append(right)
    
def display_curr_score(curr_score):
    score_txt = font.render(f"{curr_score} m", True, (255, 255, 255))
    
    # set up background for score
    score_width = score_txt.get_width()
    score_height = score_txt.get_height()
    score_background = pygame.Rect((SCREEN_WIDTH-score_width)/2-10, 3*score_height-5, score_width+20, score_height+10)
    
    # display score and background
    pygame.draw.rect(WIN, (128,128,128), score_background)
    WIN.blit(score_txt, ((SCREEN_WIDTH-score_width) / 2, 3 * score_height))

    
def display_high_score(high_score):
    high_score_txt = font.render(f"HIGH SCORE: {high_score}", True, (255, 255, 255))
    high_score_width = high_score_txt.get_width()
    high_score_height = high_score_txt.get_height()
    high_score_background = pygame.Rect(0, 0, high_score_width+10, high_score_height+10)
    
    # display high score and background
    pygame.draw.rect(WIN, (128,128,128), high_score_background)
    WIN.blit(high_score_txt, (5,5))
    
def game_over(high_score):    
    over_font = pygame.font.Font('freesansbold.ttf', 45)
    over_text = over_font.render("GAME OVER!", True, (54, 100, 139, 255))
    over_width = over_text.get_width()
    WIN.blit(over_text, ((SCREEN_WIDTH-over_width) / 2, 150))
    
    restart_font = pygame.font.Font('freesansbold.ttf', 20)
    restart_text = restart_font.render("Press (r) to restart or (c) to close", True, (54, 100, 139, 255))
    restart_width = restart_text.get_width()
    WIN.blit(restart_text, ((SCREEN_WIDTH-restart_width) / 2, 250))
    
    pygame.display.update()
    
    # check if restarting game
    keys = pygame.key.get_pressed()
    if keys[pygame.K_r]:
        main(high_score)
        return False
    elif keys[pygame.K_c]:
        pygame.quit()
        return True


def main(high_score):
    active = True
    framerate = 60
    frame_count = 0
    
    chicken = pygame.Rect((SCREEN_WIDTH - bunny_width, 504, bunny_width, bunny_height))
    
    BLOCK0 = pygame.Rect(0, -10, 75, 130)
    BLOCK1 = pygame.Rect(0, -300, 75, 130)
    BLOCK2 = pygame.Rect(0, -600, 75, 130)
    BLOCK3 = pygame.Rect(0, -900, 75, 130)
    
    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(framerate)
        velocity = 5
        accel = 1
        
        WIN.fill(background)
        WIN.blit(back, (0, 0))
        WIN.blit(stone_image, (BLOCK0.x, BLOCK0.y))
        WIN.blit(stone_image, (BLOCK1.x, BLOCK1.y))
        WIN.blit(stone_image, (BLOCK2.x, BLOCK2.y))
        WIN.blit(stone_image, (BLOCK3.x, BLOCK3.y))
        
        # player
        #pygame.draw.rect(WIN, (0, 250, 200), chicken, 1)
        WIN.blit(bunny_image, (chicken.x, chicken.y))
        press = pygame.key.get_pressed()
        
        # score
        curr_score = frame_count // (framerate//6)
        display_curr_score(curr_score)
        display_high_score(high_score)
        
        # event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                active = False
            if event.type == pygame.KEYUP:   
                if event.key == pygame.K_LEFT and chicken.x == SCREEN_WIDTH - bunny_width and active:
                    chicken.move_ip(-(SCREEN_WIDTH - bunny_width), 0)
                elif event.key == pygame.K_RIGHT and chicken.x == 0 and active:
                    chicken.move_ip(SCREEN_WIDTH - bunny_width, 0)  
        
        # events
        if chicken.colliderect(BLOCK0) or chicken.colliderect(BLOCK1) or chicken.colliderect(BLOCK2) or chicken.colliderect(BLOCK3) or not active:
            active = False
            accel = 1
            game_over(high_score)
            
            # set best score if needed
            if curr_score > high_score:
                high_score = curr_score
            
        
        if active:
            frame_count += 1
            if (BLOCK0.y == 0):
                BLOCK1.y = -400
                BLOCK1.x = lst_pos.pop(0)
            
            if (BLOCK1.y == 0):
                BLOCK2.y = -400
                BLOCK2.x = lst_pos.pop(0)
                
            if (BLOCK2.y == 0):
                BLOCK3.y = -400
                BLOCK3.x = lst_pos.pop(0)
            
            if (BLOCK3.y == 0):
                BLOCK0.y = -400
                BLOCK0.x = lst_pos.pop(0)
            
            BLOCK0.y += velocity * accel
            BLOCK1.y += velocity * accel
            BLOCK2.y += velocity * accel
            BLOCK3.y += velocity * accel
    
        pygame.display.update()
        
        if frame_count % 20 == 0:
            accel *= 2
        
    pygame.quit()


if __name__ == "__main__":
    main(0)
