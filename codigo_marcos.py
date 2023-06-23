from PPlay.window import *
from PPlay.sprite import *
from PPlay.gameimage import *

janela = Window(1280,720)
teclado = Window.get_keyboard()
mouse = Window.get_mouse()
fundo = GameImage("assets/fundo.jpeg")

jogar = Sprite("assets/jogar.png",1)
dificuldade = Sprite("assets/dificuldade.png",1)
rank = Sprite("assets/rank.png",1)
sair = Sprite("assets/quit.png",1)
facil = Sprite("assets/botao_facil.png",1)
medio = Sprite("assets/botao_medio.png",1)
dificil = Sprite("assets/botao_dificil.png",1)

nave = Sprite("assets/nave.png", 1)
sprite_monstro = Sprite("assets\monstro (1).png")

def jogo():

    nave.set_position(janela.width/2 - nave.width/2, janela.height - nave.height - 5)
    velocidade_nave = 500
    velocidade_tiro = 200
    tempo_de_recarga = 0.3
    lista_tiros = []
    timer_tiros = tempo_de_recarga + 1 # inicializa o cronometro maior que o tempo de recarga para que a nave possa atirar logo no início
    matriz_monstros = []
    linhas = 5
    colunas = 10
    velocidade_monstros = 100
    colidiu = False
    morreu = False
    pontos = 0
    pts_ultimo_monstro = 0 # pontos recebidos pelo último monstro que foi morto
    pixels_borda = 50 # variável que limita o quão perto das bordas laterais da janela os monstros vão antes de ter o movimento invertido

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

        #incrementa o cronometro de tiros
        timer_tiros += dt

        #movimenta os tiros
        for tiro in lista_tiros:
            tiro.y -= velocidade_tiro * dt

        #retira os tiros que saíram da janela
        for tiro in lista_tiros:
            if(tiro.y<0):
                lista_tiros.remove(tiro)
            
        #colisão dos tiros com os monstros
        for tiro in lista_tiros:
            if tiro_dentro_caixa(tiro, matriz_monstros):
                print("Dentro")
                for linha in matriz_monstros:
                    for monstro in linha:
                        if tiro.collided(monstro):
                            lista_tiros.remove(tiro)
                            linha.remove(monstro)
                            if linha == []:
                                matriz_monstros.remove(linha)
                            pts_ultimo_monstro = (janela.height - monstro.y)//10
                            pontos += pts_ultimo_monstro

        #função que checa se a matriz de monstros colidiu com as bordas
        colidiu = checa_colisao(matriz_monstros, velocidade_monstros, pixels_borda)

        if colidiu:
            velocidade_monstros = - velocidade_monstros
        
        #função que move o conjunto de monstros
        move_monstros(matriz_monstros, dt, velocidade_monstros, colidiu)

        #função que checa se os monstros chegaram ao final da fase
        morreu = checa_morte(matriz_monstros)

        if morreu:
            menu()
        
        #FPS
        relogio += dt
        contador_de_frames += 1
        if(relogio >= 1):
            relogio = 0
            FPS = contador_de_frames
            contador_de_frames = 0

        fundo.draw()
        janela.draw_text(str(FPS), 40, (janela.height - 40), 30, color=(255,0,0))
        janela.draw_text(f"pts : {str(pontos)}", 40, 40, 30, color=(255,0,0))
        janela.draw_text(f"pts ultimo monstro : {str(pts_ultimo_monstro)}", 40, 80, 30, color=(255,0,0))
        nave.draw()

        for linha in matriz_monstros:
            for monstro in linha:
                monstro.draw()

        for tiro in lista_tiros:
            tiro.draw()
        janela.update()

def diff():

    facil.set_position((janela.width - jogar.width)/2, facil.height/2)
    medio.set_position((janela.width - jogar.width)/2, janela.height/2 - medio.height/2)
    dificil.set_position((janela.width - jogar.width)/2, janela.height - dificil.height*3/2)
    
    while(True):

        if mouse.is_over_object(facil) and mouse.is_button_pressed(1):
            jogo()
        if mouse.is_over_object(medio) and mouse.is_button_pressed(1):
            jogo()
        if mouse.is_over_object(dificil) and mouse.is_button_pressed(1):
            jogo()
        
        if teclado.key_pressed("ESC"):
            menu()

        fundo.draw()
        facil.draw()
        medio.draw()
        dificil.draw()
        janela.update()

def menu():
    
    espaco_entre_botoes = janela.height - 4 * (jogar.height)
    espaco_entre_botoes = espaco_entre_botoes / 5

    jogar.set_position((janela.width - jogar.width)/2, espaco_entre_botoes)
    dificuldade.set_position((janela.width - dificuldade.width)/2, jogar.y + jogar.height + espaco_entre_botoes)
    rank.set_position((janela.width - rank.width)/2, dificuldade.y + dificuldade.height + espaco_entre_botoes)
    sair.set_position((janela.width - sair.width)/2, rank.y + rank.height + espaco_entre_botoes)

    while (True):
        
        if mouse.is_over_object(jogar) and mouse.is_button_pressed(1):
            jogo()

        if mouse.is_over_object(dificuldade) and mouse.is_button_pressed(1):
            diff()

        #if mouse.is_over_object(rank):
            #if mouse.is_button_pressed(1):
              
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
                monstro.y += monstro.height

def checa_colisao(matriz, velocidade, largura_borda):
    colidiu = False
    caixa = caixa_monstros(matriz)
    if caixa != "matriz vazia":
        esquerda = caixa[2]
        direita = caixa[3]
        if direita > (janela.width - largura_borda) or esquerda < largura_borda:
            colidiu = True
    return colidiu

def checa_morte(matriz):
    morreu = False
    caixa = caixa_monstros(matriz)
    if caixa != "matriz vazia":
        baixo = caixa[1]
        if baixo > janela.height - 50:
            morreu = True
    return morreu

#função que retorna os limites da 'caixa' que envolve os monstros
def caixa_monstros(matriz):
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
        return "matriz vazia"

def tiro_dentro_caixa(tiro, matriz):
    caixa = caixa_monstros(matriz)
    if caixa != "matriz vazia":
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
    

menu()