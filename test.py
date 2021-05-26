import pygame
import pygame_menu

pygame.init()
surface = pygame.display.set_mode((800, 800))

def set_difficulty(value, difficulty):
    # Do the job here !
    print(str(value)+"___"+str(difficulty))

def start_the_game():
    # Do the job here !
    surface.fill((255,255,255))
    menu = pygame_menu.Menu(300, 400, 'Welcome',
                       theme=pygame_menu.themes.THEME_BLUE)
    menu.add.label("Win", max_char = -1, font_size =20)
    menu.mainloop(surface)

menu = pygame_menu.Menu(300, 400, 'Welcome',
                       theme=pygame_menu.themes.THEME_BLUE)

menu.add.text_input('Name :', default='John Doe')
menu.add.selector('Difficulty :', [('Hard', 1), ('Easy', 2)], onchange=set_difficulty)
menu.add.button('Play', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)

menu.mainloop(surface)