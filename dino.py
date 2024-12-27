import pygame
import random

# Inisialisasi Pygame
pygame.init()

# Konstanta
WIDTH, HEIGHT = 800, 400
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DINO_WIDTH, DINO_HEIGHT = 60, 60  # Ukuran Dinosaurus
OBSTACLE_WIDTH, OBSTACLE_HEIGHT = 35, 35  # Ukuran Rintangan

# Setup layar tanpa opsi resizable
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dino Game")

# Memuat gambar
background_image = pygame.transform.scale(pygame.image.load('background.png'), (WIDTH, HEIGHT))
dino_image = pygame.image.load('dino_char.png')
obstacle_image = pygame.image.load('rintangan.png')

# Kelas untuk Dinosaurus
class Dino:
    def __init__(self):
        self._x = 50
        self._y = HEIGHT - DINO_HEIGHT - 20
        self._jump = False
        self._jump_count = 10

    def draw(self):
        dino_scaled = pygame.transform.scale(dino_image, (DINO_WIDTH, DINO_HEIGHT))
        screen.blit(dino_scaled, (self._x, self._y))

    def update(self):
        if self._jump:
            if self._jump_count >= -10:
                neg = 1 if self._jump_count >= 0 else -1
                self._y -= (self._jump_count ** 2) * 0.5 * neg
                self._jump_count -= 1
            else:
                self._jump = False
                self._jump_count = 10

        if self._y > HEIGHT - DINO_HEIGHT:
            self._y = HEIGHT - DINO_HEIGHT

    def collides_with(self, obstacle):
        return (self._x < obstacle.x + OBSTACLE_WIDTH and
                self._x + DINO_WIDTH > obstacle.x and
                self._y < obstacle.y + OBSTACLE_HEIGHT and
                self._y + DINO_HEIGHT > obstacle.y)

# Kelas dasar untuk Rintangan
class Obstacle:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        raise NotImplementedError("Metode ini harus diimplementasikan oleh subclass")

    def update(self, speed):
        self.x -= speed

    def is_off_screen(self):
        return self.x < 0

# Kelas untuk Rintangan Spesifik
class SingleObstacle(Obstacle):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.y = HEIGHT - OBSTACLE_HEIGHT - 20  # Menyesuaikan posisi Y agar sejajar dengan Dinosaurus

    def draw(self):
        obstacle_scaled = pygame.transform.scale(obstacle_image, (OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
        screen.blit(obstacle_scaled, (self.x, self.y))

class StackedObstacle(Obstacle):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.y = HEIGHT - OBSTACLE_HEIGHT - 20  # Menyesuaikan posisi Y agar sejajar dengan Dinosaurus

    def draw(self):
        obstacle_scaled = pygame.transform.scale(obstacle_image, (OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
        screen.blit(obstacle_scaled, (self.x, self.y))
        screen.blit(obstacle_scaled, (self.x, self.y - OBSTACLE_HEIGHT))

class DoubleObstacle(Obstacle):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.y = HEIGHT - OBSTACLE_HEIGHT - 20  # Menyesuaikan posisi Y agar sejajar dengan Dinosaurus

    def draw(self):
        obstacle_scaled = pygame.transform.scale(obstacle_image, (OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
        screen.blit(obstacle_scaled, (self.x, self.y))
        screen.blit(obstacle_scaled, (self.x + OBSTACLE_WIDTH, self.y))

class VerticalObstacle(Obstacle):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.y = HEIGHT - OBSTACLE_HEIGHT - 20  # Menyesuaikan posisi Y agar sejajar dengan Dinosaurus

    def draw(self):
        obstacle_scaled = pygame.transform.scale(obstacle_image, (OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
        screen.blit(obstacle_scaled, (self.x, self.y))
        screen.blit(obstacle_scaled, (self.x, self.y - OBSTACLE_HEIGHT))

# Fungsi untuk menampilkan layar akhir
def display_end_screen(score):
    font = pygame.font.Font(None, 36)
    screen.fill(WHITE)
    
    score_text = font.render(f'Skor Akhir: {score}', True, BLACK)
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - 50))
    
    restart_text = font.render('Tekan R untuk Main Lagi', True, BLACK)
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2))
    
    exit_text = font.render('Tekan Q untuk Keluar', True, BLACK)
    screen.blit(exit_text, (WIDTH // 2 - exit_text.get_width() // 2, HEIGHT // 2 + 50))
    
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False
                    return True
                if event.key == pygame.K_q:
                    pygame.quit()
                    exit()

# Fungsi utama
def main():
    # Langsung mulai permainan tanpa layar awal
    while True:
        clock = pygame.time.Clock()
        dino = Dino()
        obstacles = []
        score = 0
        run = True
        obstacle_timer = 0
        speed = 10

        while run:
            clock.tick(30)
            screen.blit(background_image, (0, 0))

            font = pygame.font.Font(None, 36)
            score_text = font.render(f'Skor: {score}', True, BLACK)
            screen.blit(score_text, (10, 10))

            obstacle_timer += 1
            if obstacle_timer > 60:
                x_position = WIDTH
                obstacle_type = random.choice([SingleObstacle, StackedObstacle, DoubleObstacle, VerticalObstacle])
                obstacles.append(obstacle_type(x_position, HEIGHT - OBSTACLE_HEIGHT - 10))
                obstacle_timer = 0

            dino.draw()
            dino.update()

            for obstacle in obstacles:
                obstacle.draw()
                obstacle.update(speed)
                if obstacle.is_off_screen():
                    obstacles.remove(obstacle)
                    score += 1
                if dino.collides_with(obstacle):
                    run = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and not dino._jump:
                        dino._jump = True

            pygame.display.update()

        display_end_screen(score)

if __name__ == "__main__":
    main()
