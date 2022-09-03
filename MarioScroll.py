from game2d import *
from actor import Actor, Arena
from bounce import Bird,Wall,Mario,Enemy,Bonus,Fungo, Bandiera, Luigi





def update():
    global view_x, view_y, view_w, view_h,bonus_fungo
    
    image_blit(canvas, background, (0, 0),area=(view_x, view_y, view_w, view_h))  # BG
   ## canvas_fill(canvas,(127,0,0))
    arena.move_all()
    for a in arena.actors():
        x, y, w, h = a.rect()
        xs, ys = a.symbol()
        
        if mario.bonus_activation() != True:
            
            if mario.died() == True:
                image_blit(canvas,end,(0,0))
                return
            if bandiera.win() == True:
                image_blit(canvas,win,(0,0))
            #elif a != fungo:
            else:
                image_blit(canvas, sprites, (x-view_x,y-view_y), area=(xs, ys, w,h))
        else:
            #print("Fungo")
##            if mario.actived_bonus() == True:
##                    image_blit(canvas, sprites, (x-view_x,y-view_y), area=(xs, ys, w,h))
            if bandiera.win() != True:
                if bonus_fungo == True:
                    bonus_creation()
                    bonus_fungo = False
                if mario.died() == True:
                    image_blit(canvas,end,(0,0))
                    return
                else:
                    image_blit(canvas, sprites, (x-view_x,y-view_y), area=(xs, ys, w,h))
            else:
                image_blit(canvas,win,(0,0))
                
            
def bonus_creation():
    fungo = Fungo(arena,250,550)


def keydown(e):
    global view_x, view_y
    arena_w, arena_h = arena.size()
    x,y,w,h = mario.rect()
    code = e.code
    if e.keyCode == K_SPACE:
##        if code == "ArrowRight":
##            if x > 100:
##                view_x = min(view_x + 3, arena_w - view_w)
##        elif code == "ArrowLeft":
##            view_x = max(view_x - 3,
        
## CHIEDERE AL PROF LA DOPPIA COMBINAZIONE
        mario.jump()
        

    elif code == "ArrowRight":
        mario.go_right()
        
        if x > 100:
            view_x = min(view_x + 4, arena_w - view_w)
        
       
    elif code == "ArrowLeft":
        mario.go_left()
        
        view_x = max(view_x - 4, 0)
    elif e.keyCode == a:
        print("Entrato")
        luigi.go_left()
        
            


def keyup(e):
    if e.code in ("ArrowLeft", "ArrowRight"):
        mario.stay()
        luigi.stay()

arena = Arena(1200, 675)

mario = Mario(arena, 0, 605)
luigi = Luigi(arena,40,605)
muro = Wall(arena, 100,540,63,676,48,7)
muro2 = Wall(arena,170,540,63,676,48,7)
tubo = Wall(arena, 500,567,271,1152,32,49)
tubo2 = Wall(arena, 1000,567,271,1152,32,49)
bonus = Bonus(arena,250,567)
bandiera = Bandiera(arena,1100,447)
bird = Bird(arena, 30,20)
nemico = Enemy(arena,100,600)
nemico2 = Enemy(arena,700,600)



view_x, view_y, view_w, view_h = 0, 0, 600, 675
bonus_fungo = True

canvas = canvas_init((view_w, view_h))

sprites = image_load("smb_sprites.png")
background = image_load("viewport.png")
end = image_load("GameOver.png")
win = image_load("Win.png")

set_interval(update, 1000 // 30)  # Millis
doc.onkeydown = keydown
doc.onkeyup = keyup

