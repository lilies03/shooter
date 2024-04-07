#Создай собственный Шутер!
from random import randint
from time import sleep,time as timer
from pygame import *
import sys
import os
def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    elif hasattr(sys, "_MEIPASS2"):
        return os.path.join(sys._MEIPASS2, relative_path)
    else:
        return os.path.join(os.path.abspath("."), relative_path)

image_folder=resource_path(".")

w=500
h=700
FPS=60
white=(255, 255, 255)
red=(255, 0, 0)
yel=(252, 235, 3)
green=(32, 252, 3)
color=green
# pyinstaller --onefile -n "Shooter_game" --add-data "galaxy.jpg;." --add-data "fl.png;." --add-data "h.png;."  --add-data "rocket.png;." --add-data "bullet.png;." --add-data "ufo.png;." --add-data "space.ogg;." --add-data "fire.ogg;." --add-data "asteroid.png;." --noconsole shooter_game.py
img_hero=os.path.join(image_folder,'rocket.png')
img_evil=os.path.join(image_folder,'ufo.png')
img_bul=os.path.join(image_folder,'bullet.png')
img_back=os.path.join(image_folder,'galaxy.jpg')
img_astr=os.path.join(image_folder,'asteroid.png')
music_back=os.path.join(image_folder,'space.ogg')
m_fire=os.path.join(image_folder,'fire.ogg')
heart=os.path.join(image_folder,'h.png')
flash=os.path.join(image_folder,'fl.png')
window=display.set_mode((h,w))
display.set_caption('pygame window')


#задай фон сцены
background=transform.scale(image.load(img_back),(h,w))

clock=time.Clock()
mixer.init()
font.init()
mixer.music.load(music_back)
mixer.music.play(-1)
mixer.music.set_volume(0.1)

font_text=font.Font(None,35)

win_t=font_text.render('YOU WIN!!!',True,(252, 215, 3))
lose_t=font_text.render('YOU LOSE!!!',True,(196, 56, 27))
t1=0
t2=0
t3=15


class GameSprite(sprite.Sprite):
    def __init__(self,img:str,x:int,y:int,h:int,w:int,speed:int):
        super().__init__()
        self.image=transform.scale(image.load(img),(w,h))
        self.speed=speed
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y

    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))
        
class Player(GameSprite):
    def update(self):
        key_pressed=key.get_pressed()
        if key_pressed[K_LEFT] and self.rect.x>self.speed:
            self.rect.x-=self.speed
        if key_pressed[K_RIGHT] and self.rect.x<h-100:
            self.rect.x+=self.speed 
    def fire(self):
        b.play()
        bul=Bullet(img_bul,self.rect.centerx,self.rect.top,15,20,15)
        bullets.add(bul)

class Enemy(GameSprite):
    def update(self):
       self.rect.y+=self.speed
       global t2
       if self.rect.y>=500:
           self.rect.y=0
           self.rect.x=randint(60,h-80)
           t2+=1
class Astr(GameSprite):
    def update(self):
        self.rect.y+=self.speed
        if self.rect.y>=500:
            self.rect.y=0
            # sleep(3)
            self.rect.x=randint(60,h-80)
class Buster(GameSprite):
    def update(self):
        self.rect.y+=self.speed
        if self.rect.y==500:
            self.kill()

pl=Player(img_hero,350,405,90,100,10)

class Bullet(GameSprite):
    def update(self):
        self.rect.y-=self.speed
        if self.rect.y==0:
            self.kill()
        
busters=sprite.Group()
busters_1=sprite.Group()
enemies=sprite.Group()
for i in range(5):
    en1=Enemy(img_evil,randint(60,h-80),0,80,85,randint(1,5))
    enemies.add(en1)

asteroids=sprite.Group()
for i in range(3):
    astr1=Astr(img_astr,randint(60,h-80),0,30,35,randint(1,6))
    asteroids.add(astr1)

bullets=sprite.Group()

b=mixer.Sound(m_fire)
b.set_volume(0.1)
run=True
finish=False
v=False
while run:
    for e in event.get():
        if e.type==QUIT:
            run=False
        if e.type==KEYDOWN:
            if e.key==K_SPACE:
                pl.fire()
            
    if not finish:
        window.blit(background,(0,0))
        pl.reset()
        pl.update()
        
        enemies.draw(window)
        enemies.update()

        asteroids.draw(window)
        asteroids.update()
        
        busters.draw(window)
        busters.update()

        busters_1.draw(window)
        busters_1.update()

        bullets.draw(window)
        bullets.update()
        
        sprites_list=sprite.groupcollide(enemies,bullets,True,True)
        for i in sprites_list:
            t1+=1
            en1=Enemy(img_evil,randint(60,h-80),0,80,85,randint(1,5))
            enemies.add(en1)

        if randint(1,1500)==1:
            buster=Buster(heart,randint(0,h-50),0,50,50,5)
            busters.add(buster)
        
        bonus_collide=sprite.spritecollide(pl,busters,True)
        for i in bonus_collide:
            t3+=1
        
        if randint(1,500)==1:
            buster=Buster(flash,randint(0,h-50),0,50,50,5)
            busters_1.add(buster)
        
        bonus_collide=sprite.spritecollide(pl,busters_1,True)
        for i in bonus_collide:
            v=True
            vr1=timer()
            pl.speed+=5
        if v:    
            now=timer() 
            if now-vr1>=5:
                pl.speed-=5
                v=False


        if sprite.spritecollide(pl,asteroids,False) or sprite.spritecollide(pl,enemies,False) :
            sprite.spritecollide(pl,asteroids,True)
            sprite.spritecollide(pl,enemies,True)
            t3-=1
            # en1=Enemy(img_evil,randint(60,h-80),0,80,85,randint(1,5))
            # enemies.add(en1)
            # astr1=Astr(img_astr,randint(60,h-80),0,30,35,randint(1,6))
            # asteroids.add(astr1)

        if t3==3:
            color=green
        if t3==2:
            color=yel
        if t3==1:
            color=red
        count_w=font_text.render('Счёт:'+str(t1),True,white)
        count_l=font_text.render('Пропущено:'+str(t2),True,white)
        live=font_text.render('Жизни:'+str(t3),True,color)
        window.blit(count_w,(10,20))
        window.blit(count_l,(10,50))
        window.blit(live,(10,80))
        
        if t2>=100 or t3==0:
           finish=True
           window.blit(lose_t,(h//2,w//2))

        if t1>=10:
            finish=True
            window.blit(win_t,(h//2,w//2))
    else:
        t1=0
        t2=0
        t3=3
        finish=False
        

        for en1 in enemies:
            en1.kill()
        for bull in bullets:
            bull.kill()
        for astr in asteroids:
            astr.kill()
        sleep(5)

        for i in range(5):
            en1=Enemy(img_evil,randint(60,h-80),0,80,85,randint(1,5))
            enemies.add(en1)

        for i in range(3):
            astr1=Astr(img_astr,randint(60,h-80),0,30,35,randint(1,6))
            asteroids.add(astr1)

        




    display.update()
    clock.tick(FPS)
