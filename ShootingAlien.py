import os
import random
from typing import List
import pygame as pg 

if not pg.image.get_extended(): 
    raise SystemExit("Sorry, extended image module required") 

# ตั้งค่าภาพพื้นหลัง 
BackGround = 'background-night.png' # background.gif, background-day.png, background-night.png

# ตั้งค่าตัวละคร 
character = 'player1.gif' # player1.gif, jetfighter.png, jetfighter2.png


ms = 2  
ao = 22 
bo = 60  
ar = 15  
sr = pg.Rect(0, 0, 640, 480)
S = 0
md = os.path.split(os.path.abspath(__file__))[0]

def load_sound(file): 
    if not pg.mixer: 
        return None 
    file = os.path.join(md, "image", file) 
    try: 
        sound = pg.mixer.Sound(file) 
        return sound 
    except pg.error: 
        print(f"Warning, unable to load, {file}") 
    return None 
def load_image(file):
    file = os.path.join(md, "image", file) 
    try: 
        surface = pg.image.load(file) 
    except pg.error:
        raise SystemExit(f'Could not load image "{file}" {pg.get_error()}') 
    return surface.convert() 


class Player(pg.sprite.Sprite): 
    s = 10
    b = 24
    go = -11
    images: List[pg.Surface] = []
    def __init__(self, *groups):
        pg.sprite.Sprite.__init__(self, *groups)
        self.image = self.images[0]
        self.rect = self.image.get_rect(midbottom=sr.midbottom)
        self.reloading = 0
        self.origtop = self.rect.top
        self.facing = -1
    def move(self, dire):
        if dire:
            self.facing = dire
        self.rect.move_ip(dire * self.s, 0)
        self.rect = self.rect.clamp(sr)
        if dire < 0:
            self.image = self.images[0]
        elif dire > 0:
            self.image = self.images[1]
        self.rect.top = self.origtop - (self.rect.left // self.b % 2)
    def gunpos(self):
        pos = self.facing * self.go + self.rect.centerx
        return pos, self.rect.top

class Alien(pg.sprite.Sprite):
    s = 13
    animcycle = 12
    images: List[pg.Surface] = []
    def __init__(self, *groups):
        pg.sprite.Sprite.__init__(self, *groups)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.facing = random.choice((-1, 1)) * Alien.s
        self.frame = 0
        if self.facing < 0:
            self.rect.right = sr.right
    def update(self, *args, **kwargs):
        self.rect.move_ip(self.facing, 0)
        if not sr.contains(self.rect):
            self.facing = -self.facing
            self.rect.top = self.rect.bottom + 1
            self.rect = self.rect.clamp(sr)
        self.frame = self.frame + 1
        self.image = self.images[self.frame // self.animcycle % 3]

class Explosion(pg.sprite.Sprite):
    defaultlife = 12
    animcycle = 3
    images: List[pg.Surface] = []
    def __init__(self, actor, *groups):
        pg.sprite.Sprite.__init__(self, *groups)
        self.image = self.images[0]
        self.rect = self.image.get_rect(center=actor.rect.center)
        self.life = self.defaultlife
    def update(self, *args, **kwargs):
        self.life = self.life - 1
        self.image = self.images[self.life // self.animcycle % 2]
        if self.life <= 0:
            self.kill()


class Shot(pg.sprite.Sprite):
    s = -11
    images: List[pg.Surface] = []
    def __init__(self, pos, *groups):
        pg.sprite.Sprite.__init__(self, *groups)
        self.image = self.images[0]
        self.rect = self.image.get_rect(midbottom=pos)

    def update(self, *args, **kwargs):
        self.rect.move_ip(0, self.s)
        if self.rect.top <= 0:
            self.kill()
class Bomb(pg.sprite.Sprite):
    s = 9
    images: List[pg.Surface] = []
    def __init__(self, alien, egro, *groups):
        pg.sprite.Sprite.__init__(self, *groups)
        self.image = self.images[0]
        self.rect = self.image.get_rect(midbottom=alien.rect.move(0, 5).midbottom)
        self.egro = egro
    def update(self, *args, **kwargs):
        self.rect.move_ip(0, self.s)
        if self.rect.bottom >= 470:
            Explosion(self, self.egro)
            self.kill()

class Score(pg.sprite.Sprite):
    def __init__(self, *groups):
        pg.sprite.Sprite.__init__(self, *groups)
        self.font = pg.font.Font(None, 20)
        self.font.set_italic(1)
        self.color = "white"
        self.lastscore = -1
        self.update()
        self.rect = self.image.get_rect().move(10, 450)
    def update(self, *args, **kwargs):
        if S != self.lastscore:
            self.lastscore = S
            msg = f"Score: {S}"
            self.image = self.font.render(msg, 0, self.color)

def get_input(screen, alienreload, S, clock):  
    for event in pg.event.get(): 
        if event.type == pg.QUIT: 
            return 
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE: 
            return 
        if event.type == pg.KEYDOWN: 
            if event.key == pg.K_f: 
                if not fullscreen: 
                    print("Changing to FULLSCREEN") 
                    screen_backup = screen.copy() 
                    screen = pg.display.set_mode(sr.size, winstyle | pg.FULLSCREEN, bestdepth )
                    screen.blit(screen_backup, (0, 0)) 
                else: 
                    print("Changing to windowed mode")
                    screen_backup = screen.copy()
                    screen = pg.display.set_mode(sr.size, winstyle, bestdepth)
                    screen.blit(screen_backup, (0, 0))
                pg.display.flip()
                fullscreen = not fullscreen

    keystate = pg.key.get_pressed()
    all.clear(screen, background)
    all.update()
    dire = keystate[pg.K_RIGHT] - keystate[pg.K_LEFT]
    player.move(dire)
    firing = keystate[pg.K_SPACE]
    if not player.reloading and firing and len(sht) < ms:
        Shot(player.gunpos(), sht, all)
        if pg.mixer and shoot_sound is not None:
            shoot_sound.play()
    player.reloading = firing
    if alienreload:
        alienreload = alienreload - 1
    elif not int(random.random() * ao):
        Alien(alie, all, lasalie)
        alienreload = ar
    if lasalie and not int(random.random() * bo):
        Bomb(lasalie.sprite, all, bom, all)
    for alien in pg.sprite.spritecollide(player, alie, 1):
        if pg.mixer and boom_sound is not None:
            boom_sound.play()
        Explosion(alien, all)
        Explosion(player, all)
        S = S + 1
        player.kill()
        kil = True 
    for alien in pg.sprite.groupcollide(alie, sht, 1, 1).keys():
        if pg.mixer and boom_sound is not None:
            boom_sound.play()
        Explosion(alien, all)
        S = S + 1

    for bomb in pg.sprite.spritecollide(player, bom, 1):
        if pg.mixer and boom_sound is not None:
            boom_sound.play()
        Explosion(player, all)
        Explosion(bomb, all)
        player.kill() 
        kil = True 
    dirty = all.draw(screen)
    pg.display.update(dirty)
    clock.tick(40)
    return screen, alienreload, S, clock  

if pg.get_sdl_version()[0] == 2: 
    pg.mixer.pre_init(44100, 32, 2, 1024) 
pg.init() 
if pg.mixer and not pg.mixer.get_init(): 
    print("Warning, no sound") 
    pg.mixer = None 
fullscreen = False 
winstyle = 0 
bestdepth = pg.display.mode_ok(sr.size, winstyle, 32) 
screen = pg.display.set_mode(sr.size, winstyle, bestdepth) 
img = load_image(f"{character}") 
Player.images = [img, pg.transform.flip(img, 1, 0)]
img = load_image("explosion1.gif")
Explosion.images = [img, pg.transform.flip(img, 1, 1)]
Alien.images = [load_image(im) for im in ("alien1.gif", "alien2.gif", "alien3.gif")]
Bomb.images = [load_image("bomb.gif")]
Shot.images = [load_image("shot.gif")]
icon = pg.transform.scale(Alien.images[0], (32, 32)) 
pg.display.set_icon(icon) 
pg.display.set_caption("Shooting Aliens Games") 
pg.mouse.set_visible(0) 
bgdtile = load_image(f"{BackGround}") 
background = pg.Surface(sr.size) 
for x in range(0, sr.width, bgdtile.get_width()): 
    background.blit(bgdtile, (x, 0)) 
screen.blit(background, (0, 0)) 
pg.display.flip() 
boom_sound = load_sound("boom.wav") 
shoot_sound = load_sound("car_door.wav") 
if pg.mixer: 
    music = os.path.join(md, "image", "house_lo.wav") 
    pg.mixer.music.load(music) 
    pg.mixer.music.play(-1) 
alie = pg.sprite.Group() 
sht = pg.sprite.Group() 
bom = pg.sprite.Group() 
all = pg.sprite.RenderUpdates() 
lasalie = pg.sprite.GroupSingle() 
alienreload = ar 
clock = pg.time.Clock() 
player = Player(all) 
Alien(alie, all, lasalie) 
if pg.font:
    all.add(Score(all))
while player.alive():
    screen, alienreload, S, clock = get_input(screen=screen, alienreload=alienreload, S=S, clock=clock) 
print(f"คุณแพ้.. คะแนนของคุณ = {S}") 

if pg.mixer:
    pg.mixer.music.fadeout(1000)
pg.time.wait(1000)


