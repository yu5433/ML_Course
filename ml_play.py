class MLPlay:
    def __init__(self, player):
        self.player = player
        if self.player == "player1":
            self.player_no = 0
        elif self.player == "player2":
            self.player_no = 1
        elif self.player == "player3":
            self.player_no = 2
        elif self.player == "player4":
            self.player_no = 3
        self.car_vel = 15                          # speed initial
        self.car_pos = (0,0)                        # pos initial
        self.car_lane = self.car_pos[0] // 70       # lanes 0 ~ 8
        self.action = 0
        self.lanes = [35, 105, 175, 245, 315, 385, 455, 525, 595]  # lanes center
        pass

    def update(self, scene_info):
        """
        9 grid relative position
        |    |    |    |    |
        | 10 |  1 |  2 |  3 | 12
        |    |    |  5 |    |
        |    |  4 |  c |  6 |
        |    |    |    |    |
        | 11 |  7 |  8 |  9 | 13
        |    |    |    |    |       
        """
        def check_grid():
            grid = set()
            speed_ahead = 100
            if self.car_pos[0] <= 40: # left bound
                grid.add(1)
                grid.add(4)
                grid.add(7)
                #grid.add(10)
                #grid.add(11)
            elif self.car_pos[0] >= 565: # right bound
                grid.add(3)
                grid.add(6)
                grid.add(9)
                #grid.add(12)
                #grid.add(13)
            
           
            for car in scene_info["cars_info"]:
                self.left = False
                self.right = False
                if car["id"] != self.player_no:
                    x = self.car_pos[0] - car["pos"][0] # x relative position
                    y = self.car_pos[1] - car["pos"][1] # y relative position
                    if x <= -100 and x > -160:
                        if y >= 50 and y < 180:
                            grid.add(12)
                        elif y < -50 and y > -180:
                            grid.add(13)
                    if x >= 100 and x < 160:
                        if y >= 50 and y < 180:    
                            grid.add(10)
                        elif y < -50 and y > -180:
                            grid.add(11)
                    if x <= 40 and x >= -40 :      
                        if y > 0 and y < 300:
                            grid.add(2)
                            speed_ahead = car["velocity"] 
                            if y < 200:
                                speed_ahead = car["velocity"]
                                grid.add(5) 
                        elif y < 0 and y > -200:
                            grid.add(8)
                    if x > -100 and x < -40 :
                        if y > 80 and y < 180:
                            grid.add(3)
                        elif y < -80 and y > -180:
                            grid.add(9)
                        elif y < 80 and y > -80:
                            grid.add(6)
                    if x < 100 and x > 40:
                        if y > 80 and y < 180:
                            grid.add(1)
                        elif y < -80 and y > -180:
                            grid.add(7)
                        elif y < 80 and y > -80:
                            grid.add(4)
                #print([self.player_no, grid])
                
            return move(grid= grid, speed_ahead = speed_ahead)
            
        def move(grid, speed_ahead): 
            # if self.player_no == 0:
            #     print(grid)
            if len(grid) == 0:
                return ["SPEED"]
            else:
                if (2 not in grid): # Check forward 
                    # Back to lane center
                    if self.car_pos[0] > self.lanes[self.car_lane]:
                        return ["SPEED", "MOVE_LEFT"]
                    elif self.car_pos[0 ] < self.lanes[self.car_lane]:
                        return ["SPEED", "MOVE_RIGHT"]
                    else :return ["SPEED"]
                else:
                    if (5 in grid): # NEED to BRAKE
                        if (3 in grid) and (6 not in grid):
                            if self.car_vel < speed_ahead:
                                return ["SPEED", "MOVE_LEFT"]
                            else:
                                return ["BRAKE", "MOVE_LEFT"]
                        if (1 in grid) and (4 not in grid):
                            if self.car_vel < speed_ahead:
                                return ["SPEED", "MOVE_RIGHT"]
                            else:
                                return ["BRAKE", "MOVE_RIGHT"]
                        if (1 in grid) and (10 not in grid):
                            if self.car_vel < speed_ahead:
                                return ["SPEED", "MOVE_LEFT"]
                            else:
                                return ["BRAKE", "MOVE_LEFT"]
                        if (3 in grid) and (12 not in grid):
                            if self.car_vel < speed_ahead:
                                return ["SPEED", "MOVE_RIGHT"]
                            else:
                                return ["BRAKE", "MOVE_RIGHT"]
                        if (4 not in grid) and (1 not in grid): # turn left    and (7 not in grid) 
                            if self.car_vel < speed_ahead:
                                return ["SPEED", "MOVE_LEFT"]
                            else:
                                return ["BRAKE", "MOVE_LEFT"]
                        elif (6 not in grid) and (3 not in grid) and (12 not in grid): # turn right   and (9 not in grid)
                            if self.car_vel < speed_ahead:
                                return ["SPEED", "MOVE_RIGHT"]
                            else:
                                return ["BRAKE", "MOVE_RIGHT"]
                        else : 
                            if self.car_vel < speed_ahead:  # BRAKE
                                return ["SPEED"]
                            else:
                                return ["BRAKE"]
                    """

                    if (3 in grid) or (6 in grid):
                        if (4 not in grid) and (1 not in grid):
                            return["SPEED", "MOVE_LEFT"]
                        if (4 not in grid) and (1 in grid) and (10 not in grid):
                            return ["SPEED", "MOVE_LEFT"]
                        if (1 in grid):
                            if self.car_vel < speed_ahead:  # BRAKE
                                return ["SPEED"]
                            else:
                                return ["BRAKE"]
                        
                    if (1 in grid) or (4 in grid):
                        if (3 not in grid) and (6 not in grid):
                            return["SPEED", "MOVE_RIGHT"]             
                        if (3 in grid) and (6 not in grid) and (12 not in grid):
                            return ["SPEED", "MOVE_RIGHT"]
                        if (3 in grid):
                            if self.car_vel < speed_ahead:  # BRAKE
                                return ["SPEED"]
                            else:
                                return ["BRAKE"]       
                    """
                    if (4 in grid) and (3 in grid) and (6 not in grid) and (12 not in grid): # turn right
                        print("right")
                        return ["SPEED", "MOVE_RIGHT"]
                    if (6 in grid) and (4 not in grid) and (1 in grid) and (10 not in grid):
                        print("golllleeeft")
                        return [ "SPEED","MOVE_LEFT"]
                    if (3 not in grid) and (6 not in grid): # turn right
                        return ["SPEED", "MOVE_RIGHT"]
                    if (self.car_pos[0] < 30 ):
                        return ["SPEED", "MOVE_RIGHT"]
                    if (1 not in grid) and (4 not in grid) and (7 not in grid): # turn left 
                        return ["SPEED", "MOVE_LEFT"]
                    
                    if (1 not in grid) and (4 not in grid): # turn left 
                        return ["SPEED", "MOVE_LEFT"]
                    
                    if (4 not in grid) and (7 not in grid): # turn left 
                        return ["MOVE_LEFT"]    
                    if (6 not in grid) and (9 not in grid): # turn right
                        return ["MOVE_RIGHT"]
                    
                                
                    
        if len(scene_info[self.player]) != 0:
            self.car_pos = scene_info[self.player]

        for car in scene_info["cars_info"]:
            if car["id"]==self.player_no:
                self.car_vel = car["velocity"]

        if scene_info["status"] != "ALIVE":
            return "RESET"
        self.car_lane = self.car_pos[0] // 70
        return check_grid()

    def reset(self):
        """
        Reset the status
        """
        pass
