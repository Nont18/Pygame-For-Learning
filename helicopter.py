import random
import pygame

pygame.init()

# ตั้งค่าภาพพื้นหลัง 
background_color = 'blue' # red, green, blue, yellow, white, pink 

# ตั้งค่าตัวละคร 
player_image = 'helicopter.png' # helicopter.png, spaceship.png, goku.png, flappy_bird.png

H = 600 
W = 1000 
s = pygame.display.set_mode([W, H])
pygame.display.set_caption('Helicopter Game')
font = pygame.font.Font('freesansbold.ttf', 20)
f = 60
t = pygame.time.Clock()
rw = 10
tr = W // rw
spacer = 10
player_x = 100
player_y = 300
g = 0.3
ms = 2
sc = 0
hs = 0
heli = pygame.transform.scale(pygame.image.load(f'./image/{player_image}'), (60, 60))


def dma(rects, background_color):
    for i in range(len(rects)):
        pygame.draw.rect(s, background_color, rects[i])
    pygame.draw.rect(s, 'dark gray', [0, 0, W, H], 12)
def gne():
    global player_y
    rects = []
    th = random.randint(0, 300)
    player_y = th + 150
    for i in range(tr):
        th = random.randint(th - spacer, th + spacer)
        if th < 0:
            th = 0
        elif th > 300:
            th = 300
        top_rect = pygame.draw.rect(s, 'green', [i * rw, 0, rw, th])
        bot_rect = pygame.draw.rect(s, 'green', [i * rw, th + 300, rw, H])
        rects.append(top_rect)
        rects.append(bot_rect)
    return rects
def draw_player():
    player = pygame.draw.circle(s, 'black', (player_x, player_y), 20)
    s.blit(heli, (player_x - 40, player_y - 30))
    return player
def move_player(y_pos, spe, fly):
    if fly:
        spe += g
    else:
        spe -= g
    y_pos -= spe
    return y_pos, spe
def check_collision(rects, circle, act):
    for i in range(len(rects)):
        if circle.colliderect(rects[i]):
            act = False
    return act
def move_rects(rects):
    global sc
    for i in range(len(rects)):
        rects[i] = (rects[i][0] - ms, rects[i][1], rw, rects[i][3])
        if rects[i][0] + rw < 0:
            rects.pop(1)
            rects.pop(0)
            th = random.randint(rects[-2][3] - spacer, rects[-2][3] + spacer)
            if th < 0:
                th = 0
            elif th > 300:
                th = 300
            rects.append((rects[-2][0] + rw, 0, rw, th))
            rects.append((rects[-2][0] + rw, th + 300, rw, H))
            sc += 1
    return rects


ru = True
nma = True
marec = []
fl = False
y_s = 0
active = True
while ru:
    s.fill('black')
    t.tick(f)
    if nma:
        marec = gne()
        nma = False
    dma(marec, background_color)
    player_circle = draw_player()
    if active:
        player_y, y_s = move_player(player_y, y_s, fl)
        marec = move_rects(marec)
    active = check_collision(marec, player_circle, active)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ru = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                fl = True
            if event.key == pygame.K_RETURN:
                if not active:
                    nma = True
                    active = True
                    y_s = 0
                    ms = 2
                    if sc > hs:
                        hs = sc
                    sc = 0
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                fl = False
    ms = 2 + sc//50
    spacer = 10 + sc//100
    s.blit(font.render(f'Score: {sc}', True, 'black'), (20, 15))
    s.blit(font.render(f'Highest Score: {hs}', True, 'black'), (20, 565)) 
    s.blit(font.render(f'Press Spacebar to hold the helicopter.', True, 'black'), (350, 500)) 
    if not active:
        s.blit(font.render('Press Enter to Restart', True, 'black'), (300, 15))
    pygame.display.flip()
pygame.quit()


