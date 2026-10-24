from pyamaze import maze, agent, COLOR

m = maze(10, 10)  
m.CreateMaze(theme=COLOR.light)  

ai_agent = agent(m, x=m.rows, y=1, shape='arrow', footprints=True, color=COLOR.red) 
user_agent = agent(m, x=1, y=m.cols, shape='arrow', footprints=True, color=COLOR.blue)  

m.tracePath({ai_agent: m.path}, delay=300)  # adjust the delay as u like , and see when will u beat the Ai Agent :)
m.enableArrowKey(user_agent)

m.run()
