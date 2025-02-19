from script.utils import print_text

class Highscore:
    def __init__(self, game):
        '''создаёт объукт класса Highscore'''
        self.game = game
        self.array = []
        self.left = 0
        self.right = 30
        name = open('data/name.txt')
        score = open('data/score.txt')
        tmp1 = list(name.read().split('\n'))
        tmp2 = list(score.read().split('\n'))
        length = len(tmp1) - 1
        for i in range(length):
            self.array.append((int(tmp2[i]), tmp1[i]))
        self.array.sort(reverse=True)
    
    def Add(self, score, username):
        '''добавляет в таблицы результаты'''
        txt = open('data/name.txt', 'a')
        txt.write(username + '\n')
        txt.close()
        txt = open('data/score.txt', 'a')
        txt.write(str(score) + '\n')
        txt.close()
        self.array.append((score, username))
        self.array.sort(reverse=True)
        
    def print(self):
        '''выводит таблицу на экран'''
        print_text(self.game.screen, self.game.font, "Local Records: ", (240, 0))
        for i in range(self.left, min(self.right, len(self.array))):
            print_text(self.game.screen, self.game.font, str(i + 1) + ".  " + self.array[i][1], (60, 50 + (i - self.left) * 30))
            print_text(self.game.screen, self.game.font, str(self.array[i][0]), (430, 50 + 30 * (i - self.left)))