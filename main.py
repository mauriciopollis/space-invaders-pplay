from PPlay.window import *
from PPlay.sprite import *
from PPlay.gameimage import *

DIFICULDADE = 1

def menu():

    #inicialização
    janela = Window(1280, 720)
    janela.set_title('Tela de Menu')
    fundo = GameImage("assets/fundo_espaco.jpg")
    titulo = Sprite("assets/space_invaders_title.png", 1)
    titulo.set_position(150, 20)
    botao_jogar = Sprite("assets/botao_jogar.png", 2)
    botao_jogar.set_position(195, 330)
    botao_dificuldade = Sprite("assets/botao_dificuldade.png", 2)
    botao_dificuldade.set_position(195, 430)
    botao_ranking = Sprite("assets/botao_ranking.png", 2)
    botao_ranking.set_position(685, 330)
    botao_sair = Sprite("assets/botao_sair.png", 2)
    botao_sair.set_position(685, 430)
    mouse = janela.get_mouse()

    #loop
    while True:

        #checa qual botão do menu foi apertado
        if(mouse.is_over_object(botao_jogar)):
            botao_jogar.set_curr_frame(1)
            if(mouse.is_button_pressed(1)):
                print("Jogar")
                tela_de_jogo(janela)
        else:
            botao_jogar.set_curr_frame(0)
        if(mouse.is_over_object(botao_dificuldade)):
            botao_dificuldade.set_curr_frame(1)
            if(mouse.is_button_pressed(1)):
                print("Dificuldade")
                tela_de_dificuldade(janela)
        else:
            botao_dificuldade.set_curr_frame(0)
        if(mouse.is_over_object(botao_ranking)):
            botao_ranking.set_curr_frame(1)
            if(mouse.is_button_pressed(1)):
                print("Ranking")
        else:
            botao_ranking.set_curr_frame(0)
        if(mouse.is_over_object(botao_sair)):
            botao_sair.set_curr_frame(1)
            if(mouse.is_button_pressed(1)):
                print("Sair")
                janela.close()
        else:
            botao_sair.set_curr_frame(0)

        #desenho
        fundo.draw()
        botao_jogar.draw()
        botao_dificuldade.draw()
        botao_ranking.draw()
        botao_sair.draw()
        titulo.draw()
        janela.update()

def tela_de_jogo(janela):
    janela.set_title('Tela de Jogo')
    teclado = janela.get_keyboard()
    nave = Sprite("assets/nave.png", 1)
    nave.set_position(janela.width/2 - nave.width/2, janela.height - nave.height - 5)
    velocidade_nave = 500
    velocidade_tiro = 200
    lista_tiros = []
    tempo_de_recarga = 0.3
    cronometro = tempo_de_recarga + 1

    while True:

        dt = janela.delta_time()

        if(teclado.key_pressed("ESC")):
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
            if(cronometro >= tempo_de_recarga):
                cronometro = 0
                tiro = Sprite("assets/tiro.png", 1)
                tiro.set_position(nave.x + nave.width/2, nave.y)
                lista_tiros.append(tiro)

        #incrementa o cronometro de tiros
        cronometro += dt

        #movimenta os tiros
        for tiro in lista_tiros:
            tiro.y -= velocidade_tiro * dt

        #retira os tiros que saíram da janela
        for tiro in lista_tiros:
            if(tiro.y<0):
                lista_tiros.remove(tiro) 

        janela.set_background_color((0,0,0))
        nave.draw()
        for tiro in lista_tiros:
            tiro.draw()
        janela.update()


        #desenho
        janela.set_background_color((0,0,0))
        janela.update()

def tela_de_dificuldade(janela):
    janela.set_title('Tela de Dificuldade')
    mouse = janela.get_mouse()

    botao_facil = Sprite("assets/botao_facil.png", 1)
    botao_facil.set_position(800, 40)
    botao_medio = Sprite("assets/botao_medio.png", 1)
    botao_medio.set_position(800, 200)
    botao_dificil = Sprite("assets/botao_dificil.png", 1)
    botao_dificil.set_position(800, 360)
    apertou_botao_esquerdo = False

    while True:

        #checa se o mouse está em cima de algum botão e se houve clique
        if(mouse.is_over_object(botao_facil) and mouse.is_button_pressed(1) and not apertou_botao_esquerdo):
            print("Facil")
            apertou_botao_esquerdo = True
            DIFICULDADE = 1
            tela_de_jogo(janela)
        if(mouse.is_over_object(botao_medio) and mouse.is_button_pressed(1) and not apertou_botao_esquerdo):
            print("Medio")
            apertou_botao_esquerdo = True
            DIFICULDADE = 2
            tela_de_jogo(janela)
        if(mouse.is_over_object(botao_dificil) and mouse.is_button_pressed(1) and not apertou_botao_esquerdo):
            print("Dificil")
            apertou_botao_esquerdo = True
            DIFICULDADE = 3
            tela_de_jogo(janela)

        # desenho
        janela.set_background_color((0,0,0))
        botao_facil.draw()
        botao_medio.draw()
        botao_dificil.draw()
        janela.update()

menu()

"""

from PPlay.window import *
from PPlay.sprite import *
from PPlay.gameimage import *

janela = Window(1000,800)
teclado = Window.get_keyboard()
mouse = Window.get_mouse()
fundo = GameImage("assets/fundo.jpeg")

jogar = Sprite("assets/jogar.png",1)
dificuldade = Sprite("assets/dificuldade.png",1)
rank = Sprite("assets/rank.png",1)
sair = Sprite("assets/quit.png",1)
facil = Sprite("assets/quit.png",1)
medio = Sprite("assets/quit.png",1)
dificil = Sprite("assets/quit.png",1)

nave = Sprite("assets/nave.png", 1)

def jogo():

    nave.set_position(janela.width/2 - nave.width/2, janela.height - nave.height - 5)
    velocidade_nave = 500
    velocidade_tiro = 200
    tempo_de_recarga = 0.3
    lista_tiros = []
    cronometro = tempo_de_recarga + 1 # inicializa o cronometro maior que o tempo de recarga para que a nave possa atirar logo no início

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
            if(cronometro >= tempo_de_recarga):
                cronometro = 0
                tiro = Sprite("assets/tiro.png", 1)
                tiro.set_position(nave.x + nave.width/2, nave.y)
                lista_tiros.append(tiro)

        #incrementa o cronometro de tiros
        cronometro += dt

        #movimenta os tiros
        for tiro in lista_tiros:
            tiro.y -= velocidade_tiro * dt

        #retira os tiros que saíram da janela
        for tiro in lista_tiros:
            if(tiro.y<0):
                lista_tiros.remove(tiro) 

        fundo.draw()
        nave.draw()
        for tiro in lista_tiros:
            tiro.draw()
        janela.update()

def diff():
    while(True):
        facil.set_position((janela.width - jogar.width)/2, facil.height/2)
        medio.set_position((janela.width - jogar.width)/2, janela.height/2 - medio.height/2)
        dificil.set_position((janela.width - jogar.width)/2, janela.height - dificil.height*3/2)

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
    jogar.set_position((janela.width - jogar.width)/2,jogar.height/2)
    dificuldade.set_position((janela.width - dificuldade.width)/2,dificuldade.height*2)
    rank.set_position((janela.width - rank.width)/2,rank.height * 2 + rank.height* 3/2)
    sair.set_position((janela.width - sair.width)/2,sair.height * 4 + sair.height)

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

menu()
codigo_marcos.py
Exibindo codigo_marcos.py…

"""