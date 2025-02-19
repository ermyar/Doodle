import random, pygame

from script.border import PhysicsEntity

class Item(PhysicsEntity):
    '''класс, описывающий поведение предметов, что на платформах'''
    
    def __init__(self, border):
        '''создаёт объъект класса Item'''
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
        '''моделирует поведение платформы, при контакте с игроком'''
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