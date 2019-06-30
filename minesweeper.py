import sys
from random import randrange

# usage python3 minesweeper.py [height] [width]
# note if only height is given, the grid will use it as both height and width

def printgrid(grid):
	#-2 for uncovered, 0 for blank, -1 for bomb, 1-8 for bomb count
	#represented as - for uncoverred, number for non-bomb and blank, * for bomb
	#TODO: change such that console lines are overwritten
	for i in range(len(grid)):
		for j in range(len(grid[i])):
			if grid[i][j] == -2:
				print('-',end='')
			elif grid[i][j] == -1:
				print('*',end='')
			else:
				print(grid[i][j],end='')
		print()

def main():
	height, width = 16, 16
	if len(sys.argv) > 1:
		try:
			tempheight = int(sys.argv[1])
			tempwidth = int(sys.argv[1]) if len(sys.argv) == 2 else int(sys.argv[2])
			if tempheight > 100 or tempwidth > 150:
				raise Exception('Range out of bounds')
		except TypeError as e:
			print('Requires integer arguments')
		except Exception as e:
			print(e)
	# table is 0 for blank, -1 for bomb and number for number
	table = [[0 for _ in range(width)] for _ in range(height)]
	#5% of squares will be bombs
	bombs = []
	for _ in range(int(width*height*0.05)):
		r = randrange(0,height)
		c = randrange(0,width)
		while(table[r][c] == -1):
			r = randrange(0,height)
			c = randrange(0,width)
		top = max(0,r - 1)
		bottom = min(height - 1, r + 1)
		left = max(0, c - 1)
		right = min(width - 1, c + 1)
		for i in range(top, bottom + 1):
			for j in range(left, right + 1):
				if table[i][j] == -1:
					continue
				table[i][j] += 1
		table[r][c] = -1
		bombs.append((r,c))
	#grid is -2 for uncoverred, rest holds
	grid = [[-2 for _ in range(width)] for _ in range(height)]
	printgrid(grid)
	numFound = 0
	while numFound < width*height - len(bombs):
		userin = input()
		try:
			r, c = userin.split()
			r = int(r)
			c = int(c)
			if r >= height:
				raise ValueError()
			if c >= width:
				raise ValueError()
		except ValueError as e:
			print('user input invalid')
			print('use two space seperated integers 0->height-1 0->width-1')
			continue
		#technically can remove top if statement but makes code more readable
		if table[r][c] > 0:
			grid[r][c] = table[r][c]
			numFound += 1
		elif grid[r][c] == -1:
			for bomb in bombs:
				grid[bomb[0]][bomb[1]] = -1
			printgrid(grid)
			print('You Lose')
			break
		else:
			stack = [(r,c)]
			visited = set()
			while stack:
				coords = stack.pop()
				numFound += 1
				grid[coords[0]][coords[1]] = table[coords[0]][coords[1]]
				if table[coords[0]][coords[1]] == 0:
					if coords[0] > 0:
						if (coords[0] - 1, coords[1]) not in visited:
							foo = (coords[0] - 1, coords[1])
							stack.append(foo)
							visited.add(foo)
					if coords[0] < height - 1:
						if (coords[0] + 1, coords[1]) not in visited:
							foo = (coords[0] + 1, coords[1])
							stack.append(foo)
							visited.add(foo)
					if coords[1] < width - 1:
						if (coords[0], coords[1] + 1) not in visited:
							foo = (coords[0], coords[1] + 1)
							stack.append(foo)
							visited.add(foo)
					if  coords[1] > 0:
						if (coords[0], coords[1] - 1) not in visited:
							foo = (coords[0], coords[1] - 1)
							stack.append(foo)
							visited.add(foo)
		printgrid(grid)
	if numFound == width*height - len(bombs):
		print('You Win')

if __name__ == '__main__':
	main()