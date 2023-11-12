import pygame

BASE_IMG_PATH = 'data/pictures/'
chars = "qwertyuiopasdfghjklzxcvbnm1234567890"

def load_image(path):
    '''загружает файл по адресу'''
    img = pygame.image.load(BASE_IMG_PATH + path).convert_alpha()
    return img

def init_font(height):
    '''иницилиазирует и возвращает шрифт системы'''
    pygame.font.init()
    my_font = pygame.font.Font('data/DoodleJump.ttf', height)
    my_font.set_bold(0)
    return my_font

def print_text(surf, my_font, message, pos):
    '''печатает текст на экран'''
    text_surface = my_font.render(message, False, (0, 0, 0))
    surf.blit(text_surface, pos)
    
def print_image(path, pos, surf):
    '''выводит текст на экран'''
    bg = load_image(path)
    surf.blit(bg, pos)
    
    
def inputs(event, username, shift):
    '''считывает данные с клавиатуры'''
    if (event.type == pygame.KEYDOWN):
        if (event.key == pygame.K_BACKSPACE):
            username = username[0:len(username)-1]  
        elif (event.key == pygame.K_LALT or event.key == pygame.K_RALT or event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL):
            pass
        elif (event.key == pygame.K_CAPSLOCK or event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT):
            shift = 1 - shift
        elif (event.key == pygame.K_SPACE):
            if (len(username) == 16):
                return (username, shift)
            username += ' '
        elif (chr(event.key) in chars):
            if (len(username) == 16):
                return (username, shift)
            if (shift):
                match (chr(event.key)):
                    case ('1'):
                        username += '!'
                    case ('2'):
                        username += '@'
                    case ('3'):
                        username += '#'
                    case ('4'):
                        username += '$'
                    case ('5'):
                        username += '%'
                    case ('6'):
                        username += '^'
                    case ('7'):
                        username += '&'
                    case ('8'):
                        username += '*'
                    case ('9'):
                        username += '('
                    case ('0'):
                        username += ')'
                    case _:
                        username += chr(event.key).upper()
            else:
                username += chr(event.key)
            
    if (event.type == pygame.KEYUP):
        if (event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT):
            shift = 1 - shift
    
    return (username, shift)
    