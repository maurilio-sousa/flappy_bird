import pygame
import os
import random

# tamanho de tela do jogo
altura = 800
largura = 500

# importando ás imagens do jogo
imagem_do_cano = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'pipe.png')))
imagem_do_fundo = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'base.png')))
imagem_do_solo = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bg.png'))) 
imagens_do_passaro = [
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird1.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird2.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird3.png')))
]

# criando e inicializando o contador de pontuação
pygame.font.init()
fonte_da_pontuacao = pygame.font.SysFont('arial', 40)

# criando os objetos
class passaro:
    imgs = imagens_do_passaro
    rotacao_max = 25
    velocidade_rotacao = 20
    tempo_de_animacao = 5
    # atribuição de localização eixo X e Y
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.angulo = 0
        self.velocidade = 0
        self.altura = self.y
        self.tempo = 0
        self.contagem_da_imagem = 0
        self.imagem = self.imgs[0]

    # função de pular
    def pular(self):
        self.velocidade = -10.5
        self.tempo = 0
        self.altura = self.y

    # função mover
    def mover(self):
    # calcular o deslocamento
        self.tempo += 1
        deslocamento = 1.5 * (self.tempo ** 2) *self.velocidade * self.tempo

    # restringir o deslocamento
        if (deslocamento > 16):
            deslocamento = 16
        elif (deslocamento < 0):
            deslocamento -= 2

    # realizando o deslocamento do passáro
        self.y += deslocamento

    # angulo do pássaro 
        if  (deslocamento < 0) or ((self.y < self.altura + 50)):
            if (self.angulo < self.rotacao_max):
                self.angulo = self.rotacao_max
        else:
            if (self. angulo - 90):
                self.angulo -= self.velocidade_rotacao

    def desenhar (self, tela):
        # definir qual imagem irá usar em tal momento
        self.contagem_da_imagem += 1
        if (self.contagem_da_imagem < self.tempo_de_animacao):
            self.imagem = self.imgs[0]
        elif (self.contagem_da_imagem < self.tempo_de_animacao * 2):
            self.imagem = self.imgs[1]
        elif (self.contagem_da_imagem < self.tempo_de_animacao * 3):
            self.imagem = self.imgs[2]
        elif (self.contagem_da_imagem < self.tempo_de_animacao * 4):
            self.imagem = self.imgs[1]
        elif (self.contagem_da_imagem < self.tempo_de_animacao * 4 + 1):
            self.imagem = self.imgs[0]
            self.contagem_da_imagem = 0
         

        # quando o passáro tiver caindo 
        if (self.angulo <= - 80):
            self.imagem = self.imgs[1]
            self.contagem_da_imagem = self.tempo_de_animacao * 2
            
        # desenhar a imagem
        imagem_rotacionada = pygame.transform.rotate(self.imagem, self.angulo)
        posicao_centro_da_imagem = self.imagen.get_rect(topleft=(self.x, self.y)).center
        retangulo = imagem_rotacionada.get_rect(center = posicao_centro_da_imagem)
        tela.blit(imagem_rotacionada, retangulo.topleft)

    # mascára de pixel para colisão
    def get_mask(self):
        return pygame.mask.from_surface(self.imagem)

class cano:
    distancia = 200
    velocidade = 5

    def __init__(self,x):
        self.x = self.x
        self.altura = 0
        self.posicao_topo = 0
        self.pos_chao = 0
        self.cano_topo =pygame.transform.flip(imagem_do_cano, False, True)
        self.cano_chao = imagem_do_cano
        self.passou = False
        self.definir_altura()

    def definir_altura(self):
        self.altura = random.randrange(50, 450)
        self.posicao_topo = self.altura - self.cano_topo.get_height()
        self.pos_chao = self.altura + self.distancia

    def mover(self):
        self.x -= self.velocidade

    def desenhar(self, tela):
        tela.blit(self.cano_topo, (self.x, self.posicao_topo))
        tela.blit(self.cano_chao, (self.x, self.pos_chao))

    def colidir(self, passaro):
        passaro_mask = passaro.get_mask()
        topo_mask = pygame.mask.from_surface(self.cano_topo)
        chao_mask = pygame.mask.from_surface(self.cano_chao)

        dist_cano_topo = self.x - passaro.x, self.posicao_topo - round(passaro.y)
        dist_cano_chao = self.x - passaro.x, self.posicao_chao - round(passaro.y)

        topo_ponto = passaro_mask.overlap(chao_mask, dist_cano_topo)
        chao_ponto = passaro_mask.overlap(chao_mask, dist_cano_chao)

        if (chao_ponto or topo_ponto):
            return True
        else:
            return False

class chao:
    velocidae = 5
    largura = imagem_do_solo.get_width()
    imagem = imagem_do_solo

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.largura

    def mover(self):
        self.x1 -= self.velocidae
        self.x2 -= self.velocidae

        if (self.x1 + self.largura < 0):
            self.x1 = self.x1 + self.largura
        if (self.x2 + self.largura < 0):
            self.x2 = self.x2 + self.largura

    def desenhar(self, tela):
        tela.blit(self.imagem, (self.x1, self.y))
        tela.blit(self.cano_chao, (self.x2, self.y))

def desenhar_tela(tela, passaros, canos, chao, placar):
    tela.blit = (imagem_do_fundo, (0,0))
    for passaro in passaros:
        passaro.desenhar(tela)
    for cano in canos:
        cano.desenhar(tela)
        
    texto = fonte_da_pontuacao.render(f'pontuação: {placar}', 1, (255, 255, 255))
    tela.blit(texto, (largura - 10 - texto.get_width(), 10))
    chao.desenhar(tela)
    pygame.display.update()

def main():
    passaros = [passaro(230, 350)]
    chao = [chao(730)]
    canos = [cano(700)]
    tela = pygame.display.set_mode(largura, altura)
    placar = 0
    relogio = pygame.time.Clock()
        
    rodando = True
    while (rodando):
            relogio.tick(30)

            for evento in pygame.event.get():
                if (evento.type == pygame.QUIT):
                    rodando = False
                    pygame.quit()
                    quit()
                if (evento.type == pygame.KEYDOWN):
                    if (evento.key == pygame.K_SPACE):
                        for passaro in passaros:
                            passaro.pular()
            for passaro in passaros:
                passaro.mover()
            chao.mover()

            adicionar_cano = False
            remover_canos = []
            for cano in canos:
                for i, passaro in enumerate(passaros):
                    if (cano.colidir(passaro)):
                        passaros.pop(i)
                    if (not cano.passou and passaro.x > cano.x):
                        cano.passou = True
                        adicionar_cano = True
                cano.mover()
                if (cano.x + cano.cano_topo.get_width() < 0):
                    remover_canos.append(cano)

            if (adicionar_cano):
                pontos += 1
                canos.append(cano(600))
            for cano in remover_canos:
                canos.remove(cano)

            for i, passaro in enumerate(passaros):
                if (passaro.y + passaro.imagem.get_height()) > cano.y or (passaro.y < 0):
                    passaros.pop(i)
    desenhar_tela(tela, passaros, canos, chao, placar)
    

    if __name__ == '__main__':
        main()