import random, pygame

from script.entities import PhysicsEntity
from script.item import Item

class Border(PhysicsEntity):
    '''класс, описывающий поведение платформ'''
    def generate(self, type): 
        '''генерирует новою платформу, для гарантии того, что прыгунть и продолжить игру можно. между нагенерированной и исходной создаются пустые'''
        st = ""
        if (80 < type <= 100):
            st = "blue_hor5"
        elif (60 < type <= 80):
            st = "one_punch"
        elif (0 < type <= 60):
            st = "green_stable"
        
        
        tmp = Border(self.game, st, 
                    (random.randint(0, self.game.WIDTH - self.size[0]), 
                    self.pos[1] - 5 * random.randint(4, 8)), self.size)
        
        
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
        '''отображение платформы на экран в зависимости от типа'''
        self.update(movement)
            
        if (self.type == 'broken0'):
            if (55 == self.tm):
                self.type = "broken1"
        elif (self.type == 'broken1'):
            if (50 == self.tm):
                self.type = "broken2"
        elif (self.type == 'broken2'):
            if (45 == self.tm):
                self.type = "broken3"
                
        if (self.type != 'hide'):
            self.render(surf)
        
            
    def Rect(self, player):
        '''моделирует поведение платформы, при контакте с игроком'''
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
            