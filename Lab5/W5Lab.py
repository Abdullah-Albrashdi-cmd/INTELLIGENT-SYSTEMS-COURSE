import time

board = {i: '' for i in range(1,10)} # a global variable

#1: a function to print the board 
def printboard():
    print("\n--------------------")
    print(f"|   {board[1]}  |   {board[2]}  |   {board[3]}  |")
    print("\n--------------------")
    print(f"|   {board[4]}  |   {board[5]}  |   {board[6]}  |")
    print("\n--------------------")
    print(f"|   {board[7]}  |   {board[8]}  |   {board[9]}  |")
    print("\n--------------------") 

#2: a function to check if there is a free space for a given position
def isSpaceFree(position):
    return (board[position] == '')

#3: a function to check for a win 
def checkforwin():
    winning_position = [
        (1,2,3),(4,5,6),(7,8,9),
        (1,4,7),(2,5,8),(3,6,9),
        (1,5,9),(3,5,7)
    ]
    for pos in winning_position:
        if (board[pos[0]] == board[pos[1]] == board[pos[2]] and board[pos[0]] != ''):
            return board[pos[0]]
        
    return None

#4: a function to check roe a draw
def checkfordraw():
    return all(board[pos] !='' for pos in board.keys())

#5: a function to do the insertion of letter. This is used by both AI and Human.
#input: position, player
#output: updated board position.
def insertLetter(player, position):

    if isSpaceFree(position):
        board[position] = player
        printboard()

        winner = checkforwin()
        if winner:
            print(f"Player {winner} Won!")
            exit()
        
        if checkfordraw():
            print("Game Has Ended in DEAW!")
            exit()            
    else:
        position = int(input("Wrong Move, Please re-enter: "))
        insertLetter(player, position)

#6:
def bestMove():
    move = None #move stors the best location to play.
    bestScore = -float('Inf')
    for pos in board.keys():
        if isSpaceFree(pos):
            board[pos] = 'X'     #assuming x is our AI player
            score = minimax(False) # letting the o player to play
            board[pos] = ''
            if score > bestScore:
                bestScore = score
                move = pos
    return move #move stores the position that lead to optimal value.

def minimax(isMaximizer):

    winner = checkforwin()
    if winner == 'X':
        return 1
    elif winner == 'O':
        return -1
    elif checkfordraw():
        return 0
    
    if isMaximizer:
        bestScore = -float('Inf')
        for pos in board.keys():
            if isSpaceFree(pos):
                board[pos] = 'X'
                score = minimax(False)
                board[pos] = ''
                bestScore = max(score, bestScore)

    else:
        bestScore = float('Inf')
        for pos in board.keys():
            if isSpaceFree(pos):
                board[pos] = 'O'
                score = minimax(True)
                board[pos] = ''
                bestScore = min(score, bestScore)
    return bestScore

def playerX():
    print("AI is Playing...")
    time.sleep(2)
    position = bestMove()
    insertLetter('X', position)

def playerO():
    position = int(input("It is your turn to play now: "))
    insertLetter('O', position)

while not checkforwin():
    playerX()
    playerO()


