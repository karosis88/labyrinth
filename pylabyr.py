import random
import pygame
import os
import time

from pygame.constants import MOUSEBUTTONDOWN

os.system('cls')
def msgtoclient(msg):
	print(msg)
	time.sleep(1)

while True:
	try:
		WIDTH = int(input('Number of rectangles on X axis (minimum 12)։ '))
		HEIGHT = int(input('Number of rectangles on Y axis (minimum 12)։ '))
		CELL_SIZE = int(input('Number of rectangle size in pixels (minimum 10)։ '))
		WIDTH = 89
		HEIGHT = 69
		CELL_SIZE = 10
		if WIDTH < 12 or HEIGHT < 12 or CELL_SIZE < 10:
			msgtoclient('Invalid Data')
			continue

		while CELL_SIZE%4 != 0:
			CELL_SIZE+=1

		break

	except ValueError:
		msgtoclient('Number should be integer not float')


T = (WIDTH+HEIGHT) // 2
WAYS = ( (1, 0), (0, 1), (-1, 0), (0, -1) )
BACKGROUND_COLOR = (60,54,79)

WALLS_COLOR = (243, 80, 46)
WALL_3D_COLOR = (141, 33, 10)
START_POINT_COLOR = (255, 195, 0)
END_POINT_COLOR = (39, 174, 96)
ROUTE_COLOR = (218, 247, 166)
screen = pygame.display.set_mode((WIDTH*CELL_SIZE, HEIGHT*CELL_SIZE))
rect_matrix = []
start_point = None
end_point = None
route = None
clock = pygame.time.Clock()
still_drawing = True
x_middle_off = CELL_SIZE/2-CELL_SIZE/8
y_middle_off= (CELL_SIZE-CELL_SIZE/3)/2+CELL_SIZE/3-CELL_SIZE/8
break_current = False


matrix = [['x' for y in range(WIDTH)] for l in range(HEIGHT)]

# points = [ (random.randint(0, len(matrix)-1), random.randint(0, len(matrix[0])-1)) ]
points = [(random.choice([i for i in range(1, HEIGHT, 2)]), random.choice([i for i in range(1, HEIGHT, 2)]))]
matrix[points[0][0]][points[0][1]] = ' '

DIRECTIONS = [(0, 2), (2, 0), (-2, 0), (0, -2)]


class Rect(pygame.Rect):
    def __init__(self, color=(0, 0, 0), *a, **k):
        super(Rect, self).__init__(*a, **k)
        self.color = color


while points:
	random.shuffle(DIRECTIONS)
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
    j = random.randint(0, len(matrix)-2)
    i = random.randint(0, len(matrix[0])-2)
    csum = (( (-1, 0), (1,0) ), ((0, -1), (0, 1)))
    if (matrix[j][i] == 'x') and j >= 1 and i >= 1:
        for k in range(len(csum)):
            ji, si = csum[k]
            if matrix[j+ji[0]][i+ji[1]] == ' ' and matrix[j+si[0]][i+si[1]] == ' ':
                matrix[j][i] = ' '
                T-=1

def bfslabr(q, endpoint):
    visited = set()

    while q:

        x, y, path = q.pop(0)
        if (x,y) in visited:
            continue
        visited.add((x,y))
        if (x,y) == endpoint:
            return path


        for i, j in WAYS:
            if x+i >= 0 and x+i < HEIGHT and j+y >=0 and j+y < WIDTH and matrix[x+i][y+j] == ' ':
                q.append((x+i, y+j, path+[(x+i, j+y)]))

while True:
	clock.tick(200)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()
		if event.type == pygame.MOUSEBUTTONDOWN:
			if matrix[event.pos[1]//CELL_SIZE][event.pos[0]//CELL_SIZE] == ' ':

				if event.button == 1:
					if (not end_point.collidepoint(event.pos) if end_point else True):
						start_point = Rect(START_POINT_COLOR, (event.pos[0]//CELL_SIZE)*CELL_SIZE + CELL_SIZE/8, (event.pos[1]//CELL_SIZE)*CELL_SIZE+CELL_SIZE/4 +2, CELL_SIZE-CELL_SIZE/4, CELL_SIZE-CELL_SIZE/4 - CELL_SIZE/12.5)
				elif event.button == 3:
					if (not start_point.collidepoint(event.pos) if start_point else True):
						end_point = Rect(END_POINT_COLOR, (event.pos[0]//CELL_SIZE)*CELL_SIZE + CELL_SIZE/8, (event.pos[1]//CELL_SIZE)*CELL_SIZE+CELL_SIZE/4 + 2, CELL_SIZE-CELL_SIZE/4, CELL_SIZE-CELL_SIZE/4 - CELL_SIZE/12.5)
				if start_point and end_point and event.button in (1, 3):
					still_drawing=True
					route = bfslabr([(start_point.y//CELL_SIZE, start_point.x//CELL_SIZE, [(start_point.y//CELL_SIZE, start_point.x//CELL_SIZE)])], (end_point.y//CELL_SIZE, end_point.x//CELL_SIZE))
			
	screen.fill(BACKGROUND_COLOR)

	for y, line in enumerate(matrix): 
		for x, cell in enumerate(line): 
			if cell == "x":
				pygame.draw.rect(screen, WALLS_COLOR, ((x)*CELL_SIZE, (y)*CELL_SIZE, CELL_SIZE, CELL_SIZE))
				if y+1 < HEIGHT and matrix[y+1][x] != 'x':
					pygame.draw.rect(screen, WALL_3D_COLOR, ((x)*CELL_SIZE, (y)*CELL_SIZE+3*CELL_SIZE/3, CELL_SIZE, CELL_SIZE/3)) 

	if start_point:
		pygame.draw.rect(screen, start_point.color, start_point)
	if end_point:
		pygame.draw.rect(screen, end_point.color, end_point)

	if route:
		for i in range(1, len(route)-1):
			for event in pygame.event.get():
				pygame.event.post(event)
				if event.type == pygame.QUIT:
					break
				if event.type == pygame.MOUSEBUTTONDOWN:
					if matrix[event.pos[1]//CELL_SIZE][event.pos[0]//CELL_SIZE] == ' ' and event.button in (1, 3):
						route = []
						break

			else:
				cur_x, cur_y = route[i][1]*CELL_SIZE, route[i][0]*CELL_SIZE
				if route[i-1][0] != route[i+1][0] and route[i-1][1] != route[i+1][1]:

					pygame.draw.rect(screen, ROUTE_COLOR, ((cur_x + (x_middle_off*(1 if route[i][0] == route[i+1][0] and route[i-1][1]<route[i+1][1] else -1)* \
					(-1 if route[i-1][1] > route[i+1][1] and route[i][1] == route[i+1][1] else 1))), cur_y+y_middle_off, CELL_SIZE, CELL_SIZE/4))
					
					pygame.draw.rect(screen, ROUTE_COLOR, (cur_x + x_middle_off ,(cur_y + (y_middle_off*(1 if route[i][1] == route[i+1][1] and route[i-1][0]>route[i+1][0] else -1)* \
					(1 if route[i-1][0] < route[i+1][0] and route[i][0] == route[i+1][0] else -1)))+CELL_SIZE/7.66666666667, CELL_SIZE/4, CELL_SIZE))

				elif route[i][1] == route[i+1][1]:
					pygame.draw.rect(screen, ROUTE_COLOR, (cur_x+x_middle_off, cur_y, CELL_SIZE/4, CELL_SIZE/2 + CELL_SIZE/12.5))
					pygame.draw.rect(screen, ROUTE_COLOR, (cur_x+x_middle_off, cur_y+CELL_SIZE/2, CELL_SIZE/4, CELL_SIZE/2+CELL_SIZE/12.5))
				else:
					pygame.draw.rect(screen, ROUTE_COLOR, (cur_x, cur_y+y_middle_off, CELL_SIZE/2+2, CELL_SIZE/4))
					pygame.draw.rect(screen, ROUTE_COLOR, (cur_x + CELL_SIZE/2, cur_y+y_middle_off, CELL_SIZE/2+2, CELL_SIZE/4))
				if still_drawing: 
					time.sleep(0.028)
					pygame.display.update()
				continue
			break
		still_drawing = False

	pygame.display.update()