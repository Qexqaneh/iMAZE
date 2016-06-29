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
import time

PATH = 0
WALL = 1
START = 2
FINISH = 3
VISITED = 4
LOWEST_COST = 10
LEFT = "left"
RIGHT = "right"
UP = "up"
DOWN = "down"
WIN = "win!"
FAIL = "epic fail"

def InitializeMaze():
    #"""lecture csv et initialisation labyrinthe"""
	maze = []
	fileName = raw_input("please enter the file name:")
	with open('mazes/'+fileName+'.csv', 'rb') as csvfile:
	    data = csv.reader(csvfile, delimiter=';')
	    for row in data:
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
	# il suffit de supprimer cette ligne pour que le programme ne s'arrete que lorsque la sortie aura ete trouvee, mais en passant eventuellement plusieurs fois par le meme point
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

def DoDijkstra(maze, start, finish):
	# structure de allCosts : tableau a deux dimensions
	# chaque tableau a l'interieur de allCosts possede 3 valeurs : coordonnee x, coordonnee y, cout de la case
	allCosts = []
	startWithCost = list(start)
	startWithCost.append(LOWEST_COST)
	allCosts.append(startWithCost)

	iteration = 0
	exitFound = False

	while not exitFound:
		exitFound = SearchForNeighbours(maze, allCosts, iteration)
		iteration += 1

def DoReverseTravel(maze, start, finish):
	"""execute le chemin inverse, de l'arrivee au depart, grace aux couts, et renvoie un tableau avec les mouvements a effectuer pour sortir du labyrinthe"""
	currentPosition = list(finish)
	result = []

	while maze[currentPosition[0]][currentPosition[1]] != START:
		#insert pour ajouter au debut de la liste, vu que le chemin sera inverse
		result.insert(0, ChooseTheLowestCost(maze, currentPosition))

	result.append(WIN)

	return result

def ChooseTheLowestCost(maze, currentPosition):
	"""cherche la case voisine avec le cout le moins eleve, l'affecte a currentPosition et renvoie le deplacement inverse necessaire"""
	x = currentPosition[0]
	y = currentPosition[1]
	# tableau a deux dimensions, avec pour chaque tableau :
	# coordonnee x, coordonnee y, cout, mouvement inverse
	possibilities = []

	#test
	#print maze[currentPosition[0]][currentPosition[1]]

	# on regarde en haut
	if x > 0:
		if maze[x - 1][y] >= LOWEST_COST:
			# deplacements inverses car on va de l'arrivee vers le depart
			cost = maze[x - 1][y]
			goDown = [x - 1, y, cost, DOWN]
			possibilities.append(goDown)
		if maze[x - 1][y] == START:
			currentPosition[0] = x - 1
			return DOWN

	# on regarde en bas
	if x < len(maze) - 1:
		if maze[x + 1][y] >= LOWEST_COST:
			cost = maze[x + 1][y]
			goUp = [x + 1, y, cost, UP]
			possibilities.append(goUp)
		if maze[x + 1][y] == START:
			currentPosition[0] = x + 1
			return UP

	# on regarde a gauche
	if y > 0:
		if maze[x][y - 1] >= LOWEST_COST:
			cost = maze[x][y - 1]
			goRight = [x, y - 1, cost, RIGHT]
			possibilities.append(goRight)
		if maze[x][y - 1] == START:
			currentPosition[1] = y - 1
			return RIGHT

	# on regarde a droite
	if y < len(maze[0]) - 1:
		if maze[x][y + 1] >= LOWEST_COST:
			cost = maze[x][y + 1]
			goLeft = [x, y + 1, cost, LEFT]
			possibilities.append(goLeft)
		if maze[x][y + 1] == START:
			currentPosition[1] = y + 1
			return LEFT

	#test
	#print possibilities

	currentPosition[0] = possibilities[0][0]
	currentPosition[1] = possibilities[0][1]
	lowestCost = possibilities[0][2]
	move = possibilities[0][3]

	for i in range(1, len(possibilities)):
		if possibilities[i][2] < lowestCost:
			currentPosition[0] = possibilities[i][0]
			currentPosition[1] = possibilities[i][1]
			move = possibilities[i][3]

	#test
	#print move
	#time.sleep(1)

	return move

def SearchForNeighbours(maze, allCosts, iteration):
	"""ajoute dans allCosts tous les voisins de l'iteration actuelle disponibles, avec un cout superieur, et renvoie True si l'arrivee en fait partie"""
	x = allCosts[iteration][0]
	y = allCosts[iteration][1]
	newCost = allCosts[iteration][2] + 1

	# on regarde en haut
	if x > 0:
		if maze[x - 1][y] == FINISH:
			return True
		elif maze[x - 1][y] == PATH and IsNotAlreadyInTheList(allCosts, x - 1, y, newCost):
			allCosts.append([x - 1, y, newCost])
			maze[x - 1][y] = newCost

	# on regarde en bas
	if x < len(maze) - 1:
		if maze[x + 1][y] == FINISH:
			return True
		if maze[x + 1][y] == PATH and IsNotAlreadyInTheList(allCosts, x + 1, y, newCost):
			allCosts.append([x + 1, y, newCost])
			maze[x + 1][y] = newCost

	# on regarde a gauche
	if y > 0:
		if maze[x][y - 1] == FINISH:
			return True
		if maze[x][y - 1] == PATH and IsNotAlreadyInTheList(allCosts, x, y - 1, newCost):
			allCosts.append([x, y - 1, newCost])
			maze[x][y - 1] = newCost

	# on regarde a droite
	if y < len(maze[0]) - 1:
		if maze[x][y + 1] == FINISH:
			return True
	 	if maze[x][y + 1] == PATH and IsNotAlreadyInTheList(allCosts, x, y + 1, newCost):
			allCosts.append([x, y + 1, newCost])
			maze[x][y + 1] = newCost

	return False

def IsNotAlreadyInTheList(allCosts, x, y, newCost):
	"""compare les nouvelles valeurs avec celles deja presentes dans allCosts, et renvoie False si un cas est deja existant et moins couteux, sinon renvoie True"""
	for i in range(len(allCosts)):
		if allCosts[i][0] == x and allCosts[i][1] == y and allCosts[i][2] < newCost:
			# cas deja existant, et avec un cout inferieur, donc inutile de traiter ce nouveau cas
			return False
	# si rien n'a ete trouve, alors ce n'est effectivement pas deja dans la liste
	return True

# MAIN
maze = InitializeMaze()
start = Find(maze, START)
finish = Find(maze, FINISH)
DoDijkstra(maze, start, finish)
#for i in range(len(maze)):
#	print maze[i]
print DoReverseTravel(maze, start, finish)

#ancienne methode
#print GetOutOfHere(maze, start, finish)