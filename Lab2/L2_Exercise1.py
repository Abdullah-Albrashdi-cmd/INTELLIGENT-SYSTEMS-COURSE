#L2_Exercise 1

from pyamaze import maze, agent, COLOR

m = maze()

m.CreateMaze()

a = agent(m, footprints=True, color=COLOR.green)

m.tracePath({a:m.path})

m.run()