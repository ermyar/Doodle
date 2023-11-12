from script.entities import PhysicsEntity
from script.utils import load_image

class Player(PhysicsEntity):
    '''класс, дополняющий поведение игрока'''
    base = 'doodlick/'
    timer = 0
    reason = "none"
    
    def print(self, movement, surf):
        '''обновление и отображение игрока на экран'''
        self.update(movement)
        self.render_over(surf)
        
    def custom(self):
        '''обновление изображения игрока, используется при кастомизации игрока'''
        self.game.assets['player'] = load_image(self.base + self.game.set + 'left.png')
        
    def change(self, direction):
        '''меняет ориентацию игрока, на соответствующую напрвлению его движения'''
        self.game.assets['player'] = load_image(self.base + self.game.set + direction)
 