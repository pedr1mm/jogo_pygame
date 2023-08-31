import pygame
import random
import sys

# Inicialização do Pygame
pygame.init()




# Configurações da tela
screen_width = 400
screen_height = 300
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Mano Game")

# Cores
white = (255, 255, 255)
black = (0, 0, 0)

# Carregar imagens
mano = pygame.image.load("assets/mano.png")
lixo = pygame.image.load("assets/lixo.png")

# Posição inicial do "mano"
mano_x = 50
mano_y = screen_height - mano.get_height()
mano_y_speed = 0
on_ground = True

# Posição inicial do "lixo"
lixo_x = screen_width
lixo_y = screen_height - lixo.get_height()

# Velocidades
mano_speed = 5
lixo_speed = 5
jump_strength = -6
gravity = 0.50

# Contadores
score = 0
score_to_speed_up = 3

# Estados do jogo
START_SCREEN = 0
GAME_SCREEN = 1
game_state = START_SCREEN

# Numerador de pulos
pulos = 1
if pulos <= 0:
    on_ground = False

font = pygame.font.Font(None, 36)

def draw_text(text, x, y):
    text_surface = font.render(text, True, black)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

# Loop principal do jogo
clock = pygame.time.Clock()
game_over = False

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if game_state == START_SCREEN:
                game_state = GAME_SCREEN
            elif game_state == GAME_SCREEN and on_ground:
                mano_y_speed = jump_strength
                on_ground = False
                pulos = pulos - 1
            
    
    if game_state == GAME_SCREEN:
        # Movimento do "mano"
        mano_y_speed += gravity
        mano_y += mano_y_speed
        
        # Verificar se o "mano" está no chão
        if mano_y >= screen_height - mano.get_height():
            mano_y = screen_height - mano.get_height()
            mano_y_speed = 0
            on_ground = True
        
        # Movimento do "lixo"
        lixo_x -= lixo_speed
        if lixo_x < 0:
            lixo_x = screen_width
            lixo_y = screen_height - lixo.get_height()
            score += 1
            if score % score_to_speed_up == 3:
                lixo_speed += 1
        
        # Colisão
        mano_rect = pygame.Rect(mano_x, mano_y, mano.get_width(), mano.get_height())
        lixo_rect = pygame.Rect(lixo_x, lixo_y, lixo.get_width(), lixo.get_height())
        if mano_rect.colliderect(lixo_rect):
            game_state = START_SCREEN
            # Resetar variáveis de jogo após perder
            lixo_speed = 5
            score = 0
            mano_y = screen_height - mano.get_height()
            mano_y_speed = 0
            on_ground = True
    
    # Limpar a tela
    screen.fill(white)
    
    if game_state == START_SCREEN:
        draw_text("Aperte Espaço Para Começar", screen_width // 2, screen_height // 2)
    elif game_state == GAME_SCREEN:
        screen.blit(mano, (mano_x, mano_y))
        screen.blit(lixo, (lixo_x, lixo_y))
        draw_text("Pontuação: " + str(score), screen_width - 100, 20)
    
    pygame.display.update()
    clock.tick(30)


   

pygame.quit()
sys.exit()
