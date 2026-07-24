import pygame
import random
import sys

# Pygame Başlatma
pygame.init()

# Ekran Boyutları (Dikey Mobil Oran)
WIDTH, HEIGHT = 400, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Retro Arcade - Mobil Paket")

clock = pygame.time.Clock()

# Renkler
BG_COLOR = (15, 15, 25)
PANEL_COLOR = (30, 30, 45)
BTN_COLOR = (50, 50, 80)
BTN_HOVER = (70, 70, 120)
TEXT_COLOR = (240, 240, 240)
ACCENT_COLOR = (0, 255, 128)
SNAKE_COLOR = (0, 200, 100)
FOOD_COLOR = (255, 60, 60)
PADDLE_COLOR = (100, 150, 255)
BALL_COLOR = (255, 255, 255)

# Fontlar
font_title = pygame.font.SysFont("Arial", 28, bold=True)
font_btn = pygame.font.SysFont("Arial", 20, bold=True)
font_small = pygame.font.SysFont("Arial", 16)

# Oyun Durumları (States)
STATE_MENU = "menu"
STATE_SNAKE = "snake"
STATE_PONG = "pong"
current_state = STATE_MENU

# --- YILAN OYUNU DEĞİŞKENLERİ ---
GRID_SIZE = 20
snake = []
snake_dir = [0, 0]
food = [0, 0]
snake_score = 0
snake_timer = 0

def init_snake():
    global snake, snake_dir, food, snake_score, snake_timer
    snake = [[100, 200], [80, 200], [60, 200]]
    snake_dir = [GRID_SIZE, 0]
    spawn_food()
    snake_score = 0
    snake_timer = 0

def spawn_food():
    global food
    food = [
        random.randrange(0, WIDTH // GRID_SIZE) * GRID_SIZE,
        random.randrange(100 // GRID_SIZE, HEIGHT // GRID_SIZE) * GRID_SIZE
    ]

# --- PONG OYUNU DEĞİŞKENLERİ ---
paddle_x = 150
paddle_w = 100
paddle_h = 15
ball_x = 200
ball_y = 350
ball_dx = 4
ball_dy = -4
pong_score = 0

def init_pong():
    global paddle_x, ball_x, ball_y, ball_dx, ball_dy, pong_score
    paddle_x = WIDTH // 2 - paddle_w // 2
    ball_x = WIDTH // 2
    ball_y = HEIGHT // 2
    ball_dx = random.choice([-4, 4])
    ball_dy = -4
    pong_score = 0

# Buton Çizim Yardımcısı (Konum ve boyut parametreleri tamamen ayrıldı)
def draw_button(text, x, y, w, h, is_active=True):
    mouse_pos = pygame.mouse.get_pos()
    rect = pygame.Rect(x, y, w, h)
    
    # Aktif olmayan (yakında eklenecek) butonlar için gri ton
    if not is_active:
        pygame.draw.rect(screen, (40, 40, 40), rect, border_radius=10)
        pygame.draw.rect(screen, (80, 80, 80), rect, 2, border_radius=10)
        txt_surf = font_btn.render(text, True, (120, 120, 120))
        txt_rect = txt_surf.get_rect(center=rect.center)
        screen.blit(txt_surf, txt_rect)
        return False
        
    if rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, BTN_HOVER, rect, border_radius=10)
    else:
        pygame.draw.rect(screen, BTN_COLOR, rect, border_radius=10)
        
    pygame.draw.rect(screen, ACCENT_COLOR, rect, 2, border_radius=10)
    
    txt_surf = font_btn.render(text, True, TEXT_COLOR)
    txt_rect = txt_surf.get_rect(center=rect.center)
    screen.blit(txt_surf, txt_rect)
    
    return rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]

# Ana Oyun Döngüsü
running = True
click_cooldown = 0

while running:
    screen.fill(BG_COLOR)
    
    if click_cooldown > 0:
        click_cooldown -= 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- ANA MENÜ ---
    if current_state == STATE_MENU:
        title_surf = font_title.render("RETRO ARCADE PAKETİ", True, ACCENT_COLOR)
        title_rect = title_surf.get_rect(center=(WIDTH // 2, 100))
        screen.blit(title_surf, title_rect)
        
        sub_surf = font_small.render("Dokunmatik / Fare Uyumlu", True, (150, 150, 180))
        sub_rect = sub_surf.get_rect(center=(WIDTH // 2, 140))
        screen.blit(sub_surf, sub_rect)

        if draw_button("YILAN", 50, 220, 300, 50) and click_cooldown == 0:
            init_snake()
            current_state = STATE_SNAKE
            click_cooldown = 20
            
        if draw_button("PONG", 50, 290, 300, 50) and click_cooldown == 0:
            init_pong()
            current_state = STATE_PONG
            click_cooldown = 20
            
        # Tetris için görsel yer tutucu (şu an inaktif)
        draw_button("TETRİS (YAKINDA)", 50, 360, 300, 50, is_active=False)
        
        if draw_button("ÇIKIŞ", 50, 550, 300, 50) and click_cooldown == 0:
            running = False

    # --- YILAN OYUNU ---
    elif current_state == STATE_SNAKE:
        # Üst Bilgi Paneli
        pygame.draw.rect(screen, PANEL_COLOR, (0, 0, WIDTH, 60))
        score_surf = font_btn.render(f"Skor: {snake_score}", True, TEXT_COLOR)
        screen.blit(score_surf, (20, 18))
        
        # Menüye Dönüş Butonu
        if draw_button("Menü", 300, 10, 80, 40) and click_cooldown == 0:
            current_state = STATE_MENU
            click_cooldown = 20

        # Yılan Hızı ve Mantığı
        snake_timer += 1
        if snake_timer > 6: # Hız ayarı
            snake_timer = 0
            new_head = [snake[0][0] + snake_dir[0], snake[0][1] + snake_dir[1]]
            
            # Duvar Çarpışması veya Kendine Çarpma
            if (new_head[0] < 0 or new_head[0] >= WIDTH or 
                new_head[1] < 60 or new_head[1] >= HEIGHT or 
                new_head in snake):
                init_snake()
            else:
                snake.insert(0, new_head)
                if new_head == food:
                    snake_score += 10
                    spawn_food()
                else:
                    snake.pop()

        # Klavye Yönlendirme (Test İçin)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and snake_dir[1] == 0: snake_dir = [0, -GRID_SIZE]
        if keys[pygame.K_DOWN] and snake_dir[1] == 0: snake_dir = [0, GRID_SIZE]
        if keys[pygame.K_LEFT] and snake_dir[0] == 0: snake_dir = [-GRID_SIZE, 0]
        if keys[pygame.K_RIGHT] and snake_dir[0] == 0: snake_dir = [GRID_SIZE, 0]

        # Dokunmatik / Fare Yönlendirme
        if pygame.mouse.get_pressed()[0] and click_cooldown == 0:
            mx, my = pygame.mouse.get_pos()
            if my > 70: # Panelin altına tıklandıysa
                head = snake[0]
                # Parmağın yılanın kafasına göre nerede olduğuna bakarak yön bul
                if abs(mx - head[0]) > abs(my - head[1]):
                    if mx > head[0] and snake_dir[0] == 0: snake_dir = [GRID_SIZE, 0]
                    elif mx < head[0] and snake_dir[0] == 0: snake_dir = [-GRID_SIZE, 0]
                else:
                    if my > head[1] and snake_dir[1] == 0: snake_dir = [0, GRID_SIZE]
                    elif my < head[1] and snake_dir[1] == 0: snake_dir = [0, -GRID_SIZE]

        # Çizimler
        pygame.draw.rect(screen, FOOD_COLOR, (food[0], food[1], GRID_SIZE - 2, GRID_SIZE - 2), border_radius=4)
        for block in snake:
            pygame.draw.rect(screen, SNAKE_COLOR, (block[0], block[1], GRID_SIZE - 2, GRID_SIZE - 2), border_radius=4)

    # --- PONG OYUNU ---
    elif current_state == STATE_PONG:
        pygame.draw.rect(screen, PANEL_COLOR, (0, 0, WIDTH, 60))
        score_surf = font_btn.render(f"Skor: {pong_score}", True, TEXT_COLOR)
        screen.blit(score_surf, (20, 18))
        
        # Menüye Dönüş Butonu
        if draw_button("Menü", 300, 10, 80, 40) and click_cooldown == 0:
            current_state = STATE_MENU
            click_cooldown = 20

        # Pong Hareket Mantığı
        ball_x += ball_dx
        ball_y += ball_dy

        # Duvar Çarpışmaları
        if ball_x <= 10 or ball_x >= WIDTH - 10:
            ball_dx *= -1
        if ball_y <= 70: # Üst panele çarpma
            ball_dy *= -1

        # Paddle Çarpışması
        paddle_y_pos = HEIGHT - 50
        if (paddle_y_pos <= ball_y + 8 <= paddle_y_pos + paddle_h) and (paddle_x <= ball_x <= paddle_x + paddle_w):
            ball_dy *= -1
            pong_score += 1
            # Topun sekme açısına ufak bir rastgelelik kat
            ball_dx += random.uniform(-0.5, 0.5) 

        # Alt Çizgi (Game Over)
        if ball_y > HEIGHT:
            init_pong()

        # Fare veya Dokunmatik ile Paddle Kontrolü
        if pygame.mouse.get_pressed()[0] and click_cooldown == 0:
            mx, my = pygame.mouse.get_pos()
            if my > 60: # Panelin altına tıklandığında çalışsın
                paddle_x = mx - paddle_w // 2

        # Sınırlar
        if paddle_x < 0: paddle_x = 0
        if paddle_x > WIDTH - paddle_w: paddle_x = WIDTH - paddle_w

        # Çizimler
        pygame.draw.rect(screen, PADDLE_COLOR, (paddle_x, paddle_y_pos, paddle_w, paddle_h), border_radius=6)
        pygame.draw.circle(screen, BALL_COLOR, (int(ball_x), int(ball_y)), 8)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()