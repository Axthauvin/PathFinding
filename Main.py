from tkinter import *
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from playsound import playsound
import os
root = Tk()
rmatrix = [
  [1, 1, 1, 1, 1,"D"],
  [1, 0, 1, 0, 0, 0],
  [1, 1, 1, 1, 1, 1],
  [0, 0, 1, 0, 0, 1],
  [1, 1, 1, 1, 1, 1]
]
mmatrix = rmatrix
def FindWhatToSeen(what):
    """Permet de savoir quel est la couleur de l'objet à afficher sur Tkinter"""
    if what == 1:
        return "white"
    
    if what == "A":
        return "Green"
    if what == 0:
        return "grey"
    if what == "D":
        return "Red"
    if what == "P":
        return "Red"
    if what == "E":
        return "Yellow"
    if what >= 2:
        return "blue"
c = Canvas(root)
c.pack()
for i in range(0, len(rmatrix)):
        for j in range(0, len(rmatrix[i])):
            what = FindWhatToSeen(rmatrix[i][j])
            if what == "Red":
                mmatrix[i][j] = 1
                startr = [j, i]
                c.create_rectangle(j * 50, i * 50, j * 50 + 50, i * 50 + 50, fill = "White", outline = "black")
                Player = c.create_rectangle(j * 50, i * 50, j * 50 + 50, i * 50 + 50, fill = what, outline = "black")
            else:
                if what == "Yellow":
                    mmatrix[i][j] = 1
                    c.create_rectangle(j * 50, i * 50, j * 50 + 50, i * 50 + 50, fill = "White", outline = "black")
                    Ennemy = c.create_rectangle(j * 50, i * 50, j * 50 + 50, i * 50 + 50, fill = what, outline = "black", tags = "Ennemy")
                else:
                    if what == "Green":
                        mmatrix[i][j] = 1
                        endr = [j, i]
                        Arrive = c.create_rectangle(j * 50, i * 50, j * 50 + 50, i * 50 + 50, fill = what, outline = "black")
                    else:
                        if what != "Red":
                            c.create_rectangle(j * 50, i * 50, j * 50 + 50, i * 50 + 50, fill = what, outline = "black")
                    

                          
grid = Grid(matrix=mmatrix)
start = grid.node(startr[0], startr[1])
#end = grid.node(endr[0], endr[1])
                
               



t1 = Label(root, text = "Rouge = Joueur")
t1.pack()
t2 = Label(root, text = "Blanc = Sol")
t2.pack()
t3 = Label(root, text = "Gris = Mur")
t3.pack()

   


def MouvePlayer(event):
    global startr
    for i in range(0, len(mmatrix)):
        for j in range(0, len(mmatrix[i])):
            if mmatrix[i][j] == "P":
                mmatrix[i][j] = 1
                startr = [j, i]

                
    grid = Grid(matrix=mmatrix)
    start = grid.node(startr[0], startr[1])
    Targetx = event.x
    Targety = event.y
    #Arrondi le x du clic
    XChanged = str(Targetx)
    if Targetx >= 100:
        XChanged = XChanged[1] + XChanged[2]
    XChanged = int(XChanged)
    if XChanged >= 50:
        TargetxArrondi = Targetx + (50 - XChanged)
    else:
        TargetxArrondi = Targetx - XChanged

    #Arrondi le y du clic
    YChanged = str(Targety)
    if Targety >= 100:
        YChanged = YChanged[1] + YChanged[2]
    YChanged = int(YChanged)
    if YChanged >= 50:
        TargetyArrondi = Targety + (50 - YChanged)
    else:
        TargetyArrondi = Targety - YChanged
    #print(TargetyArrondi) : The coords of your click
    end = grid.node(int(TargetxArrondi / 50), int(TargetyArrondi / 50))
    finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
    path, runs = finder.find_path(start, end, grid)
    if len(path) == 0:
        print("C'est un cul de sac")
        #I tryed to play a song, but it doesn't work :/
        os.system('start Nope.mp3')
    else:
        PlayerPosition = startr
        #print(path) : Write the path the algorithm gonna use ! Pretty cool right ?
        Speed = 50
        for mouvement in range(0, len(path)):
            oldP = PlayerPosition
            thenext = path[mouvement]
            colorcase = FindWhatToSeen(mmatrix[thenext[1]][thenext[0]])
            oldcasePriority = mmatrix[thenext[1]][thenext[0]]
            PlayerPosition = path[mouvement]
            mmatrix[PlayerPosition[1]][PlayerPosition[0]] = "P"
            mmatrix[oldP[1]][oldP[0]] = oldcasePriority
            c.coords(Player, PlayerPosition[0] * 50, PlayerPosition[1] * 50, PlayerPosition[0] * 50 + 50, PlayerPosition[1] * 50 + 50)
            c.update()
            c.tag_raise(Player)
            Factor = 1
            if colorcase == "blue":
                Factor = oldcasePriority * 10
            c.after(Speed * Factor)
            #Change the speed with the Factor : In progress
    Grid.cleanup(grid)





c.bind('<Button-1>', MouvePlayer)
root.mainloop()
