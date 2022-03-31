import pygame , sys
from random import randint

pygame.init()

clock = pygame.time.Clock()
FPS = 15


def end_game(arr, value):
    zer = 0

    for row in arr:
        zer += row.count(0)
        if row.count(value) == 3:
            return value
    
    for col in range(3):
        if arr[0][col] == value and arr[1][col] == value and arr[2][col] == value:
            return value

    if arr[0][0] == value and arr[1][1] == value and arr[2][2] == value:
        return value
    if arr[0][2] == value and arr[1][1] == value and arr[2][0] == value:
        return value
    if zer == 0:
        return "piece"

    return False


def print_message(message, x, y, color, font = 'Calibri', font_size=55):
    font_type = pygame.font.SysFont(font, font_size)
    text = font_type.render(message, True, color)
    screen.blit(text, (x,y))

class Button:
    players = 0
    
    def __init__(self, width, height):
        self.width = width 
        self.height = height
        self.idle_color = (7,110,156)
        self.hover_color = (38,179,242)

    def draw(self, x, y, message, action = None, font_size = 30):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height:
            pygame.draw.rect(screen, self.hover_color, (x, y, self.width, self.height))

            if click[0] == 1 and action is not None:
                if action == pygame.QUIT:
                    sys.exit()

                elif action == start_game_1:
                    Button.players = 1
                    action()

                elif action == start_game_2:
                    Button.players = 2
                    action()
                else:
                    action()
        
        else:
            pygame.draw.rect(screen, self.idle_color, (x, y, self.width, self.height))

        print_message(message=message, x=x + 10, y=y + 10, color=BLACK)

size_block = 150
null = 15
size_x = size_y = size_block * 3 + null * 4
screen = pygame.display.set_mode((size_x,size_y))
pygame.display.set_caption("X/O")

WHITE = (255,255,255)
BLACK = (0,0,0)
RED =  (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
arr = [[0]*3 for i in range (3)]
in_game = True
count = 0
numbers = 0
game_over_x = game_over_o =False
game_running = True

def start_game_1():
    start_game()

def start_game_2():
    start_game()    

def start_game():
    global in_game, count, arr, game_over_x, game_over_o, size_block, null, game_running, numbers
    screen.fill(BLACK)

    while game_running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN and in_game:
                x_mouse, y_mouse = pygame.mouse.get_pos()
                col = x_mouse // (size_block+null)
                row = y_mouse // (size_block+null)
                if Button.players == 2:
                    if arr[row][col] == 0:
                        if numbers % 2 == 0:
                            arr[row][col] = 'x'
                            game_over_x = end_game(arr, 'x')
                        else:
                            arr[row][col] = 'o'
                            game_over_o = end_game(arr, 'o')
                        numbers += 1
                else:
                    if arr[row][col] == 0:
                        arr[row][col] = 'x'
                        game_over_x = end_game(arr, 'x')
                        if game_over_x != 'x' and game_over_x != 'piece':
                            while True:
                                rand_row = randint(0,2)
                                rand_col = randint(0,2)
                                count += 1
                                if arr[rand_row][rand_col] != 'x' and arr[rand_row][rand_col] !='o':
                                    arr[rand_row][rand_col]='o'
                                    game_over_o = end_game(arr, 'o')
                                    print (count)
                                    break

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                in_game = True
                count = 0
                arr = [[0]*3 for i in range (3)]
                screen.fill(BLACK)
                game_over_o = game_over_x = False

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                in_game = True
                count = 0
                arr = [[0]*3 for i in range (3)]
                screen.fill(BLACK)
                game_over_o = game_over_x = False
                main_menu()

        if in_game:
            for row in range(3):
                for col in range(3):
                    if arr[row][col] == 'x':
                        color = RED
                    elif arr[row][col] == 'o':
                        color = BLUE
                    else: 
                        color = WHITE
                    x = col * size_block + (col+1) * null
                    y = row * size_block + (row+1) * null
                    pygame.draw.rect(screen, color, (x, y, size_block, size_block))
                    if color == RED:
                        pygame.draw.line(screen, BLACK, (x + 10, y + 10), (x + size_block - 10, y + size_block - 10), 15)
                        pygame.draw.line(screen, BLACK, (x + size_block - 10, y + 10), (x + 10, y + size_block - 10), 15)
                    elif color == BLUE:
                        pygame.draw.circle(screen, BLACK, (x + size_block // 2, y + size_block // 2), size_block // 2 - 10, 15)
        
        if game_over_o or game_over_x:
            if Button.players == 2:
                in_game = False
                screen.fill(BLACK)
                if game_over_x == 'x':
                    print_message("Победа X", 100,110, WHITE, font_size=80)
                elif game_over_o:
                    print_message("Победа O", 100,110, WHITE, font_size=80)
                else:
                    print_message("Ничья", 145,110, WHITE, font_size=80)
            else:
                in_game = False
                screen.fill(BLACK)
                if game_over_x == 'x':
                    print_message("Победа", 130,110, WHITE, font_size=80)
                elif game_over_o:
                    print_message("Поражение", 75,110, WHITE, font_size=80)
                else:
                    print_message("Ничья", 130,110, WHITE, font_size=80)

            print_message("SPACE для перезагрузки", 100,250, WHITE, font_size=30)
            print_message("ESC для выхода в главное меню", 65,350, WHITE, font_size=30)

        pygame.display.update()

        clock.tick(FPS)

def main_menu():
    menu_bg = pygame.image.load('menu.jpeg')

    start_1_players_btn = Button(230,70)
    start_2_players_btn = Button(230,70)
    quit_btn = Button(230, 70)

    show_menu = True
    while show_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        screen.blit(menu_bg, (0, 0))
        start_1_players_btn.draw(35,70, "1 Игрок", start_game_1)
        start_2_players_btn.draw(35,230, "2 Игрока", start_game_2)
        quit_btn.draw(35,390, "Выход", sys.exit)
        pygame.display.update()
        clock.tick(FPS)


main_menu()

