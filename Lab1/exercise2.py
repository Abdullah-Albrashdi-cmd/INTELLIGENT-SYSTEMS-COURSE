from pyamaze import maze, agent, COLOR

m = maze(7, 7)
m.CreateMaze(x=5, y=7, theme = COLOR.light)

a = agent(m, 1, 1, shape='square', color=COLOR.blue)
m.tracePath({a: m.path}, delay=180)

m.run()
