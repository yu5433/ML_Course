"""
The template of the main script of the machine learning process
"""

import games.arkanoid.communication as comm
from games.arkanoid.communication import ( \
    SceneInfo, GameStatus, PlatformAction
)

def ml_loop():
    """
    The main loop of the machine learning process

    This loop is run in a separate process, and communicates with the game process.

    Note that the game process won't wait for the ml process to generate the
    GameInstruction. It is possible that the frame of the GameInstruction
    is behind of the current frame in the game process. Try to decrease the fps
    to avoid this situation.
    """

    # === Here is the execution order of the loop === #
    # 1. Put the initialization code here.
    ball_served = False

    # 2. Inform the game process that ml process is ready before start the loop.
    comm.ml_ready()

    # 3. Start an endless loop.
    while True:
        # 3.1. Receive the scene information sent from the game process.
        scene_info = comm.get_scene_info()

        # 3.2. If the game is over or passed, the game process will reset
        #      the scene and wait for ml process doing resetting job.
        if scene_info.status == GameStatus.GAME_OVER or \
            scene_info.status == GameStatus.GAME_PASS:
            # Do some stuff if needed
            ball_served = False

            # 3.2.1. Inform the game process that ml process is ready
            comm.ml_ready()
            continue

        # 3.3. Put the code here to handle the scene information

        # 3.4. Send the instruction for this frame to the game process
        if not ball_served:
            comm.send_instruction(scene_info.frame, PlatformAction.SERVE_TO_LEFT)
            ball_served = True
            hit = False
            expect_x = 75
            pre_x = 75
            pre_y = 0
        else:
            ball_x = scene_info.ball[0]
            ball_y = 400 - scene_info.ball[1]
            plat_x = scene_info.platform[0]
            
            vec_x = ball_x - pre_x
            vec_y = ball_y - pre_y

            if(vec_y >0 and ball_y > 280):
                expect_x = 75
            if(vec_x < 0 and vec_y < 0):
                    if(ball_y >= 195):
                       expect_x = 390 - (ball_y - ball_x)
                       print("S")
                       if(expect_x >= 195):
                           expect_x = ball_y - ball_x
                    elif(ball_y > ball_x):
                        expect_x = ball_y - ball_x
                        print("2")
                        if(expect_x < 0):
                            expect_x = ball_x - ball_y
                            print("2-2")
                    else:
                        expect_x = ball_x - ball_y
            if(vec_x > 0 and vec_y < 0):
                    if(ball_y >= 195):
                        expect_x = ball_y + ball_x - 390
                        print("3-1")
                        if(expect_x < 0):
                            expect_x = 390 - ball_x - ball_y
                            print("3")
                    else:
                        expect_x = ball_x + ball_y                    
                        if(expect_x > 195):
                            expect_x = 390 - ball_x - ball_y


            pre_x = ball_x
            pre_y = ball_y    
            print(expect_x)

            if (plat_x< expect_x) and (plat_x + 20 > expect_x):
                comm.send_instruction(scene_info.frame, PlatformAction.NONE)
            elif plat_x > expect_x:
                comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
            elif plat_x < expect_x:
                comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
                        
                    

        """
            if(ball_y > 300 ):
                expect_x = 75

            print(expect_x)

            if ball_x == 0:
                print('ball:' , ball_y)
                if ball_y > 200:
                    expect_x = 400 - ball_y
                else:
                    expect_x = ball_y
                print('expect:', expect_x)

            if ball_x == 195:
                print('right')
                print('ball:' , ball_y)
                if ball_y > 200:
                    expect_x = ball_y - 200
                else:
                    expect_x = 400 - ball_y -200
                print('expect:', expect_x)
                    
            if expect_x != 0:
                if (plat_x< expect_x) and (plat_x + 30 > expect_x):
                    comm.send_instruction(scene_info.frame, PlatformAction.NONE)
                elif plat_x > expect_x:
                    comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
                elif plat_x < expect_x:
                    comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
        """