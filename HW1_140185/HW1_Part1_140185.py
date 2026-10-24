#HW1_Part1_140185
'''My code let the user inter the mize type 
(Predefined or Randomly generated)'''

from pyamaze import maze, agent, COLOR, textLabel
import csv,os

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


def dfs_with_dead_end(m, start = None):
    if start == None:
        start = (m.rows, m.cols)
    explore = []
    frontier = [start]  
    searchPath = []
    dead_ends = []
    dead_end_paths = []
    parent = {}

    while len(frontier) > 0:
        current = frontier.pop()
        explore.append(current)
        searchPath.append(current)

        if current == m._goal:
            break


        for d in ['E', 'W', 'N', 'S']:
            if m.maze_map[current][d]:
                if d == 'E':
                    child = (current[0], current[1] + 1)
                elif d == 'W':
                    child = (current[0], current[1] - 1)
                elif d == 'N':
                    child = (current[0] - 1, current[1])
                elif d == 'S':
                    child = (current[0] + 1, current[1])
                
                if child not in frontier and child not in explore:                    
                    frontier.append(child)
                    parent[child] = current

        #check if current cell is dead end 
        walls = sum(1 for d in ['E', 'W', 'N', 'S'] if not m.maze_map[current][d])
        if walls == 3 and current != start and current != m._goal:
            dead_ends.append(current)
            #record pathe to the dead end
            path = []
            c = current
            while c in parent:
                path.append(c)
                c = parent[c]
            path.append(start)
            dead_end_paths.append(path[::-1])

    return searchPath, dead_ends, dead_end_paths
        
#user input
print("\n--- DFS Navigation Agent with Dead-Ends ---\n")
maze_choice = input("Choose maze type: \n[1] Predefined \n[2] Randomly generated\nEnter 1 or 2:").strip()


if maze_choice == '1':
    m = load_maze('ta_maze.csv')

    
else:
    m = maze()
    m.CreateMaze(loopPercent=0) #random maze 


path, dead_ends, dead_end_paths = dfs_with_dead_end(m)

dfs_agent = agent(m, shape='arrow',filled= True, color= COLOR.blue, footprints=True)
m.tracePath({dfs_agent: path}, delay=100)

for cell in dead_ends:
    dead_agent = agent(m, x=cell[0], y=cell[1],filled=True, shape='square', color=COLOR.red)

textLabel(m, "Nodes Visited", len(path))
textLabel(m, "Dead Ends", len(dead_ends))

m.run()