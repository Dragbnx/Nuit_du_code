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
        pyxel.init(self.w, self.h, title="Nuit du Code")
        self.salle1 = Salle(1)
        self.perso = Perso()
        pyxel.run(self.update, self.draw)

    def mvt(self, direction):
        x, y = direction
        if self.salle1.est_sol((self.perso.y + y) // 8, (self.perso.x + x) // 8):
            self.perso.x, self.perso.y = self.perso.x + x, self.perso.y + y

    def deplacement(self):
        for cle in MOUVEMENT:
            if pyxel.btn(cle):
                self.mvt(MOUVEMENT[cle])



    def mvt_monstre(self, direction):
        x, y = direction
        if self.salle1.est_sol((self.salle1.y + y) // 8, (self.perso.x + x) // 8):
            self.perso.x, self.perso.y = self.perso.x + x, self.perso.y + y



    def mort(self):
        for monstre in self.salle1.monstre:
            x, y = monstre.x, monstre.y
            xp, yp = self.perso.x, self.perso.y
            if xp == x and yp == y:
                self.perso.vie = False

    def update(self):
        self.deplacement()
        self.salle1.update()
        self.mort()

    def draw(self):
        pyxel.cls(0)
        self.salle1.affiche()
        self.perso.affiche()


class Salle:
    def __init__(self, type):
        self.type = type
        self.salle = [[7 for i in range(128 // BLOC)] for j in range(128 // BLOC)]
        self.monstre = []
        self.nb_monstre = 6 if type == 1 else 2
        self.genere_salle()

    def genere_salle(self):
        motif_salle = self.type
        porte1, porte2, porte3, porte4 = True, True, True, True
        if 1 == motif_salle:
            for i in range(16):
                ligne = False
                for j in range(16):
                    choix = pyxel.rndi(0, 1)
                    choix2 = pyxel.rndi(0, 10)
                    if i == 0 or j == 0 or i == (128 // BLOC) - 1 or j == (128 // BLOC) - 1:
                        self.salle[i][j] = 0
                    if i == 0 and choix == 1 and porte1 and j != 0 and j != 15:
                        self.salle[i][j] = 8
                        porte1 = False
                    if i == 15 and choix == 1 and porte2 and j != 0 and j != 15:
                        self.salle[i][j] = 8
                        porte2 = False
                    if j == 0 and choix == 1 and porte3 and i != 0 and i != 15:
                        self.salle[i][j] = 8
                        porte3 = False
                    if j == 15 and choix == 1 and porte4 and i != 0 and i != 15:
                        self.salle[i][j] = 8
                        porte4 = False
                    if 2 <= i <= 14 and 2 <= j <= 14 and choix2 == 0 and self.nb_monstre > 0 and not ligne:
                        self.monstre.append(Monstre(i*8, j*8))
                        self.nb_monstre -= 1
                        ligne = True
        if 2 == motif_salle:
            for i in range(128 // BLOC):
                ligne = False
                for j in range(128 // BLOC):
                    choix = pyxel.rndi(0, 1)
                    if i <= 0 or j <= 3 or i >= (128 // BLOC) - 1 or j >= (128 // BLOC) - 4:
                        self.salle[i][j] = 0
                    if i == 0 and choix == 1 and porte1 and 4 <= j <= 11:
                        self.salle[i][j] = 8
                        porte1 = False
                    if i == 15 and choix == 1 and porte2 and 4 <= j <= 11:
                        self.salle[i][j] = 8
                        porte2 = False
                    if j == 3 and choix == 1 and porte3 and i != 0 and i != 15:
                        self.salle[i][j] = 8
                        porte3 = False
                    if j == 12 and choix == 1 and porte4 and i != 0 and i != 15:
                        self.salle[i][j] = 8
                        porte4 = False
                    if 2 <= i <= 14 and 4 <= j <= 11 and choix2 == 0 and self.nb_monstre > 0 and not ligne:
                        self.monstre.append(Monstre(i*8, j*8))
                        self.nb_monstre -= 1
                        ligne = True
        for i in range(15):
            self.salle[pyxel.rndi(0, 15)][pyxel.rndi(0, 15)] = 0

    def est_sol(self, x, y):
        return self.salle[x][y] == 7


    def mvt(self,monstre, direction):
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
                pyxel.rect(j * 8, i * 8, 8, 8, self.salle[i][j])
        for monstre in self.monstre:
            monstre.affiche()



class Perso:
    def __init__(self):
        self.x = 8
        self.y = 8
        self.vie = True

    def affiche(self):
        if self.vie:
            pyxel.rect(self.x, self.y, 8, 8, 11)


class Monstre:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.peut_deplace = 4
        self.direction = ''
        self.cycle = 0

    def choix(self):
        if self.cycle == 0:
            deplacement = pyxel.rndi(0, 3)
            self.direction = DIRECTION[deplacement]
            self.cycle = 4
        else:
            self.cycle -= 1


    def affiche(self):
        pyxel.rect(self.x, self.y, 8, 8, 10)



App()
