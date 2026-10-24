from pyamaze import maze, agent, COLOR, textLabel
from queue import PriorityQueue

def h(cell1, cell2):
    x1,y1 = cell1
    x2,y2 = cell2
    return (abs(x1-x2)+abs(y1-y2))

def g(parent):
    length = len(parent)
    return length


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
                temp = h(child, m._goal) # calculate destance from child to goal
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
    steps = len(actual_path)
    return actual_path, steps


def A_star(m, s=None):
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
                temp = h(child, m._goal)+g(parent)
                if temp < h_score[child]:
                    open.put((temp, child))
                    h_score[child] = temp
                    parent[child] = curr

            if m.maze_map[curr]["W"]:
                child = (curr[0], curr[1]-1)
                temp = h(child, m._goal)+g(parent)
                if temp < h_score[child]:
                    open.put((temp, child))
                    h_score[child] = temp
                    parent[child] = curr

            if m.maze_map[curr]["N"]:
                child = (curr[0]-1, curr[1])
                temp = h(child, m._goal)+g(parent)
                if temp < h_score[child]:
                    open.put((temp, child))
                    h_score[child] = temp
                    parent[child] = curr

            if m.maze_map[curr]["S"]:
                child = (curr[0]+1, curr[1])
                temp = h(child, m._goal)+g(parent)
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
    steps = len(actual_path)
    return actual_path, steps


m = maze(10,10)
m.CreateMaze(loopPercent=50)
g_path, g_steps = g_bfs(m)
a_path, a_steps = A_star(m)
a = agent(m,  footprints= True,color=COLOR.blue)
b = agent(m, footprints= True,filled=True, color=COLOR.red)
m.tracePath({a:g_path}, delay=100)
m.tracePath({b:a_path}, delay=100)
g_bfs_steps = textLabel(m, 'G_BFS_Steps:', g_steps)
A_steps = textLabel(m, 'A_Star_Steps:', a_steps)
m.run()