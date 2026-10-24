N = 8 #is a global variable.

board = [-1]*N  #is a global variable.

def consistent(col, row):
    #row: Row pos for the new queen to be placed
    #col: column pos for the new queen to be placed 
    #returns: a boolean value (True if consistent) or (False if not)
    for c in range(col): #c--> column of the queen aleardy placed
        r = board[c] #getting the row position of the queen already placec

        same_row = (r==row) #boolean variable
        same_diag = abs(r - row) == abs(c - col) #boolean variable
        if same_row or same_diag:
            return False

    return True


def backtrack(col=0): #returning a True(CONSISTENT) or False(Not Cons)
    #col: to begin with col is initialized to 0 
    #and gets incremented by 1 progressivly.
    #this is going to be a recursive function.
    if col == N:
        return True #that means there is a solution found

    for row in range(N):
        if consistent(col, row):
            board[col] = row #Khalli queen. place the queen.
            print_board()
            if backtrack(col+1):
                return True
            board[col] = -1 #undo (backtrack)

    return False #no value worked --> backtracking could not solve (3x3,2x2)


def print_board(): #print the given board state.
    for r in range(N):
        print(" ".join("Q" if board[c] == r else "." for c in range(N)))
    print("\n")

# main CSP solving
if backtrack():
    print_board()
else:
    print("No solution")

