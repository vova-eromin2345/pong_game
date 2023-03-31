from pygame import *
from random import randint

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
        self.rect.clamp_ip(window.get_rect())
        
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
            self.select_btn_index = min(0, self.select_btn_index+direction)
    
    def draw_menu(self, padding_x, padding_y):
        for index, btn in enumerate(self.buttons):
            rect = Rect(padding_x, (index+1)*padding_y, btn.get_width()+20, 
                        btn.get_height()+20)
            if index == self.select_btn_index:
                draw.rect(window, (200, 200, 0), rect)
            window.blit(btn, rect)
    def add_option(self, btn_text, function, btn_color):
        btn = self.font.render(btn_text, True, btn_color)
        self.buttons.append(btn)
        self.functions.append(function)
    def do_func(self):
        self.functions[self.select_btn_index]()
w, h = 700, 500
window = display.set_mode((w, h))
display.set_caption('Ping Pong')


clock = time.Clock()
FPS = 60

goal = 5

font.init()
score_font = font.SysFont('Verdana', 90)
text2 = font.Font(None, 80)

pong_group = sprite.Group()
player_width, player_height = 40, 140
player_l = Player('images/pong rocket.png', player_width, player_height, 5, 5)
player_r = Player('images/pong rocket.png', player_width, player_height, 5, w-player_width-5)
pong_group.add(player_l, player_r)

ball = Ball('images/ball.png', 70, 70, randint(3, 5), randint(3, 5))


def menu():
    menu = True
    while menu:
        for ev in event.get():
            if ev.type == QUIT:
                menu = False
        window.fill((0, 0, 0))
        display.update()
        clock.tick(FPS)

def game():
    global goal
    game = True
    finish = False

    while game:
        for ev in event.get():
            if ev.type == QUIT:
                game = False
        
        window.fill((112, 190, 250))
        if not finish:
            draw.line(window, (0, 0, 0), (w//2, 0), (w//2, h))
            pong_group.draw(window)
            player_l.update_l()
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
            ball.speed_x, ball.speed_y = randint(4, 6), randint(4, 6)
            finish = False

        display.update()
        
        clock.tick(FPS)

game()