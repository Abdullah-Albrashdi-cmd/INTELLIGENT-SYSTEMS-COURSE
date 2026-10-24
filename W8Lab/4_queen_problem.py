N = 4 

#queens = input("Enter the Queens Position (ex.1212): ").split()

queens = [1,2,1,2]

def h_attacks(queens):
    h = 0

    for c1 in range(4):
        for c2 in range(c1+1, N):
            r1, r2 = queens[c1], queens[c2]
            if (r1 == r2) or abs(r1-r2) == abs(c1-c2):
                h += 1
    return h 

def print_board(queens):
    print(queens)
    for row in range(N):
        line = ["Q" if queens[c] == row else "." for c in range(N)]
        print(" ".join(line))
    print(" Number of Attacks = ",h_attacks(queens))

current_h = h_attacks(queens)
print("Initial Attacks")
print_board(queens)

MAX_STEPS = 100
step = 0

while step < MAX_STEPS:
    step += 1
    best_move = None
    best_h = current_h

    for c in range(N): #for every column in the board 
        orig_row = queens[c]
        for row in range(N): #for moving queen to a different row within same 
            if row == orig_row:
                continue
            trial = queens[:] #save temprorily in another variable 
            trial[c] = row 
            hh = h_attacks(trial)
            if hh < best_h:
                best_h = hh
                best_move = (best_h, c, row) #moving from colum c to row.

    if best_move is None:
        print("Reached global/local minmum")
        break
    best_h, c, r = best_move
    queens[c] = r
    current_h = best_h
    print(f"Step - {step}: Move the Queeen in Colum {c} to Row {r}")
    print_board(queens)

if current_h == 0:
    print("Reached Global Minimum")
else:
    print(f"Stuck in Local Minimum with h = {h_attacks(queens)}")
        
                
