class Player64:

	def __init__(self):
		self.player_mark = 'Z'
		self.opponent_mark = 'Y'

	def move(self,temp_board,temp_block,old_move,flag):
		#print 'Entered move, prev move'+str(old_move)
		current_board_state = temp_board[:]
		current_block_state = temp_block[:]
		#List of permitted blocks, based on old move.
		#print 'Calling blocks allowed - '
		blocks_allowed = self.get_allowed_blocks(old_move, current_block_state)
		#print 'Blocks allowed + ' + str(blocks_allowed)
		self.player_mark = flag
		self.opponent_mark = self.compliment_mark(flag)
		#Get list of empty valid cells
		#print 'Allowed cars - '
		cells = self.get_actions(current_board_state, current_block_state, blocks_allowed)
		#print 'Allowed cells +' + str(cells)
		return self.minimax_decision(current_board_state, current_block_state, cells, flag)

	def minimax_decision(self, current_board_state, current_block_state, actions, flag):
		#print 'Entered minimax_decision'
		for current_action in actions:
			block_won, block_num = self.update_state(current_board_state, current_block_state, current_action, flag)
			current_min_value = self.min_value(current_board_state, current_block_state, current_action, self.compliment_mark(flag), 0)
			if current_action == actions[0] or current_min_value > best_value:
				best_action = current_action
				best_value = current_min_value
				#print 'Best value ' + str(best_value)
			self.revert_state(current_board_state, current_block_state, current_action, block_won, block_num)

		return best_action


	def min_value(self, current_board_state, current_block_state, prev_action, flag, depth):
		#print 'Entered min value'
		#print 'Depth = ' + str(depth)
		if self.terminal_test(current_board_state, current_block_state, depth) == True:
			return self.utility(current_board_state, current_block_state)

		blocks_allowed  = self.get_allowed_blocks(prev_action, current_block_state)
		actions = self.get_actions(current_board_state, current_block_state, blocks_allowed)

		for current_action in actions:
			block_won, block_num = self.update_state(current_board_state, current_block_state, current_action, flag)
			current_max_value = self.max_value(current_board_state, current_block_state, current_action, self.compliment_mark(flag), depth + 1)
			#print 'Current min value' + str(current_max_value)
			if current_action == actions[0] or current_max_value < best_min_value:
				best_min_value = current_max_value
			self.revert_state(current_board_state, current_block_state, current_action, block_won, block_num)

		return best_min_value

	def max_value(self, current_board_state, current_block_state, prev_action, flag, depth):
		#print 'Entered max value'
		if self.terminal_test(current_board_state, current_block_state, depth) == True:
			return self.utility(current_board_state, current_block_state)

		blocks_allowed  = self.get_allowed_blocks(prev_action, current_block_state)
		actions = self.get_actions(current_board_state, current_block_state, blocks_allowed)

		for current_action in actions:
			block_won, block_num = self.update_state(current_board_state, current_block_state, current_action, flag)
			current_min_value = self.min_value(current_board_state, current_block_state, current_action, self.compliment_mark(flag), depth + 1)
			#print 'Current min value' + str(current_min_value)
			if current_action == actions[0] or current_min_value > best_max_value:
				best_max_value = current_min_value
			self.revert_state(current_board_state, current_block_state, current_action, block_won, block_num)

		return best_max_value

	def terminal_test(self, current_board_state, current_block_state, depth):
		if depth % 2 == 0 and depth >= 2:
			#print 'Returning true'
			return True
		else:
			return False

	def calculate_score(self, board_state, block_num, factor, mark):
		#print 'Entered calculate_score'
		#print 'Board state' + str(board_state)
		score = 0
		idx1 = (block_num/3)*3
		idx2 = (block_num%3)*3

		#First Diagonal
		if board_state[idx1][idx2] == board_state[idx1 + 1][idx2 + 1] and board_state[idx1 + 1][idx2 + 1] == board_state[idx1 + 2][idx2 + 2] and board_state[idx1][idx2] == mark:
			score += (factor * 100)
		elif (board_state[idx1][idx2] == board_state[idx1 + 1][idx2 + 1] and board_state[idx1][idx2] == mark) or (board_state[idx1 + 1][idx2 + 1] == board_state[idx1 + 2][idx2 + 2] and board_state[idx1 + 1][idx2 + 1] == mark):
			score += (factor * 10)
		elif board_state[idx1][idx2] == mark or board_state[idx1+1][idx2+1] == mark or board_state[idx1+1][idx2+1] == mark:
			score += (factor * 1)

		#print 'Score D = ' + str(score)

		#Second Diagonal
		if board_state[idx1+2][idx2] == board_state[idx1 + 1][idx2 + 1] and board_state[idx1 + 1][idx2 + 1] == board_state[idx1][idx2 + 2] and board_state[idx1 + 2][idx2] == mark:
			score += (factor * 100)
		elif (board_state[idx1+2][idx2] == board_state[idx1 + 1][idx2 + 1] and board_state[idx1+2][idx2] == mark) or (board_state[idx1 + 1][idx2 + 1] == board_state[idx1][idx2 + 2] and board_state[idx1 + 1][idx2 + 1] == mark): 
			score += (factor * 10)
		elif board_state[idx1+2][idx2] == mark or board_state[idx1 + 1][idx2 + 1] == mark or board_state[idx1][idx2 + 2] == mark:
			score += (factor * 1)

		#Rows
		for i in range(idx1,idx1+3):
			if board_state[i][idx2] == board_state[i][idx2 + 1] and board_state[i][idx2 + 1] == board_state[i][idx2 + 2] and board_state[i][idx2] == mark:
				score += (factor * 100)
			elif (board_state[i][idx2] == board_state[i][idx2 + 1] and board_state[i][idx2] ==mark) or (board_state[i][idx2 + 1] == board_state[i][idx2 + 2] and board_state[i][idx2 + 1] == mark):
				score += (factor * 10)
			elif board_state[i][idx2] == mark or board_state[i][idx2 + 1] == mark or board_state[i][idx2 + 2] == mark:
				score += (factor * 1)

		#Columns
		for i in range(idx2,idx2+3):
			if board_state[idx1][i] == board_state[idx1+1][i] and board_state[idx1+1][i] == board_state[idx1+2][i] and board_state[idx1][i] == mark:
				score += (factor * 100)
			elif (board_state[idx1][i] == board_state[idx1+1][i] and board_state[idx1][i] == mark) or (board_state[idx1+1][i] == board_state[idx1+2][i] and board_state[idx1+1][i] == mark):
				score += (factor * 10)
			elif board_state[idx1][i] == mark or board_state[idx1+1][i] == mark or board_state[idx1+2][i] == mark:
				score += (factor * 1)

		#print 'Score = ' + str(score)
		return score


	def utility(self, current_board_state, current_block_state):
		#print 'Entered utiluty'
		sum_score = 0
		board_utility = [[0 for j in range(3)] for i in range(3)]
		for block_num in range(8):
			row = block_num/3
			col = block_num%3
			board_utility[row][col] = self.calculate_score(current_board_state, block_num, 1, self.player_mark)
			board_utility[row][col] += self.calculate_score(current_board_state, block_num, -1, self.opponent_mark)
			sum_score += board_utility[row][col]
			#print 'Score for block = '+str(block_num)+" is = "+ str(sum_score)

		#print 'Final score to be returned' + str(sum_score)
		return sum_score
		
	def compliment_mark(self, flag):
		if flag == 'x':
			return 'o'
		elif flag == 'o':
			return 'x'
		else:
			return 'Z'
		
	def get_allowed_blocks(self, prev_move, block_status):
		#print 'Entered get allowed block**'
		blocks = []
		if prev_move[0]%3 == 0 and prev_move[1]%3 == 0:
			blocks = [1, 3]
		elif prev_move[0]%3 == 0 and prev_move[1]%3 == 1:
			blocks = [0, 2]
		elif prev_move[0]%3 == 0 and prev_move[1]%3 == 2:
			blocks = [1, 5]
		elif prev_move[0]%3 == 1 and prev_move[1]%3 == 0:
			blocks = [0, 6]
		elif prev_move[0]%3 == 1 and prev_move[1]%3 == 1:
			blocks = [4]
		elif prev_move[0]%3 == 1 and prev_move[1]%3 == 2:
			blocks = [2, 8]
		elif prev_move[0]%3 == 2 and prev_move[1]%3 == 0:
			blocks = [3, 7]
		elif prev_move[0]%3 == 2 and prev_move[1]%3 == 1:
			blocks = [6, 8]
		elif prev_move[0]%3 == 2 and prev_move[1]%3 == 2:
			blocks = [5, 7]

		allowed_blocks = []
		for block_num in blocks:
			if block_status[block_num] == '-':
				allowed_blocks.append(block_num)
		#print 'Returning allowed_blocks' + str(allowed_blocks)

		return allowed_blocks

	def update_state(self, board_state, block_state, action, flag):

		board_state[action[0]][action[1]] = flag

		block_num = (action[0]/3)*3 + action[1]%3
		#Coordinates of top left cell of the modified block
		idx1 = (block_num/3)*3
		idx2 = (block_num%3)*3
		flag = False
		if block_state[block_num] == '-':
			#Checking diagonals
			if board_state[idx1][idx2] == board_state[idx1 + 1][idx2 + 1] and board_state[idx1 + 1][idx2 + 1] == board_state[idx1 + 2][idx2 + 2] and board_state[idx1][idx2] != '-':
				flag = True
			elif board_state[idx1+2][idx2] == board_state[idx1 + 1][idx2 + 1] and board_state[idx1 + 1][idx2 + 1] == board_state[idx1][idx2 + 2] and board_state[idx1 + 2][idx2] != '-':
				flag = True

			#Checking rows
			if flag != True:
				for i in range(idx1,idx1+3):
					if board_state[i][idx2] == board_state[i][idx2 + 1] and board_state[i][idx2 + 1] == board_state[i][idx2 + 2] and board_state[i][idx2] != '-':
						flag = True
						break
			#Checking columns
			if flag != True:
				for i in range(idx2,idx2+3):
					if board_state[idx1][i] == board_state[idx1+1][i] and board_state[idx1+1][i] == board_state[idx1+2][i] and board_state[idx1][i] != '-':
						flag = True
						break

		if flag == True:
			block_state[block_num] = flag
			return True,block_num
		else:
			return False,-1


	def revert_state(self, board_state, block_state, action, block_won, block_num):

		board_state[action[0]][action[1]] = '-'
		if block_won:
			block_state[block_num] = '-'

	def get_actions(self, board_state, block_state, blocks_allowed):
		actions = []
		for block_num in blocks_allowed:
			#Coordinates of top left cell of the modified block
			idx1 = (block_num/3)*3
			idx2 = (block_num%3)*3
			for i in range(idx1, idx1 + 3):
				for j in range(idx2, idx2 + 3):
					if board_state[i][j] == '-':
						actions.append((i,j))

		if actions == []:
			for block_num in range(1,9):
				if block_state[block_num] != '-':
					continue
				idx1 = (block_num/3)*3
				idx2 = (block_num%3)*3
				for i in range(idx1, idx1 + 3):
					for j in range(idx2, idx2 + 3):
						if board_state[i][j] == '-':
							actions.append((i,j))

		return actions