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
		else:
			lowestCost = lastCost

		iteration += 1
		print iteration

		for i in range(len(finalMaze)):
			for j in range(len(finalMaze[0])):
				if finalMaze[i][j] == VISITED:
					finalMaze[i][j] = 0
		for i in range(len(entirePath) - 1): # on n'ecrase pas la case ARRIVEE
				finalMaze[entirePath[i][X]][entirePath[i][Y]] = VISITED

		with open('output/rightHand' + str(iteration) + '.csv', 'wb') as exitFile:
		    csv_writer = csv.writer(exitFile, delimiter=';')
		    csv_writer.writerows(finalMaze)

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

# MAIN
maze = InitializeMaze()
finalMaze = InitializeMaze()
start = Find(maze, START)
#finish = Find(maze, FINISH)
SearchForBestPath(maze, finalMaze, start)

with open('output/rightHand.csv', 'wb') as exitFile:
    csv_writer = csv.writer(exitFile, delimiter=';')
    csv_writer.writerows(finalMaze)