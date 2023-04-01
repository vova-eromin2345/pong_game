from pygame import *
from random import choice

mixer.init()

class Text:
    def __init__(self, font, value, color):
        self.value = value
        self.font = font
        self.color = color
        self.text_object = self.font.render(self.value, True, self.color)
    def draw(self, position):
        window.blit(self.text_object, position)

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, size_x, size_y, player_speed, player_x=0, player_y=0):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, player_image, size_x, size_y, player_speed, player_x):
        super().__init__(player_image, size_x, size_y, player_speed, player_x)
        self.rect.centery = h / 2
        self.score = 0
    def update_l(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        elif keys[K_s] and self.rect.bottom < h-5:
            self.rect.y += self.speed
    def update_r(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        elif keys[K_DOWN] and self.rect.bottom < h-5:
            self.rect.y += self.speed
    def update_ai(self, ball):
        self.rect.y = ball.rect.y
        self.rect.clamp_ip(Rect(5, 5, window.get_width()-10, window.get_height()-10))
        
    def draw_score(self, font):
        score_text = font.render(f'{self.score}', True, (0, 0, 0))
        window.blit(score_text, ( abs(self.rect.centerx - 200) , 100))
        
    def reset_score(self):
        self.score = 0

class Ball(GameSprite):
    def __init__(self, player_image, size_x, size_y, player_speed_x, player_speed_y):
        super().__init__(player_image, size_x, size_y, None)
        self.rect.center = w//2, h//2
        self.speed_x, self.speed_y = player_speed_x, player_speed_y
    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.y <= 0 or self.rect.bottom >= h:
            self.speed_y *= -1
        if sprite.spritecollide(self, pong_group, False):
            self.speed_x *= -1
            mixer.Sound('music/collide_sound.ogg').play()
            
class Menu:
    def __init__(self, font):
        self.font = font
        self.buttons = []
        self.functions = []
        self.select_btn_index = 0
    
    def select(self, direction):
        if direction == 1:
            self.select_btn_index = min(self.select_btn_index+direction, len(self.buttons)-1)
        elif direction == -1:
            self.select_btn_index = max(0, self.select_btn_index+direction)
    
    def draw_menu(self, padding_y):
        for index, btn in enumerate(self.buttons):
            obj = btn.text_object
            x, y = w//2-obj.get_width()//2, (index+1)*padding_y
            if index == self.select_btn_index:
                draw.rect(window, (200, 200, 0), Rect(x-10, y-10, obj.get_width()+20, obj.get_height()+20 ), 4)
            btn.draw((x, y))
    def add_option(self, btn_text, btn_color, function):
        btn = Text(self.font, btn_text, btn_color)
        self.buttons.append(btn)
        self.functions.append(function)
    def do_func(self):
        self.functions[self.select_btn_index]()
        

w, h = 700, 500
window = display.set_mode((w, h))

clock = time.Clock()
FPS = 60

goal = 5
players_length = 1
font.init()
score_font = font.SysFont('Verdana', 90)
text2 = font.Font(None, 80)
menu_font = font.SysFont("Arial", 100)

pong_group = sprite.Group()
player_width, player_height = 40, 140
player_l = Player('images/pong rocket.png', player_width, player_height, 5, 5)
player_r = Player('images/pong rocket.png', player_width, player_height, 5, w-player_width-5)
pong_group.add(player_l, player_r)

possibl_ball_speed = [i for i in range(-3, 4)  if abs(i) not in [0, 1]]
ball = Ball('images/ball.png', 70, 70, choice(possibl_ball_speed), choice(possibl_ball_speed))

main_menu = Menu(menu_font)
main_menu.add_option("Play", (0, 0, 200), lambda: call_settings_menu())
main_menu.add_option("Exit", (200, 0, 0), lambda: call_main_menu.quit_menu())

settings_menu = Menu(menu_font)
settings_menu.add_option("1 Player", (255, 255, 255), lambda: game())
settings_menu.add_option("2 Players", (255, 255, 255), lambda: game())


def call_main_menu():
    display.set_caption("Menu")
    menu = True
    def quit_menu():
        nonlocal menu
        menu = False
    call_main_menu.quit_menu = quit_menu
    while menu:
        for ev in event.get():
            if ev.type == QUIT:
                quit_menu()
            elif ev.type == KEYDOWN:
                if ev.key == K_UP:
                    main_menu.select(-1)
                elif ev.key == K_DOWN:
                    main_menu.select(1)
                elif ev.key == K_RETURN:
                    quit_menu()
                    main_menu.do_func()
        window.fill((0, 0, 0))
        main_menu.draw_menu(150)
        display.update()
        clock.tick(FPS)

def call_settings_menu():
    global players_length
    display.set_caption("Settings menu")
    menu = True
    def quit_menu():
        nonlocal menu
        menu = False
    call_settings_menu.quit_menu = quit_menu
    while menu:
        for ev in event.get():
            if ev.type == QUIT:
                quit_menu()
            elif ev.type == KEYDOWN:
                if ev.key == K_UP:
                    settings_menu.select(-1)
                elif ev.key == K_DOWN:
                    settings_menu.select(1)
                elif ev.key == K_RETURN:
                    players_length = int(settings_menu.buttons[settings_menu.select_btn_index].value.split()[0] )
                    quit_menu()
                    settings_menu.do_func()
        window.fill((0, 0, 0))
        settings_menu.draw_menu(150)
        display.update()
        clock.tick(FPS)

def game():
    global goal, players_length
    game = True
    finish = False
    quit_game = False
    left_player_update = {
        players_length==1: lambda: player_l.update_ai(ball),
        players_length==2: player_l.update_l
    }
    display.set_caption('Ping Pong')
    while game:
        for ev in event.get():
            if ev.type == QUIT:
                finish = True
                quit_game = True
        window.fill((112, 190, 250))
        if not finish:
            draw.line(window, (0, 0, 0), (w//2, 0), (w//2, h))
            pong_group.draw(window)
            left_player_update[True]()
            player_r.update_r()
            ball.reset()
            ball.update()
            [x.draw_score(score_font) for x in pong_group]
            player_lose = {
                player_l.score>=goal:'Left player',
                player_r.score>=goal:'Right player'
            }
            if player_lose.get(True):
                lose_text = text2.render(f'{player_lose.get(True)} win!', True, (0, 150, 0) )
                window.blit(lose_text, (200, 50))
                mixer.Sound('music/win_sound.ogg').play()
                [x.reset_score()for x in pong_group]
                display.update()
                time.delay(3000)
                finish = True
            if ball.rect.left <= 5:
                player_r.score += 1
                finish = True
            elif ball.rect.right >= w-5:
                player_l.score += 1
                finish = True
        else:
            ball.rect.center = w//2, h//2
            ball.speed_x, ball.speed = choice(possibl_ball_speed), choice(possibl_ball_speed)
            finish = False
            if quit_game:
                [x.reset_score()for x in pong_group]
                game = False
                call_main_menu()
        display.update()
        
        clock.tick(FPS)

call_main_menu()
