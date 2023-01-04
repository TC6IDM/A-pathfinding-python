#DATE: 2021/06/21
#AUTHORS: Andrew T, Max S, Alexander P, Christian R
#DESCRIPTION: https://en.wikipedia.org/wiki/A*_search_algorithm 
#a path finding algorithm which knows the start and end positions, as well as any obstructions, and attempts to find the optimal path between the start and end.

import pygame#imports the pygame library
import math#imports the math library
from queue import PriorityQueue#imports queue from PriorityQueue, for sorting
import os#imports the OS
WIDTH = 500#sets the width of the screen, also the height
WIN = pygame.display.set_mode((WIDTH,WIDTH))#creates the window
pygame.display.set_caption("A* Path Finding Algorithm")#creates a header with the title of the program

#Defines a bunch of colors
RED = (255, 0, 0) 
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE= (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


Mode=""#sets the mode of the game to a string
os.system('clear')#clears the screen
while Mode.lower() !="diagonal" and  Mode.lower() !="standard":#runs untill the user picks diagonal or standard
	Mode=str(input('Would you like to use the "standard" approach or a "diagonal" one? ')).lower()#asks the user if they want to use a diagonal or standard approach for the path finding algorithm
	os.system('clear')#clears the screen
print("draw on the board and press space to start the simulation\nORANGE = Start\nBLUE = END\nBLACK = BARRIER\nLEFT CLICK: to draw\nRIGHT CLICK: to delete\nPRESS C: to clear the screen")#gives some information about the game

class Spot:
	'''A class that holds information about a pixel or a spot'''
	def __init__(self,row,col,width,total_rows):
		'''initilises a spot'''
		self.row = row#sets the row of the spot
		self.col = col#sets the col of the spot
		self.x = row * width#sets the x value of the spot
		self.y = col * width#sets the y value of the spot
		self.color = WHITE#sets the color of the spot to white
		self.neighbors = []#creates a list to hold all the neighbors of the current spot
		self.width = width#defines the width of the screen
		self.total_rows = total_rows#defines the total amount of rows 

	def get_pos(self):
		'''Returns the position of the spot'''
		return self.row,self.col

	def is_closed(self):
		'''Checks if the spot is closed'''
		return self.color == RED
	
	def is_open(self):
		'''Checks if the spot is open'''
		return self.color == GREEN

	def is_barrier(self):
		'''Checks if the spot is a barrier'''
		return self.color == BLACK
	
	def is_start(self):
		'''Checks if the spot is the start'''
		return self.color == ORANGE

	def is_end(self):
		'''Checks if the spot is the end'''
		return self.color == TURQUOISE

	def reset(self):
		'''Sets the spot's color to white (resets the spot)'''
		self.color = WHITE
	
	def make_closed(self):
		'''Sets the spot's color to red (closes the spot)'''
		self.color = RED
	
	def make_open(self):
		'''Sets the spot's color to green (opens the spot)'''
		self.color = GREEN

	def make_barrier(self):
		'''Sets the spot's color to black (makes the spot a barrier)'''
		self.color = BLACK
	
	def make_start(self):
		'''Sets the spot's color to orange (makes the spot a start position)'''
		self.color = ORANGE

	def make_end(self):
		'''Sets the spot's color to turquoise (makes the spot an end position)'''
		self.color = TURQUOISE

	def make_path(self):
		'''Sets the spot's color to purple (makes the spot a path)'''
		self.color = PURPLE

	def draw(self,win):
		'''draws the spot'''
		pygame.draw.rect(win,self.color,(self.x,self.y,self.width,self.width))

	def update_neighbors(self,grid):
		'''Updates the spot's neighbors'''
		self.neighbors=[]#sets the neighbors to an empty list

		if self.row<self.total_rows-1 and not grid[self.row+1][self.col].is_barrier(): #checks if a spot exists below, and if it is not a barrier
			self.neighbors.append(grid[self.row+1][self.col])#adds this spot to the list of neighbors 
			
			if Mode == "diagonal":#checks if the mode is diagonal

				if self.col<self.total_rows-1 and not grid[self.row+1][self.col+1].is_barrier(): #checks if a spot exists below and to the right, and if it is not a barrier

					self.neighbors.append(grid[self.row+1][self.col+1])#adds this spot to the list of neighbors 
				
				if self.col>0 and not grid[self.row+1][self.col-1].is_barrier(): #checks if a spot exists below and to the left, and if it is not a barrier

					self.neighbors.append(grid[self.row+1][self.col-1])#adds this spot to the list of neighbors 

		if self.row>0 and not grid[self.row-1][self.col].is_barrier(): #checks if a spot exists above, and if it is not a barrier

			self.neighbors.append(grid[self.row-1][self.col])#adds this spot to the list of neighbors 

			if Mode == "diagonal":#checks if the mode is diagonal

				if self.col<self.total_rows-1 and not grid[self.row-1][self.col+1].is_barrier(): #checks if a spot exists above and to the right, and if it is not a barrier

					self.neighbors.append(grid[self.row-1][self.col+1])#adds this spot to the list of neighbors 

				if self.col>0 and not grid[self.row-1][self.col-1].is_barrier(): #checks if a spot exists above and to the left, and if it is not a barrier

					self.neighbors.append(grid[self.row-1][self.col-1])#adds this spot to the list of neighbors 

		if self.col<self.total_rows-1 and not grid[self.row][self.col+1].is_barrier(): #checks if a spot exists to the right, and if it is not a barrier

			self.neighbors.append(grid[self.row][self.col+1])#adds this spot to the list of neighbors 

		if self.col>0 and not grid[self.row][self.col-1].is_barrier(): #checks if a spot exists to the left, and if it is not a barrier

			self.neighbors.append(grid[self.row][self.col-1])#adds this spot to the list of neighbors 

def h(p1,p2):
	'''Calculates the distance between p1 and p2'''
	x1,y1=p1 #converts p1 to its x and y position
	x2,y2=p2 #converts p2 to its x and y position

	if Mode == "diagonal":#checks if the mode is diagonal
		return math.sqrt(abs(x2-x1)**2 + abs(y2-y1)**2) #calculates the distance between the 2 points using pythagorean theorem
	else:#the mode is standard
		return abs(x2-x1) + abs(y2-y1) #calculates the distance between the 2 points regularly

def reconstruct_path(came_from,current,draw):
	'''Reconstructs the path once the end is found'''
	while current in came_from:#checks if the current position given is in the list which holds each spot on the way to the end
		current = came_from[current]#sets the current spot back one to the last spot
		current.make_path()#sets this spot to be a path
		draw()#draws the screen

def algorithm(draw,grid,start,end):
	count = 0#starts a count and sets it to 0
	open_set=PriorityQueue()#creates a PriorityQueue as the open set
	open_set.put((0,count,start))#puts this tuple into the open set
	came_from = {}#defines the spot where the current one came from
	g_score = {spot:float("inf") for row in grid for spot in row} #all g scores set to infinity
	g_score[start] = 0#start g score set to 0
	f_score = {spot:float("inf") for row in grid for spot in row} #all f scores set to infinity
	f_score[start] = h(start.get_pos(),end.get_pos()) #calculates the first f score

	open_set_hash = {start}#defines the open_set_hash variable as the start spot

	while not open_set.empty():#loops through this code if the open set is not empty, so it will run forever since the open set is never empty
		for event in pygame.event.get():#loops throguh
			if event.type == pygame.QUIT:#checks if the user wants to quit the program
				pygame.quit()#quits the program

		current = open_set.get()[2]#gets the current spot
		open_set_hash.remove(current)#removes the current spot from the open_set_hash
		if current == end:#checks if the algorithm has found the end,and makes a Path
			reconstruct_path(came_from,end,draw)#Reconstructs the path
			end.make_end()#makes the current spot the end spot
			return True#returns true
		
		for neighbor in current.neighbors:#loops through all the neighbors of this spot 
			temp_g_score = g_score[current]+1#gets the g score of the spot and adds 1 

			if temp_g_score < g_score[neighbor]:#checks if the g score is larger than the temperary g score
				came_from[neighbor] = current #sets the index of where the spot came from to the current spot
				g_score[neighbor] = temp_g_score#sets the G score to the temperary g score
				f_score[neighbor] = temp_g_score + h(neighbor.get_pos(),end.get_pos())# sets the f score to the g score plus the h score
				if neighbor not in open_set_hash:#checks if the neighbor is not in the open set hash
					count+=1#increases the count by 1
					open_set.put((f_score[neighbor],count,neighbor))#puts the f score, the count and the neighbor into the open set 
					open_set_hash.add(neighbor)#puts the neighbor into the open set hash
					neighbor.make_open()#makes the neighbor an open pixel
		
		draw()#draws the whole screen

		if current != start:#checks if the current position is not the start position
			current.make_closed()#closes the spot

	return False#returns false

def make_grid(rows,width):
	'''Creates a grid of spots'''
	grid=[]#creates a grid 
	gap = width // rows#floor divides the width by the rows to get the gap
	for i in range (rows):#loops through all the colums
		grid.append([])#appends a list to the grid
		for j in range (rows):#loops through all the rows
			spot=Spot(i,j,gap,rows)#creates a new spot
			grid[i].append(spot)#appends this spot to the grid
	return grid#returns the grid

def draw_grid(win,rows,width):
	'''Draws the grid'''
	gap=width//rows#floor divides the width by the rows to get the gap
	for i in range(rows):#loops through all the rows
		pygame.draw.line(win,GREY,(0,i*gap),(width,i*gap))#draws a line across the screen
	for j in range(rows):#loops through all the colums
		pygame.draw.line(win,GREY,(j*gap,0),(j*gap,width))#draws a line down the screen
	
def draw(win,grid,rows,width):
	'''Draws the whole screen'''
	win.fill(WHITE)#fills the screen white
	for row in grid:#loops through each row in the grid
		for spot in row:#loops through each spot in the row
			spot.draw(win)#draws the spot
	draw_grid(win,rows,width)#draws the grid
	pygame.display.update()#updates the screen

def get_clicked_pos(pos,rows,width):
	'''Gets the position of the click'''
	gap=width//rows#floor divides the width by the rows to get the gap
	y,x=pos#splits the position to the x and y values
	row = y//gap#gets the row of the position
	col = x//gap#gets the col of the position
	return row,col#returns the row and colum of the position

def main (win,width):
	'''Main loop of the program'''
	ROWS = 50#sets the amount of rows to 50
	grid=make_grid(ROWS,width)#creates the grid
	
	start=None#no start yet
	end=None#no end yet

	run=True#the program is running

	while run:#while the program is running
		draw(win,grid,ROWS,width)#draws the whole screen
		for event in pygame.event.get():#goes through each pygame event
			if event.type==pygame.QUIT:#checks if the user quits
				run=False#stops the program
			if pygame.mouse.get_pressed()[0]: #checks if there is a left click
				pos=pygame.mouse.get_pos()#gets the position of the mouse click
				row,col=get_clicked_pos(pos,ROWS,width)#gets the row and column of the click
				spot = grid[row][col]#sets the spot to the spot at this position

				if not start and spot != end:#checks if there is no start and this spot is not the end
					start = spot#sets the spot to the start
					start.make_start()#makes this spot the start

				elif not end and spot != start:#checks if there is no end and this spot is not the start
					end = spot#sets the spot to the end
					end.make_end()#makes this spot the end

				elif spot != end and spot != start:#checks if this spot is not the end and not the start
					spot.make_barrier()#makes this spot a barrier

			elif pygame.mouse.get_pressed()[2]: #checks if there is a right click
				pos=pygame.mouse.get_pos()#gets the position of the click
				row,col=get_clicked_pos(pos,ROWS,width)#gets the row and column of the click
				spot = grid[row][col]#gets the spot at this position
				spot.reset()#resets the spot
				if spot == start:#checks if this spot is the start spot
					start = None#sets the start spot to None
				
				elif spot==end:#checks if this spot is the end spot
					end = None#sets the end spot to None
			

			if event.type == pygame.KEYDOWN:#checks if there was a keydown event 
				if event.key==pygame.K_SPACE and start and end:#checks if the space key has been pressed
					for row in grid:#loops through each row in the grid
						for spot in row:#loops through each spot in the row
							spot.update_neighbors(grid)#updates the neighbors of the spot
					
					algorithm(lambda: draw(win,grid,ROWS,width),grid,start,end)#runs the algorithm, passes through a function as draw using the lambda operator

				if event.key==pygame.K_c:#checks if the c key has been pressed
					start=None#resets the start position
					end=None#resets the end position
					grid=make_grid(ROWS,width)#re-creates the grid

	pygame.quit()#quits the pygame application

main(WIN,WIDTH)#runs the main loop of the program