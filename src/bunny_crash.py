import pygame
import random
import os
from pygame.locals import *

active = True

#initialization of pygame
pygame.init()

#screen display

SCREEN_WIDTH = 370
SCREEN_HEIGHT = 760

WIN = pygame.display.set_mode((370,760))
pygame.display.set_caption('insert name')
font = pygame.font.Font('freesansbold.ttf', 16)
active = True

FPS = 60

# player 80, 80
stone_image = pygame.image.load(os.path.join('stone.jpg')) #75, 130
#stone_image = pygame.transform.scale(stone, 0 , (75,90))

LEFT_x, LEFT_y = 0,0 #1
RIGHT_x, RIGHT_y = (370-75), 0 #2
left = 0
right = 370-75

# resize by BLOCK_LEFT = pygame.transform.scale(BLOCK,LEFT, (100,100))
# rotate by .transform.rotate

lst_tiles = []
lst_pos = []

n = 999

for i in range(n):
    lst_tiles.append(random.randint(1,2))

for i in range(len(lst_tiles)-1):
    if lst_tiles[i] == 1:
        lst_pos.append(left)
        
    elif lst_tiles[i] == 2:
        lst_pos.append(right)
    
        
def game_over(high_score):
    over_font = pygame.font.Font('freesansbold.ttf', 45)
    over_text = over_font.render("GAME OVER!", True, (54, 100, 139, 255))
    WIN.blit(over_text, (15, 150))
    
    restart_font = pygame.font.Font('freesansbold.ttf', 20)
    restart_text = restart_font.render("Press (r) to restart or (c) to exit", True, (54, 100, 139, 255))
    WIN.blit(restart_text, (25,250))
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
    
    chicken = pygame.Rect((290, 504, 80, 80))
    
    BLOCK0 = pygame.Rect(0, -10, 75, 130)
    BLOCK1 = pygame.Rect(0, -300, 75, 130)
    BLOCK2 = pygame.Rect(0, -600, 75, 130)
    BLOCK3 = pygame.Rect(0, -900, 75, 130)
    
    clock = pygame.time.Clock()
    run = True
    while run:
        
        clock.tick(framerate)
        
        WIN.fill((153, 204, 255))
        
        WIN.blit(stone_image, (BLOCK0.x, BLOCK0.y))
        WIN.blit(stone_image, (BLOCK1.x, BLOCK1.y))
        WIN.blit(stone_image, (BLOCK2.x, BLOCK2.y))
        WIN.blit(stone_image, (BLOCK3.x, BLOCK3.y))
        
        # player
        pygame.draw.rect(WIN, (0, 250, 200), chicken)
        press = pygame.key.get_pressed()
        
        # score
        curr_score = frame_count // (framerate//6) # 
        score_txt = font.render(f"{curr_score} m", True, (255, 255, 255))
        
        # set up background for score
        score_width = score_txt.get_width()
        score_height = score_txt.get_height()
        score_background = pygame.Rect((SCREEN_WIDTH-score_width)/2-10, 3*score_height-5, score_width+20, score_height+10)
        
        # display score and background
        pygame.draw.rect(WIN, (128,128,128), score_background)
        WIN.blit(score_txt, ((SCREEN_WIDTH-score_width) / 2, 3 * score_height))
        
        # high score
        high_score_txt = font.render(f"HIGH SCORE: {high_score}", True, (255, 255, 255))
        high_score_width = high_score_txt.get_width()
        high_score_height = high_score_txt.get_height()
        high_score_background = pygame.Rect(0, 0, high_score_width+10, high_score_height+10)
        
        # display high score and background
        pygame.draw.rect(WIN, (128,128,128), high_score_background)
        WIN.blit(high_score_txt, (5,5))

        frame_count += 1    
        
        
        # event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                active = False
            if event.type == pygame.KEYUP:   
                if event.key == pygame.K_j and chicken.x == 290 and active:
                    chicken.move_ip(-290, 0)

                elif event.key == pygame.K_l and chicken.x == 0 and active:
                    chicken.move_ip(290, 0)  
        
        # events
        if chicken.colliderect(BLOCK0) or chicken.colliderect(BLOCK1) or chicken.colliderect(BLOCK2) or chicken.colliderect(BLOCK3) or not active:
            active = False
            game_over(high_score)

            # reset score
            frame_count = 0
            # set best score if needed
            if curr_score > high_score:
                high_score = curr_score
        
        if active:
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
            
            BLOCK0.y += 5
            BLOCK1.y += 5
            BLOCK2.y += 5
            BLOCK3.y += 5

        pygame.display.update()
        
    pygame.quit()



if __name__ == "__main__":
    main(0)
