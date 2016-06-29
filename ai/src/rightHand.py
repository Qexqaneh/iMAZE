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

PATH = 10
WALL = 1
START = 2
FINISH = 3
VISITED = 4
LEFT = 2
RIGHT = 0
UP = 1
DOWN = 3
WIN = "win!"
FAIL = "epic fail"
X = 0
Y = 1
PHEROMONE = 2
DIRECTION = 3

fileName = None

def InitializeMaze():
    #"""lecture csv et initialisation labyrinthe"""
	maze = []
	global fileName

	if fileName == None:
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

def DoDijkstra(maze, start, finish):
	# structure de allcosts : tableau a deux dimensions
	# chaque tableau a l'interieur de allcosts possede 3 valeurs : coordonnee x, coordonnee y, cout de la case
	allcosts = []
	startWithCost = list(start)
	startWithCost.append(0)
	allcosts.append(startWithCost)

	iteration = 0
	exitFound = False

	while not exitFound:
		exitFound = SearchForNeighbours(maze, allcosts, iteration)
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
	print maze[currentPosition[0]][currentPosition[1]]

	# on regarde en haut
	if x > 0:
		if maze[x - 1][y] > 0:
			# deplacements inverses car on va de l'arrivee vers le depart
			cost = maze[x - 1][y]
			goDown = [x - 1, y, cost, DOWN]
			possibilities.append(goDown)
		if maze[x - 1][y] == START:
			currentPosition[0] = x - 1
			return DOWN

	# on regarde en bas
	if x < len(maze) - 1:
		if maze[x + 1][y] > 0:
			cost = maze[x + 1][y]
			goUp = [x + 1, y, cost, UP]
			possibilities.append(goUp)
		if maze[x + 1][y] == START:
			currentPosition[0] = x + 1
			return UP

	# on regarde a gauche
	if y > 0:
		if maze[x][y - 1] > 0:
			cost = maze[x][y - 1]
			goRight = [x, y - 1, cost, RIGHT]
			possibilities.append(goRight)
		if maze[x][y - 1] == START:
			currentPosition[1] = y - 1
			return RIGHT

	# on regarde a droite
	if y < len(maze[0]) - 1:
		if maze[x][y + 1] > 0:
			cost = maze[x][y + 1]
			goLeft = [x, y + 1, cost, LEFT]
			possibilities.append(goLeft)
		if maze[x][y + 1] == START:
			currentPosition[1] = y + 1
			return LEFT

	currentPosition[0] = possibilities[0][0]
	currentPosition[1] = possibilities[0][1]
	lowestCost = possibilities[0][2]
	move = possibilities[0][3]

	for i in range(1, len(possibilities) - 1):
		if possibilities[i][2] < lowestCost:
			currentPosition[0] = possibilities[i][0]
			currentPosition[1] = possibilities[i][1]
			move = possibilities[i][3]

	#test
	print move

	return move

def SearchForNeighbours(maze, allcosts, iteration):
	"""ajoute dans allcosts tous les voisins de l'iteration actuelle disponibles, avec un cout superieur, et renvoie True si l'arrivee en fait partie"""
	x = allcosts[iteration][0]
	y = allcosts[iteration][1]
	newCost = allcosts[iteration][2] + 1

	# on regarde en haut
	if x > 0:
		if maze[x - 1][y] == FINISH:
			return True
		elif maze[x - 1][y] == PATH and IsNotAlreadyInTheList(allcosts, x - 1, y, newCost):
			allcosts.append([x - 1, y, newCost])
			maze[x - 1][y] = newCost

	# on regarde en bas
	if x < len(maze) - 1:
		if maze[x + 1][y] == FINISH:
			return True
		if maze[x + 1][y] == PATH and IsNotAlreadyInTheList(allcosts, x + 1, y, newCost):
			allcosts.append([x + 1, y, newCost])
			maze[x + 1][y] = newCost

	# on regarde a gauche
	if y > 0:
		if maze[x][y - 1] == FINISH:
			return True
		if maze[x][y - 1] == PATH and IsNotAlreadyInTheList(allcosts, x, y - 1, newCost):
			allcosts.append([x, y - 1, newCost])
			maze[x][y - 1] = newCost

	# on regarde a droite
	if y < len(maze[0]) - 1:
		if maze[x][y + 1] == FINISH:
			return True
	 	if maze[x][y + 1] == PATH and IsNotAlreadyInTheList(allcosts, x, y + 1, newCost):
			allcosts.append([x, y + 1, newCost])
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

def SearchForBestPath(maze, finalMaze, start):
	temporaryMaze = list(maze)
	bestPathFound = False
	lowestCost = None
	iteration = 0

	for i in range(len(maze)):
		for j in range(len(maze[0])):
			if maze[i][j] == 0:
				maze[i][j] = PATH

	while not bestPathFound:
		entirePath = DoRightHand(temporaryMaze, start)
		lastCost = len(entirePath)

		# evaporation
		for i in range(len(maze)):
			for j in range(len(maze[0])):
				if (maze[i][j] == PATH + 1):
					maze[i][j] -= 1

		if (lowestCost != None) and (lowestCost == lastCost):
			bestPathFound = True

			for i in range(len(entirePath) - 1): # on n'ecrase pas la case ARRIVEE
				finalMaze[entirePath[i][X]][entirePath[i][Y]] = VISITED
		else:
			lowestCost = lastCost

		iteration += 1
		print iteration

def DoRightHand(temporaryMaze, start):
	currentPosition = [start[0], start[1], 0, None] # PHEROMONE = 0 au cas d'un retour a la case depart
	entirePath = []
	exitFound = False
	iteration = 0

	while not exitFound:
		bestSolution = [None, None, None, None]
		sortedPossiblePositions = []

		possiblePositions = FindPossiblePositions(temporaryMaze, currentPosition)

		if (currentPosition[DIRECTION] == RIGHT) or (currentPosition[DIRECTION] == None):
			if possiblePositions[DOWN][X] != None:
				sortedPossiblePositions.append(possiblePositions[DOWN])
			if possiblePositions[RIGHT][X] != None:
				sortedPossiblePositions.append(possiblePositions[RIGHT])
			if possiblePositions[UP][X] != None:
				sortedPossiblePositions.append(possiblePositions[UP])
			if possiblePositions[LEFT][X] != None:
				sortedPossiblePositions.append(possiblePositions[LEFT])
		elif currentPosition[DIRECTION] == UP:
			if possiblePositions[RIGHT][X] != None:
				sortedPossiblePositions.append(possiblePositions[RIGHT])
			if possiblePositions[UP][X] != None:
				sortedPossiblePositions.append(possiblePositions[UP])
			if possiblePositions[LEFT][X] != None:
				sortedPossiblePositions.append(possiblePositions[LEFT])
			if possiblePositions[DOWN][X] != None:
				sortedPossiblePositions.append(possiblePositions[DOWN])
		elif currentPosition[DIRECTION] == LEFT:
			if possiblePositions[UP][X] != None:
				sortedPossiblePositions.append(possiblePositions[UP])
			if possiblePositions[LEFT][X] != None:
				sortedPossiblePositions.append(possiblePositions[LEFT])
			if possiblePositions[DOWN][X] != None:
				sortedPossiblePositions.append(possiblePositions[DOWN])
			if possiblePositions[RIGHT][X] != None:
				sortedPossiblePositions.append(possiblePositions[RIGHT])
		elif currentPosition[DIRECTION] == DOWN:
			if possiblePositions[LEFT][X] != None:
				sortedPossiblePositions.append(possiblePositions[LEFT])
			if possiblePositions[DOWN][X] != None:
				sortedPossiblePositions.append(possiblePositions[DOWN])
			if possiblePositions[RIGHT][X] != None:
				sortedPossiblePositions.append(possiblePositions[RIGHT])
			if possiblePositions[UP][X] != None:
				sortedPossiblePositions.append(possiblePositions[UP])

		bestSolution = sortedPossiblePositions[0]

		if len(sortedPossiblePositions) > 1:
			for i in range(1, len(sortedPossiblePositions) - 1):
				if sortedPossiblePositions[i][PHEROMONE] < bestSolution[PHEROMONE]:
					bestSolution = sortedPossiblePositions[i]

		if bestSolution[X] == None:
			bestSolution = sortedPossiblePositions[len(sortedPossiblePositions)]

		currentPosition = bestSolution

		# on incremente les pheromones
		if currentPosition[PHEROMONE] != FINISH:
			temporaryMaze[currentPosition[X]][currentPosition[Y]] = currentPosition[PHEROMONE] + 1

		#print currentPosition

		if bestSolution[PHEROMONE] == FINISH:
			exitFound = True

		iteration += 1
		# print iteration

		entirePath.append([currentPosition[X], currentPosition[Y], currentPosition[DIRECTION]])
	return entirePath

def FindPossiblePositions(temporaryMaze, currentPosition):
	"""retourne un tableau avec 0=coordonneeXNouvellePosition, 1=coordonneeYNouvellePosition, 2=direction, 3=sortieTrouvee (0 ou 1)"""
	x = currentPosition[X]
	y = currentPosition[Y]
	possiblePositions = [[None for a in range(4)] for b in range(4)] 

	# on regarde a droite
	if (y < len(temporaryMaze[0]) - 1):
		if temporaryMaze[x][y + 1] == FINISH or temporaryMaze[x][y + 1] >= PATH:
			possiblePositions[RIGHT][X] = x
			possiblePositions[RIGHT][Y] = y + 1
			possiblePositions[RIGHT][PHEROMONE] = temporaryMaze[x][y + 1]
			possiblePositions[RIGHT][DIRECTION] = RIGHT

	# on regarde en haut
	if (x > 0):
		if temporaryMaze[x - 1][y] == FINISH or temporaryMaze[x - 1][y] >= PATH:
			possiblePositions[UP][X] = x - 1
			possiblePositions[UP][Y] = y
			possiblePositions[UP][PHEROMONE] = temporaryMaze[x - 1][y]
			possiblePositions[UP][DIRECTION] = UP

	# on regarde a gauche
	if (y > 0):
		if temporaryMaze[x][y - 1] == FINISH or temporaryMaze[x][y - 1] >= PATH:
			possiblePositions[LEFT][X] = x
			possiblePositions[LEFT][Y] = y - 1
			possiblePositions[LEFT][PHEROMONE] = temporaryMaze[x][y - 1]
			possiblePositions[LEFT][DIRECTION] = LEFT

	# on regarde en bas
	if (x < len(temporaryMaze) - 1):
		if temporaryMaze[x + 1][y] == FINISH or temporaryMaze[x + 1][y] >= PATH:
			possiblePositions[DOWN][X] = x + 1
			possiblePositions[DOWN][Y] = y
			possiblePositions[DOWN][PHEROMONE] = temporaryMaze[x + 1][y]
			possiblePositions[DOWN][DIRECTION] = DOWN

	return possiblePositions

# on part de la case depart
# on regarde les cases autour, on va sur la seule case PATH possible, on enregistre la direction du dernier mouvement
# tableau 0=droite 1=haut 2=gauche 3=bas
# tant que case actuelle != arrivee
#	verification dernierMouvement-1 = PATH, puis +0, +1, +2 (avec modulo 4) - 1
#		prendre la valeur la moins grande >= 0, si plusieurs valeurs la plus faible identiques => dans l'ordre croissant du tableau des mouvemments
# haut = -1/0
# bas = +1/0
# gauche = 0/-1
# droite = 0/+1
#
# on regarde a droite par rapport a la derniere direction
#	si direction = gauche : haut, gauche, bas

# MAIN
maze = InitializeMaze()
finalMaze = InitializeMaze()
start = Find(maze, START)
#finish = Find(maze, FINISH)
SearchForBestPath(maze, finalMaze, start)
#DoDijkstra(maze, start, finish)
#print DoReverseTravel(maze, start, finish)

with open('rightHand.csv', 'wb') as exitFile:
    csv_writer = csv.writer(exitFile, delimiter=';')
    csv_writer.writerows(finalMaze)