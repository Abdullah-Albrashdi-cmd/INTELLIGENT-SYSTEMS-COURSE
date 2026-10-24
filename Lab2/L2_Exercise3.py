from pyamaze import maze, agent, COLOR
from queue import PriorityQueue

def h(cell1, cell2):
    x1,y1 = cell1
    x2,y2 = cell2
    return (abs(x1-x2)+abs(y1-y2))

def g_bfs(m, s=None):
    if s is None:
        s = (m.rows, m.cols)
    open = PriorityQueue()
    open.put((h(s,m._goal),s))
    h_score = {cell: float("inf") for cell in m.grid}
    parent = {}
    parent[s] = None
    h_score[s] = h(s, m._goal)

    while not open.empty():
        curr = open.get()[1]
        if curr == m._goal:
            break

        if m.maze_map[curr]["E"]:
            child = (curr[0], curr[1]+1)
            temp = h(child, m._goal)
            if temp < h_score[child]:
                open.put((temp, child))
                h_score[child] = temp
                parent[child] = curr

        if m.maze_map[curr]["W"]:
            child = (curr[0], curr[1]-1)
            temp = h(child, m._goal)
            if temp < h_score[child]:
                open.put((temp, child))
                h_score[child] = temp
                parent[child] = curr

        if m.maze_map[curr]["N"]:
            child = (curr[0]-1, curr[1])
            temp = h(child, m._goal)
            if temp < h_score[child]:
                open.put((temp, child))
                h_score[child] = temp
                parent[child] = curr

        if m.maze_map[curr]["S"]:
            child = (curr[0]+1, curr[1])
            temp = h(child, m._goal)
            if temp < h_score[child]:
                open.put((temp, child))
                h_score[child] = temp
                parent[child] = curr

    actual_path = []
    cell = m._goal
    while cell is not None:
        actual_path.append(cell)
        cell = parent[cell]
    actual_path.reverse()
    return actual_path


m = maze(10,10)
m.CreateMaze()
g__path = g_bfs(m)
a = agent(m,  color=COLOR.blue, footprints= True)
m.tracePath({a:g__path})
m.run()