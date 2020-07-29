'''
    2*3迷宫，内藏一枚炸弹和一个终点。
'''


import numpy as np 

class Maze():
    def __init__(self):
        self.maze = np.array([[0,1,0],
                            [1,-1000,1000]])
                    
        self.state = 0
        self.MAX_STATE = 6
        self.MAX_ACTION = 4

        self.action_dict = {    # 存储每个位置可以走到的位置
            0: [1,3],
            1: [1,2,3],
            2: [1,2],
            3: [0,3],
            4: [0,2,3],
            5: [0,2]
        }

        self.action_num = {     # 存储行动和对应的代表值，即行动0就是往上走
            "up": 0,
            "down": 1,
            "left": 2,
            "right": 3
        }

    def actions(self):
        '获得当前状态可做的动作'
        return self.action_dict[self.state]

    def move(self, action, update_state=True):
        '''
            有时候，move只是想看看执行该操作后获得的reward，而不是真的要移动。
            所以提供以下标志位:
                update_state: whether or not refresh the state after self.move, default is True.
        '''
        state = self.state
        isWall = True
        if action in self.actions():
            if action == 0:
                state -= 3
            elif action == 1:
                state += 3
            elif action == 2:
                state -= 1
            elif action == 3:
                state += 1
            isWall = False

        if update_state:
            # print('state {} | action {} | next_state {}'.format(self.state, action , state))
            self.state = state
        
        return state, isWall
        
    def value(self, action=None):
        '''
            action = None: 返回当前位置value
            action != None: 返回执行action之后位置的value
        '''
        state = self.state
        isWall = False
        if action:
            state, isWall= self.move(action, update_state=False)
        
        w = state // 3
        h = state % 3
        return self.maze[w][h] if isWall == False else 0  # isWall==False说明action执行后有移动, 否则是碰到了墙壁, 没有奖励. 

    def isEnd(self):
        '返回值代表是否走到了迷宫终点（即位置5）'
        return True if self.state == 5 else False

    def restart(self):
        '需要给RL提供可以重开游戏的方法，对于迷宫，就是回到原点。'
        self.state = 0

if __name__ == "__main__":
    maze = Maze()
    print(maze.maze)
    for action in maze.action_dict[maze.state]:
        print(action)


