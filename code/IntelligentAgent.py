#NAME: ANUSHKA AGARWAL
#UNI: aa5477

from random import randint
from BaseAI import BaseAI
import time

# Time Limit Before Losing
timeLimit = 0.15

class IntelligentAgent(BaseAI):
	def getMove(self, grid):
		self.prevTime = time.time()
		self.depth_max = 1  # Start with minimal depth
		self.over = False
		moves = grid.getAvailableMoves()
		
		final_move = None
		while not self.over:
			start_time = time.time()
			self.updateAlarm(time.time())
			# self.depth_max += 1
			
			# Adjust depth based on game state
			largest_tile = grid.getMaxTile()
			if largest_tile >= 512:
				self.depth_max = min(self.depth_max + 1, 5)  # Allow deeper search when larger tiles are on board
			else:
				self.depth_max = min(self.depth_max + 1, 3)  # Keep a lower max depth when tiles are smaller
			#depth code end

			player_move = self.maximize(grid, -10**9, 10**9, 1)[0]

			if player_move is not None:
				final_move = player_move
			
			# Dynamically adjust max depth based on time per move
			time_taken = time.time() - start_time
			if time_taken * self.depth_max > 0.2:
				self.depth_max -= 1  # Reduce depth to stay within time limit
				break

		return final_move if moves else None


	def updateAlarm(self, currTime):
		if currTime - self.prevTime > timeLimit:
			self.over = True

	#Minimize function for the expectiminimax algorithm with alpha-beta pruning
	def minimize(self, grid, alpha, beta, depth):
		if grid.getAvailableCells() == []:
			return (None, self.evaluate(grid))

		if depth == self.depth_max:
			return (None, self.evaluate(grid))

		min_utility = float('inf')
		min_cell = None

		for child_cell in grid.getAvailableCells():
			gridCopy = grid.clone()

			# Calculate the weighted utility for 2
			gridCopy.setCellValue(child_cell, 2)
			utility_2 = self.maximize(gridCopy, alpha, beta, depth + 1)[1]
			utility_2 = utility_2 if utility_2 is not None else float('inf')
			# Calculate the weighted utility for 4
			gridCopy.setCellValue(child_cell, 4)
			utility_4 = self.maximize(gridCopy, alpha, beta, depth + 1)[1]
			utility_4 = utility_4 if utility_4 is not None else float('inf')

			# Expectiminimax: Weighted average
			utility = 0.9 * utility_2 + 0.1 * utility_4
			
			# Prune if time limit is reached
			self.updateAlarm(time.time())
			if self.over or utility is None:
				return (None, None)

			if utility < min_utility:
				min_utility = utility
				min_cell = child_cell

			if min_utility <= alpha:		#alpha beta pruning
				break
			beta = min(beta, min_utility)

		return (min_cell, min_utility)
	
	#Maximize function for the expectiminimax algorithm with alpha-beta pruning
	def maximize(self, grid, alpha, beta, depth):
		if grid.getAvailableMoves() == []:
			return (None, self.evaluate(grid))
	
		max_utility = -float('inf')
		max_move = None

		# Preliminary heuristic evaluation to order moves
		moves = grid.getAvailableMoves()
		moves.sort(key=lambda x: self.evaluate(x[1]), reverse=True)  # Sort moves by heuristic value

		for move, gridCopy in moves:
			utility = self.minimize(gridCopy, alpha, beta, depth)[1]
			self.updateAlarm(time.time())
			if self.over or utility is None:
				return (None, None)
			if utility > max_utility:
				max_utility = utility
				max_move = move
			if max_utility >= beta:				#alpha beta pruning
				break
			alpha = max(alpha, max_utility)

		return (max_move, max_utility)


	def evaluate(self, grid):
		# (w1, w2, w3, w4, w5) = (1, 1, 1, 1, 2)
		(w1, w2, w3, w4, w5) = (1, 1.5, 0.5, 2.5, 3)
		##heuristic number one : available number of tiles
		avail = grid.getAvailableCells()
		monoton = self.monotonicity(grid)
		ident = self.identicity(grid)
		corner = self.corner(grid)
		penal = self.penalty(grid)
		return w1*len(avail)*grid.getMaxTile() + w2*monoton + w3*ident + w4*corner + w5*penal


	def monotonicity(self, grid):
		value= 0
		for i in range(grid.size-1):
			for j in range (grid.size):
				if grid.map[i][j]==grid.map[i+1][j]/2:
					value +=grid.map[i+1][j]

		for i in range(grid.size):
			for j in range (grid.size-1):
				if grid.map[i][j]==grid.map[i][j+1]/2:
					value +=grid.map[i][j+1]
		return value

	def identicity(self, grid):
		value= 0
		for i in range(grid.size-1):
			for j in range (grid.size):
				if grid.map[i][j]==grid.map[i+1][j]:
					value +=grid.map[i][j]

		for i in range(grid.size):
			for j in range (grid.size-1):
				if grid.map[i][j]==grid.map[i][j+1]:
					value +=grid.map[i][j]
		return value

	def corner(self, grid):
		value=0
		for x in range(grid.size):
			for y in range(grid.size):
				if (grid.map[x][y] != 0):
					value+=grid.map[x][y]*(x*x*y*y)
		return value

	def penalty(self, grid):
		value=0
		for x in range(grid.size-1):
			for y in range(grid.size):
				if grid.map[x][y] not in (grid.map[x+1][y]/2, grid.map[x+1][y]) and grid.map[x][y] != 0:
					if grid.map[x][y] < grid.map[x+1][y]:
						value -= grid.map[x+1][y]-grid.map[x][y]
					else:
						value -= 2*(grid.map[x][y]-grid.map[x+1][y]/2)

		for x in range(grid.size):
			for y in range(grid.size-1):
				if grid.map[x][y] not in (grid.map[x][y+1]/2, grid.map[x][y+1]) and grid.map[x][y] != 0:
					if grid.map[x][y] < grid.map[x][y+1]:
						value -= grid.map[x][y+1]-grid.map[x][y]
					else:
						value -= 2*(grid.map[x][y]-grid.map[x][y+1]/2)
		return value