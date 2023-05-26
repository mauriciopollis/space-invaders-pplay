from PPlay.window import *
from PPlay.sprite import *

DIFICULDADE = 1

def menu():

    #inicialização
    janela = Window(1280, 720)
    janela.set_title('Tela de Menu')
    botao_jogar = Sprite("assets/botao_jogar.png", 1)
    botao_jogar.set_position(400, 40)
    botao_dificuldade = Sprite("assets/botao_dificuldade.png", 1)
    botao_dificuldade.set_position(400, 200)
    botao_ranking = Sprite("assets/botao_ranking.png", 1)
    botao_ranking.set_position(400, 360)
    botao_sair = Sprite("assets/botao_sair.png", 1)
    botao_sair.set_position(400, 520)
    mouse = janela.get_mouse()
    apertou_botao_esquerdo = False

    #loop
    while True:

        #checa se o mouse está em cima de algum botão e se houve clique
        if(mouse.is_over_object(botao_jogar) and mouse.is_button_pressed(1) and not apertou_botao_esquerdo):
            print("Jogar")
            apertou_botao_esquerdo = True
            tela_de_jogo(janela)
        if(mouse.is_over_object(botao_dificuldade) and mouse.is_button_pressed(1) and not apertou_botao_esquerdo):
            print("Dificuldade")
            apertou_botao_esquerdo = True
            tela_de_dificuldade(janela)
        if(mouse.is_over_object(botao_ranking) and mouse.is_button_pressed(1) and not apertou_botao_esquerdo):
            print("Ranking")
            apertou_botao_esquerdo = True
        if(mouse.is_over_object(botao_sair) and mouse.is_button_pressed(1) and not apertou_botao_esquerdo):
            print("Sair")
            apertou_botao_esquerdo = True
            janela.close()

        #desenho
        janela.set_background_color((0,0,0))
        botao_jogar.draw()
        botao_dificuldade.draw()
        botao_ranking.draw()
        botao_sair.draw()
        janela.update()

def tela_de_jogo(janela):
    janela.set_title('Tela de Jogo')
    teclado = janela.get_keyboard()

    while True:
        
        if(teclado.key_pressed("ESC")):
            menu()

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