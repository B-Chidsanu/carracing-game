import pygame
from pygame import mixer 
import time
import random
import os

pygame.init()

# ขนาดของหน้าต่าง
width = 1280
height = 700

# สี
green = (0, 100, 0)
cyan = (0, 255, 255)
red = (240, 0, 0)
blue = (0,0, 200)
yellow = (255,255,51)
pink = (255,20,147)
black = (0,0,0)
bright_red = (255,0,0)
bright_light = (240,255,255)
bright_blue = (0,0,255)
bright_yellow = (255,255,51)

# สร้างหน้าต่างของเกม
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("CAR RACING")
clock = pygame.time.Clock()
carimg = pygame.transform.scale(pygame.image.load('car_imgs/tile000.png'),(100, 140))
icon = pygame.image.load('imgs/icon.png')
pygame.display.set_icon(icon)
pygame.display.update()

# โหลดพื้นหลัง
backgroundimg = pygame.image.load('imgs/road.png')
background1 = pygame.transform.scale(pygame.image.load("imgs/road2.jpg"),(width,height))
background2 = pygame.transform.scale(pygame.image.load("imgs/road1.jpg"),(width, height))
background3 = pygame.transform.scale(pygame.image.load("imgs/bg01.jpg"),(width, height))
car_width = 50
pause=False

# เสียงที่ใช้ในเกม
player_sound = mixer.Sound('sounds/car-music-other.mp3')
hit_sound = mixer.Sound('sounds/hit.wav')
horn_sound = mixer.Sound('sounds/horn.wav')
countdown_sound = mixer.Sound('sounds/countdown.wav')
end_sound = mixer.Sound('sounds/end.wav')
pygame.mixer.music.load("sounds/music.wav")

# เก็บ High Score
score=0
high_score = 0
if os.path.exists('highscore.txt'):
    with open('highscore.txt', 'r') as file:
        high_score = int(file.read())
else:
    high_score = 0

# หน้า Menu ของเกม
def intro_loop():
    global high_score,score
    intro=True
    if score > high_score:
            high_score = score
            with open('highscore.txt', 'w') as file:
                file.write(str(high_score))
    print(high_score)
    pygame.mixer.music.play(-1)
    while intro:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()

        screen.blit(background1,(0,0))
        largetext = pygame.font.Font('font/PixelPowerline-11Mg.ttf', 80)
        mediumtext= pygame.font.Font('freesansbold.ttf',18)
        TextSurf, TextRect = text_object("CAR RACING", largetext)
        TextRect.center = ((width/2),(height/4.5))
        screen.blit(TextSurf,TextRect)
        button("START",250,500,200,70,green,bright_light,"play")
        button("QUIT",550,500,200,70,black,bright_yellow,"quit")
        button("INSTRUCTION",850,500,200,70,blue,bright_blue,"intro")
        font = pygame.font.Font("font/NeonSans.ttf", 40) 
        text = font.render("High Score = " + str(high_score), 1, yellow)
        screen.blit(text, (490, 620))
        Textname,Textrext= text_object("Create By: Chidsanupong Boonma StudentID:64015031",mediumtext)
        Textrext.center=((1030),(690))
        screen.blit(Textname,Textrext)
        pygame.display.update()
        clock.tick(100)


# ส่วนควบคุมปุ่ม
def button(msg,x,y,w,h,ic,ac,action=None):
    mouse=pygame.mouse.get_pos()
    click=pygame.mouse.get_pressed()
    if x+w>mouse[0]>x and y+h>mouse[1]>y:
        pygame.draw.rect(screen,ac,(x,y,w,h))
        if click[0]==1 and action!=None:
            if action=="play":
                countdown()
            elif action=="quit":
                pygame.quit()
                quit()
            elif action=="intro":
                introduction()
            elif action=="menu":
                intro_loop()
            elif action=="pause":
                paused()
            elif action=="unpause":
                unpaused()
    else:
        pygame.draw.rect(screen,ic,(x,y,w,h))
    smalltext = pygame.font.Font("font/EvilEmpire-4BBVK.ttf",20)
    textsurf,textrect= text_object(msg,smalltext)
    textrect.center=((x+(w/2)),(y+(h/2)))
    screen.blit(textsurf,textrect)


# หน้าแนะนำวิธีการเล่น
def introduction():
    introduction = True
    x_x0 = 0
    y_y0 = 0
    x2 = 0
    y2 = -height
    while introduction:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
                
        y2 += 5
        y_y0 += 5
        screen.blit(backgroundimg, (x_x0,y_y0))
        screen.blit(backgroundimg, (x2, y2))
        if y_y0 > height:
            y_y0 = -height
        if y2 > height:
            y2 = -height

        largetext = pygame.font.Font('font/PixelPowerline-11Mg.ttf',60)
        mediumtext = pygame.font.Font('freesansbold.ttf',30)
        nametext = pygame.font.Font('freesansbold.ttf',18)
        TextSurf,TextRect=text_object("INSTRUCTION",largetext)
        TextRect.center=((width/2),(height/6))
        sTextSurf,sTextRect = text_object("CONTROLS",mediumtext)
        sTextRect.center =((width/2),(height/2))
        stextSurf,stextRect=text_object("ARROW LEFT : LEFT TURN",mediumtext)
        stextRect=((445),(400))
        hTextSurf,hTextRect=text_object("ARROW RIGHT : RIGHT TURN",mediumtext)
        hTextRect.center=((663),(480))
        iTextSurf,iTextRect= text_object("Don't crash the curb!!",mediumtext)
        iTextRect.center=((width/2),(height/1.3))
        Textname,Textrext=text_object("Create By: Chidsanupong Boonma StudentID:64015031",nametext)
        Textrext.center=((width/2),(height/1.02))
         
        screen.blit(TextSurf,TextRect)
        screen.blit(sTextSurf,sTextRect)
        screen.blit(stextSurf,stextRect)
        screen.blit(hTextSurf,hTextRect)
        screen.blit(iTextSurf,iTextRect)
        screen.blit(Textname,Textrext)
        
        button("BACK",800,600,100,50,blue,bright_blue,"menu")
        pygame.display.update()
        clock.tick(30)


# หน้า Paised
def paused():
    global pause
    player_sound.stop()
    while pause:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    quit()
            screen.blit(background2,(0,0))
            largetext=pygame.font.Font('font/PixelPowerline-11Mg.ttf',115)
            TextSurf,TextRect=text_object("PAUSED",largetext)
            TextRect.center=((width/2),(height/4))
            screen.blit(TextSurf,TextRect)
            button("CONTINUE",250,500,200,70,green,bright_light,"unpause")
            button("RESTART",550,500,200,70,blue,bright_blue,"play")
            button("MAIN MENU",850,500,200,70,black,bright_light,"menu")
            pygame.display.update()
            clock.tick(30)


# Unpaused
def unpaused():
    global pause
    pause=False
    if pause==False:
        player_sound.play()


# พื้นหลังหน้านับถอยหลัง
def countdown_background():
    font= pygame.font.Font("font/NeonSans.ttf", 30) 
    x = (width *0.46)
    y = (height * 0.8)
    screen.blit(backgroundimg, (0,0))
    screen.blit(carimg, (x, y))
    text = font.render("passed: 0", True, cyan)
    score = font.render("SCORE: 0", True, pink)
    screen.blit(text, (0, 50))
    screen.blit(score, (0, 20))
    button("PAUSE", 1130, 0, 150, 50, blue, bright_blue, "pause")


# นับถอยหลัง
def countdown():
    global score
    countdown=True
    mixer.music.stop()
    countdown_sound.play()
    while countdown:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    quit()

            screen.fill(green)
            countdown_background()
            largetext=pygame.font.Font('font/PixelPowerline-11Mg.ttf',115)
            TextSurf,TextRect=text_object("3",largetext)
            TextRect.center=((width/2),(height/2))
            screen.blit(TextSurf,TextRect)
            pygame.display.update()
            clock.tick(1)
            screen.fill(green)
            countdown_background()

            largetext=pygame.font.Font('font/PixelPowerline-11Mg.ttf',115)
            TextSurf,TextRect=text_object("2",largetext)
            TextRect.center=((width/2),(height/2))
            screen.blit(TextSurf,TextRect)
            pygame.display.update()
            clock.tick(1)
            screen.fill(green)
            countdown_background()

            largetext=pygame.font.Font('font/PixelPowerline-11Mg.ttf',115)
            TextSurf,TextRect=text_object("1",largetext)
            TextRect.center=((width/2),(height/2))
            screen.blit(TextSurf,TextRect)
            pygame.display.update()
            clock.tick(1)
            screen.fill(green)
            countdown_background()

            largetext=pygame.font.Font('font/PixelPowerline-11Mg.ttf',115)
            TextSurf,TextRect=text_object("GO!!!",largetext)
            TextRect.center=((width/2),(height/2))
            screen.blit(TextSurf,TextRect)
            pygame.display.update()
            clock.tick(1)
            score = 0
            main()


# import enemy เข้ามา
def Enemy(enemy_startx,enemy_starty,enemy):
    if enemy==0:
        enemy_pic = pygame.transform.scale(pygame.image.load("car_imgs/tile001.png"), (100, 140))
    elif enemy==1:
        enemy_pic = pygame.transform.scale(pygame.image.load("car_imgs/tile002.png"), (100, 140))
    else:
        enemy_pic = pygame.transform.scale(pygame.image.load("car_imgs/tile003.png"), (100, 140))

    screen.blit(enemy_pic, (enemy_startx,enemy_starty))


# Show score
def score_system(passed,score):
    font = pygame.font.Font("font/NeonSans.ttf", 60)
    text = font.render("passed " +str(passed),True,cyan)
    score = font.render("score " +str(score),True,pink)

    screen.blit(text, (0,70))
    screen.blit(score, (0,15))


def text_object(text,font):
    textsurface = font.render(text, True, pink)
    return textsurface,textsurface.get_rect()


def message_display(text):
    largetext = pygame.font.Font("font/PixelPowerline-11Mg.ttf", 80)
    textsurf,textrect = text_object(text,largetext)
    textrect.center = ((width/2),(height/2))
    screen.blit(textsurf,textrect)
    pygame.display.update()
    time.sleep(3)


# หน้า Restart
def restart():
    global pause
    player_sound.stop()
    end_sound.play()
    while pause:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    quit()

            screen.blit(background3,(0,0))
            largetext=pygame.font.Font('font/PixelPowerline-11Mg.ttf',80)
            TextSurf,TextRect=text_object("Can you play again?",largetext)
            TextRect.center=((width/2),(height/3.5))
            screen.blit(TextSurf,TextRect)
            button("RESTART",250,430,200,70,green,bright_light,"play")
            button("QUIT",550,430,200,70,black,bright_yellow,"quit")
            button("MAIN MENU",850,430,200,70,blue,bright_light,"menu")
            font = pygame.font.Font("font/NeonSans.ttf", 60) 
            text = font.render("High Score = " + str(high_score), 1, red)
            screen.blit(text, (400, 260))
            font1 = pygame.font.Font("font/NeonSans.ttf", 40) 
            text = font1.render("Your Score = " + str(score), 1, yellow)
            screen.blit(text, (500, 350))
            pygame.display.update()
            clock.tick(30)
    

# แจ้งเตือนตอนชน
def crash():
    player_sound.stop()
    hit_sound.play()
    message_display("YOU CRASHED")
    restart()



def background():
    screen.blit(backgroundimg, (0, 0))


# Random เสียงบีบแตร
def probability(percent=100, chance=100):
    if 0 <= percent <= 100:
        number = random.randint(1, chance)
        if number <= round(percent):
            return True
        return False
    else:
        raise ValueError


# ตัว Player
def car(x, y):
    screen.blit(carimg, (x, y))
    if probability(1, 150):
        horn_sound.play()


# Loop ของเกม
def main():
    global pause,score
    FPS=120
    mixer.music.stop()
    player_sound.play()
    x = (width*0.46)
    y = (height*0.8)
    x_change = 0
    obstracle_speed = 5
    enemy=0
    enemy_startx= random.randint(360, 800)
    enemy_starty= 0
    enemy_width=85
    enemy_height=130
    passed=0
    level=0
    ax_y=15
    x_x = 0
    y_y = 0
    x1 = 0
    y1 = -height
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change -= 3
                if event.key == pygame.K_RIGHT:
                    x_change += 3
                if event.key == pygame.K_a:
                    obstracle_speed += 2
                if event.key == pygame.K_b:
                    obstracle_speed -= 2
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
                
        x += x_change
        pause=True

        y1 += 5
        y_y += 5
        screen.blit(backgroundimg, (x_x,y_y))
        screen.blit(backgroundimg, (x1, y1))
        if y_y > height:
            y_y = -height
        if y1 > height:
            y1 = -height

        ax_y+=obstracle_speed

        enemy_starty-=(obstracle_speed/2)
        Enemy(enemy_startx,enemy_starty,enemy)
        enemy_starty+=obstracle_speed

        car(x,y)
        score_system(passed,score)

        if x>868-car_width or x<360:
            crash()
        
        if enemy_starty > height:
            enemy_starty = 0 - enemy_height
            enemy_startx = random.randint(360, 800)
            enemy = random.randrange(0, 3)
            passed += 1
            score += 50

            
            if int(passed)%10 == 0:
                level+=1
                obstracle_speed+=3
                largetext = pygame.font.Font("font/PixelPowerline-11Mg.ttf", 80)
                textsurf, textrect = text_object("LEVEL"+str(level),largetext)
                textrect.center = ((width / 2), (height / 2))
                screen.blit(textsurf, textrect)
                pygame.display.update()
                time.sleep(3)


        if y < enemy_starty+enemy_height:
            if x > enemy_startx-enemy_width and x < enemy_startx+enemy_width or x+car_width > enemy_startx and x+car_width < enemy_startx+enemy_width:
                crash()

        
        button("Pause",1130,0,150,50,blue,bright_blue,"pause")
        pygame.display.update()
        clock.tick(FPS)

intro_loop()
main()
pygame.quit()
quit()
