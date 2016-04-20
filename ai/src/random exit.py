#evaluation du score :
#- premiere phase : totalement aleatoire (impossible d'evaluer le score si arrivee non atteinte)
#- deuxieme phase : nombre de deplacements necessaires le moins eleve
#
#particularites :
#- ne peut pas faire demi-tour
#- Nao sait ou se trouve l'arrivee => possibilite d'utiliser l'algorithme a-star
#
#chromosomes = choix successifs des deplacements (de 1 a 4)

import csv
import random

PATH = 0
WALL = 1
START = 2
FINISH = 3
VISITED = 4
LEFT = "left"
RIGHT = "right"
UP = "up"
DOWN = "down"
WIN = "win!"
FAIL = "epic fail"

def InitializeMaze():
    #"""lecture csv et initialisation labyrinthe"""
	maze = []
	with open('maze1.csv', 'rb') as csvfile:
	    data = csv.reader(csvfile, delimiter=';')
	    for row in data:
	        print row
	        rowMaze = []
	        for cell in row:
	        	rowMaze.append(int(cell))
	    	maze.append(rowMaze)
	return maze

def Find(maze, value):
	"""trouve une valeur dans le labyrinthe (depart ou arrivee)"""
	coordonates = []
	for row in range(len(maze)):
		for cell in range(len(maze[0])):
			if maze[row][cell] == value:
				coordonates = [row, cell]
				break
	return coordonates

def GetOutOfHere(maze, start, finish):
	"""essaye de sortir du labyrinthe et renvoie le resultat"""
	currentPosition = list(start) # on cree une copie du start pour s'assurer de ne pas le modifier
	possibilities = []
	result = ["let's go"]
	end = False

	while not end:
		# on regarde les pssibilites
		possibilities = LookAround(maze, currentPosition)

		# cas sans issue
		if possibilities[0] == FAIL:
			result.append(FAIL)
			break

		# on choisit une direction
		result.append(ChooseYourWay(maze, possibilities, currentPosition))

		# on verifie si on est arrive
		if maze[currentPosition[0]][currentPosition[1]] == FINISH:
			result.append(WIN)
			end = True

	return result

def LookAround(maze, coordonates):
	"""regarde les issues possibles et les renvoie sous forme de tableau"""
	possibilities = []

	# on regarde en haut
	if (coordonates[0] > 0) and (maze[coordonates[0] - 1][coordonates[1]] == PATH or maze[coordonates[0] - 1][coordonates[1]] == FINISH):
		possibilities.append(UP)

	# on regarde en bas
	if (coordonates[0] < len(maze) - 1) and (maze[coordonates[0] + 1][coordonates[1]] == PATH or maze[coordonates[0] + 1][coordonates[1]] == FINISH):
		possibilities.append(DOWN)

	# on regarde a gauche
	if (coordonates[1] > 0) and (maze[coordonates[0]][coordonates[1] - 1] == PATH or maze[coordonates[0]][coordonates[1] - 1] == FINISH):
		possibilities.append(LEFT)

	# on regarde a droite
	if (coordonates[1] < len(maze[0]) - 1) and (maze[coordonates[0]][coordonates[1] + 1] == PATH or maze[coordonates[0]][coordonates[1] + 1] == FINISH):
		possibilities.append(RIGHT)

	# si aucune issue, c'est la mer noire
	if len(possibilities) == 0: 
		possibilities.append(FAIL)

	return possibilities

def ChooseYourWay(maze, possibilities, currentPosition):
	"""choisit une destination parmi la liste des possibles, aleatoirement, et modifie la position actuelle"""
	newDirection = possibilities[random.randint(0, len(possibilities) - 1)]

	# on indique que la case a deja ete visitee
	# il suffit de supprimer cette ligne pour que le programme ne s'arrete que lorsque la sortie aura ete trouvee, mais en passant éventuellement plusieurs fois par le meme point
	maze[currentPosition[0]][currentPosition[1]] = VISITED

	# modification de la position
	if newDirection == UP:
		currentPosition[0] -= 1
	elif newDirection == DOWN:
		currentPosition[0] += 1
	elif newDirection == LEFT:
		currentPosition[1] -= 1
	elif newDirection == RIGHT:
		currentPosition[1] += 1

	# on renvoie la direction
	return newDirection

# MAIN
maze = InitializeMaze()
start = Find(maze, START)
finish = Find(maze, FINISH)
print GetOutOfHere(maze, start, finish)