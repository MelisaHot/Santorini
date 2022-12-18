import pygame
import random
import sys
import utils
import copy
import time
from utils import *


sirina = 30 # igrac
sirinaPolja = 100 # polje na tabli
displej = pygame.display.set_mode((500,500), pygame.DOUBLEBUF | pygame.HWSURFACE,16) #displej po kojem ce se sve crtati


    # 1 bit -- 0 visina
    # 2 bit -- 1 visina
    # 3 bit -- 2 visina
    # 4 bit -- 3 visina
    
    # 5 bit -- kupola
    # 6 bit -- 1 igrac
    # 7 bit -- 2 igrac
    # 8 bit -- moguca pozicija
tabla = [[nemaTornja,nemaTornja,nemaTornja,nemaTornja,nemaTornja],
         [nemaTornja,nemaTornja,nemaTornja,nemaTornja,nemaTornja],
         [nemaTornja,nemaTornja,nemaTornja,nemaTornja,nemaTornja],
         [nemaTornja,nemaTornja,nemaTornja,nemaTornja,nemaTornja],
         [nemaTornja,nemaTornja,nemaTornja,nemaTornja,nemaTornja]]
tablaZaAlgoritam = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]


def CrtajTablu():
    for red in range(0, 600, sirinaPolja):
        pygame.draw.line(displej, (0,0,255), (0,red), (500,red), 10)
    for kol in range(0, 600, sirinaPolja):
        pygame.draw.line(displej, (0,0,255), (kol,0), (kol,500), 10)

def CrtajIgrace():
    boja = (255,0,0)
    for iRed, red in enumerate(tabla):
        for iKol, kol in enumerate(red):
            if tabla[iRed][iKol] & igrac1:
                pygame.draw.circle(displej, (255,0,0), (iKol*sirinaPolja + int(sirinaPolja/2), iRed*sirinaPolja + int(sirinaPolja/2)),sirina)
            elif tabla[iRed][iKol] & igrac2:
                pygame.draw.circle(displej, (0,255,0), (iKol*sirinaPolja + int(sirinaPolja/2), iRed*sirinaPolja + int(sirinaPolja/2)),sirina)

def CrtajMoguca():
    for iRed, red in enumerate(tabla):
        for iKol, kol in enumerate(red):
            if tabla[iRed][iKol] & mogucaPozicija:
                pygame.draw.circle(displej, (255,255,0), (iKol*sirinaPolja + int(sirinaPolja/2), iRed*sirinaPolja + int(sirinaPolja/2)),10)
                 


def CrtajTornjeve():
    for iRed, red in enumerate(tabla):
        for iKol, kol in enumerate(red):
            if tabla[iRed][iKol] & toranj1:
                pygame.draw.rect(displej, (179,59,0), (iKol*100 + 40, iRed*100 +40, 60, 60))
            elif tabla[iRed][iKol] & toranj2:
                pygame.draw.rect(displej, (179,59,0), (iKol*100 + 40, iRed*100 +40, 60, 60))
                pygame.draw.rect(displej, (189,69,0), (iKol*100 + 30, iRed*100 +30, 50, 50))
            elif tabla[iRed][iKol] & toranj3:
                pygame.draw.rect(displej, (179,59,0), (iKol*100 + 40, iRed*100 +40, 60, 60))
                pygame.draw.rect(displej, (189,69,0), (iKol*100 + 30, iRed*100 +30, 50, 50))
                pygame.draw.rect(displej, (199,79,0), (iKol*100 + 20, iRed*100 + 20, 40, 40))
            elif tabla[iRed][iKol] & kupola:
                pygame.draw.rect(displej, (179,59,0), (iKol*100 + 40, iRed*100 +40, 60, 60))
                pygame.draw.rect(displej, (189,69,0), (iKol*100 + 30, iRed*100 + 30, 50, 50))
                pygame.draw.rect(displej, (199,79,0), (iKol*100 + 20, iRed*100 + 20, 40, 40))
                pygame.draw.rect(displej, (255,255,0), (iKol*100 + 10, iRed*100 + 10, 30, 30))

def GameLoop():
    #inicijalizacija
    pygame.init()
    pygame.font.init()
    txt = pygame.font.Font(None, 42)
    AI = False
    global displej
    global tablaZaAlgoritam
    global algoritamPozicije
    global tabla
    global root
   

    #main loop
    loop = True
    stanja = ["meni", "tezina", "inicijalizacija", "pomeranjeFigure1", "gradnja1", "pomeranjeFigure2", "gradnja2" ]
    stanje = stanja[0]
    tezine = ["easy","medium","hard"]
    tezina = None
    postavljeno = 1
    zadnjaPozicijaX = 0
    zadnjaPozicijaY = 0
    gradnja = False
    while loop:
        for event in pygame.event.get():#svaki event
            if event.type == pygame.QUIT: # da li je prekinuo igru
                sys.exit() #izadji iz igre
            if event.type == pygame.MOUSEBUTTONDOWN: #registruje klik
                x,y = event.pos #pozicvije klika i skupljanje pozicija
                if stanje == stanja[0]:
                    if x > 100 and x < 400 and y > 100 and y < 200:#ako bira igrac protiv igraca
                        AI = False # ako je protiv igraca 
                        stanje = stanja[2]
                    elif x > 100 and x < 400 and y > 250 and y < 350:
                        AI = True
                        stanje = stanja[1]
                elif stanje == stanja[1]:#igrac protiv ai
                    if x > 100 and x < 400 and y > 50 and y < 150:#bira tezinu
                        tezina = tezine[0]
                        stanje = stanja[2]
                    elif x > 100 and x < 400 and y > 200 and y < 300:
                        tezina = tezine[1]
                        stanje = stanja[2]
                    elif x > 100 and x < 400 and y > 350 and y < 450:
                        tezina = tezine[2]
                        stanje = stanja[2]
                elif stanje == stanja[2]:# ako je postavljanje figura
                    if postavljeno != 5:#brojimo postavljene figure
                        if not (tabla[int(y/sirinaPolja)][int(x/sirinaPolja)] & igrac1 | tabla[int(y/sirinaPolja)][int(x/sirinaPolja)] & igrac2):
                            if postavljeno < 3:# postavljamo figure za 1. igraca
                                tabla[int(y/sirinaPolja)][int(x/sirinaPolja)] = tabla[int(y/sirinaPolja)][int(x/sirinaPolja)] | igrac1
                                tablaZaAlgoritam[int(y/sirinaPolja)][int(x/sirinaPolja)] = -1
                            elif not AI: #ako ne igra ai
                                tabla[int(y/sirinaPolja)][int(x/sirinaPolja)] = tabla[int(y/sirinaPolja)][int(x/sirinaPolja)] | igrac2
                            postavljeno += 1
                            if postavljeno == 5: # kada je sve postavljeno - gradnja za prvog
                                stanje = stanja[3]
                elif stanje == stanja[3] or stanje == stanja[5]: # da li je kretanje prvog ili drugog
                    igrac = 0
                    if stanje == stanja[3]:
                        igrac = igrac1
                    else:
                        igrac = igrac2

                    
                    if tabla[int(y/sirinaPolja)][int(x/sirinaPolja)] & igrac: # ako je kliknuto na igraca
                        IzracunajMoguce(int(x/sirinaPolja),int(y/sirinaPolja), True,tabla)# racunaj poteze za tog igraca
                        if stanje == stanja[3] or stanje == stanja[5]:
                            brojac = 0
                            for iRed, red in enumerate(tabla):
                                for iKol, kol in enumerate(red):
                                    if tabla[iRed][iKol] & mogucaPozicija:
                                        brojac += 1
                            if brojac == 0: # ako nema vise mogucih poteza znaci da je igra gotova
                                stanje = stanja[0]
                                tabla = [[nemaTornja,nemaTornja,nemaTornja,nemaTornja,nemaTornja],
                                     [nemaTornja,nemaTornja,nemaTornja,nemaTornja,nemaTornja],
                                     [nemaTornja,nemaTornja,nemaTornja,nemaTornja,nemaTornja],
                                     [nemaTornja,nemaTornja,nemaTornja,nemaTornja,nemaTornja],
                                     [nemaTornja,nemaTornja,nemaTornja,nemaTornja,nemaTornja]]
                                postavljeno = 1 # restartuje sve
                            
                        zadnjaPozicijaX = int(x/sirinaPolja) # uzima tu gde je kliknuto kao zadnju poziciju
                        zadnjaPozicijaY = int(y/sirinaPolja)
                    elif tabla[int(y/sirinaPolja)][int(x/sirinaPolja)] & mogucaPozicija: # da li je kliknuo gde je moguca pozicija
                        ObrisiMoguce(tabla)
                        tabla[int(y/sirinaPolja)][int(x/sirinaPolja)] = tabla[int(y/sirinaPolja)][int(x/sirinaPolja)] | igrac # postavlja na tu poziciju igraca
                        tabla[zadnjaPozicijaY][zadnjaPozicijaX] = tabla[zadnjaPozicijaY][zadnjaPozicijaX] & ~igrac # brise ga sa zadnje pozicije
                        if stanje == stanja[3]: # ako je pomera 1. igrac njegova je gradnja
                            stanje = stanja[4]
                        else:
                            stanje = stanja[6]
                        if tabla[int(y/sirinaPolja)][int(x/sirinaPolja)] & toranj3: # da li je na tornju 3 pobedio je
                            stanje = stanja[0]
                            tabla = [[nemaTornja,nemaTornja,nemaTornja,nemaTornja,nemaTornja],
                                     [nemaTornja,nemaTornja,nemaTornja,nemaTornja,nemaTornja],
                                     [nemaTornja,nemaTornja,nemaTornja,nemaTornja,nemaTornja],
                                     [nemaTornja,nemaTornja,nemaTornja,nemaTornja,nemaTornja],
                                     [nemaTornja,nemaTornja,nemaTornja,nemaTornja,nemaTornja]]
                            postavljeno = 1 # brojac koliko j figura postavljeno na tabli
                            print("Human win")

                # za gradnje           
                if stanje == stanja[4] or stanje == stanja[6]:
                    if not gradnja: # moguce pozcije ya gradnju
                        IzracunajMoguce(int(x/sirinaPolja),int(y/sirinaPolja), False,tabla)
                        gradnja = True
                    else:
                        if tabla[int(y/sirinaPolja)][int(x/sirinaPolja)] & mogucaPozicija: # DA LI je kliknuo na mogucu poziciju
                            gradnja = False
                            ObrisiMoguce(tabla)
                            tabla[int(y/sirinaPolja)][int(x/sirinaPolja)] = tabla[int(y/sirinaPolja)][int(x/sirinaPolja)] << 1 # iygradi toranj tako sto odradi bitwise shift na mogucoj lokaciji
                            if stanje == stanja[4]: # ciji je sada potez
                                stanje = stanja[5]
                            else:
                                stanje = stanja[3]
                            

        if AI: # ako je protiv ai
            if stanje == stanja[2] and postavljeno >= 3: # proverava da li je u stanju postavljeno i da li je prvi igrac postavio svoje
                PostavljanjeAlgo(tablaZaAlgoritam) # pozivamo postavljanjeAlgo iz algoritam.py
                while postavljeno < 5:
                    for poz in algoritamPozicije:
                        if len(algoritamPozicije[poz]) == 0:
                            continue
                        kol, red = algoritamPozicije[poz][random.randint(0, len(algoritamPozicije[poz]) - 1)] # uzima nasumicno od najboljih pozicija
                        algoritamPozicije[poz].remove((kol,red)) # i makne je iz recnika
                        tabla[kol][red] = igrac2 | tabla[kol][red] # postavi ga na to mesto
                        postavljeno += 1
                        break
                else:
                    stanje = stanja[3]
            elif stanje == stanja[5]:
                tb = tabla
                ig1f1 = None
                ig1f2 = None
                ig2f1 = None
                ig2f2 = None
                for iRed, red in enumerate(tb): # prolazi kroz tablu i pamti gde su sve igraci
                    for iKol, kol in enumerate(red):
                        if tb[iRed][iKol] & igrac1:
                            if ig1f1: # ako sam sacuvao figuru 1 onda cuva figiri 2 ako nije nasao onda nju cuva
                                ig1f2 = (iKol,iRed)
                            else:
                                ig1f1 = (iKol,iRed)
                        elif tb[iRed][iKol] & igrac2:
                            if ig2f1:
                                ig2f2 = (iKol,iRed)
                            else:
                                ig2f1 = (iKol,iRed)
                root = Node(0,0,0,0,0,0,None,tb,[ig1f1,ig1f2],[ig2f1,ig2f2],tezina,3) # pocetni node stabla od kojeg polazi
                tajm = time.perf_counter() # za koliko je izvrsio potez
                MinMax(root,3,True,root) # salje minmax u njemu ima root node, dubinu, oznaka za igraca, alfa - beskonacno, beta beskonacno, maximalna dubina, tezina
                print("Exec time: ", time.perf_counter() - tajm) # racuna koliko mu je vremena trebalo za minmax
                tar = root.RootGet() 
                root.Track()
                X,Y = tar.polazna
                pX,pY = tar.potez
                gX,gY = tar.gradnja
                tabla[Y][X] = tabla[Y][X] & ~igrac2
                tabla[pY][pX] = tabla[pY][pX] | igrac2
                tabla[gY][gX] = tabla[gY][gX] << 1
                stanje = stanja[3]
                if tabla[pY][pX] & toranj3:
                    stanje = stanja[0]
                    tabla = [[nemaTornja,nemaTornja,nemaTornja,nemaTornja,nemaTornja],
                                     [nemaTornja,nemaTornja,nemaTornja,nemaTornja,nemaTornja],
                                     [nemaTornja,nemaTornja,nemaTornja,nemaTornja,nemaTornja],
                                     [nemaTornja,nemaTornja,nemaTornja,nemaTornja,nemaTornja],
                                     [nemaTornja,nemaTornja,nemaTornja,nemaTornja,nemaTornja]]
                    postavljeno = 1
                    print("AI WINS!")
            elif stanje == stanja[6]:
                stanje = stanja[3]
        
        CrtajTablu()
        if stanje == stanja[0]:
            pygame.draw.rect(displej, (0,255,255), (100, 100,300, 100),10)
            pygame.draw.rect(displej, (0,255,255), (100, 250,300, 100),10)
            displej.blit(txt.render("VS man", True,(0,255,0)),(200,130))
            displej.blit(txt.render("VS AI", True,(0,255,0)),(200,280))
        elif stanje == stanja[1]:
            pygame.draw.rect(displej, (0,255,255), (100, 50,300, 100),10)
            pygame.draw.rect(displej, (0,255,255), (100, 200,300, 100),10)
            pygame.draw.rect(displej, (0,255,255), (100, 350,300, 100),10)
            displej.blit(txt.render("Easy", True,(0,255,0)),(200,80))
            displej.blit(txt.render("Medium", True,(0,255,0)),(200,230))
            displej.blit(txt.render("Hard", True,(0,255,0)),(200,380))
        else:
            CrtajTornjeve()
            CrtajIgrace()
            CrtajMoguca()        
        
        pygame.display.update()
        displej.fill((0,0,0))
   
GameLoop()