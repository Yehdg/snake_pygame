import pygame
import random
import sys
import os

pygame.init()
width = 600
height = 600

white = (255, 255, 255)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

#建立視窗
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Snake GAME")

#時間
clock = pygame.time.Clock()

if getattr(sys, 'frozen', False):
    # 如果是打包後的exe
    base_path = os.path.dirname(sys.executable)
else:
    # 開發階段
    base_path = os.path.dirname(__file__)

HIGHSCORE_FILE = os.path.join(base_path, "highscore.txt")

# 如果沒有就先建立
if not os.path.exists(HIGHSCORE_FILE):
    with open(HIGHSCORE_FILE, "w") as f:
        f.write("0")

# 讀取高分
with open(HIGHSCORE_FILE, "r") as f:
    content = f.read().strip()
    try:
        high_score = int(content) if content else 0
    except ValueError:
        high_score = 0

snake_block = 10
snake_speed = 15
wall_thickness = 10 

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

def my_score(score,high_score):
    value = score_font.render(f"Score: {score}  High Score: {high_score}",True, white)
    screen.blit(value, [0, 0]) 

def my_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(screen, white, [x[0], x[1], snake_block, snake_block])

def update_high_score(current_score):
    global high_score
    if current_score > high_score:
        high_score = current_score
        with open(HIGHSCORE_FILE, "w") as f:
            f.write(str(high_score))

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    screen.blit(mesg, [width / 6, height / 3])


def gameLoop():
    global snake_speed, high_score
    game_over = False
    game_close = False

    snake_list = []
    length_of_snake = 1 #初始長度

    x1 = width / 2
    y1 = height / 2

    x1_change = 0
    y1_change = 0
   
    def generate_food():
        while True:
            foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0

            valid_x = (foodx >= wall_thickness and foodx <= width - wall_thickness - snake_block)
            valid_y = (foody >= 50 + wall_thickness and foody <= height - wall_thickness - snake_block)

            if valid_x and valid_y:
                return foodx, foody
    foodx, foody = generate_food()

    while not game_over:
        while game_close:
            screen.fill(green)
            message("Game Over!Press the C-Play or Q-Quit",red)
            my_score(length_of_snake - 1, high_score)
            pygame.display.update()
            update_high_score(length_of_snake-1)#更新歷史高分

            for event in pygame.event.get():
                if event.type == pygame.QUIT: #按下關閉視窗的叉叉
                    #update_high_score(length_of_snake-1)
                    game_over = True
                    game_close = False
                        
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        #update_high_score(length_of_snake-1)
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        #update_high_score(length_of_snake-1)
                        gameLoop()
                    

        for event in pygame.event.get():
            if event.type == pygame.QUIT: #按下關閉視窗的叉叉
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                if event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                if event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                if event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0
        if x1 >= width or x1 < 0 or y1 >= height or y1 < 0: #檢查蛇頭是否超出寬、高的邊界
            game_close = True
              
        x1 += x1_change
        y1 += y1_change
        screen.fill(black)
        
        
        # 上牆
        pygame.draw.rect(screen, blue, [0, 50, width, wall_thickness])
        # 下牆
        pygame.draw.rect(screen, blue, [0, height - wall_thickness, width, wall_thickness])
        # 左牆
        pygame.draw.rect(screen, blue, [0, 50, wall_thickness, height])
        # 右牆
        pygame.draw.rect(screen, blue, [width - wall_thickness, 50, wall_thickness, height])
        #食物
        pygame.draw.rect(screen, green, [foodx, foody, snake_block, snake_block])

        snake_head = [x1, y1]
        snake_list.append(snake_head)
        
        if len(snake_list) > length_of_snake:
            del snake_list[0] #刪掉尾巴
        for x in snake_list[:-1]:
            if x == snake_head:
                game_close = True

        my_snake(snake_block, snake_list)
        my_score(length_of_snake - 1, high_score)
        pygame.display.update()

        if x1 < wall_thickness or x1 >= width - wall_thickness or \
            y1 >= height - wall_thickness or \
            (y1 >= 50 and y1 < 50 + wall_thickness):
            game_close = True

        if x1 == foodx and y1 == foody:
            foodx, foody = generate_food()
            length_of_snake += 1
            #snake_speed += 0.5 
        
        clock.tick(snake_speed) #每秒更新次數      

    pygame.quit()
    quit()

gameLoop()
