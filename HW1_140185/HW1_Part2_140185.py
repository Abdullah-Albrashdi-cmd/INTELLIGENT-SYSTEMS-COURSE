#HW1_Part2_140185
'''My code let the user inter the mize type 
(Predefined or Randomly generated)'''


from pyamaze import maze, agent, COLOR, textLabel
import math
import csv, os

def load_maze(filename='ta_maze.csv'):
    """
    Load a maze from CSV file in the format you specified
    """
    if not os.path.exists(filename):
        print(f"Error: File {filename} not found!")
        return None
    
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        
        # Skip header
        next(reader)
        
        # First pass: determine maze dimensions
        max_row = 0
        max_col = 0
        cell_data = []
        
        for row in reader:
            if not row:  # Skip empty rows
                continue
            
            # Parse cell coordinates - handle the triple quote issue
            cell_str = row[0]
            
            # Clean up the string - remove all quotes and extra characters
            cell_str = cell_str.replace('"', '')  # Remove all quotes
            cell_str = cell_str.strip('()')  # Remove parentheses
            
            # Split by comma and convert to integers
            i, j = map(int, cell_str.split(','))
            
            max_row = max(max_row, i)
            max_col = max(max_col, j)
            cell_data.append((i, j, row[1], row[2], row[3], row[4]))
    
    # Create maze object
    loaded_maze = maze(max_row, max_col)
    
    # Rebuild maze_map from stored data
    for data in cell_data:
        i, j, e_wall, w_wall, n_wall, s_wall = data
        cell = (i, j)
        
        loaded_maze.maze_map[cell] = {
            'E': bool(int(e_wall)),
            'W': bool(int(w_wall)),
            'N': bool(int(n_wall)), 
            'S': bool(int(s_wall))
        }
    
    # Don't use loadMaze parameter, just create the maze normally
    loaded_maze.CreateMaze(loadMaze=filename)
    
    print(f"Maze loaded successfully from {filename}")
    return loaded_maze


def distance(a, b, mode):
    if mode == 'm':  #m = manhattan
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    elif mode == 'e':  #e = euclidean
        return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

def dfs_with_vision(m, start, vision_range, mode):
    frontier = [start]
    explored = []
    visible_cells = []
    parent = {}

    while frontier:
        current = frontier.pop()
        explored.append(current)

        if distance(start, current, mode) <= vision_range:
            visible_cells.append(current)

        for d in ['E', 'W', 'N', 'S']:
            if m.maze_map[current][d]:
                if d == 'E': child = (current[0], current[1]+1)
                elif d == 'W': child = (current[0], current[1]-1)
                elif d == 'N': child = (current[0]-1, current[1])
                elif d == 'S': child = (current[0]+1, current[1])
                if child not in frontier and child not in explored:
                    frontier.append(child)
                    parent[child] = current

    return visible_cells, explored


#user input
print("\n--- DFS Navigation Agent with Limited Vision ---\n")
maze_choice = input("Choose maze type: \n[1] Predefined \n[2] Randomly generated\nEnter 1 or 2:").strip()
vision_range = int(input("\nEnter vision range: "))
distance_mode = input("Enter distance mode ('m' for manhattan/ 'e' for euclidean): ").strip().lower()


if maze_choice == '1':
    m = load_maze('ta_maze.csv')
else:
    print("\n--Maze Size--")
    rows = int(input("Enter maze rows: "))
    cols = int(input("Enter maze columns: "))
    m = maze(rows, cols)
    m.CreateMaze(loopPercent=0)
    
start = (m.rows // 2 + 1, m.cols // 2 + 1) #start from the center

visible_cells, explored = dfs_with_vision(m, start, vision_range, distance_mode)

start_agent = agent(m, x=start[0], y=start[1], filled=True, shape='square', color=COLOR.red)

for cell in visible_cells:
    if cell != start:
        agent(m, x=cell[0], y=cell[1], filled=True, shape='square', color=COLOR.blue)

textLabel(m, f"{distance_mode.capitalize()} Cells", len(visible_cells))
textLabel(m, "Vision range", vision_range)

m.run()