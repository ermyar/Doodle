import random
import pygame

from script.utils import load_image

class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.type = e_type
        self.pos = list(pos)
        self.size = size
        self.velocity = [0, 0, 0, 0, 0]
        self.tm = 0
    def update(self, movement):
        if (self.tm > 0):
            self.tm -= 1
            self.velocity[1] += 0.1
        
        frame_movement = (movement[0] + self.velocity[0] - self.velocity[2], 
                          movement[1] + self.velocity[1] - self.velocity[3])
        
        self.pos[0] += frame_movement[0]
        self.pos[1] += frame_movement[1]

        
    def render(self, surf):
        surf.blit(self.game.assets[self.type], self.pos)
        
    def render_over(self, surf):
        if (self.pos[0] >= self.game.WIDTH):
            self.pos[0] -= self.game.WIDTH
            self.render(surf)
        elif (self.pos[0] + self.size[0] > self.game.WIDTH):
            self.render(surf)
            self.pos[0] -= self.game.WIDTH
            self.render(surf)
            self.pos[0] += self.game.WIDTH
        elif (self.pos[0] <= -self.size[0]):
            self.pos[0] += self.game.WIDTH
            self.render(surf)
        elif (self.pos[0] < 0):
            self.render(surf)
            self.pos[0] += self.game.WIDTH
            self.render(surf)
            self.pos[0] -= self.game.WIDTH
        else:
            self.render(surf)
    
        
class Player(PhysicsEntity):
    base = 'doodlick/'
    timer = 0
    reason = "none"
    
    def print(self, movement, surf):
        self.update(movement)
        self.render_over(surf)
        
    def custom(self):
        self.game.assets['player'] = load_image(self.base + self.game.set + 'left.png')
        
    def change(self, direction):
        self.game.assets['player'] = load_image(self.base + self.game.set + direction)
            

class Border(PhysicsEntity):
    
    def generate(self, type): 
        st = ""
        if (80 < type <= 100):
            st = "blue_hor5"
        elif (60 < type <= 80):
            st = "one_punch"
        elif (0 < type <= 60):
            st = "green_stable"
        
        
        tmp = Border(self.game, st, 
                    (random.randint(0, self.game.WIDTH - self.size[0]), 
                    self.pos[1] - 6 * random.randint(4, 12)), self.size)
        
        while (self.game.borders[-1].pos[1] - tmp.pos[1] > 30):
            self.game.borders.append(
                Border(self.game, 'broken0', (random.randint(0, 590), self.game.borders[-1].pos[1] - 
                    random.randint(20, int(self.game.borders[-1].pos[1] - tmp.pos[1]))), self.size))
            
        tmp.pos[1] -= 30

        chance = random.randint(1, 15)
        
        if (chance == 1 and st == 'green_stable'):
            self.game.items.append(Item(tmp))
            
        
        if (st == "blue_hor5"):
            if (random.randint(0, 1) == 1):
                tmp.velocity[0] = 1.5
            else:
                tmp.velocity[0] = -1.5    
        return tmp
    
    def print(self, movement, surf):
        self.update(movement)
        
        if (self.type == 'blue_hor5'):
            self.render_over(surf)
            
        elif (self.type == 'broken0'):
            if (55 == self.tm):
                self.type = "broken1"
            self.render(surf)
        elif (self.type == 'broken1'):
            if (50 == self.tm):
                self.type = "broken2"
            self.render(surf)
        elif (self.type == 'broken2'):
            if (45 == self.tm):
                self.type = "broken3"
            self.render(surf)
        elif (self.type == 'broken3'):
            self.render(surf)
        elif (self.type == 'green_stable'):
            self.render(surf)
        elif (self.type == 'one_punch'):
            self.render(surf)
            
    def Rect(self, player):
        player_r = pygame.Rect(player.pos[0], player.pos[1] + player.size[1] - 1, player.size[0], 1)

        if (self.type == 'broken3' or self.type == 'broken1' or self.type == 'broken2' or self.type == 'hide'):
            return
        if (player.velocity[1] >= 0 and player_r.colliderect(pygame.Rect(self.pos, self.size))):
            if (self.type == 'broken0'):
                self.tm = 60
            else:
                player.velocity[1] = -6
                if (self.type == 'one_punch'):
                    self.type = 'hide'
                if (player.pos[1] <= self.game.lst):
                    self.game.cnt += (self.game.lst - player.pos[1]) // 3
            
            
class Item(Border):
    def __init__(self, border):
        self.game = border.game
        self.tm = 0
        self.velocity = [0, 0, 0, 0, 0]
        tmp = random.randint(1, 10)
        if (tmp == 1):
            self.type = 'hat'
        elif (tmp <= 3):
            self.type = 'batoot'
        else:
            self.type = 'spring0' 
        self.size = self.game.sizes[self.type]
        self.pos = [border.pos[0] + (border.size[0] - self.size[0]) / 2, border.pos[1] - self.size[1]]
        
        
    def Rect(self, player):
        if (self.type == 'hat'):
            player_r = pygame.Rect(player.pos[0], player.pos[1], player.size[0], player.size[1])
            if player_r.colliderect(pygame.Rect(self.pos, self.size)):
                player.timer = 300
                player.velocity[1] = -30
                player.reason = "hat"
                if (player.pos[1] > self.game.lst):
                    player.velocity[4] = (player.pos[1] - self.game.lst) / player.timer
                else:
                    player.velocity[4] = 0
                
        if (self.type == 'spring0'):
            player_r = pygame.Rect(player.pos[0], player.pos[1] + player.size[1] - 1, player.size[0], 1)
            if player.velocity[1] >= 0 and player_r.colliderect(pygame.Rect(self.pos, self.size)):
                player.velocity[1] = -12
                player.timer = 120
                self.pos[1] -= 16
                self.type = "spring1"
                if (player.pos[1] > self.game.lst):
                    player.velocity[4] = (player.pos[1] - self.game.lst) / player.timer
                else:
                    player.velocity[4] = 0
                
        
        if (self.type == 'batoot'):
            player_r = pygame.Rect(player.pos[0], player.pos[1] + player.size[1] - 1, player.size[0], 1)
            if player.velocity[1] >= 0 and player_r.colliderect(pygame.Rect(self.pos, self.size)):
                player.velocity[1] = -18
                player.timer = 180
                player.reason = 'batoot'
                if (player.pos[1] > self.game.lst):
                    player.velocity[4] = (player.pos[1] - self.game.lst) / player.timer
                else:
                    player.velocity[4] = 0
                
                    