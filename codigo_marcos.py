from PPlay.window import *
from PPlay.sprite import *
from PPlay.gameimage import *

janela = Window(1000,900)
teclado = Window.get_keyboard()
mouse = Window.get_mouse()
fundo = GameImage("fundo.jpeg")

jogar = Sprite("jogar.png",1)
dificuldade = Sprite("dificuldade.png",1)
rank = Sprite("rank.png",1)
sair = Sprite("quit.png",1)
facil = Sprite("quit.png",1)
medio = Sprite("quit.png",1)
dificil = Sprite("quit.png",1)

def jogo():
    while (True):
        fundo.draw()
        if teclado.key_pressed("ESC"):
            menu()
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