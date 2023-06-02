from PPlay.window import *
from PPlay.sprite import *
from PPlay.gameimage import *

janela = Window(1000,720)
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