import pygame
import pygame.joystick as j
import time

#Initialize both joystick module and individual joystick
j.init()
js = j.Joystick(0)
js.init()

DISPLAY_WIDTH, DISPLAY_HEIGHT = 1000, 800

BLACK=(0,0,0)
WHITE=(235,235,235)
RED=(235,0,0)
GREEN=(0,235,0)
BLUE=(0,0,235)
AQUA = (  0, 255, 255)
FUCHSIA= (255,   0, 255)
GRAY = (128, 128, 128)
LIGHT_GREEN = (  0, 128,   0)
LIME = (  0, 255,   0)
MAROON = (128,  0,   0)
NAVY_BLUE = (  0,  0, 128)
OLIVE = (128, 128,   0)
PURPLE = (128,  0, 128)
SILVER = (192, 192, 192)
TEAL = (  0, 128, 128)
YELLOW = (255, 255,   0)

FPS=50
clock = pygame.time.Clock()

ufo_image = []
ufo_image.append(pygame.image.load("ufo1.jpg"))
ufo_image.append(pygame.image.load("ufo2.jpg"))
ufo_image.append(pygame.image.load("ufo3.jpg"))

pygame.init()
screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
background = pygame.Surface(screen.get_size())

class Ship(pygame.sprite.Sprite):
    def __init__(self, gamepad):
        pygame.sprite.Sprite.__init__(self)
        self.gamepad = gamepad

        self.imageMaster = pygame.image.load("spaceship2.jpg")
        self.imageMaster = self.imageMaster.convert()
        self.imageMaster.set_colorkey((0,0,0))
        self.image = self.imageMaster
        self.rect = self.image.get_rect()
        self.height = self.image.get_height()
        self.width = self.image.get_width()
        self.rect.center = (0,0)
        self.speed = 10
        self.movement = 0.0
        self.rect.y = DISPLAY_HEIGHT - self.height
        self.fire = 0
        self.cannon_loaded = 0
        self.rect.x = DISPLAY_WIDTH//2

    def update(self):
        self.get_input()

        self.rect.x += self.speed * self.movement

        if self.fire == 1 and self.cannon_loaded <= 0:
            bullet = Bullet(self)
            all_sprites_group.add(bullet)
            bullet_group.add(bullet)

            self.cannon_loaded = 25

        self.cannon_loaded += -1

    def get_input(self):
        self.movement = self.gamepad.get_axis(0)
        self.fire = self.gamepad.get_button(2)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, boss):
        pygame.sprite.Sprite.__init__(self)
        self.boss = boss
        self.speed = 10

        self.image = pygame.Surface((4,4))
        self.image.fill(RED)

        self.rect = self.image.get_rect()
        self.rect.y = self.boss.rect.y - 10
        self.rect.x = boss.rect.x + self.boss.width//2 - self.image.get_width()//2


    def update(self):
        self.rect.y += -1*self.speed

class UFO(pygame.sprite.Sprite):
    def __init__(self,x,y, img):
        pygame.sprite.Sprite.__init__(self)

        self.imageMaster = img
        self.imageMaster = self.imageMaster.convert()
        self.imageMaster.set_colorkey((0,0,0))
        self.image = self.imageMaster
        self.rect = self.image.get_rect()
        self.height = self.image.get_height()
        self.width = self.image.get_width()
        self.speed = 3

        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x


    def update(self):
        self.rect.x += self.speed

        if self.rect.x + self.width >= DISPLAY_WIDTH:
            self.speed *= -1
            self.rect.y += 75

        if self.rect.x <= 0:
            self.speed *= -1
            self.rect.y += 75


def print_text(text, x, y, size=15, color=BLACK, fontname='Arial'):
    text_font = pygame.font.SysFont(fontname, size)
    text_surface= text_font.render(text, True, color)
    screen.blit(text_surface, (x,y))

#Defining groups
all_sprites_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()


def main_game_loop():
    game_running = True

    player1 = Ship(js)
    score = 0
    hit_player = []
    columns = 9
    rows = 3
    col_y = 50
    col_x = 50
    i = 0

    for ufo in range(rows):
        for ufo2 in range(columns):
            enemy = UFO(col_x, col_y, ufo_image[i])
            all_sprites_group.add(enemy)
            enemy_group.add(enemy)
            col_x += 100

        i += 1
        col_y += 150
        col_x = 50

    player_group.add(player1)
    all_sprites_group.add(player1)


    #Main game loop
    while game_running==True:

        #Event handling loop
        for event in pygame.event.get():
            #quitting the game
            if event.type == pygame.QUIT:
                game_running = False

        #Game logic
        all_sprites_group.update()

        for bul in all_sprites_group:
            if bul.rect.y < 0:
                bul.kill()

        for bullet in bullet_group:
            hit_enemies = pygame.sprite.spritecollide(bullet, enemy_group, True)

            if len(hit_enemies)>0:
                bullet_group.remove(bullet)
                all_sprites_group.remove(bullet)
                for enemy in hit_enemies:
                    all_sprites_group.remove(enemy)
                    score += 1

        hit_player = pygame.sprite.spritecollide(player1, enemy_group, False)

        #Drawing
        screen.fill(BLACK)
        all_sprites_group.draw(screen)
        text = "Kills: " + str(score)
        print_text(text, 10, 10, size=15, color=WHITE, fontname='Arial')
        if len(hit_player) > 0:
            print_text("YOU ARE DEAD", 100, DISPLAY_HEIGHT//2-50, size=100, color=WHITE)

        #Updates the screen
        pygame.display.update()
        clock.tick(FPS)

# main
main_game_loop()
pygame.quit()
quit()
