import pygame
import sys

# Inicializa o pygame
pygame.init()

# Define as dimensões da janela
largura, altura = 300, 200
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Janela com Botão")

# Define as cores
branco = (255, 255, 255)
cinza = (200, 200, 200)
preto = (0, 0, 0)

# Carrega a sprite sheet do personagem
sprite_sheet = pygame.image.load("Attack.png").convert_alpha()
num_quadros = 8

quadro_largura = sprite_sheet.get_width() // num_quadros
quadro_altura = sprite_sheet.get_height()
quadros = [sprite_sheet.subsurface((i * quadro_largura, 52, quadro_largura, quadro_altura - 52)) for i in range(num_quadros)]

# Função para desenhar o botão
def desenha_botao(tela, cor, pos, tamanho, texto):
    fonte = pygame.font.Font(None, 36)
    pygame.draw.rect(tela, cor, (pos[0], pos[1], tamanho[0], tamanho[1]))
    texto_surface = fonte.render(texto, True, preto)
    texto_rect = texto_surface.get_rect(center=(pos[0] + tamanho[0] // 2, pos[1] + tamanho[1] // 2))
    tela.blit(texto_surface, texto_rect)

# Dimensões e posição do botão
largura_botao, altura_botao = 100, 50
x_botao = largura - largura_botao - 10
y_botao = altura - altura_botao - 10
botao = pygame.Rect(x_botao, y_botao, largura_botao, altura_botao)

# Animação
indice_quadro = 0
tempo_animacao = 200
ultimo_tempo = pygame.time.get_ticks()

# Posição do sprite
pos_x = 10
pos_y = 10
movimento = 0.5  # Velocidade ajustável

# Loop principal
rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if botao.collidepoint(evento.pos):
                rodando = False

    # Captura teclas pressionadas
    teclas = pygame.key.get_pressed()
    nova_x = pos_x
    nova_y = pos_y

    if teclas[pygame.K_RIGHT]:
        nova_x += movimento
    if teclas[pygame.K_LEFT]:
        nova_x -= movimento
    if teclas[pygame.K_DOWN]:
        nova_y += movimento
    if teclas[pygame.K_UP]:
        nova_y -= movimento

    # Mantém o sprite dentro da janela
    nova_x = max(0, min(nova_x, largura - quadro_largura))
    nova_y = max(0, min(nova_y, altura - (quadro_altura - 52)))

    # Verifica colisão com o botão
    sprite_rect = pygame.Rect(nova_x, nova_y, quadro_largura, quadro_altura - 52)
    if not sprite_rect.colliderect(botao):
        pos_x, pos_y = nova_x, nova_y
    else:
        # Tenta mover em um eixo de cada vez (contornar)
        temp_rect_x = pygame.Rect(nova_x, pos_y, quadro_largura, quadro_altura - 52)
        temp_rect_y = pygame.Rect(pos_x, nova_y, quadro_largura, quadro_altura - 52)
        if not temp_rect_x.colliderect(botao):
            pos_x = nova_x
        elif not temp_rect_y.colliderect(botao):
            pos_y = nova_y
        # Se colidir nos dois, não move

    # Atualiza animação
    agora = pygame.time.get_ticks()
    if agora - ultimo_tempo > tempo_animacao:
        indice_quadro = (indice_quadro + 1) % num_quadros
        ultimo_tempo = agora

    # Desenha fundo, sprite e botão
    tela.fill(branco)
    tela.blit(quadros[indice_quadro], (pos_x, pos_y))
    desenha_botao(tela, cinza, botao.topleft, botao.size, "Sair")

    # Atualiza tela
    pygame.display.flip()

# Encerra
pygame.quit()
sys.exit()
