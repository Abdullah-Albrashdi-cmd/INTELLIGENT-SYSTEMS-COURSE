#L2_Exercise 2


from pyamaze import maze, agent, COLOR

m = maze(4,4)

def dfs(m, start=None):
    if start == None:
        start = (m.rows, m.cols)
        frontier = [start]
        Exploer = []
        searchPath = []
        dead_ends = [] 

        while len(frontier) > 0:
            current = frontier.pop()
            searchPath.append(current)
            if current == m._goal:
                break
            Exploer.append(current)

            if m.maze_map[current]['N']:
                child = (current[0]-1, current[1])
                if child not in frontier and child not in Exploer:
                    frontier.append(child)

            if m.maze_map[current]['S']:
                child = (current[0]+1, current[1])
                if child not in frontier and child not in Exploer:
                    frontier.append(child)

            if m.maze_map[current]['E']:
                child = (current[0], current[1]+1)
                if child not in frontier and child not in Exploer:
                    frontier.append(child)

            if m.maze_map[current]['W']:
                child = (current[0], current[1]-1)
                if child not in frontier and child not in Exploer:
                    frontier.append(child)
                    
            dirc =  [d for d in 'EWNS' if m.maze_map[current][d]]
            if len(dirc) == 1:
                dead_ends.append(current)
             
    return searchPath, dead_ends



m.CreateMaze()

dfs_agent1 = agent(m, footprints=True,shape='arrow',filled= True, color= COLOR.blue)

dfsSearch , deadEnds = dfs(m)
print(deadEnds)
m.tracePath({dfs_agent1: dfsSearch}, delay=150)

m.run()

