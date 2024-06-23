import pyxel

BLOC = 8
HAUT, BAS, GAUCHE, DROITE = (0, -BLOC), (0, BLOC), (-BLOC, 0), (BLOC, 0)
DIRECTION = [HAUT, BAS, GAUCHE, DROITE]
MOUVEMENT = {pyxel.KEY_Z: HAUT,
             pyxel.KEY_S: BAS,
             pyxel.KEY_Q: GAUCHE,
             pyxel.KEY_D: DROITE}


class App:
    def __init__(self):
        self.w = 128
        self.h = 128
        self.win = False
        pyxel.init(self.w, self.h, title="Nuit du Code")
        self.salle = [Salle(['h', 'b', 'd'], -1)]
        self.actu = 0
        pyxel.load('my_resource.pyxres')
        pyxel.playm(0, loop = True)
        self.perso = Perso()
        pyxel.run(self.update, self.draw)

    def mvt(self, direction):
        x, y = direction
        d = {HAUT:'h',
             BAS: 'b',
             DROITE:'d',
             GAUCHE:'g'}
        if self.salle[self.actu].est_sol((self.perso.y + y) // 8, (self.perso.x + x) // 8):
            self.perso.x, self.perso.y = self.perso.x + x, self.perso.y + y
            if y > 0:    # on verifie si l'avatar monte ou descends (face ou dos au joueur)
                self.perso.ligne=2
            else:
                self.perso.ligne=3
            if not x==0 and x>0 :
                self.perso.ligne=4
            elif not x==0 and x<0:
                self.perso.ligne=5
            self.perso.colonne= (self.perso.colonne+1)%3
        elif self.salle[self.actu].est_porte((self.perso.y + y) // 8, (self.perso.x + x) // 8):
            if d[direction] == self.salle[self.actu].porte_avant_num:
                if direction == HAUT:
                    self.perso.y = 112
                elif direction == BAS:
                    self.perso.y = 8
                elif direction == GAUCHE:
                    self.perso.x = 112
                elif direction == DROITE:
                    self.perso.x = 8
                self.actu -= 1
            elif direction == HAUT:
                self.perso.y = 112
                if self.actu > 10:
                    self.salle.append(Salle(['f', 'f', 'f'], 'b'))
                else:
                    self.salle.append(Salle(['h', 'g', 'd'], 'b'))
                self.actu += 1
            elif direction == BAS:
                self.perso.y = 8
                if self.actu > 10:
                    self.salle.append(Salle(['f', 'f', 'f'], 'h'))
                else:
                    self.salle.append(Salle(['b', 'g', 'd'], 'h'))
                self.actu += 1
            elif direction == GAUCHE:
                self.perso.x = 112
                if self.actu > 10:
                    self.salle.append(Salle(['f', 'f', 'f'], 'd'))
                else:
                    self.salle.append(Salle(['h', 'g', 'b'], 'd'))
                self.actu += 1
            elif direction == DROITE:
                self.perso.x = 8
                if self.actu > 10:
                    self.salle.append(Salle(['f', 'f', 'f'], 'g'))
                else:
                    self.salle.append(Salle(['h', 'b', 'd'], 'g'))
                self.actu += 1

    def deplacement(self):
        for cle in MOUVEMENT:
            if pyxel.btn(cle):
                self.mvt(MOUVEMENT[cle])

    def mort(self):
        for monstre in self.salle[self.actu].monstre:
            x, y = monstre.x, monstre.y
            xp, yp = self.perso.x, self.perso.y
            if xp == x and yp == y:
                self.perso.vie = False
                pyxel.playm(1)

    def update(self):
        self.deplacement()
        self.salle[self.actu].update()
        #self.mort()
        if self.actu > 10:
            self.win = True

    def draw(self):
        pyxel.cls(0)
        self.salle[self.actu].affiche()
        self.perso.affiche()
        if self.win:
            pyxel.text(10, 64, "YOU'VE GOT THE COOKIE ! :D", 0)



class Salle:
    def __init__(self, porte, num):
        self.salle = [[7 for i in range(128 // BLOC)] for j in range(128 // BLOC)]
        self.monstre = []
        self.poss_porte = porte
        self.porte_avant_num = num
        self.nb_monstre = 6
        self.texture = {0: (0, 0),
                        4: (24, 32),
                        7: (32, 0),
                        8: (0, 8),
                        14: (16, 0),
                        15: (24, 8)}
        self.genere_salle()

    def genere_salle(self):
        porte = True
        if self.porte_avant_num != -1:
            porte_avant = True
        else:
            porte_avant = False
        n_porte = self.poss_porte[pyxel.rndi(0, 2)]
        for i in range(16):
            ligne = False
            for j in range(16):
                choix = pyxel.rndi(0, 1)
                choix2 = pyxel.rndi(0, 10)
                if i == 0 or j == 0 or i == (128 // BLOC) - 1 or j == (128 // BLOC) - 1:
                    self.salle[i][j] = 0
                if i == 0 and (porte or porte_avant) and j == 7 and (
                        n_porte == 'h' or self.porte_avant_num == 'h'):
                    self.salle[i][j] = 8
                    porte = False
                if i == 15 and (porte or porte_avant) and j == 7 and (
                        n_porte == 'b' or self.porte_avant_num == 'b'):
                    self.salle[i][j] = 8
                    porte = False
                if j == 0 and (porte or porte_avant) and i == 7 and (
                        n_porte == 'g' or self.porte_avant_num == 'g'):
                    self.salle[i][j] = 8
                    porte = False
                if j == 15 and (porte or porte_avant) and i == 7 and (
                        n_porte == 'd' or self.porte_avant_num == 'd'):
                    self.salle[i][j] = 8
                    porte = False
                if 2 <= i <= 14 and 2 <= j <= 14 and choix2 == 0 and self.nb_monstre > 0 and not ligne:
                    self.monstre.append(Monstre(i * 8, j * 8))
                    self.nb_monstre -= 1
                    ligne = True
        for i in range(15):
            x = [pyxel.rndi(0, 6), pyxel.rndi(8, 15)]
            y = [pyxel.rndi(0, 6), pyxel.rndi(8, 15)]
            if n_porte == 'f':
                self.salle[8][8] = 4
            else:
                self.salle[x[pyxel.rndi(0, 1)]][y[pyxel.rndi(0, 1)]] = [14,15][pyxel.rndi(0, 1)]

    def est_sol(self, x, y):
        return self.salle[x][y] == 7

    def est_porte(self, x, y):
        return self.salle[x][y] == 8

    def mvt(self, monstre, direction):
        x, y = direction
        if self.est_sol((monstre.y + y) // 8, (monstre.x + x) // 8):
            monstre.x, monstre.y = monstre.x + x, monstre.y + y

    def update(self):
        for monstre in self.monstre:
            monstre.choix()
            if monstre.peut_deplace == 8:
                self.mvt(monstre, monstre.direction)
                monstre.peut_deplace = 0
            else:
                monstre.peut_deplace += 1

    def affiche(self):
        for i in range(len(self.salle)):
            for j in range(len(self.salle[i])):
                u, v = self.texture[self.salle[i][j]]
                pyxel.blt(j*8, i*8, 0, u, v, 8, 8)
        for monstre in self.monstre:
            monstre.affiche()


class Perso:
    def __init__(self):
        self.x = 8
        self.y = 8
        self.vie = True
        self.ligne = 2
        self.colonne = 0
        self.neg = 8

    def affiche(self):
        if self.vie:
            pyxel.blt(self.x, self.y, 0, (self.colonne) * 8, (self.ligne) * 8, self.neg, self.neg, 0)

class Monstre:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.peut_deplace = 8
        self.direction = ''
        self.cycle = 0
        self.type = pyxel.rndi(0, 2)
        self.bestiaire = {0: 6, 1: 7, 2: 8}  # 0,blob1; 1,blob2; 2,blob3.
        self.ligne = self.bestiaire[self.type]
        self.colonne = 0

    def choix(self):
        if self.cycle == 0:
            deplacement = pyxel.rndi(0, 3)
            self.direction = DIRECTION[deplacement]
            self.cycle = 4
        else:
            self.cycle -= 1

    def affiche(self):
        self.colonne = (self.colonne + 1) % 2
        pyxel.blt(self.x, self.y, 0, (self.colonne) * 8, (self.ligne) * 8, 8, 8, 0)

App()
