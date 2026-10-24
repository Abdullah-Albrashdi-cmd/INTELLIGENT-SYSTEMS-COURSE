from pyamaze import maze, agent, COLOR

m = maze(5,5)
m.CreateMaze(pattern='v', theme = COLOR.light)

a = agent(m, x=5, y=4, shape='arrow', color=COLOR.red)

m.run()