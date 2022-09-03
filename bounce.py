from random import choice, randrange
from actor import *

##CLASSI COMPLETATE NON TOCCARE FUNZIONANO




class Wall(Actor):
   # W,H = 33,49
                    def __init__(self, arena, x, y,simX,simY,w,h):
                            self._x, self._y = x, y
                            self._simX, self._simY = simX, simY
                            self._w, self._h = w, h
                            self._arena = arena
                            arena.add(self)

                    def move(self):
                            pass

                    def collide(self, other):
                            pass
                
                    def rect(self):
                        return self._x, self._y, self._w, self._h

                    def symbol(self):
                        return self._simX,self._simY

class Bird(Actor):
        SPEED = 5
        W,H = 19,18
        symX,symY = 179,559
        condition = False
        def __init__(self, arena, x, y):
                    self._x, self._y = x, y
                    self._dx = self.SPEED
                    self._arena = arena
                    arena.add(self)

        def move(self):
            arena_w, arena_h = self._arena.size()
            #print(arena_w,arena_h)
            if not (0 <= self._x + self._dx <= arena_w - self.W):
                self._dx = -self._dx
                if self.condition == False:
                    self.symX,self.symY = 147,559
                    self.condition = True
                else:
                    self.symX,self.symY = 179,559
                    self.condition = False
            self._x += self._dx
     

        def collide(self,other):
            pass

        def rect(self) -> (int, int, int, int):
            return self._x, self._y, self.W, self.H

        def symbol(self):
            return self.symX,self.symY



##-----------------------FINE------------------------------

class Fungo(Actor):
    W,H = 18,17
    symX,symY = 183,671
    SPEED = 5
    GRAVITY = 1.7
    ok_move = False
    
    def __init__(self, arena, x, y):
                self._x, self._y = x, y
                self._dx, self._dy = self.SPEED, self.SPEED
                self._arena = arena
                self._landed = False
                arena.add(self)

    def move(self):
        arena_w, arena_h = self._arena.size()
        
        if not (0 <= self._x + self._dx <= arena_w - self.W):
            self._dx = -self._dx
        if not self._y > arena_h - self.H-60:
            self._y += self.GRAVITY
        self._x += self._dx

    def collide(self,other):
        if isinstance(other, Wall):
            x, y, w, h = other.rect()
            if x < self._x:
                self._dx = self.SPEED
            else:
                self._dx = -self.SPEED

        elif isinstance(other, Mario):
            if other.bonus_activation() == True:
                self._arena.remove(self)

    def rect(self) -> (int, int, int, int):
        return self._x, self._y, self.W, self.H

    def symbol(self):
        return self.symX,self.symY



class Bonus(Actor):
        W,H = 17,17
        symX,symY = 64,641
        condition = False
        def __init__(self, arena, x, y):
                    self._x, self._y = x, y
                    self._arena = arena
                    arena.add(self)

        def move(self):
                    pass

        def collide(self,other):
            pass


        def rect(self) -> (int, int, int, int):
            return self._x, self._y, self.W, self.H

        def symbol(self):
            return self.symX,self.symY

##DA MODIFICARE




class Bandiera(Actor):
        W,H = 16,169
        symX,symY = 123,1345
        vittoria = False
        def __init__(self, arena, x, y):
                    self._x, self._y = x, y
                    self._arena = arena
                    arena.add(self)

        def move(self):
            pass

        def collide(self,other):
            if isinstance(other,Mario):
                print("Colliso con bandiera")
                self.vittoria = True
    
        def win(self):
            return self.vittoria
        def rect(self) -> (int, int, int, int):
            return self._x, self._y, self.W, self.H

        def symbol(self):
            return self.symX,self.symY


class Mario(Actor):
    W, H = 15, 15
    symX,symY = 210,0
    SPEED = 4
    morte = False
    fungo_bonus = False
    bonus_block = False
    active_bonus = False
    super_vita = False
    

    def __init__(self, arena, x, y):
        self._x, self._y = x, y
        self._dx, self._dy = 0, 0
        self._landed = False
        self._arena = arena
        arena.add(self)

    def move(self):
        arena_w, arena_h = self._arena.size()
        self._y += self._dy
        if self._y < 0:
            self._y = 0
        elif self._y > arena_h - self.H-60:
            self._y = arena_h - self.H-60
            self._landed = True


        if not self._landed:
            self._dy += 0.3

        self._x += self._dx
        if self._x < 0:
            self._x = 0
        elif self._x > arena_w - self.W:
            self._x = arena_w - self.W

        

    def go_left(self):
        self._dx= -self.SPEED
        if self.active_bonus == True:
            self.symX,self.symY = 180,52
        else:    
            self.symX,self.symY = 180,0
        
        
    def go_right(self):
        self._dx = +self.SPEED
        if self.active_bonus == True:
            self.symX,self.symY = 209,52
        else:
            self.symX,self.symY = 210,0
        

    def jump(self):
        if self.active_bonus == True:
            self.symX,self.symY = 262,86
        else:
            self.symX,self.symY = 360,0
        if self._landed:
            self._dy = -self.SPEED * 2

        self._landed = False
            
    def stay(self):
        self._dx = 0

    def bonus_activation(self):
        #print("Fungo attivato")
        return self.fungo_bonus

    def actived_bonus(self):
        #print("Bonus attivato")
        self.super_vita = True
        return self.active_bonus
    
    def collide(self, other):
            if isinstance(other,Wall):
                    x, y, w, h = other.rect()
                    border_left, border_right = x - self.W, x + w
                    border_top, border_bottom = y - self.H, y + h

                    if abs(border_left - self._x) < abs(border_right - self._x):
                            nearest_x = border_left
                            self._dy = +self.SPEED * 2
                            self._landed = False
            
                    else:
                            nearest_x = border_right
                            self._dy = +self.SPEED * 2
                            self._landed = False
                            
                    if abs(border_top - self._y) < abs(border_bottom - self._y):
                            nearest_y = border_top
                            self._landed = True
                    else:
                            nearest_y = border_bottom
                            self._landed = True

                    if abs(nearest_x - self._x) < abs(nearest_y - self._y):
                            self._x = nearest_x
                            self._dy = +self.SPEED * 2
                            self._landed = False
                            
                    else:
                            self._y = nearest_y
                            self._landed = True

            #collisione enemy laterale
            elif isinstance(other,Enemy):
                    x, y, w, h = other.rect()
                    border_left, border_right = x - self.W, x + w
                    border_top, border_bottom = y - self.H, y + h

                    if abs(border_left - self._x) < abs(border_right - self._x):
                            nearest_x = border_left
                            self._dy = +self.SPEED * 2

            
                    else:
                            nearest_x = border_right
                            self._dy = +self.SPEED * 2
                
                    if abs(border_top - self._y) < abs(border_bottom - self._y):
                            nearest_y = border_top
                            #print("Preso da sopra")
                            self._landed = True
                    else:
                            nearest_y = border_bottom
                            self._landed = True
                            
                    if abs(nearest_x - self._x) < abs(nearest_y - self._y):    
                        if self.super_vita == True:
                            print("Entrato")
                            self.super_vita = False
                            self.active_bonus = False
                            self.fungo_bonus = False
                            self._x -= 40
                            self.W,self.H = 15,15
                            self.symX, self.symY = 210,0
                        else:
                            self.morte = True
                        #self.died()


                            
                    else:
                         self._y = nearest_y

            elif isinstance(other,Bonus):
                        x, y, w, h = other.rect()
                        border_left, border_right = x - self.W, x + w
                        border_top, border_bottom = y - self.H, y + h

                        if abs(border_left - self._x) < abs(border_right - self._x):
                                nearest_x = border_left
                                self._dy = +self.SPEED * 2
                                self._landed = False
                
                        else:
                                nearest_x = border_right
                                self._dy = +self.SPEED * 2
                                self._landed = False
                                
                        if abs(border_top - self._y) < abs(border_bottom - self._y):
                                nearest_y = border_top
                                self._landed = True
                        else:
                                nearest_y = border_bottom
                                self._landed = True

                        if abs(nearest_x - self._x) < abs(nearest_y - self._y):
                                self._x = nearest_x
                                self._dy = +self.SPEED * 2
                                self._landed = False
                                
                        else:
                                self._y = nearest_y
                                self._landed = True
                                if nearest_y == border_bottom:
                                    #print("colpito da sotto")
                                    self.fungo_bonus = True
                                    self.bonus_block = True

            elif isinstance(other, Fungo):
                if self.fungo_bonus == True:
                    self.symX, self.symY = 209, 52
                    self.W, self.H = 17, 33
                    self.active_bonus = True
                    self.super_vita = True

                            
    def died(self):
        return self.morte
        
##    def remove(self):
##        self._arena.remove(self)
        
    def rect(self):
        return self._x, self._y, self.W, self.H

    def symbol(self):
##        if self.active_bonus == True:
##            self.symX, self.symY = 209, 52
##            self.W, self.H = 17, 33
            
        return self.symX,self.symY








class Luigi(Actor):
    W, H = 15, 15
    symX,symY = 272,189
    SPEED = 4
    morte = False
    fungo_bonus = False
    bonus_block = False
    active_bonus = False
    super_vita = False
    

    def __init__(self, arena, x, y):
        self._x, self._y = x, y
        self._dx, self._dy = 0, 0
        self._landed = False
        self._arena = arena
        arena.add(self)

    def move(self):
        arena_w, arena_h = self._arena.size()
        self._y += self._dy
        if self._y < 0:
            self._y = 0
        elif self._y > arena_h - self.H-60:
            self._y = arena_h - self.H-60
            self._landed = True


        if not self._landed:
            self._dy += 0.3

        self._x += self._dx
        if self._x < 0:
            self._x = 0
        elif self._x > arena_w - self.W:
            self._x = arena_w - self.W

        

    def go_left(self):
        self._dx= -self.SPEED 
        self.symX,self.symY = 181,190
        
        
    def go_right(self):
        self._dx = +self.SPEED
        self.symX,self.symY = 272,189 
        

    def jump(self):
     
        self.symX,self.symY = 360,188
        if self._landed:
            self._dy = -self.SPEED * 2

        self._landed = False
            
    def stay(self):
        self._dx = 0

    def bonus_activation(self):
        #print("Fungo attivato")
        return self.fungo_bonus

    def actived_bonus(self):
        #print("Bonus attivato")
        self.super_vita = True
        return self.active_bonus
    
    def collide(self, other):
            if isinstance(other,Wall):
                    x, y, w, h = other.rect()
                    border_left, border_right = x - self.W, x + w
                    border_top, border_bottom = y - self.H, y + h

                    if abs(border_left - self._x) < abs(border_right - self._x):
                            nearest_x = border_left
                            self._dy = +self.SPEED * 2
                            self._landed = False
            
                    else:
                            nearest_x = border_right
                            self._dy = +self.SPEED * 2
                            self._landed = False
                            
                    if abs(border_top - self._y) < abs(border_bottom - self._y):
                            nearest_y = border_top
                            self._landed = True
                    else:
                            nearest_y = border_bottom
                            self._landed = True

                    if abs(nearest_x - self._x) < abs(nearest_y - self._y):
                            self._x = nearest_x
                            self._dy = +self.SPEED * 2
                            self._landed = False
                            
                    else:
                            self._y = nearest_y
                            self._landed = True

            #collisione enemy laterale
            elif isinstance(other,Enemy):
                    x, y, w, h = other.rect()
                    border_left, border_right = x - self.W, x + w
                    border_top, border_bottom = y - self.H, y + h

                    if abs(border_left - self._x) < abs(border_right - self._x):
                            nearest_x = border_left
                            self._dy = +self.SPEED * 2

            
                    else:
                            nearest_x = border_right
                            self._dy = +self.SPEED * 2
                
                    if abs(border_top - self._y) < abs(border_bottom - self._y):
                            nearest_y = border_top
                            #print("Preso da sopra")
                            self._landed = True
                    else:
                            nearest_y = border_bottom
                            self._landed = True
                            
                    if abs(nearest_x - self._x) < abs(nearest_y - self._y):    
                        if self.super_vita == True:
                            print("Entrato")
                            self.super_vita = False
                            self.active_bonus = False
                            self.fungo_bonus = False
                            self._x -= 40
                            self.W,self.H = 15,15
                            self.symX, self.symY = 210,0
                        else:
                            self.morte = True
                        #self.died()


                            
                    else:
                         self._y = nearest_y

            elif isinstance(other,Bonus):
                        x, y, w, h = other.rect()
                        border_left, border_right = x - self.W, x + w
                        border_top, border_bottom = y - self.H, y + h

                        if abs(border_left - self._x) < abs(border_right - self._x):
                                nearest_x = border_left
                                self._dy = +self.SPEED * 2
                                self._landed = False
                
                        else:
                                nearest_x = border_right
                                self._dy = +self.SPEED * 2
                                self._landed = False
                                
                        if abs(border_top - self._y) < abs(border_bottom - self._y):
                                nearest_y = border_top
                                self._landed = True
                        else:
                                nearest_y = border_bottom
                                self._landed = True

                        if abs(nearest_x - self._x) < abs(nearest_y - self._y):
                                self._x = nearest_x
                                self._dy = +self.SPEED * 2
                                self._landed = False
                                
                        else:
                                self._y = nearest_y
                                self._landed = True
                                if nearest_y == border_bottom:
                                    #print("colpito da sotto")
                                    self.fungo_bonus = True
                                    self.bonus_block = True

            elif isinstance(other, Fungo):
                if self.fungo_bonus == True:
                    self.symX, self.symY = 209, 52
                    self.W, self.H = 17, 33
                    self.active_bonus = True
                    self.super_vita = True

                            
    def died(self):
        return self.morte
        
##    def remove(self):
##        self._arena.remove(self)
        
    def rect(self):
        return self._x, self._y, self.W, self.H

    def symbol(self):
##        if self.active_bonus == True:
##            self.symX, self.symY = 209, 52
##            self.W, self.H = 17, 33
            
        return self.symX,self.symY







                    
class Enemy(Actor):
        SPEED = 4
        W,H = 19,19
        symX,symY = 29,379
        condition = False
        def __init__(self, arena, x, y):
                    self._x, self._y = x, y
                    self._dx = self.SPEED
                    self._arena = arena
                    arena.add(self)

        def move(self):
            arena_w, arena_h = self._arena.size()
            if not (0 <= self._x + self._dx <= arena_w - self.W):
                self._dx = -self._dx
                if self.condition == False:
                    self.symX,self.symY = 0,379
                    self.condition = True
                else:
                    self.symX,self.symY = 29,379
                    self.condition = False
            self._x += self._dx
     
        def collide(self, other):
            if isinstance(other,Wall):
                x, y, w, h = other.rect()
                if x < self._x:
                    self._dx = self.SPEED
                else:
                    self._dx = -self.SPEED
                    if self.condition == False:
                        self.symX,self.symY = 0,379
                        self.condition = True
                    else:
                        self.symX,self.symY = 29,379
                        self.condition = True
            

            elif isinstance(other,Mario):        
                    x, y, w, h = other.rect()
                    border_left, border_right = x - self.W, x + w
                    border_top, border_bottom = y - self.H, y + h
                    nearest_y = border_bottom
                    if abs(border_left - self._x) < abs(border_right - self._x):    
                        nearest_x = border_left
##                            self._dy = +self.SPEED * 2
                        other.died()
            
                    else:
                            nearest_x = border_right
                            self._dy = +self.SPEED * 2
                
##                    if abs(border_top - self._y) < abs(border_bottom - self._y):
##                            nearest_y = border_top
                    if abs(nearest_x - self._x) < abs(nearest_y - self._y):
                        self._x = nearest_x
##                        self._dy = +self.SPEED * 2
                        other.died()
                    else:
                        self.died()
##            elif isinstance(other,Luigi):        
##                    x, y, w, h = other.rect()
##                    border_left, border_right = x - self.W, x + w
##                    border_top, border_bottom = y - self.H, y + h
##                    nearest_y = border_bottom
##                    if abs(border_left - self._x) < abs(border_right - self._x):    
##                        nearest_x = border_left
####                            self._dy = +self.SPEED * 2
##                        other.died()
##            
##                    else:
##                            nearest_x = border_right
##                            self._dy = +self.SPEED * 2
##                
####                    if abs(border_top - self._y) < abs(border_bottom - self._y):
####                            nearest_y = border_top
##                    if abs(nearest_x - self._x) < abs(nearest_y - self._y):
##                        self._x = nearest_x
####                        self._dy = +self.SPEED * 2
##                        other.died()
##                    else:
##                        self.died()                        

        def died(self):
            #print("Mario mi ha preso")
            self.symX,self.symY = 58,383
            self.W,self.H = 19,11
            self._y = 273
            self._arena.remove(self)
            

        def rect(self) -> (int, int, int, int):
            return self._x, self._y, self.W, self.H

        def symbol(self):
            return self.symX,self.symY



## Mostro che cammina solo sulle piattaforme
        
##class Monster(Actor):
##        SPEED = 0.2
##        W,H = 19,19
##        symX,symY = 149,531
##        condition = False
##        def __init__(self, arena, x, y):
##                    self._x, self._y = x, y
##                    self._dx = self.SPEED
##                    self._arena = arena
##                    arena.add(self)
##
##        def move(self):
##            pass
##                arena_w, arena_h = self._arena.size()
##            if not (0 <= self._x + self._dx <= arena_w - self.W):
##                self._dx = -self._dx
##                if self.condition == False:
##                    self.symX,self.symY = 116,531
##                    self.condition = True
##                else:
##                    self.symX,self.symY = 149,531
##                    self.condition = False
##                self._x += self._dx
##            if self.condition == False:
##                self.symX,self.symY = 116,531
##                self.condition = True
##            else:
##                self.symX,self.symY = 149,531
##                self.condition = False
     
##        def collide(self, other):
##            if isinstance(other,Wall):
##                    x, y, w, h = other.rect()
##                    if not (0 <= self._x + self._dx <= w - self.W):
##                        self._dx = -self._dx
##                        if self.condition == False:
##                            self.symX,self.symY = 116,531
##                            self.condition = True
##                        else:
##                            self.symX,self.symY = 149,531
##                            self.condition = False
##                    self._x += self._dx

                            
##            
##
##            elif isinstance(other,Mario):        
##                    x, y, w, h = other.rect()
##                    border_left, border_right = x - self.W, x + w
##                    border_top, border_bottom = y - self.H, y + h
##                    nearest_y = border_bottom
##                    if abs(border_left - self._x) < abs(border_right - self._x):
##                            nearest_x = border_left
##                            self._dy = +self.SPEED * 2
##
##            
##                    else:
##                            nearest_x = border_right
##                            self._dy = +self.SPEED * 2
                
##                    if abs(border_top - self._y) < abs(border_bottom - self._y):
##                            nearest_y = border_top
##                    if abs(nearest_x - self._x) < abs(nearest_y - self._y):
##                        self._x = nearest_x
##                        self._dy = +self.SPEED * 2

##                        print("Ho preso Mario")
##                        self.W,self.H = 17,16
##                        self.symX,self.symY = 389,15
                           
##                            
##                    else:
##                        self.died()
##
##                            
##                           
##                            
##
##        def died(self):
##            print("Mario mi ha preso")
##            self.symX,self.symY = 58,383
##            self.W,self.H = 19,11
##            self._y = 273
##            self._arena.remove(self)
##            
##
##
##
##        def rect(self) -> (int, int, int, int):
##            return self._x, self._y, self.W, self.H
##
##        def symbol(self):
##            return self.symX,self.symY
##--------------------FINE---------------------------------
