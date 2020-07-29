'''
    迷宫配套的Qlearning。

'''

from maze import Maze 
import numpy as np
import random

class QLearning():
    def __init__(self, random=0.6, discount_factor=0.8, learning_rate=None):
        self.random = random # 以random的概率选择最优走法
        self.discount_factor = discount_factor  # 折现因子，设置此参数可改变当前状态对未来奖励的关注度。若为0，则是贪心算法。
        self.maze = Maze()
        self.times = 0
        self.punish = 1.5 # 每走一步都有惩罚
        self.Qtable = np.zeros(shape=[self.maze.MAX_STATE, self.maze.MAX_ACTION]) # Q表
        self.user_learning_rate = learning_rate

    @property
    def learning_rate(self):
        return self.user_learning_rate if self.user_learning_rate else np.exp((-self.times) / 20)

    def next_state_reward(self, action):
        '返回执行action后的奖励'
        return self.maze.value(action=action) - self.punish

    def Qmax(self, state):
        '返回state下所有action中最大的Q值'
        # print('Qmax state', state)
        return max(self.Qtable[state])

    def policy(self):
        '根据state和random做出policy'
        rand = np.random.random()
        if rand < self.random:
            metaQ = list(self.Qtable[self.maze.state])
            action = metaQ.index(max(metaQ))
        else:
            action = random.randint(0, self.maze.MAX_ACTION-1)
        return action

    def learn(self, action):
        self.times += 1
        w = self.maze.state
        h = action
        q_sa = self.Qtable[w][h]
        reward = self.next_state_reward(action)
        state, _ = self.maze.move(action)  # 移动state
        Qmax = self.Qmax(state)

        new_q_sa = (1 - self.learning_rate) * q_sa + \
            self.learning_rate * (reward + self.discount_factor * Qmax) 
        myprint('new_q_sa', new_q_sa)
        self.Qtable[w][h] = new_q_sa

        isEnd = self.maze.isEnd()
        if isEnd:
            self.restart()
        return isEnd

    def restart(self):
        self.maze.restart()

def myprint(*args):
    '为了统一调配print函数，用myprint代替，省得一个个改。'
    # print(args)
    pass


if __name__ == "__main__":
    Q = QLearning()
    epoch = 500
    for _ in range(epoch):
        myprint('\n-----start------')
        isEnd = False
        while isEnd == False:
            action = Q.policy()
            isEnd = Q.learn(action) 
        myprint('-----end------\n')

    print('Q表:')
    print(Q.Qtable)





