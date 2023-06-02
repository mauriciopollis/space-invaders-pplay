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
                tela_de_jogo(janela, dificuldade=1)
        else:
            botao_jogar.set_curr_frame(0)
        if(mouse.is_over_object(botao_dificuldade)):
            botao_dificuldade.set_curr_frame(1)
            if(mouse.is_button_pressed(1)):
                tela_de_dificuldade(janela)
        else:
            botao_dificuldade.set_curr_frame(0)
        if(mouse.is_over_object(botao_ranking)):
            botao_ranking.set_curr_frame(1)
            if(mouse.is_button_pressed(1)):
                pass
        else:
            botao_ranking.set_curr_frame(0)
        if(mouse.is_over_object(botao_sair)):
            botao_sair.set_curr_frame(1)
            if(mouse.is_button_pressed(1)):
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

def tela_de_jogo(janela, dificuldade):
    janela.set_title('Tela de Jogo')
    teclado = janela.get_keyboard()
    nave = Sprite("assets/nave.png", 1)
    nave.set_position(janela.width/2 - nave.width/2, janela.height - nave.height - 5)
    velocidade_nave = 500
    velocidade_tiro = 200/dificuldade
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
                tiro.set_position(nave.x + nave.width/2 - tiro.width/2, nave.y)
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

        #desenho
        janela.set_background_color((0,0,0))
        nave.draw()
        for tiro in lista_tiros:
            tiro.draw()
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

    while True:

        #checa se o mouse está em cima de algum botão e se houve clique
        if(mouse.is_over_object(botao_facil) and mouse.is_button_pressed(1)):
            dificuldade = 1
            tela_de_jogo(janela, dificuldade)
        if(mouse.is_over_object(botao_medio) and mouse.is_button_pressed(1)):
            dificuldade = 5
            tela_de_jogo(janela, dificuldade)
        if(mouse.is_over_object(botao_dificil) and mouse.is_button_pressed(1)):
            dificuldade = 10
            tela_de_jogo(janela, dificuldade)

        # desenho
        janela.set_background_color((0,0,0))
        botao_facil.draw()
        botao_medio.draw()
        botao_dificil.draw()
        janela.update()

menu()
