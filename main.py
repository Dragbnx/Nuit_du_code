import pyxel


BLOC = 8



class App:
    def __init__(self):
        self.w = 128
        self.h = 128
        pyxel.init(self.w, self.h, title="Nuit du Code")
        self.salle1 = Salle()
        pyxel.run(self.update, self.draw)


    def update(self):
        pass



    def draw(self):
        pyxel.cls(0)
        self.salle1.affiche()






class Salle:
    def __init__(self):
        self.salle = [[7 for i in range(128//BLOC)] for j in range(128//BLOC)]
        self.genere_salle()




    def genere_salle(self):
        motif_salle = pyxel.rndi(1, 2)
        porte1, porte2, porte3, porte4 = True, True, True, True
        if 1 == motif_salle:
            for i in range(16):
                for j in range(16):
                    choix = pyxel.rndi(0,1)
                    if i == 0 or j == 0 or i == (128//BLOC)-1 or j == (128//BLOC)-1:
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
        if 2 == motif_salle:
            for i in range(128 // BLOC):
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
        for i in range(15):
            self.salle[pyxel.rndi(0, 15)][pyxel.rndi(0, 15)] = 0


    def affiche(self):
        for i in range(len(self.salle)):
            for j in range(len(self.salle[i])):
                pyxel.rect(j*8, i*8, 8, 8, self.salle[i][j])



    


App()
