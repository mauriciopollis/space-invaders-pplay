from PPlay.window import *
from PPlay.sprite import *
from PPlay.gameimage import *
import random
import time

janela = Window(1280,720)
teclado = Window.get_keyboard()
mouse = Window.get_mouse()
fundo = GameImage("assets/fundo_espaco.jpg")

jogar = Sprite("assets/jogar.png",1)
dificuldade = Sprite("assets/dificuldade.png",1)
rank = Sprite("assets/rank.png",1)
sair = Sprite("assets/quit.png",1)
facil = Sprite("assets/botao_facil.png",1)
medio = Sprite("assets/botao_medio.png",1)
dificil = Sprite("assets/botao_dificil.png",1)

nave = Sprite("assets/nave.png", 2)
sprite_monstro = Sprite("assets\monstro (1).png")

def jogo(dificuldade, _pontos=0, _vidas=3):
    
    nave.set_position(janela.width/2 - nave.width/2, janela.height - nave.height - 5)
    nave.set_sequence(0, 2, True)
    nave.set_total_duration(300)
    
    # variáveis afetadas pela dificuldade:
    velocidade_nave = 500 - 10 * dificuldade
    velocidade_tiro = 400 - 10 * dificuldade
    velocidade_tiro_monstro = 200 + 10 * dificuldade
    tempo_de_recarga = 0.3 + 0.1 * dificuldade
    tempo_recarga_media_monstros = 2 / dificuldade
    linhas = 3 + 2 * dificuldade
    colunas = 5 + 2 * dificuldade
    velocidade_monstros = 100 + 10 * dificuldade

    variacao_recarga_monstros = 0.3 * tempo_recarga_media_monstros
    tempo_de_recarga_monstros = random.uniform(tempo_recarga_media_monstros - variacao_recarga_monstros, 
                                               tempo_recarga_media_monstros + variacao_recarga_monstros)
    lista_tiros = []
    lista_tiros_monstros = []
    timer_tiros = tempo_de_recarga + 1 # inicializa o cronometro maior que o tempo de recarga para que a nave possa atirar logo no início
    timer_tiros_monstros = tempo_recarga_media_monstros
    matriz_monstros = []
    colidiu = False
    morreu = False
    pontos = _pontos
    pts_ultimo_monstro = 0 # pontos recebidos pelo último monstro que foi morto
    pixels_borda = 50 # variável que limita o quão perto das bordas laterais da janela os monstros vão antes de ter o movimento invertido
    vidas = _vidas

    tempo_invencibilidade = 2
    instante_morte = -tempo_invencibilidade
    invencivel = False

    contador_de_frames = 0
    FPS = 0
    relogio = 0

    #coloca os monstros na matriz
    for i in range(linhas):
        linha = []
        matriz_monstros.append(linha)
        for j in range(colunas):
            monstro = Sprite("assets\monstro (1).png")
            linha.append(monstro)

    # posiciona os monstros
    for i in range(len(matriz_monstros)):
        for j in range(len(matriz_monstros[i])):
            matriz_monstros[i][j].set_position(100 + j * (sprite_monstro.width + sprite_monstro.width/2), 50 + i * (sprite_monstro.height + sprite_monstro.height/2))

    while (True):

        dt = janela.delta_time()

        if teclado.key_pressed("ESC"):
            menu()
        
        #movimento da nave
        if(teclado.key_pressed("LEFT")):
            nave.x += -velocidade_nave * dt
        if(teclado.key_pressed("RIGHT")):
            nave.x += velocidade_nave * dt

        #colisão da nave com as paredes laterais
        if((nave.x + nave.width)>=janela.width):
            nave.x = janela.width - nave.width
        if((nave.x<0)):
            nave.x = 0
        
        #cria o tiro quando a barra de espaço é pressionada
        if(teclado.key_pressed("SPACE")):
            if(timer_tiros >= tempo_de_recarga):
                timer_tiros = 0
                tiro = Sprite("assets/tiro.png", 1)
                tiro.set_position(nave.x + nave.width/2 - tiro.width/2, nave.y)
                lista_tiros.append(tiro)

        # checa se os monstros podem atirar
        if timer_tiros_monstros > tempo_de_recarga_monstros:
            if len(matriz_monstros) != 0:
                monstro_atira(matriz_monstros, lista_tiros_monstros)
                timer_tiros_monstros = 0
                tempo_de_recarga_monstros = random.uniform(tempo_recarga_media_monstros - variacao_recarga_monstros, 
                                                           tempo_recarga_media_monstros + variacao_recarga_monstros)

        #incrementa o cronometro de tiros
        timer_tiros += dt
        timer_tiros_monstros += dt

        #movimenta os tiros
        for tiro in lista_tiros:
            tiro.y -= velocidade_tiro * dt
        
        #movimenta os tiros dos monstros
        for tiro in lista_tiros_monstros:
            tiro.y += velocidade_tiro_monstro * dt

        #retira os tiros que saíram da janela
        for tiro in lista_tiros:
            if(tiro.y<0):
                lista_tiros.remove(tiro)
        
        #retira os tiros dos monstros que saíram da janela
        for tiro in lista_tiros_monstros:
            if(tiro.y > janela.height):
                lista_tiros_monstros.remove(tiro)

        #colisão dos tiros com os monstros, começando a checagem pelos monstros mais baixos
        for tiro in lista_tiros:
            if tiro_dentro_caixa(tiro, matriz_monstros):
                for i in range(len(matriz_monstros) - 1, -1, -1):
                    linha = matriz_monstros[i]
                    for monstro in linha:
                        if(tiro.collided(monstro)):
                            lista_tiros.remove(tiro)
                            linha.remove(monstro)
                            pts_ultimo_monstro = (janela.height - monstro.y)//10
                            pontos += pts_ultimo_monstro

        if(time.time() - instante_morte > tempo_invencibilidade):
            invencivel = False
            nave.set_curr_frame(0)
        else:
            nave.set_loop(True)

        # colisao dos tiros dos monstros com a nave
        for tiro in lista_tiros_monstros:
            if tiro.collided_perfect(nave) and not invencivel:
                lista_tiros_monstros.remove(tiro)
                vidas -= 1
                instante_morte = time.time()
                invencivel = True
                nave.x = janela.width/2 - nave.width/2
                nave.y = janela.height - nave.height - 5

        #função que checa se a matriz de monstros colidiu com as bordas
        colidiu = checa_colisao(matriz_monstros, pixels_borda, velocidade_monstros, dt)

        if colidiu:
            velocidade_monstros = - velocidade_monstros
        
        #função que move o conjunto de monstros
        move_monstros(matriz_monstros, dt, velocidade_monstros, colidiu)

        #função que checa se os monstros chegaram ao limite inferior da tela
        morreu = checa_morte(matriz_monstros)

        if morreu or vidas <= 0:
            grava_ranking(pontos)
            menu()

        if matriz_monstros == []:
            jogo(dificuldade + 1, pontos, vidas)
        
        #FPS
        relogio += dt
        contador_de_frames += 1
        if(relogio >= 1):
            relogio = 0
            FPS = contador_de_frames
            contador_de_frames = 0

        fundo.draw()
        janela.draw_text(f"FPS: {str(FPS)}", 10, (janela.height - 40), 30, color=(255,0,0))
        janela.draw_text(f"pontos : {int(pontos)}", 10, 40, 30, color=(255,0,0))
        janela.draw_text(f"vidas : {vidas}", 10, 80, 30, color=(255,0,0))
        nave.draw()
        nave.update()

        for linha in matriz_monstros:
            for monstro in linha:
                monstro.draw()

        for tiro in lista_tiros:
            tiro.draw()
        
        for tiro in lista_tiros_monstros:
            tiro.draw()

        janela.update()

def diff():

    facil.set_position((janela.width - jogar.width)/2, facil.height/2)
    medio.set_position((janela.width - jogar.width)/2, janela.height/2 - medio.height/2)
    dificil.set_position((janela.width - jogar.width)/2, janela.height - dificil.height*3/2)
    
    while(True):

        if mouse.is_over_object(facil) and mouse.is_button_pressed(1):
            jogo(dificuldade=1)
        if mouse.is_over_object(medio) and mouse.is_button_pressed(1):
            jogo(dificuldade=2)
        if mouse.is_over_object(dificil) and mouse.is_button_pressed(1):
            jogo(dificuldade=3)
        
        if teclado.key_pressed("ESC"):
            menu()

        fundo.draw()
        facil.draw()
        medio.draw()
        dificil.draw()
        janela.update()

def ranking():
    while True:

        try:
            # ordena os scores no arquivo
            with open("ranking.txt", 'r', encoding='utf-8') as f:
                ranking = f.readlines()
                for i in range(len(ranking)):
                    ranking[i] = ranking[i].strip('()\n')
                    ranking[i] = ranking[i].split(',')
                    ranking[i][1] = float(ranking[i][1])
            ranking.sort(key=lambda x: x[1], reverse=True)

            top5 = ranking[0:5]
            fundo.draw()
            espacamento = (janela.height - 100) / len(top5)
            i = 0
            cabecalho = "      {:15}    {:10}{:8}     {:5}".format("NOME", "SCORE", "DATA", "HORARIO")
            janela.draw_text(cabecalho, 10, 5, size=40, color=(255, 255, 255))
            for score in top5:
                nome = score[0]
                pontuacao = score[1]
                data = f"{score[2]}/{score[3]}/{score[4]}"
                horario = f"{score[5]}:{score[6]}"
                texto = f"#{i + 1}: {nome:15} {pontuacao:10}      {data:8} {horario:5}"
                janela.draw_text(texto, 10, 100 + i * espacamento, size=40, color=(255,255,255))
                i += 1
            janela.update()

        except FileNotFoundError:
            pass

        if teclado.key_pressed("ESC"):
            break

def menu():
    
    espaco_entre_botoes = janela.height - 4 * (jogar.height)
    espaco_entre_botoes = espaco_entre_botoes / 5

    jogar.set_position((janela.width - jogar.width)/2, espaco_entre_botoes)
    dificuldade.set_position((janela.width - dificuldade.width)/2, jogar.y + jogar.height + espaco_entre_botoes)
    rank.set_position((janela.width - rank.width)/2, dificuldade.y + dificuldade.height + espaco_entre_botoes)
    sair.set_position((janela.width - sair.width)/2, rank.y + rank.height + espaco_entre_botoes)

    while (True):
        
        if mouse.is_over_object(jogar) and mouse.is_button_pressed(1):
            jogo(dificuldade=1)

        if mouse.is_over_object(dificuldade) and mouse.is_button_pressed(1):
            diff()

        if mouse.is_over_object(rank) and mouse.is_button_pressed(1):
            ranking()
              
        if mouse.is_over_object(sair) and mouse.is_button_pressed(1):
            janela.close()

        fundo.draw()
        jogar.draw()
        dificuldade.draw()
        rank.draw()
        sair.draw()
        janela.update()

def move_monstros(matriz, dt, velocidade, colidiu):
    for linha in matriz:
        for monstro in linha:
            monstro.x += velocidade * dt
    if colidiu:
        for linha in matriz:
            for monstro in linha:
                monstro.y += sprite_monstro.height

def checa_colisao(matriz, largura_borda, velocidade, dt):
    colidiu = False
    caixa = caixa_monstros(matriz)
    if caixa != (0, 0, 0, 0):
        esquerda = caixa[2]
        direita = caixa[3]
        if direita > (janela.width - largura_borda) or esquerda < largura_borda:
            colidiu = True
            for linha in matriz:
                for monstro in linha:
                    monstro.x = monstro.x - velocidade * dt

    return colidiu

def checa_morte(matriz):
    morreu = False
    caixa = caixa_monstros(matriz)
    if caixa != (0, 0, 0, 0):
        baixo = caixa[1]
        if baixo > janela.height - 50:
            morreu = True
    return morreu

#função que retorna os limites da 'caixa' que envolve os monstros
def caixa_monstros(matriz):
    for linha in matriz:
        if linha == []:
            matriz.remove(linha)
    if matriz != []:
        cima = matriz[0][0].y
        baixo = matriz[-1][0].y + matriz[-1][0].height
        esquerda = matriz[0][0].x
        direita = matriz[0][-1].x + matriz[0][-1].width
        for linha in matriz:
            if linha[0].x < esquerda:
                esquerda = linha[0].x
            if((linha[-1].x + linha[-1].width) > direita):
                direita = linha[-1].x + linha[-1].width
        return (cima, baixo, esquerda, direita)
    else:
        return (0, 0, 0, 0)

def tiro_dentro_caixa(tiro, matriz):
    caixa = caixa_monstros(matriz)
    if caixa != (0, 0, 0, 0):
        cima = caixa[0]
        baixo = caixa[1]
        esquerda = caixa[2]
        direita = caixa[3]
        if((esquerda <= tiro.x <= direita - tiro.width) and (cima <= tiro.y <= baixo - tiro.height)):
            return True
        else:
            return False
    else:
        return False

def sorteia_monstro(matriz):
    num_linhas = len(matriz)
    #sorteia a linha do monstro que vai atirar
    i = random.randint(0, num_linhas - 1)
    #sorteia o monstro da linha que vai atirar
    num_colunas = len(matriz[i])
    j = random.randint(0, num_colunas - 1)
    return i, j

def monstro_atira(matriz, tiros_monstros):
    i, j = sorteia_monstro(matriz)
    monstro = matriz[i][j]
    tiro = Sprite("assets\\tiro_monstro.png")
    tiro.x = monstro.x + monstro.width/2
    tiro.y = monstro.y + monstro.height/2
    tiros_monstros.append(tiro)

def grava_ranking(pontos=0):
    data = time.localtime()
    ano = data[0]
    mes = data[1]
    dia = data[2]
    hora = data[3]
    minuto = data[4]
    nome = input("Insira seu nome: ")
    score = f"{nome}, {pontos}, {dia}, {mes}, {ano}, {hora}, {minuto}\n"

    # escreve o score atual no arquivo
    with open("ranking.txt", 'a', encoding='utf-8') as f:
        f.write(score)

menu()