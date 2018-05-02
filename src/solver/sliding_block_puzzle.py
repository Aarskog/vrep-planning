import numpy as np
import copy
import random
from heapq import heappush
from heapq import heappop
'''
Solves the 3X3 sliding block puzzle using A* algorithm with the Manhattan
distance heuristic
'''

class board:
	board = []
	boardsize = 3
	pos_actions = [] #Possible actions i.e. child nodes
	solution = np.array(np.reshape(range(boardsize**2),(-1,boardsize)))
	h = 0 #The heuristic function value. (estimated) distance to solution
	depth = 0 #Distance from the initial node to current node
	def __init__(self,parent_board = None, action=None):
		a=1
		self.action = action
		self.parent_board = parent_board

		if parent_board is None:
			#First board, intitialize with a random board
			self.board = np.array(np.reshape(random.sample(range(self.boardsize**2), self.boardsize**2),(-1,self.boardsize)))

			# #There are 9! different boards in a 3X3 board. Only half of them are solvable
			while not self.is_solvable():
				self.board = np.array(np.reshape(random.sample(range(self.boardsize**2), self.boardsize**2),(-1,self.boardsize)))
			self.board = np.array([[8,6,7],[2,5,4],[3,0,1]])#29 moves
			self.dist_to_goal = self.h_manhattan_distance()
			self.h = self.dist_to_goal

		else:
			self.board =  copy.deepcopy(parent_board.board)
			self.do_action(action)

			self.depth = parent_board.depth + 1
			self.dist_to_goal = self.h_manhattan_distance()
			self.h = self.dist_to_goal + self.depth


	def is_solved(self):
		return (self.board == self.solution).all()

	def is_solvable(self):
		#https://www.cs.bham.ac.uk/~mdr/teaching/modules04/java2/TilesSolvability.html

		#Get the board on a single line
		single_line = copy.deepcopy(self.board).ravel()
		inversions = 0
		inversions2 = 0
		for i in range(0, self.boardsize**2 - 1):
			for j in range(i+1, self.boardsize**2 ):
				if (single_line[i] > single_line[j]):
					inversions = inversions + 1

		for i in range(1,self.boardsize**2):
			pos = np.argwhere(single_line==i)[0][0]
			inversions2 = inversions2 + abs(i-pos)

			#if both are even or odd, the board is solvable
		if (abs(inversions2-inversions)%2==0):
			return True

		return False

	#create and return child nodes
	def possible_actions(self):
		zero_position = np.argwhere(self.board==0)[0]
		self.pos_actions = []
		if zero_position[0]>0 and not self.action == 'down':
			self.pos_actions.append(board(parent_board=self,action='up'))

		if zero_position[0]<(self.boardsize-1) and not self.action == 'up':
			self.pos_actions.append(board(parent_board=self,action='down'))

		if zero_position[1]>0 and not self.action == 'right':
			self.pos_actions.append(board(parent_board=self,action='left'))

		if zero_position[1]<(self.boardsize-1) and not self.action == 'left':
			self.pos_actions.append(board(parent_board=self,action='right'))
		return self.pos_actions

	def do_action(self,action):
		zero_position = np.argwhere(self.board==0)[0]
		if action == 'up':
			#Swap
			self.board[zero_position[0]][zero_position[1]],self.board[zero_position[0]-1][zero_position[1]] = self.board[zero_position[0]-1][zero_position[1]],self.board[zero_position[0]][zero_position[1]]

		elif action == 'down':
			self.board[zero_position[0]][zero_position[1]],self.board[zero_position[0]+1][zero_position[1]] = self.board[zero_position[0]+1][zero_position[1]],self.board[zero_position[0]][zero_position[1]]

		elif action == 'left':
			self.board[zero_position[0]][zero_position[1]],self.board[zero_position[0]][zero_position[1]-1] = self.board[zero_position[0]][zero_position[1]-1],self.board[zero_position[0]][zero_position[1]]

		elif action == 'right':
			self.board[zero_position[0]][zero_position[1]],self.board[zero_position[0]][zero_position[1]+1] = self.board[zero_position[0]][zero_position[1]+1],self.board[zero_position[0]][zero_position[1]]

	def h_misplaced_tiles(self):
		#heuristic function of number of misplaces tiles
		return np.sum(self.board!=self.solution)

	def h_manhattan_distance(self):
		h = 0
		for i in range(1,self.boardsize**2):
			sx,sy = np.argwhere(self.board==i)[0]
			ex, ey =i/self.boardsize,i%self.boardsize
			h = h + abs(ex - sx) + abs(ey - sy)
		return h

	def execute_path(self,path):
		for action in path:
			print '---------------'
			self.do_action(action)
			print action
			print self.board

	def print_path(self):
		if not self.parent_board:
			return
		print_path(self.parent_board)
		print self.action

	def get_path(self,path):
		if not self.parent_board:
			return self.action
		self.parent_board.get_path(path)
		path.append(self.action)

	def __cmp__(self, other):
		#Used for heap sort
		return cmp(self.h,other.h)


def solve(init_board):

	heap = []
	heappush(heap,init_board)

	#Make a table of visited nodes as a hash function for quick check of existence
	visited = {tuple(init_board.board.data):True}

	i = 0
	while heap:

		possible_solution = heappop(heap)
		print 'States visited:',i,' length queue:',len(heap),' depth:',possible_solution.depth,\
		' State cost: ',possible_solution.h," Dist to goal: ",possible_solution.dist_to_goal
		i = i + 1

		if possible_solution.is_solved():
			print '\n\n Solution:'
			path = []
			possible_solution.get_path(path)
			init_board.execute_path(path)
			print '\nSolved'
			print 'Nodes visited = ',i
			print 'Num actions = ',possible_solution.depth
			print "Solution=\n",path

			return path


		else:

			new_nodes = possible_solution.possible_actions()

			for new_node in new_nodes:

				if not  tuple(new_node.board.data) in visited:

					visited[tuple(new_node.board.data)]=True

					#Insert into heap
					heappush(heap,new_node)


	print '---NOT SOLVABLE---'
	print 'Nodes visited = ',i
	return []

def main():
	board_to_solve = board()
	print 'Board =\n', board_to_solve.board
	solve(board_to_solve)

if __name__== "__main__":
	main()
