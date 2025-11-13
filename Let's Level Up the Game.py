import pygame
import random
import os

# --- Settings ---
SCREEN_WIDTH, SCREEN_HEIGHT = 500, 400
MOVEMENT_SPEED = 5
FONT_SIZE = 72
BG_IMAGE_PATH = "Mario.jpg"   # put your image in the same folder or change this path

# --- Init ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sprite Collision")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Times New Roman", FONT_SIZE)

# --- Background (optional image) ---
def load_background():
    try:
        img = pygame.image.load(BG_IMAGE_PATH)
        return pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT))
    except Exception:
        # Fallback if image not found
        surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        surf.fill(pygame.Color("white"))
        return surf

background_image = load_background()

# --- Sprite class ---
class Sprite(pygame.sprite.Sprite):
    def __init__(self, color, width, height, x=0, y=0):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(pygame.Color('dodgerblue'))  # base fill
        pygame.draw.rect(self.image, color, pygame.Rect(0, 0, width, height))
        self.rect = self.image.get_rect(topleft=(x, y))

    def move(self, dx, dy):
        # Update position
        self.rect.x += dx
        self.rect.y += dy
        # Clamp to screen bounds
        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, SCREEN_HEIGHT - self.rect.height))

# --- Create sprites ---
all_sprites = pygame.sprite.Group()

player = Sprite(pygame.Color('black'), 30, 30, x=20, y=20)
all_sprites.add(player)

# Place the target at a random position
target = Sprite(pygame.Color('red'), 30, 30,
                x=random.randint(0, SCREEN_WIDTH - 30),
                y=random.randint(0, SCREEN_HEIGHT - 30))
all_sprites.add(target)

# --- Game loop ---
running = True
won = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (
            event.type == pygame.KEYDOWN and event.key == pygame.K_x
        ):
            running = False

    if not won:
        keys = pygame.key.get_pressed()
        dx = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * MOVEMENT_SPEED
        dy = (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * MOVEMENT_SPEED
        player.move(dx, dy)

        if player.rect.colliderect(target.rect):
            all_sprites.remove(target)
            won = True

    # --- Draw ---
    screen.blit(background_image, (0, 0))
    all_sprites.draw(screen)

    if won:
        win_text = font.render("You Win !!", True, pygame.Color('black'))
        screen.blit(
            win_text,
            ((SCREEN_WIDTH - win_text.get_width()) // 2,
             (SCREEN_HEIGHT - win_text.get_height()) // 2)
        )

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
