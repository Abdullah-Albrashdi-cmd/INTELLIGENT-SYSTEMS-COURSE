from pyamaze import maze, agent, COLOR  

m = maze(10, 10)  
m.CreateMaze(theme=COLOR.light)  

red_agent = agent(m, x=m.rows, y=1, shape='arrow', footprints=True, color=COLOR.red)  
blue_agent = agent(m, x=1, y=m.cols, shape='arrow', footprints=True, color=COLOR.blue)   

m.tracePath({red_agent: m.path}, delay=200)  
m.tracePath({blue_agent: m.path}, delay=200)  
 
m.run()
