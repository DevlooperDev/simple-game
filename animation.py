import pygame

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Animation Example")

idle_spritesheet = pygame.image.load('C:/Users/devan/Documents/Python/Simple Game/newguy.png').convert_alpha()
run_spritesheet = pygame.image.load('C:/Users/devan/Documents/Python/Simple Game/newguy_run.png').convert_alpha()

BG = (50, 50, 50)

def get_image(spritesheet, frame_num, width, height, scale):
    image = pygame.Surface((width, height)).convert_alpha()
    image.blit(spritesheet, (0, 0), (frame_num * width, 0, width, height))
    image = pygame.transform.scale(image, (width * scale, height * scale))
    return image

# Animation variables
idle_frames = 4
run_frames = 6
current_animation = "idle"
current_frame = 0
frame_counter = 0
frame_delay = 100
last_update_time = pygame.time.get_ticks()

running = True

while running:
    screen.fill(BG)

    # Get current spritesheet
    if current_animation == "idle":
        spritesheet = idle_spritesheet
        total_frames = idle_frames
    else:
        spritesheet = run_spritesheet
        total_frames = run_frames

    # Update animation
    frame_counter += 1
    if frame_counter >= frame_delay:
        frame_counter = 0
        current_frame = (current_frame + 1) % total_frames
    print(frame_counter)
    frame = get_image(spritesheet, current_frame, 16, 16, 3)
    screen.blit(frame, (100, 100))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                current_animation = "run"
                current_frame = 0
            elif event.key == pygame.K_i:
                current_animation = "idle"
                current_frame = 0

    pygame.display.update()

pygame.quit()
