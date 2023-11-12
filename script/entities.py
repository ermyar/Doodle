from script.utils import load_image

class PhysicsEntity:
    '''класс, описывающий поведение физического тела в игре'''
    def __init__(self, game, e_type, pos, size):
        '''создаёт объект класс PhysicsEntity'''
        self.game = game
        self.type = e_type
        self.pos = list(pos)
        self.size = size
        self.velocity = [0, 0, 0, 0, 0]
        self.tm = 0
    def update(self, movement):
        '''обновляет параметры объекта, исходя из движения всей системы'''
        if (self.tm > 0):
            self.tm -= 1
            self.velocity[1] += 0.1
        
        frame_movement = (movement[0] + self.velocity[0] - self.velocity[2], 
                          movement[1] + self.velocity[1] - self.velocity[3])
        
        self.pos[0] += frame_movement[0]
        self.pos[1] += frame_movement[1]

        
    def render(self, surf):
        '''отображает на дисплее картинку'''
        surf.blit(self.game.assets[self.type], self.pos)
        
    def render_over(self, surf):
        '''продвинутое отображение. объект, выходяющий за границы окна, будет отображен с другой стороны (по сути это замыкание по кругу)'''
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
