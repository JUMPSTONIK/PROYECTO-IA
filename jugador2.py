import socketio, random, math

sio = socketio.Client()

username = 'JUMPSTONIK'
tournament_id = '14'
game_server = 'http://localhost:4000' #server de Sam
movesH = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]
movesV = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]
turno = 1
# Client para el totito chino

@sio.event
def connect():
	sio.emit('signin', {
	'user_name': username,
	'tournament_id': tournament_id,
	'user_role': 'player'})


@sio.event
def disconnect():
	print('Disconnected from server')

@sio.on('ok_signin')
def ok_signin():
	print('Successfully signed in!')

@sio.on('ready')
def ready(data):
	#print(data)
	global movesH
	global movesV
	global turno
	cant = 0
	jugadorN = data['player_turn_id']
	turn = data['movementNumber']
	board = data['board']
	movimiento = 0
	ran1 = random.randint(0,1)
	tablero = []
	if jugadorN == 1:
		if turno > 2:
			ValMoves(board)
			cant, ran1, movimiento = minimax(board,3,-1, 1, True)
		else:
			movimiento, tablero = AnBoard(ran1,data['board'])
	else:
		if turno > 3:
			ValMoves(board)
			cant, ran1, movimiento = minimax(board,3,-1, 1, False)
		else:
			movimiento, tablero = AnBoard(ran1,data['board'])
	
	#print('tablero actual')
	#ShowBoard(data['board'])
	#print('tablero con el movimiento')
	#ShowBoard(tablero)	
	# AI logic
	
	sio.emit('play',{
	'tournament_id': tournament_id,
	'player_turn_id': data['player_turn_id'],
	'game_id': data['game_id'],
	'movement': [ran1, movimiento]})

@sio.on('finish')
def finish(data):
	global movesH
	global movesV
	movesH = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]
	movesV = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]
	print('tournament is over', data)
	gameID = data['game_id']
	playerTurnID = data['player_turn_id']
	winnerTurnID = data['winner_turn_id']
	board = data['board']
	sio.emit('player_ready', {
		'tournament_id': tournament_id,
		'player_turn_id': playerTurnID,
		'game_id': gameID
		})

def AnBoard(ran,board):
	global movesH
	global movesV
	move = 0
	for x in range(0,len(board[0])-1):
		if board[1][x] != 99:
			try:
				movexV.remove(x)
			except:
				pass

		if board[0][x] != 99 :
			try:
				movexH.remove(x)
			except:
				pass
		
	if (ran == 0) and (len(movesH) > 0):
		ran2 = random.randint(0,len(movesH)-1)
		move = movesH[ran2]
		movesH.pop(ran2)
	if (ran == 1) and (len(movesV) > 0):
		ran2 = random.randint(0,len(movesV)-1)
		move = movesV[ran2]
		movesV.pop(ran2)
	#print(str(len(board[ran])) + " y " + str(move))
	board[ran][move-1] = 0

	return move-1,board

def ShowBoard(board):
	print('(' + str(board[0][0]) + ',' + str(board[1][0]) + ')' + '(' + str(board[0][1]) + ',' + str(board[1][1]) + ')' + '(' + str(board[0][2]) + ',' + str(board[1][2]) + ')' + '(' + str(board[0][3]) + ',' + str(board[1][3]) + ')' + '(' + str(board[0][4]) + ',' + str(board[1][4]) + ')' + '(' + str(board[0][5]) + ',' + str(board[1][5]) + ')\n' + '(' + str(board[0][6]) + ',' + str(board[1][6]) + ')' + '(' + str(board[0][7]) + ',' + str(board[1][7]) + ')' + '(' + str(board[0][8]) + ',' + str(board[1][8]) + ')' + '(' + str(board[0][9]) + ',' + str(board[1][9]) + ')' + '(' + str(board[0][10]) + ',' + str(board[1][10]) + ')' + '(' + str(board[0][11]) + ',' + str(board[1][11]) + ')\n' + '(' + str(board[0][12]) + ',' + str(board[1][12]) + ')' + '(' + str(board[0][13]) + ',' + str(board[1][13]) + ')' + '(' + str(board[0][14]) + ',' + str(board[1][14]) + ')' + '(' + str(board[0][15]) + ',' + str(board[1][15]) + ')' +  '(' + str(board[0][16]) + ',' + str(board[1][16]) + ')' + '(' + str(board[0][17]) + ',' + str(board[1][17]) + ')\n' + '(' + str(board[0][18]) + ',' + str(board[1][18]) + ')' + '(' + str(board[0][19]) + ',' + str(board[1][19]) + ')' + '(' + str(board[0][20]) + ',' + str(board[1][20]) + ')' + '(' + str(board[0][21]) + ',' + str(board[1][21]) + ')' + '(' + str(board[0][22]) + ',' + str(board[1][22]) + ')' + '(' + str(board[0][23]) + ',' + str(board[1][23]) + ')\n' + '(' + str(board[0][24]) + ',' + str(board[1][24]) + ')' + '(' + str(board[0][25]) + ',' + str(board[1][25]) + ')' + '(' + str(board[0][26]) + ',' + str(board[1][26]) + ')' + '(' + str(board[0][27]) + ',' + str(board[1][27]) + ')' + '(' + str(board[0][28]) + ',' + str(board[1][28]) + ')' + '(' + str(board[0][29]) + ',' + str(board[1][29]) + ')\n')

def minimax(board, depth,alpha, beta, maximizingPlayer):

	if maximizingPlayer:
		maxEval = -1
		for x in movesH:
			val = minimax(evalBoard(board,0,x), depth -1, alpha, beta, False)
			maxEval = max(maxEval,val)
			alpha = max(alpha,val)
			if beta <= alpha:
				break
			return maxEval, 0, x

	else:
		maxEval = 1
		for x in movesH:
			val = minimax(evalBoard(board,0,x), depth -1, alpha, beta, True)
			minEval = min(minEval,val)
			alpha = min(beta,val)
			if beta <= alpha:
				break
			return minEval, 0, x
		


#evaluo si se obtiene 1,2,-1,-2 o 0 con un movimiento			
def evalBoard(boardP, ori, pos):
	x1,x2 = adPoses(pos)
	cont1 = 0
	cont2 = 0
	if ori == 1:
		#comprobando el tiro en caso sea uno vertical
		if x1 != None and x2 != None:

			if boardP[0][x2] != 99:
				cont2+=1
			if boardP[0][x2+1] != 99:
				cont2+=1
			if boardP[ori][pos +1] != 99:
				cont2+=1

			if boardP[0][x2] != 99:
				cont1+=1
			if boardP[0][x2+1] != 99:
				cont1+=1
			if boardP[ori][pos -1] != 99:
				cont1+=1

			if cont1 ==3 and cont2 == 3:
				boardP[ori][pos]=2
			else:
				if cont1 ==3 or cont2 == 3:
					boardP[ori][pos]=1
				else:
					boardP[ori][pos]=0
		else:
			if x1 == None:
				if boardP[0][x2] != 99:
					cont2+=1
				if boardP[0][x2+1] != 99:
					cont2+=1
				if boardP[ori][pos +1] != 99:
					cont2+=1
				if cont2 ==3:
					boardP[ori][pos]=1
				else:
					boardP[ori][pos]=0
			if x2 == None:
				if boardP[0][x2] != 99:
					cont1+=1
				if boardP[0][x2+1] != 99:
					cont1+=1
				if boardP[ori][pos -1] != 99:
					cont1+=1
				if cont1 ==3:
					boardP[ori][pos]=1
				else:
					boardP[ori][pos]=0
	else:
		#comprobando en caso sea horizontal
		if x1 != None and x2 != None:

			if boardP[1][x2] != 99:
				cont2+=1
			if boardP[1][x2+1] != 99:
				cont2+=1
			if boardP[ori][pos +1] != 99:
				cont2+=1

			if boardP[1][x2] != 99:
				cont1+=1
			if boardP[1][x2+1] != 99:
				cont1+=1
			if boardP[ori][pos -1] != 99:
				cont1+=1

			if cont1 ==3 and cont2 == 3:
				boardP[ori][pos]=2
			else:
				if cont1 ==3 or cont2 == 3:
					boardP[ori][pos]=1
				else:
					boardP[ori][pos]=0
		else:
			if x1 == None:
				if boardP[1][x2] != 99:
					cont2+=1
				if boardP[1][x2+1] != 99:
					cont2+=1
				if boardP[ori][pos +1] != 99:
					cont2+=1
				if cont2 ==3:
					boardP[ori][pos]=1
				else:
					boardP[ori][pos]=0
			if x2 == None:
				if boardP[1][x2] != 99:
					cont1+=1
				if boardP[1][x2+1] != 99:
					cont1+=1
				if boardP[ori][pos -1] != 99:
					cont1+=1
				if cont1 ==3:
					boardP[ori][pos]=1
				else:
					boardP[ori][pos]=0	
	return boardP

def adPoses(pos):
	x1,x2 = None

	if pos >=0 and pos <=5:
		if pos == 0:
			x2 = ((pos-1)*6)+6
		else:
			x1 = (pos-1)*6
			if pos == 5:
				pass
			else:
				x2 = x1+6
	if pos >= 6 and pos <=11:
		if pos == 6:
			x2 = 1
		else:
			if pos == 7:
				x1 =pos-6
			if pos >7:
				x1 = (pos -6-1)*6+1
			if pos !=11:
				x2 = x1 +6
	if pos >=12 and pos <=17:
		if pos ==12:
			x2 = 2
		if pos == 13:
			x1 = 2
			x2 = 8
		if pos == 14:
			x1 = 8
			x2 = 14
		if pos == 15:
			x1 = 14
			x2 = 20
		if pos == 16:
			x1 == 20
			x2 == 26
		if pos == 17:
			x1 == 25
	if pos >= 18 and pos <=23:
		if pos ==18:
			x2 = 3
		if pos == 19:
			x1 = 3
			x2 = 9
		if pos == 20:
			x1 = 9
			x2 = 15
		if pos == 21:
			x1 = 15
			x2 = 21
		if pos == 22:
			x1 == 21
			x2 == 27
		if pos == 23:
			x1 == 27
	if pos >= 24 and pos <=29:
		if pos ==24:
			x2 = 4
		if pos == 25:
			x1 = 4
			x2 = 10
		if pos == 26:
			x1 = 10
			x2 = 16
		if pos == 27:
			x1 = 16
			x2 = 22
		if pos == 28:
			x1 == 22
			x2 == 28
		if pos == 29:
			x1 == 28
	return x1,x2

#evaluar los movimientos disponibles dentro del tablero
def ValMoves(board):
	global movesH
	global movesV
	move = 0
	for x in range(0,len(board[0])-1):
		if board[1][x] != 99:
			try:
				movexV.remove(x)
			except:
				pass

		if board[0][x] != 99 :
			try:
				movexH.remove(x)
			except:
				pass

def sumator(Tboard):
	sum = 0
	for x in range(0,len(Tboard[0])-1):
		if board[1][x] != 99:
			sum += board[1][x]

		if board[0][x] != 99 :
			sum += board[0][x]
	return sum

sio.connect(game_server)
sio.wait()
