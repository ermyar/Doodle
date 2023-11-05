import sys
import pygame

from script.entities import *
from script.utils import *
from script.highscore import *

class Game:

    def __init__(self):
        pygame.init()
        
        self.HEIGHT = 960
        self.WIDTH = 640
        pygame.display.set_caption('Doodle Jump')
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        
        self.font = init_font(30)
        self.clock = pygame.time.Clock()
        self.lst = 0
        self.cnt = 0
        self.movement = [0, 0]
        self.high = Highscore(self)
        self.assets = {
            'player': load_image('doodlick/classic/left.png'),
            'green_stable': load_image('borders/green_border.png'),
            'blue_hor5': load_image('borders/blue_hor.png'),
            'broken0': load_image('borders/broken0.png'),
            'broken1': load_image('borders/broken1.png'),
            'broken2': load_image('borders/broken2.png'),
            'broken3': load_image('borders/broken3.png'),
            'one_punch': load_image('borders/one_punch.png'), 
            'spring0': load_image('items/pressed.png'),
            'spring1': load_image('items/unpressed.png'),
            'hat': load_image('items/hat.png'),
            'batoot': load_image('items/batoot.png')
        }
        
        self.items = []
        self.sets = ['blue', 'bunny', 'classic', 'jungle', 'soccer', 'space', 'underwater']
        self.sizes = {
            'batoot': (36, 14),
            'hat': (32, 20),
            'spring0': (17, 12),
            'spring1': (17, 28)
        }
        self.item_list = ['batoot', 'hat', 'spring0']
        self.set = "classic/"
        self.player = Player(self, 'player', (300, 710), (62, 60))
                
    def menu(self):
        print_image("environment/bck@2x.png", (0, 0), self.screen)
        username = ""
        shift = 0
        while True:        
            
            print_image("environment/bck@2x.png", (0, 0), self.screen)
            print_image('environment/doodle-jump@2x.png', (50, 50), self.screen)
            print_image('environment/play@2x.png', (50, 300), self.screen)
            print_image('environment/custom-button-on@2x.png', (90, 450), self.screen)
            print_text(self.screen, self.font, 'SCORES', (110, 550))
            print_text(self.screen, self.font, 'Type your nick', (330, 350))
            print_text(self.screen, self.font, username, (330, 400))            
            for event in pygame.event.get():

                if (event.type == pygame.QUIT):
                    pygame.quit()
                    sys.exit()
                if ((event.type == pygame.MOUSEBUTTONDOWN) and (50 <= event.pos[0] <= 272 and 300 <= event.pos[1] <= 380)) or (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN):
                    val = self.run()
                    if (val == -1):
                        continue
                    self.high.Add(val, username)
                    
                if (event.type == pygame.MOUSEBUTTONDOWN) and (110 <= event.pos[0] <= 210 and 550 <= event.pos[1] <= 580):
                    self.scoretable()
                if (event.type == pygame.MOUSEBUTTONDOWN) and (90 <= event.pos[0] <= 218 and 450 <= event.pos[1] <= 488):
                    self.set = self.custom()
                (username, shift) = inputs(event, username, shift)         

            pygame.display.update()
            self.clock.tick(60)   
            
    def pause(self, score):
        while True:
            print_image("environment/bck@2x.png", (0, 0), self.screen)
            print_text(self.screen, self.font, 'Total Score: ' + str(int(score)), (0, 0))
            print_image("environment/pause-cover@2x.png", (0, 0), self.screen)
            print_image("environment/resume@2x.png", (100, 600), self.screen)
            print_image("environment/menu@2x.png", (100, 700), self.screen)
            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    pygame.quit()
                    sys.exit()
                    
                if (event.type == pygame.KEYDOWN):
                    if (event.key == pygame.K_ESCAPE):
                        return 1
                if ((event.type == pygame.MOUSEBUTTONDOWN) and (100 <= event.pos[0] <= 324 and 600 <= event.pos[1] <= 680)):
                    return 0
                if ((event.type == pygame.MOUSEBUTTONDOWN) and (100 <= event.pos[0] <= 324 and 700 <= event.pos[1] <= 780)):
                    return 1
            pygame.display.update()
            self.clock.tick(60) 
        
    def run(self):
        
        self.player = Player(self, 'player', (300, 710), (62, 60))
        self.player.custom()
        self.borders = [Border(self, "green_stable", (295, 770), (57, 15))]
        
        self.items = []
        
        for i in range(20): 
            self.borders.append(self.borders[-1].generate(random.randint(1, 80)))
            
        self.cnt = 0
        self.lst = 710
        
        score = 0
        absolut = 710
        
        while True:
            print_image("environment/bck@2x.png", (0, 0), self.screen)

            self.player.velocity[1] += 0.1    
            
            if (self.player.timer == 1):
                self.movement = [0, -self.player.velocity[1]]
                self.player.timer -= 1
                self.cnt = 0
                self.player.velocity[4] = 0
                self.player.reason = "none"
            elif (self.player.timer > 1):
                self.movement = [0, -self.player.velocity[1] - self.player.velocity[4]]
                self.player.timer -= 1
            elif (self.cnt > 0):
                self.movement[1] = 3
                self.cnt -= 1
            else:
                self.movement[1] = 0
                
            for i in self.borders:
                i.print(self.movement, self.screen)
                
            for i in self.items:
                i.update(self.movement)
                i.render(self.screen)
            
            absolut += self.movement[1]

            self.player.print(self.movement, self.screen) 
            if (self.player.reason == "hat"):
                print_image('items/propeller' + str((self.player.timer // 8) % 3 + 1) + ".png", (self.player.pos[0] + 15, self.player.pos[1] - 6), self.screen)
            
            print_text(self.screen, self.font, 'Total Score: ' + str(int(score)), (0, 0))
            
            score = max(score, self.lst - self.player.pos[1] + absolut - self.lst)
                        
            while (self.borders[0].pos[1] > self.HEIGHT):
                self.borders.pop(0)
                if (self.borders[0].type[:-2] != "broken"):
                    self.borders.append(self.borders[-1].generate(random.randint(1, 100)))
            

            for i in self.borders:
                i.Rect(self.player)

            for i in self.items:
                i.Rect(self.player)
                    
            if (self.player.pos[1] >= self.HEIGHT):
                return int(score)
            
            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    pygame.quit()
                    sys.exit()
                
                if (event.type == pygame.KEYDOWN):
                    if (event.key == pygame.K_ESCAPE):
                        tmp = self.pause(score)
                        if (tmp == 1):
                            return -1
                    if (event.key == pygame.K_RIGHT):
                        self.player.velocity[0] = 4
                        self.player.change('right.png')
                    if (event.key == pygame.K_LEFT):
                        self.player.velocity[2] = 4
                        self.player.change('left.png')                       

                if (event.type == pygame.KEYUP):
                    if (event.key == pygame.K_RIGHT):
                        self.player.velocity[0] = 0
                    if (event.key == pygame.K_LEFT):
                        self.player.velocity[2] = 0

            pygame.display.update()
            self.clock.tick(60) 

    def custom(self):
        choise = self.set
        pos = [(60, 150), (210, 150), (360, 150), (510, 150), (135, 320), (285, 320), (435, 320)]
        while True:        
            print_image("environment/bck@2x.png", (0, 0), self.screen)
            print_image('environment/done.png', (400, 600), self.screen)
            print_text(self.screen, self.font, "Chooose your skin and press done", (120, 100))
            for i in range(len(pos)):
                print_image('doodlick/' + self.sets[i] + '/' + 'left@2x.png', pos[i], self.screen)
                print_text(self.screen, self.font, self.sets[i], (pos[i][0] + 20, pos[i][1] + 120))
                
            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    pygame.quit()
                    sys.exit()
                
                if (event.type == pygame.KEYDOWN):
                    if (event.key == pygame.K_RETURN):
                        return choise
                if (event.type == pygame.MOUSEBUTTONDOWN):
                    for i in range(7):
                        if (pos[i][0] <= event.pos[0] <= pos[i][0] + 124) and (pos[i][1] <= event.pos[1] <= pos[i][1] + 120):
                            choise = self.sets[i] + '/'

                    if (400 <= event.pos[0] <= 512 and 600 <= event.pos[1] <= 640):
                        return choise
            
            pygame.display.update()
            self.clock.tick(60)
        
    def scoretable(self):
        self.left = 0
        while True:
            print_image("environment/bck@2x.png", (0, 0), self.screen)
            
            self.high.print()
            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    pygame.quit()
                    sys.exit()
                    
                if (event.type == pygame.KEYDOWN):
                    if (event.key == pygame.K_DOWN):
                        if (len(self.high.array) > self.high.right):
                            self.high.left += 1
                            self.high.right += 1
                    if (event.key == pygame.K_UP):
                        if (self.high.left > 0):
                            self.high.left -= 1
                            self.high.right -= 1
                    if (event.key == pygame.K_ESCAPE):
                        return
                
            pygame.display.update()
            self.clock.tick(60) 
    
Game().menu()