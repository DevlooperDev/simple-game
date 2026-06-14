import pygame
import random
from button import Button

pygame.init()

# Main variables and stuff
w,h = 900,500
window = pygame.display.set_mode((w,h))
pygame.display.set_caption('Another long pygame project')
blue = (255,200,255)
run = True
fps = 60
startx = 0
starty = 250
lightblue = (118, 166, 245)
image = pygame.image.load('collide.png')
start_button_image = pygame.image.load('Start_button.png')
start_button_hover_image = pygame.image.load('Start_button_hover.png')
restart_button_image = pygame.image.load('Restart_button.png')
restart_button_hover_image = pygame.image.load('Restart_button_hover.png')
resume_button_image = pygame.image.load('Resume_button.png')
resume_button_hover_image = pygame.image.load('Resume_button_hover.png')
bullet_image = pygame.image.load('Bullet.png')
zombie = pygame.rect.Rect(50,50,50,50)
game_state = "main_menu"

last_update = pygame.time.get_ticks()


x = 60
y = 60

#font = pygame.font.Font(pygame.font.SysFont(None, 30), 24)
font = pygame.font.Font("Pixelify_Sans/PixelifySans-VariableFont_wght.ttf", 48)

def get_image(spritesheet, frame_num, width, height, scale):
    image = pygame.Surface((width, height)).convert_alpha()
    image.blit(spritesheet, (0, 0), (frame_num * width, 0, width, height))
    image = pygame.transform.scale(image, (width * scale, height * scale))
    return image

class Player():
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.vel = 5
        self.image = image
        self.spritesheet_idle = pygame.image.load('newguy.png').convert_alpha()
        self.spritesheet_run = pygame.image.load('newguy_run.png').convert_alpha()
        self.idle_frames = 4
        self.run_frames = 6
        self.current_animation = "idle"
        self.frame_delay = 100
        self.current_frame = 0
        self.frame_counter = 0
        self.state = "idle"
        self.facing = "right"
        self.rect = pygame.Rect(self.x, self.y, 16*3, 16*3)



    def move(self, keys):

        if keys[pygame.K_a]:
            self.current_animation = "run"
            self.facing = "left"
            self.rect.x -= self.vel
        if keys[pygame.K_d]:
            self.facing = "right"
            self.current_animation = "run"
            self.rect.x += self.vel
        if keys[pygame.K_w]:
            self.current_animation = "run"
            self.rect.y -= self.vel
        if keys[pygame.K_s]:
            self.current_animation = "run"
            self.rect.y += self.vel
        if not (keys[pygame.K_a] or keys[pygame.K_d] or keys[pygame.K_w] or keys[pygame.K_s]):
            self.current_animation = "idle"

    def collision(self, bullets):
        global game_state
        for bullet in bullets:
            if self.rect.colliderect(bullet.rect):
                lose_screen()
                return
                

    def animate(self, surface):
        global last_update
        current_time = pygame.time.get_ticks()

        if self.current_animation == "idle":
            spritesheet = self.spritesheet_idle
            total_frames = self.idle_frames
        elif self.current_animation == "run":
            spritesheet = self.spritesheet_run
            total_frames = self.run_frames

        if current_time - last_update > self.frame_delay:
            last_update = current_time
            self.current_frame = (self.current_frame + 1) % total_frames

        self.image = get_image(spritesheet, self.current_frame, 16, 16, 3)
        if self.facing == "left":
            self.image = pygame.transform.flip(self.image, True, False)

        self.image.set_colorkey((0,0,0))
        surface.blit(self.image, (self.rect.x, self.rect.y))

class Bullet(pygame.sprite.Sprite):
    def __init__(self, image):
        image = pygame.transform.scale(image, (10*2, 4*2))
        self.image = image
        self.rect = self.image.get_rect()
        self.startdirection = random.choice(['left', 'right'])
        if self.startdirection == 'left':
            self.rect.x = 0
        if self.startdirection == 'right':
            self.rect.x = 900
        self.rect.y = random.randint(5, 495)
        pygame.sprite.Sprite.__init__(self)
        self.vel = random.randint(5, 15)

    def spawn(self, surface):
        surface.blit(self.image, self.rect)

    def move(self):
        if self.startdirection == 'left':
            self.rect.x += self.vel
        if self.startdirection == 'right':
            self.rect.x -= self.vel
    
    def reset(self):
        self.startdirection = random.choice(['left', 'right'])
        if self.startdirection == 'left':
            self.rect.x = 0
        if self.startdirection == 'right':
            self.rect.x = 900
        self.rect.y = random.randint(5, 495)
        self.vel = random.randint(5, 15)


def main_menu():
    global game_state
    while True:

        game_state = "main_menu"
        mouse_pos = pygame.mouse.get_pos()
        window.fill(lightblue)

        drawText('Main Menu', font, w//2 - 100, 100)
        start_button = Button(start_button_image, start_button_hover_image, (w//2, h//2), '', font, (255,255,0), (255,0,0))
        start_button.changeColor(mouse_pos, window)
        start_button.update(window)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.checkForInput(mouse_pos):
                    player.rect.x = 60
                    player.rect.y = 60
                    for bullet in bullets:
                        bullet.reset()
                    game_state = "running"
                    return
        pygame.display.update()

def pause_menu():
    global game_state
    while True:

        game_state = "pause_menu"
        mouse_pos = pygame.mouse.get_pos()
        window.fill(lightblue)

        drawText('Paused', font, w//2 - 75, 100)
        resume_button = Button(resume_button_image, resume_button_hover_image, (w//2, h//2), '', font, (255,255,0), (255,0,0))
        resume_button.changeColor(mouse_pos, window)
        resume_button.update(window)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if resume_button.checkForInput(mouse_pos):
                    game_state = "running"
                    return
        pygame.display.update()

def lose_screen():
    global game_state
    while True:

        game_state = "stopped"
        mouse_pos = pygame.mouse.get_pos()
        window.fill(lightblue)

        drawText('You lose!', font, w//2 - 75, h//2 - 100)
        restart_button = Button(restart_button_image, restart_button_hover_image, (w//2, h//2), '', font, (255,255,0), (255,0,0))
        restart_button.changeColor(mouse_pos, window)
        restart_button.update(window)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.checkForInput(mouse_pos):
                    main_menu()
                    return
        pygame.display.update()

def drawText(text, font, x, y):
    text_surface = font.render(text, True, (128,128,192), lightblue)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    window.blit(text_surface, text_rect)

player = Player(60, 60, image)
bullets = pygame.sprite.Group()
clock = pygame.time.Clock()
# Game loop

while run:
    if game_state == "main_menu":
        main_menu()
    
    if game_state == "pause_menu":
        pause_menu()

    if game_state == "running":
        clock.tick(60)
        key = pygame.key.get_pressed()

        # Check for events

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_state = "pause_menu"

        # Spawn bullets and move them

        bullet = Bullet(bullet_image)
        total_bullets = len(bullets)
        if total_bullets < 5:
            bullets.add(bullet)
        for bullet in bullets:
            bullet.move()
            if bullet.rect.x < 0 or bullet.rect.x > 900:
                bullets.remove(bullet)

        # Finally move the player and draw everything
        player.move(key)
        window.fill(lightblue)
        #player.draw(window)
        player.animate(window)
        player.collision(bullets)
        for bullet in bullets:
            bullet.spawn(window)

        #pygame.draw.rect(window,(0,0,0),player)

    pygame.display.update()


pygame.quit()
