# -*- coding: utf-8 -*-
"""
Created on Thu Jul  4 14:42:35 2019

@author: wangz
"""
import pygame
import random
import os
display_width = 900
display_height = 600
block_size = 30 
FPS = 10

#初始化环境
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()

#pygame.font.init()

pygame.mixer.init()
#游戏边界
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('snake')
clock = pygame.time.Clock() 

#颜色设定
bialy = (255,255,255)
czarny = (0,0,0)
czerwony = (255,0,0)
LIGHT_RED = (155,0,0)

ciemnyZielony = (0,120,0)

#导入图片
#正常贪吃蛇
HEAD = pygame.image.load('source//snakehead30x30.png')
TAIL = pygame.image.load('source//snaketail30x30.png')
BODY = pygame.image.load('source//snakebody30x30.png')
TURNLEFT = pygame.image.load('source//turnleft30x30.png')
TURNRIGHT = pygame.image.load('source//turnright30x30.png')
#第二条贪吃蛇
HEAD2 = pygame.image.load('source//snakehead230x30.png')
TAIL2 = pygame.image.load('source//snaketail230x30.png')
BODY2 = pygame.image.load('source//snakebody230x30.png')
TURNLEFT2 = pygame.image.load('source//turnleft230x30.png')
TURNRIGHT2 = pygame.image.load('source//turnright230x30.png')
#超级贪吃蛇
SUPERHEAD = pygame.image.load('source//supersnakehead30x30.png')
SUPERTAIL = pygame.image.load('source//supersnaketail30x30.png')
SUPERBODY = pygame.image.load('source//supersnakebody30x30.png')
SUPERTURNLEFT = pygame.image.load('source//superturnleft30x30.png')
SUPERTURNRIGHT = pygame.image.load('source//superturnright30x30.png')
#背景
background = pygame.image.load('source//TLONOWE2.jpg')
wall = pygame.image.load('source//wall2.gif')
#苹果
APPLE = pygame.image.load('source//NEWAPPLE.png')
APPLE_BIG = pygame.image.load('source//NEWAPPLE_BIG.png')
#石头
STONE = pygame.image.load('source//stone.gif')
STONE_BIG = pygame.image.load('source//ROCK_BIG.png')
#开始界面
START = pygame.image.load('source//PRISMA1.jpg')
CONTROLS = pygame.image.load('source//PRISMA2.jpg')
GAMEOVER = pygame.image.load('source//GAMEOVER.png')

#白宝石
WHITE_DIAMOND = pygame.image.load('source//WHITE_DIAMOND.png')
WHITE_DIAMOND_BIG = pygame.image.load('source//WHITE_DIAMOND_BIG.png')
#黑宝石
BLACK_DIAMOND = pygame.image.load('source//BLACK_DIAMOND.png')
BLACK_DIAMOND_BIG = pygame.image.load('source//BLACK_DIAMOND_BIG.png')

TIMERBACKGROUND = pygame.image.load('source//TIMERBACKGROUND.png')

ACTIVE_B = pygame.image.load('source//ACTIVE.png')
INACTIVE_B = pygame.image.load('source//INACTIVE.png')
#导入音乐
POINT = pygame.mixer.Sound("source//sfx_point.wav")
HIT = pygame.mixer.Sound("source//sfx_hit.wav")
EVOLUTION = pygame.mixer.Sound("source//Star_Wars_-_Imperial_march.wav")
STONEDESTROY = pygame.mixer.Sound("source//STONEDESTROY.wav")

pygame.mixer.music.load('source//music.mp3')
pygame.mixer.music.set_volume(0.2)

# 贪吃蛇图像旋转，初始方向为向右，逆时针旋转
def rotate(segment, image):
    if segment[0] == "right":
        rotatedImage = pygame.transform.rotate(image, 0)
    elif segment[0] == "left":
        rotatedImage = pygame.transform.rotate(image, 180)
    elif segment[0] == "up":
        rotatedImage = pygame.transform.rotate(image, 90)    
    elif segment[0] == "down":
        rotatedImage = pygame.transform.rotate(image, 270)       
    return rotatedImage        
#文本，仅支持英文        
def draw_text(text, color, size, x, y):
    pygame.font.init()
    font = pygame.font.Font('source//flup.ttf', size)#也可以另外加上
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    gameDisplay.blit(text_surface, text_rect)


#分数     
def score(score):
    font = pygame.font.Font('source//flup.ttf', 25)
    text = font.render(str(score), True, czarny)
    gameDisplay.blit(text, [14,14])

#随机产生位置    
def randLocationGen (stonesList, snakeList):
    randX = round((random.randrange(block_size, display_width - 2*block_size))/block_size)*block_size
    randY = round((random.randrange(block_size, display_height - 2*block_size))/block_size)*block_size
    
    #如果产生的位置和存在石头的位置一样，或者和贪吃蛇的位置一样，则重新随机产生，返回坐标
    for stone in stonesList:
        for element in snakeList:
            if(randX == stone[0] and randY == stone[1]) or (randX == element[1] and randY == element[2]):
                print("!TEXT!" + str(randX)+str(element[1]) + str(randY)+str(element[2]))
                return randLocationGen(stonesList, snakeList)
    
    return randX, randY
#双人模式随机产生位置    
def randLocationGen2 (stonesList, snake1List,snake2List):
    randX = round((random.randrange(block_size, display_width - 2*block_size))/block_size)*block_size
    randY = round((random.randrange(block_size, display_height - 2*block_size))/block_size)*block_size
    
    #如果产生的位置和存在石头的位置一样，或者和贪吃蛇的位置一样，则重新随机产生，返回坐标
    for stone in stonesList:
        for element1 in snake1List:
            for element2 in snake2List:
                if(randX == stone[0] and randY == stone[1]) or (randX == element1[1] and randY == element1[2]) or (randX == element2[1] and randY == element2[2]):
                    print("!TEXT!" + str(randX)+str(element1[1]) +str(element2[1])+ str(randY)+str(element1[2])+str(element2[2]))
                    return randLocationGen(stonesList, snake1List,snake2List)
    
    return randX, randY
#暂停
def pause ():
    
    draw_text("PAUSE", czarny, 60, display_width/2, display_height/2 -130)
    draw_text("Press P to continue", czarny, 30, display_width/2, display_height/2)
    pygame.display.update()
    
    while True:
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    return

                
#定义石头，具有添加石头，移除石头功能
class stones:
    
    def __init__(self):
        self.list = []

    def add(self, other):
    
        newStoneX, newStoneY = randLocationGen(self.list, other.list)
        newStone = [newStoneX, newStoneY]
        self.list.append(newStone)
        
    def show(self):

        for i in range(len(self.list)):
            gameDisplay.blit(STONE, (self.list[i][0],self.list[i][1]))
            
    def destroy(self, stone):
         
        self.list.remove(stone)
        
#定义石头，具有添加石头，移除石头功能
class stones2:
    
    def __init__(self):
        self.list = []

    def add(self, other1,other2):
    
        newStoneX, newStoneY = randLocationGen2(self.list, other1.list,other2.list)
        newStone = [newStoneX, newStoneY]
        self.list.append(newStone)
        
    def show(self):

        for i in range(len(self.list)):
            gameDisplay.blit(STONE, (self.list[i][0],self.list[i][1]))
            
    def destroy(self, stone):
         
        self.list.remove(stone)
#定义苹果，具有更新苹果功能，只要和石头以及贪吃蛇的位置不重合就可以            
class apple:
    
    def __init__(self, stones, snake):
        self.renew(stones, snake)
    
    def renew(self, stones, snake):
        self.x, self.y = randLocationGen(stones.list, snake.list)
        
    def show(self):
        gameDisplay.blit(APPLE, (self.x, self.y))

#定义苹果，具有更新苹果功能，只要和石头以及贪吃蛇的位置不重合就可以            
class apple2:
    
    def __init__(self, stones, snake1,snake2):
        self.renew(stones, snake1,snake2)
    
    def renew(self, stones, snake1,snake2):
        self.x, self.y = randLocationGen2(stones.list, snake1.list,snake2.list)
        
    def show(self):
        gameDisplay.blit(APPLE, (self.x, self.y))
 
#定义道具钻石，同样具有产生，移除功能       
class diamond:
    
    def __init__(self):
        self.timer = 0
        self.x = None
        self.y = None
        
    def renew(self, stones, snake, FPS):
        self.timer = 10*FPS
        self.x, self.y = randLocationGen(stones.list, snake.list)
    
    def kill(self):
        self.timer = 0
        self.x = None
        self.y = None
        
    def show(self, color):
        if self.timer > 0:
            self.timer -= 1
        
            #if color == 'red':
                #gameDisplay.blit(RED_DIAMOND, (self.x, self.y))
            if color =='white':
                gameDisplay.blit(WHITE_DIAMOND, (self.x, self.y))
            elif color =='black':
                gameDisplay.blit(BLACK_DIAMOND, (self.x, self.y))
        else:
            self.kill()

#定义道具钻石，同样具有产生，移除功能       
class diamond2:
    
    def __init__(self):
        self.timer = 0
        self.x = None
        self.y = None
        
    def renew(self, stones, snake1,snake2, FPS):
        self.timer = 10*FPS
        self.x, self.y = randLocationGen2(stones.list, snake1.list,snake2.list)
    
    def kill(self):
        self.timer = 0
        self.x = None
        self.y = None
        
    def show(self, color):
        if self.timer > 0:
            self.timer -= 1
        
            if color =='white':
                gameDisplay.blit(WHITE_DIAMOND, (self.x, self.y))
            elif color =='black':
                gameDisplay.blit(BLACK_DIAMOND, (self.x, self.y))
        else:
            self.kill()
            
#定义贪吃蛇的状态          
class snake:
    #头坐标以及方向
    def __init__(self, lead_x, lead_y):
        self.direction = "right"
        
        self.list = [["right", lead_x-2*block_size, lead_y],
                     ["right", lead_x-block_size, lead_y],
                     ["right", lead_x, lead_y]]
                          
        self.head = ["right", lead_x, lead_y]
        self.length = 3
        self.superTimer = 0
        
    #超级道具时间为当前系统频率下的10倍   
    def superSnake(self, FPS):
        self.superTimer = 10*FPS
    
    #状态更新   
    def update(self, lead_x, lead_y):
        self.head = []
        self.head.append(self.direction)
            
        self.head.append(lead_x)
        self.head.append(lead_y)
        
        self.list.append(self.head)
        
        #将加入的节点联系在头节点上
        if len(self.list) > self.length:
            del self.list[0]

        if self.superTimer > 0:
            self.superTimer -= 1

    def show(self, FPS):
        
        if self.superTimer > 0:
            self.view(SUPERHEAD, SUPERTAIL, SUPERBODY, SUPERTURNLEFT, SUPERTURNRIGHT)
            
            #超级状态下的时间计时器
            gameDisplay.blit(TIMERBACKGROUND, (800, 529))
            font = pygame.font.Font('source//flup.ttf', 25)
            text = font.render(str(self.superTimer/FPS), True, czarny)
            gameDisplay.blit(text, [830,537])
            
        else:
            self.view(HEAD, TAIL, BODY, TURNLEFT, TURNRIGHT)
        
    def show2(self, FPS):
        
        if self.superTimer > 0:
            self.view(SUPERHEAD, SUPERTAIL, SUPERBODY, SUPERTURNLEFT, SUPERTURNRIGHT)
            
            #超级状态下的时间计时器
            gameDisplay.blit(TIMERBACKGROUND, (800, 529))
            font = pygame.font.Font('source//flup.ttf', 25)
            text = font.render(str(self.superTimer/FPS), True, czarny)
            gameDisplay.blit(text, [830,537])
            
        else:
            self.view(HEAD2, TAIL2, BODY2, TURNLEFT2, TURNRIGHT2)    
                
    def view(self, head, tail, body, turnleft, turnright):
        
        gameDisplay.blit(rotate(self.list[-1],head), (self.list[-1][1],self.list[-1][2]))       
        gameDisplay.blit(rotate(self.list[1],tail), (self.list[0][1],self.list[0][2]))#尾部的状态取决于前一个部分的状态
        
        #更新身体部分的状态
        for i in range(1, self.length-1):
            #状态不变，身体前移
            if self.list[i][0] == self.list[i+1][0]:
                gameDisplay.blit(rotate(self.list[i],body), (self.list[i][1],self.list[i][2]))
            #状态顺时针
            elif (self.list[i][0] == "down" and self.list[i+1][0] == "right") or (self.list[i][0] == "right" and self.list[i+1][0] == "up") or (self.list[i][0] == "up" and self.list[i+1][0] == "left") or (self.list[i][0] == "left" and self.list[i+1][0] == "down"):       
                gameDisplay.blit(rotate(self.list[i+1],turnleft), (self.list[i][1],self.list[i][2]))
            #状态变为逆时针
            elif (self.list[i][0] == "right" and self.list[i+1][0] == "down") or (self.list[i][0] == "down" and self.list[i+1][0] == "left") or (self.list[i][0] == "left" and self.list[i+1][0] == "up") or (self.list[i][0] == "up" and self.list[i+1][0] == "right"):        
                gameDisplay.blit(rotate(self.list[i+1],turnright), (self.list[i][1],self.list[i][2]))
        
    def isDead(self, other):
        #当和自身碰撞时
        for eachSegment in self.list[:-1]:
            if eachSegment[1] == self.head[1] and eachSegment[2] == self.head[2]:
                HIT.play()#放音乐
                pygame.mixer.music.set_volume(0.2)
                return True
        #当超级道具时间没有时，和石头碰撞以及和边界碰撞        
        if self.superTimer <= 0:
            
            for eachStone in other.list:
                if eachStone[0] == self.head[1] and eachStone[1] == self.head[2]:
                    HIT.play()
                    return  True
                    
            if self.head[1] >= display_width-block_size or self.head[1] < block_size or self.head[2] >= display_height-block_size or self.head[2] < block_size:
                HIT.play()
                return True
                
        return False
    #双人模式下判断死亡
    def isDead2(self, other,othersnake):
        #当和自身碰撞时
        for eachSegment in self.list[:-1]:
            if eachSegment[1] == self.head[1] and eachSegment[2] == self.head[2]:
                HIT.play()#放音乐
                pygame.mixer.music.set_volume(0.2)
                return True
        #当和另一条蛇碰撞
        for eachSegment in othersnake.list[:-1]: 
            if eachSegment[1] == self.head[1] and eachSegment[2] == self.head[2]:
                HIT.play()#放音乐
                pygame.mixer.music.set_volume(0.2)
                return True            
        #当超级道具时间没有时，和石头碰撞以及和边界碰撞        
        if self.superTimer <= 0:
            
            for eachStone in other.list:
                if eachStone[0] == self.head[1] and eachStone[1] == self.head[2]:
                    HIT.play()
                    return  True
                    
            if self.head[1] >= display_width-block_size or self.head[1] < block_size or self.head[2] >= display_height-block_size or self.head[2] < block_size:
                HIT.play()
                return True
                
        return False    
    
    #长度减少   
    def trim(self):
        if len(self.list) > 13:
            self.list = self.list[10:]
            self.length -= 10

#游戏主框架
def gameLoop(): 
    
    gameExit = False
    gameOver = False
    
    points = 0
    speed = FPS

    lead_x = display_width/2 
    lead_y = display_height/2 
    lead_x_change = block_size 
    lead_y_change = 0 
    
    Snake = snake(lead_x, lead_y)
    
    Stones = stones()
    Apple = apple(Stones, Snake)
    Diamond = diamond()
    Trimer = diamond()

    while not gameExit:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                gameExit = True
            
            
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_LEFT) and Snake.direction != "right":
                    Snake.direction = "left"
                elif (event.key == pygame.K_RIGHT) and Snake.direction != "left":
                    Snake.direction = "right"
                elif (event.key == pygame.K_UP) and Snake.direction != "down":
                    Snake.direction = "up"    
                elif (event.key == pygame.K_DOWN) and Snake.direction != "up":
                    Snake.direction = "down"

                if event.key == pygame.K_p:
                    pause()
                    
        if Snake.direction == "left":
            lead_x_change = -block_size
            lead_y_change = 0
        elif Snake.direction == "right":
            lead_x_change = block_size
            lead_y_change = 0
        elif Snake.direction == "up":
            lead_y_change = -block_size
            lead_x_change = 0
        elif Snake.direction == "down":
            lead_y_change = block_size
            lead_x_change = 0
        #头节点位置更新    
        lead_x += lead_x_change
        lead_y += lead_y_change
        
        #吃掉苹果，分数增加，以及分数增加带来的速度FPS的改变                   
        if (lead_x == Apple.x and lead_y == Apple.y):
            
            Apple.renew(Stones, Snake)
            Snake.length += 1
            points += 10
            POINT.play()
            
            if (points)%40 == 0:
                Stones.add(Snake)
                
            if (points)%70 == 0:
                speed += 1
                print(speed)
                
            if (points)%150 == 0:
                Diamond.renew(Stones, Snake, speed)
                
            if (points)%280 == 0:
                Trimer.renew(Stones, Snake, speed)
        
        #如果吃掉钻石，分数增加50，        
        if (lead_x == Diamond.x and lead_y == Diamond.y):
            
            points += 50
            Diamond.kill()
            Snake.superSnake(speed)
            EVOLUTION.play()
            
            if (points)%280 == 0:
                Trimer.renew(Stones, Snake, speed)
            
        if (lead_x == Trimer.x and lead_y == Trimer.y):
            points += 50
            Trimer.kill()
            Snake.trim()#长度减少10
            
            if (points)%150 == 0:
                Diamond.renew(Stones, Snake, speed)
            
        if Snake.superTimer > 0:
            if 15 <= Snake.superTimer:
                pygame.mixer.music.set_volume(0.05)
            if (15 > Snake.superTimer >= 10):
                pygame.mixer.music.set_volume(0.10)
            elif 10 > Snake.superTimer >= 5:
                pygame.mixer.music.set_volume(0.15)
            elif 5 > Snake.superTimer:
                pygame.mixer.music.set_volume(0.2)
            for stone in Stones.list:
                if stone[0] == Snake.head[1] and stone[1] == Snake.head[2]:
                    points += 20
                    Stones.destroy(stone)
                    STONEDESTROY.play()
        
                
            if lead_x >= display_width-block_size:
                lead_x = block_size
            elif lead_x < block_size:
                lead_x = display_width-2*block_size
            elif lead_y >= display_height-block_size:
                lead_y = block_size
            elif lead_y < block_size:
                lead_y = display_height-2*block_size

        Snake.update(lead_x, lead_y)
        
        gameOver = Snake.isDead(Stones)
                
        gameDisplay.blit(background, (0,0))  
        
        Apple.show()
        Stones.show()
        Diamond.show('black')
        Trimer.show('white')
        
        Snake.show(FPS)
        
        gameDisplay.blit(wall, (0,0))
        
        score(points) 
           
        pygame.display.update()   
        clock.tick(speed)
        
        while gameOver == True:

            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameExit = True
                    gameOver = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False 
                    if event.key == pygame.K_c:
                        gameLoop()
                        
            gameDisplay.blit(GAMEOVER, (0,0))
            draw_text("SCORE: " + str(points), czarny, 50, display_width/2, display_height/2-25)
                        
            button("MENU", 100, 450, 200, 70, czerwony, LIGHT_RED, action = 'menu')
            button("PLAY AGAIN", 350, 450, 200, 70, czerwony, LIGHT_RED, action = 'one play')
            button("QUIT", 600, 450, 200, 70, czerwony, LIGHT_RED, action = 'quit')
        
            pygame.display.update()
        
            clock.tick(15)
            
    pygame.quit()
    pygame.font.quit()
    quit()
    

def gameLoop2():
    gameExit=False
    gameOver=False
    
    points=0
    speed=FPS
    
    lead_x1 = display_width/2 
    lead_y1 = display_height/2 
    lead_x1_change = block_size 
    lead_y1_change = 0 
    
    lead_x2 = display_width/2 
    lead_y2 = display_height/2-60 
    lead_x2_change = block_size 
    lead_y2_change = 0 

    Snake1=snake(lead_x1,lead_y1)
    Snake2=snake(lead_x2,lead_y2)
    
    Stones=stones2()
    Apple=apple2(Stones,Snake1,Snake2)
    
    Diamond = diamond2()
    Trimer = diamond2()
    
    while not gameExit:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                gameExit = True
            
            
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_a) and Snake1.direction != "right":
                    Snake1.direction = "left"
                elif (event.key == pygame.K_d) and Snake1.direction != "left":
                    Snake1.direction = "right"
                elif (event.key == pygame.K_w) and Snake1.direction != "down":
                    Snake1.direction = "up"    
                elif (event.key == pygame.K_s) and Snake1.direction != "up":
                    Snake1.direction = "down"
                if (event.key == pygame.K_LEFT) and Snake2.direction != "right":
                    Snake2.direction = "left"
                elif (event.key == pygame.K_RIGHT) and Snake2.direction != "left":
                    Snake2.direction = "right"
                elif (event.key == pygame.K_UP) and Snake2.direction != "down":
                    Snake2.direction = "up"    
                elif (event.key == pygame.K_DOWN) and Snake2.direction != "up":
                    Snake2.direction = "down"

                if event.key == pygame.K_p:
                    pause()
                    
        if Snake1.direction == "left":
            lead_x1_change = -block_size
            lead_y1_change = 0
        elif Snake1.direction == "right":
            lead_x1_change = block_size
            lead_y1_change = 0
        elif Snake1.direction == "up":
            lead_y1_change = -block_size
            lead_x1_change = 0
        elif Snake1.direction == "down":
            lead_y1_change = block_size
            lead_x1_change = 0
        if Snake2.direction == "left":
            lead_x2_change = -block_size
            lead_y2_change = 0
        elif Snake2.direction == "right":
            lead_x2_change = block_size
            lead_y2_change = 0
        elif Snake2.direction == "up":
            lead_y2_change = -block_size
            lead_x2_change = 0
        elif Snake2.direction == "down":
            lead_y2_change = block_size
            lead_x2_change = 0            
            
        #头节点位置更新  
        
        lead_x1 += lead_x1_change
        lead_y1 += lead_y1_change
        lead_x2 += lead_x2_change
        lead_y2 += lead_y2_change    
    
        #吃掉苹果，分数增加，以及分数增加带来的速度FPS的改变                   
        if (lead_x1 == Apple.x and lead_y1 == Apple.y):
            
            Apple.renew(Stones,Snake1,Snake2)
            Snake1.length += 1
            points += 10
            POINT.play()
            
            if (points)%40 == 0:
                Stones.add(Snake1,Snake2)
                
            if (points)%70 == 0:
                speed += 1
                print(speed)
                
            if (points)%150 == 0:
                Diamond.renew(Stones, Snake1,Snake2, speed)
                
            if (points)%280 == 0:
                Trimer.renew(Stones, Snake1, Snake2,speed)
        
        if (lead_x2 == Apple.x and lead_y2 == Apple.y):
            
            Apple.renew(Stones, Snake1,Snake2)
            Snake2.length += 1
            points += 10
            POINT.play()
            
            if (points)%40 == 0:
                Stones.add(Snake1,Snake2)
                
            if (points)%70 == 0:
                speed += 1
                print(speed)
                
            if (points)%150 == 0:
                Diamond.renew(Stones, Snake1,Snake2,speed)
                
            if (points)%280 == 0:
                Trimer.renew(Stones, Snake1,Snake2,speed)
                
        #如果吃掉钻石，分数增加50，        
        if (lead_x1 == Diamond.x and lead_y1 == Diamond.y):
            
            points += 50
            Diamond.kill()
            Snake1.superSnake(speed)
            EVOLUTION.play()
            
            if (points)%280 == 0:
                Trimer.renew(Stones, Snake1,Snake2, speed)
                
        if (lead_x2 == Diamond.x and lead_y2 == Diamond.y):
            
            points += 50
            Diamond.kill()
            Snake2.superSnake(speed)
            EVOLUTION.play()
            
            if (points)%280 == 0:
                Trimer.renew(Stones, Snake1,Snake2,speed)        
        
        if (lead_x1 == Trimer.x and lead_y1 == Trimer.y):
            points += 50
            Trimer.kill()
            Snake1.trim()#长度减少10
            
            if (points)%150 == 0:
                Diamond.renew(Stones, Snake1,Snake2, speed)
        
        if (lead_x2 == Trimer.x and lead_y2 == Trimer.y):
            points += 50
            Trimer.kill()
            Snake2.trim()#长度减少10
            
            if (points)%150 == 0:
                Diamond.renew(Stones, Snake1,Snake2, speed)
                
        if Snake1.superTimer > 0:
            if 15 <= Snake1.superTimer:
                pygame.mixer.music.set_volume(0.05)
            if (15 > Snake1.superTimer >= 10):
                pygame.mixer.music.set_volume(0.10)
            elif 10 > Snake1.superTimer >= 5:
                pygame.mixer.music.set_volume(0.15)
            elif 5 > Snake1.superTimer:
                pygame.mixer.music.set_volume(0.2)
            for stone in Stones.list:
                if stone[0] == Snake1.head[1] and stone[1] == Snake1.head[2]:
                    points += 20
                    Stones.destroy(stone)
                    STONEDESTROY.play()
        
                
            if lead_x1 >= display_width-block_size:
                lead_x1 = block_size
            elif lead_x1 < block_size:
                lead_x1 = display_width-2*block_size
            elif lead_y1 >= display_height-block_size:
                lead_y1 = block_size
            elif lead_y1 < block_size:
                lead_y1 = display_height-2*block_size
        
        if Snake2.superTimer > 0:
            if 15 <= Snake2.superTimer:
                pygame.mixer.music.set_volume(0.05)
            if (15 > Snake2.superTimer >= 10):
                pygame.mixer.music.set_volume(0.10)
            elif 10 > Snake2.superTimer >= 5:
                pygame.mixer.music.set_volume(0.15)
            elif 5 > Snake2.superTimer:
                pygame.mixer.music.set_volume(0.2)
            for stone in Stones.list:
                if stone[0] == Snake2.head[1] and stone[1] == Snake2.head[2]:
                    points += 20
                    Stones.destroy(stone)
                    STONEDESTROY.play()
        
                
            if lead_x2 >= display_width-block_size:
                lead_x2 = block_size
            elif lead_x2 < block_size:
                lead_x2 = display_width-2*block_size
            elif lead_y2 >= display_height-block_size:
                lead_y2 = block_size
            elif lead_y2 < block_size:
                lead_y2 = display_height-2*block_size    
    
        Snake1.update(lead_x1,lead_y1)
        Snake2.update(lead_x2,lead_y2)
        
        #判断贪吃蛇是否死亡
        gameOver1 = Snake1.isDead2(Stones,Snake2)
        gameOver2 = Snake2.isDead2(Stones,Snake1)
        
        if gameOver1==True or gameOver2==True:
            gameOver=True
        else:
            gameOver=False
       
        gameDisplay.blit(background, (0,0))  
        Apple.show()
        Stones.show()
        Diamond.show('black')
        Trimer.show('white')
        Snake1.show(FPS)
        Snake2.show2(FPS)
        gameDisplay.blit(wall, (0,0))
        score(points) 
           
        pygame.display.update()   
        clock.tick(speed)
        
        while gameOver == True:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameExit = True
                    gameOver = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False 
                    if event.key == pygame.K_c:
                        gameLoop()
                        
            gameDisplay.blit(GAMEOVER, (0,0))
            draw_text("SCORE: " + str(points), czarny, 50, display_width/2, display_height/2-25)
                        
            button("MENU", 100, 450, 200, 70, czerwony, LIGHT_RED, action = 'menu')
            button("PLAY AGAIN", 350, 450, 200, 70, czerwony, LIGHT_RED, action = 'two plays')
            button("QUIT", 600, 450, 200, 70, czerwony, LIGHT_RED, action = 'quit')
        
            pygame.display.update()
        
            clock.tick(15)
            
    pygame.quit()
    pygame.font.quit()
    quit()

    
#########################################################################################3
    #按钮功能    
def button(text, x, y, width, height, inactive, active, text_color = czarny, action = None):
    cursor = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    if (x + width > cursor[0] > x and y + height > cursor[1] > y):
        gameDisplay.blit(ACTIVE_B, (x,y))
        
        if click[0] == 1 and action != None:
            if action ==  'one play':
                gameLoop()            
            elif action ==  'two plays':
                gameLoop2()
            elif action == 'controls' or action == 'previous':
                show_controls()
            elif action == 'quit':
                pygame.quit()
                pygame.font.quit()
                quit()
            elif action == 'menu'or action == 'again':
                show_game_intro()
            elif action == 'next':
                show_controls_next()
        
    else:
        gameDisplay.blit(INACTIVE_B, (x,y))
        
    draw_text(text, text_color, int(round(height/2)), x + width/2, y + height/4)
    
#游戏开始                    
def show_game_intro():
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                pygame.font.quit()
                quit()                
                    
        gameDisplay.blit(START, (0,0))
        
        #button(text, x, y, width, height, inactive, active, text_color = czarny, action = None)
        button("ONE PLAY", 350, 250, 200, 70, czerwony, LIGHT_RED, action = 'one play')
        button("TWO PLAY", 350, 330, 200, 70, czerwony, LIGHT_RED, action = 'two plays')
        button("CONTROLS", 350, 410, 200, 70, czerwony, LIGHT_RED, action = 'controls')
        button("QUIT", 350, 490, 200, 70, czerwony, LIGHT_RED, action = 'quit')
      
        pygame.display.update()
        
        clock.tick(30)
          
def show_controls():
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                pygame.font.quit()
                quit()
                
        gameDisplay.blit(CONTROLS, (0,0))
        
        draw_text("GREETINGS", czarny, 38, display_width/2, display_height/2 -220)
        draw_text("Use arrows to navigate your little friend on the bord.", czarny, 28, display_width/2, display_height/2 -150)
        draw_text("Collect apples    , to increase your score and grow.", czarny, 28, display_width/2, display_height/2 -100)
        draw_text("Be careful not to hit walls and sudenlly appearing", czarny, 28, display_width/2, display_height/2 -50)
        draw_text("rocks     and most importantly don't bite yourself!", czarny, 28, display_width/2, display_height/2 -0)
        draw_text("Use diamonds to unlock special powers.", czarny, 28, display_width/2, display_height/2 +50)
        
        gameDisplay.blit(APPLE_BIG, (278, display_height/2 -110))
        gameDisplay.blit(STONE, (173, display_height/2 -0))
        
        button("MENU", 50, 500, 200, 70, czerwony, LIGHT_RED, action = 'menu')
        button("NEXT", 350, 500, 200, 70, czerwony, LIGHT_RED, action = 'next')
        button("QUIT", 650, 500, 200, 70, czerwony, LIGHT_RED, action = 'quit')
        
        pygame.display.update()
        
        clock.tick(30)
        
def show_controls_next():
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                pygame.font.quit()
                quit()
              
        gameDisplay.blit(CONTROLS, (0,0))
        
        draw_text("     will allow you to go through the walls", czarny, 28, display_width/2, display_height/2 -220)
        draw_text("and crash those sneaky stones.", czarny, 28, display_width/2, display_height/2 -170)
        draw_text("This effect will remain for 10 seconds.", czarny, 28, display_width/2, display_height/2 -120)
        draw_text("     will make snake shorter and easier to maneuver.", czarny, 28, display_width/2, display_height/2 -70)
        draw_text("Whenever you want,", czarny, 28, display_width/2, display_height/2 -20)
        draw_text("you can press P to pause the game."  , czarny, 28, display_width/2, display_height/2 +30)
        draw_text("GOOD LUCK!", czarny, 35, display_width/2, display_height/2 +100)
        
        gameDisplay.blit(BLACK_DIAMOND_BIG, (150, display_height/2 -225))
        gameDisplay.blit(WHITE_DIAMOND_BIG, (75, display_height/2 -75))        
        
        button("MENU", 50, 500, 200, 70, czerwony, LIGHT_RED, action = 'menu')
        button("PREVIOUS", 350, 500, 200, 70, czerwony, LIGHT_RED, action = 'previous')
        button("QUIT", 650, 500, 200, 70, czerwony, LIGHT_RED, action = 'quit')
        
        pygame.display.update()
        
        clock.tick(30)
                    

pygame.mixer.music.play(loops=-1)
show_game_intro()

