from math import floor,sqrt,inf
import random
import time
import copy

class Node:
    def __init__(self, polaznoX, polaznoY, x, y,gX,gY, roditelj,tab,ig1,ig2,tezina,mDubina):
        self.polazna = (polaznoX, polaznoY)
        self.potez = (x,y)
        self.gradnja = (gX,gY)
        self.roditelj = roditelj
        self.figure1 = ig1
        self.figure2 = ig2
        self.deca = []
        self.tabla = tab
        self.vrednost = 0
        self.Generated = None
        self.Time = None
        self.Tezina = tezina
        self.MaxDubina = mDubina
        if roditelj == None:
            self.dubina = 0
            self.alfa = -inf
            self.beta = inf
        else:
            self.alfa = None
            self.beta = None
            self.dubina = self.roditelj.dubina + 1
            self.roditelj.deca.append(self)
    def RootGet(self):
        for dete in self.deca:
            if dete.vrednost == -self.vrednost:
                return dete
    def PlayMoves(self):
        moves = [] # uzme prazan niz
        n = self
        while n.dubina > 0: # dok nisi stigao do nultog noda - tj do korena
            moves.append(n) # dodaj node u listu 
            n = n.roditelj # idi na roditelja  u toj listi imamo putanju izmedju root i node 
        return moves            
    def Track(self):
        print("Sa: ", self.polazna, " na ", self.potez, " gradnja ", self.gradnja, " sa vrednosti: ", self.vrednost, " -- nivo: ", self.dubina )
        for dete in self.deca:
            if dete.vrednost == -self.vrednost or (dete.vrednost == self.vrednost and dete.deca == []):
                dete.Track()
                break

def Play(moveset, reverse):
    #tajm = time.perf_counter()
    if reverse: # da li povlacimo potez ili igramo. 
        for move in moveset:
            pX,pY = move.polazna
            X,Y = move.potez
            gX,gY = move.gradnja
            move.tabla[gY][gX] = move.tabla[gY][gX] >> 1
            if move.dubina % 2 != 0:
                move.tabla[Y][X] = move.tabla[Y][X] & ~igrac2
                move.tabla[pY][pX] = move.tabla[pY][pX] | igrac2
            else:
                move.tabla[Y][X] = move.tabla[Y][X] & ~igrac1
                move.tabla[pY][pX] = move.tabla[pY][pX] | igrac1
    else:
        for move in reversed(moveset):
            pX,pY = move.polazna
            X,Y = move.potez
            gX,gY = move.gradnja
            if move.dubina % 2 != 0:
                move.tabla[pY][pX] = move.tabla[pY][pX] & ~igrac2
                move.tabla[Y][X] = move.tabla[Y][X] | igrac2
            else:
                move.tabla[pY][pX] = move.tabla[pY][pX] & ~igrac1
                move.tabla[Y][X] = move.tabla[Y][X] | igrac1
            move.tabla[gY][gX] = move.tabla[gY][gX] << 1

def GenerateChildren(node,r):
    tb = node.tabla
    #printBoard(tb)
    Play(node.PlayMoves(),False) # igra potez za svaki node za koji racuna decu - poziva da odigra sve poteze izmejdu tog noda i roota
    #printBoard(tb)
    if node.dubina == 0 or node.dubina % 2 == 0: # koja je dubina ako je 0 ili je parna onda je na potezu ai
        figure = node.figure2 # uzima za figure figure 2
    else:
        figure = node.figure1
    
    brojPoz = 0 # koliko ima poteza - broj pozicija gde moze da igra
    for fig in figure: #za prvu figuru
        moguce = IzracunajMoguce(fig[0],fig[1],True,tb) #racuna moguce i stavlja ih u listu da ne ni prolazio opet kroz tablu
        random.shuffle(moguce) # da bi poboljsali performanse koristi se random. shuffle da razbaca listu 
        brojPoz += len(moguce) # na broj pozicija doda duzinu niza 
        for pos in moguce: # za pomeranje igraca 
            pY,pX = pos #uzima Y i X od pozicije mogucih
            X,Y = fig #i x i y od figure
            ObrisiMoguce(tb)       
            if node.dubina == 0 or node.dubina % 2 == 0: # koje je dubine da zna da li da pomera jednog ili drugog igraca
                tb[Y][X] = tb[Y][X] & ~igrac2
                tb[pY][pX] = tb[pY][pX] | igrac2
            else:
                tb[Y][X] = tb[Y][X] & ~igrac1
                tb[pY][pX] = tb[pY][pX] | igrac1               
            
            gradnja = IzracunajMoguce(pX,pY,False,tb) # gleda gde moze da gradi - sve smo stavili u jednom node
            random.shuffle(gradnja) # isto razbaca to 
            for gra in gradnja:
                gY,gX = gra
                ObrisiMoguce(tb) # brise moguce
                tb[gY][gX] = tb[gY][gX] << 1 #gradi sa bitwise funkcijom
                if node.dubina == 0 or node.dubina % 2 == 0: # posto smo pomerili figuru moramo da odradimo update da bi videli sta je nova situacija na tabli
                    ig1 = node.figure1 # kada igrac 2 igra, onda ne menjamo za igraca 1
                    if fig == node.figure2[0]: #koja figura se promenila
                        ig2 = [(pX,pY),node.figure2[1]] # ako je prva figura pomerena onda stavimo vr, a za drugu ostavimo ta koja je bila
                    else:
                        ig2 = [node.figure2[0],(pX,pY)]
                else:
                    ig2 = node.figure2
                    if fig == node.figure1[0]:
                        ig1 = [(pX,pY),node.figure1[1]]
                    else:
                        ig1 = [node.figure1[0],(pX,pY)]
                        
                n = Node(X,Y,pX,pY,gX,gY,node,tb,ig1,ig2,0,0) # imamo sve podatke da napravimp novi node
                if n.dubina == r.MaxDubina: # da li je stigao do potrebne dubine
                    n.vrednost = Eval(n,r.Tezina) # ako je stigao do te dubine trazi da evaluira
                tb[gY][gX] = tb[gY][gX] >> 1 # povlacimo taj toranj koji smo izgradili 
            if n.dubina % 2 != 0: # sklanja tog igraca
                tb[pY][pX] = tb[pY][pX] & ~igrac2
                tb[Y][X] = tb[Y][X] | igrac2
            else:
                tb[pY][pX] = tb[pY][pX] & ~igrac1
                tb[Y][X] = tb[Y][X] | igrac1  
    Play(node.PlayMoves(),True) # kada izvrsi svu gradnju i sve poteze  vraca tablu kako je bila na pocetku 
    if brojPoz == 0: # ako nema vise poteza
        node.vrednost = Eval(node,r.Tezina) # vrati evaluaciju tog noda

def MinMax(node, dub, igrac, r):
    if dub != 0 and not node.Generated: # da nije vec zavrsio provera i da li je nas node izgenerisan 
        GenerateChildren(node,r) # generise decu za taj node, dajemo mu node, max dubinu i do koje tezine 
        node.Generated = True # da zna da ne mora vise da racuna
    if dub == 0 or node.deca == []: # proverava na kojoj je dubili ili je stigao do kraja tj nema dece ili iz tog stanja ne moze da se krece
        return igrac * node.vrednost # vraca vrednost jednog noda 
    
    node.vrednost = -inf # za njegovu vrednost postavlja najgoru situaciju
    if node.dubina != 0:
        temp = node.roditelj.alfa 
        node.alfa = -node.roditelj.beta
        node.beta = -temp
     #za svako dete mi postavljamo vrednost, uzimamo max izmedju vrednosti njega i rekurzivne funkcije -MinMaX      
    for dete in node.deca:
        node.vrednost = max(node.vrednost,-MinMax(dete,dub-1,-igrac,r))
        node.alfa = max(node.vrednost,node.alfa)    
        if node.alfa >= node.beta:
            break #odsecanje
    return node.vrednost # svaki node ce imati vrednost koja je najbolja moguca pozicija


def TowerNear(node, tezina):
    x,y = node.potez
    val = 0
    for red in range (-1,2,1):
        for kol in range(-1,2,1):
            if x+kol<0 or y+red<0 or x+kol>=len(node.tabla[y]) or y+red >= len(node.tabla) or (red == 0 and kol == 0):
                continue
            #ako moze da se popne na visi toranj daj mu vecu vrednost
            if not (node.tabla[y+red][x+kol] & tornjevi) - ((node.tabla[y][x] & tornjevi)*2): 
                val += (node.tabla[y+red][x+kol] & tornjevi) * (node.tabla[y+red][x+kol] & tornjevi)
            else:
                val += (node.tabla[y+red][x+kol] & tornjevi)
    return val
    
def Eval(node,tezina): # heuristika na citavoj tabli vrednost heuristike je zbirna vrednost povoljnosti pozicija svih igraca s tim da suprotnog igraca oduzimamo jer je negativno ako je on dobar
    val = 0
    for pos in node.figure1 + node.figure2:
        X,Y = pos
        if node.tabla[Y][X] & igrac1:
            if node.tabla[Y][X] & toranj3:
                return -inf #Gubitak
            else:
                val -= 20 * ((node.tabla[Y][X]&tornjevi)-1)
                if not tezina == "easy":
                    val -= TowerNear(node,tezina)
        elif node.tabla[Y][X] & igrac2:
            if node.tabla[Y][X] & toranj3:
                return inf #Pobeda
            else:
                val += 20 * ((node.tabla[Y][X]&tornjevi)-1)
                if not tezina == "easy": # ako je tezina medium ili hard na tu vrednost "val" dodaj i vrednost koja se racuna funkcijom ToewrNear
                    val += TowerNear(node,tezina)
    if tezina == "hard": # ako je tezina hard daj mu vrednost "val+ToewrNear" i kazni ga za udaljenost od figura protivnickog igraca
        igrac = node.figure1
        ai = node.figure2
        d1 = Distanca(ai[0],igrac[0])
        d2 = Distanca(ai[0],igrac[1])
        if d1 < d2:
            val -= d1*d1*d1
            val -= Distanca(ai[1],igrac[1])*Distanca(ai[1],igrac[1])*Distanca(ai[1],igrac[1])
        else:
            val -= d2*d2*d2
            val -= Distanca(ai[1],igrac[0])*Distanca(ai[1],igrac[0])*Distanca(ai[1],igrac[0])
    return val
                
              
nemaTornja = 0b00000001
toranj1 = 0b00000010
toranj2 = 0b00000100
toranj3 = 0b00001000
kupola = 0b00010000
igrac1 = 0b00100000
igrac2 = 0b01000000
mogucaPozicija = 0b10000000
tornjevi = 0b00001111

def Distanca(a,b):
    aX,aY = a
    bX,bY = b
    return  floor(sqrt((aX-bX)**2 + (aY-bY)**2))

def ObrisiMoguce(t):
    for iRed, red in enumerate(t):
        for iKol, kol in enumerate(red):
            t[iRed][iKol] = t[iRed][iKol] & ~mogucaPozicija 


def IzracunajMoguce(x,y,kretanje,t):
    ObrisiMoguce(t) 
    moguca = []
    
    if t[y][x] & toranj3 and kretanje: #kraj igre
        return []
    for red in range (-1,2,1):
        for kol in range(-1,2,1):
            if x+kol<0 or y+red<0 or x+kol>=len(t[y]) or y+red >= len(t):
                continue
            if not (t[int(y+red)][int(x+kol)] & igrac1 | t[int(y+red)][int(x+kol)] & igrac2 | t[int(y+red)][int(x+kol)] & kupola):
                if kretanje:
                    if ((t[y][x] & nemaTornja) and (t[y+red][x+kol] & nemaTornja)) or ((t[y][x] & nemaTornja) and (t[y+red][x+kol] & toranj1)) or (t[y+red][x+kol] & nemaTornja):
                        t[y+red][x+kol] = t[y+red][x+kol] | mogucaPozicija
                        moguca.append((y+red,x+kol))
                    elif ((t[y][x] & toranj1) and (t[y+red][x+kol] & toranj1)) or ((t[y][x] & toranj1) and (t[y+red][x+kol] & toranj2)):
                        t[y+red][x+kol] = t[y+red][x+kol] | mogucaPozicija
                        moguca.append((y+red,x+kol))
                    elif ((t[y][x] & toranj2) and (t[y+red][x+kol] & toranj2)) or ((t[y][x] & toranj2) and (t[y+red][x+kol] & toranj3)) or ((t[y][x] & toranj2) and (t[y+red][x+kol] & toranj1)):
                        t[y+red][x+kol] = t[y+red][x+kol] | mogucaPozicija
                        moguca.append((y+red,x+kol))
                else:
                    t[y+red][x+kol] = t[y+red][x+kol] | mogucaPozicija
                    moguca.append((y+red,x+kol))
    return moguca

algoritamPozicije = {20:[],10:[],0:[]} #recnik za postavljanje figura, sadrzi vrednost i listu pozicija sa tom vrednoscu

#Algoritam za postavljanje figura. Obilazi tablu i trazi figuru protivnika i daje vrednosti:
#20 - za polja izmedju dve protivnicke figure
#10 - za polja pored samo jedne figure
# 0 - sva ostala polja - koja nisu susedi protivnickih figura 
def PostavljanjeAlgo(tablaZaAlgoritam):
    global algoriotamPozicije
    for iRed, redT in enumerate(tablaZaAlgoritam):
        for iKol, kolT in enumerate(tablaZaAlgoritam):
            if tablaZaAlgoritam[iRed][iKol] == -1: #ako je na toj poziciji -1 znaci da je tu figurica suprotnog igraca 
                for red in range (-1,2,1): #obidji oko tog igraca sva polja
                    for kol in range(-1,2,1):
                        if iKol+kol<0 or iRed+red<0 or iKol+kol>=len(tablaZaAlgoritam[iRed]) or iRed+red >= len(tablaZaAlgoritam):
                            continue # za sva polja izvan granica table (nepostojece koordinate)
                        if tablaZaAlgoritam[iRed+red][iKol+kol] == 10: # ukoliko je vrednost vec 10 znaci da je to polje izmedju dve protivnicke figure i njima ce dodeliti vrednost 20
                            tablaZaAlgoritam[iRed+red][iKol+kol] = 20
                            algoritamPozicije[20].append((iRed+red, iKol+kol)) 
                        elif tablaZaAlgoritam[iRed+red][iKol+kol] == 0: # za prvu figuru ce biti sva polja 0 i njima ce dati vrednosti 10, za drugu figuru isto
                            tablaZaAlgoritam[iRed+red][iKol+kol] = 10
                            algoritamPozicije[10].append((iRed+red, iKol+kol))
