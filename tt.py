import random

WIDTH = 100
HEIGHT = 15

matrix = [['x' for y in range(WIDTH)] for l in range(HEIGHT)]
points = [ (random.randint(0, len(matrix)-1), random.randint(0, len(matrix[0])-1)) ]
matrix[points[0][0]][points[0][1]] = ' '

DIRECTIONS = ((0, 2), (2, 0), (-2, 0), (0, -2))

T=10

while points:
	xc,yc = points.pop(random.randint(0, len(points)-1))
	change = True

	for i, j in DIRECTIONS:
		if xc+i >=0 and xc+i < len(matrix) and yc+j >= 0 and yc+j < len(matrix[0]):
			if matrix[xc+i][yc+j] == ' ' :
				if change:
					if (xc+i, yc+j) not in points:
						if  matrix[xc+i//2][yc+j//2] != ' ':
							matrix[xc+i//2][yc+j//2] = ' '
							change = False
			else:
				if (xc+i, yc+j):
					points.append((xc+i, yc+j))
					matrix[xc+i][yc+j] = ' '

while T:	
	j = random.randint(0, len(matrix)-1)
	i = random.randint(0, len(matrix[0])-1)
	if (matrix[j][i] == 'x') and j >=1 and i >=1:

		try:
			if matrix[j-1][i] and matrix[j+1][i] == ' ':
				T-=1
				matrix[j][i] = ' '
		except: pass
		try:
			if matrix[j][i-1] and matrix[j][i+1] == ' ':
				T-=1
				matrix[j][i] = ' '
		except: pass





[print(*i) for i in matrix]





