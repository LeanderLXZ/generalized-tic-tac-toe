# RL
import numpy as np
import random as rd


class QLearningTable:

    def __init__(self, size, alpha=0.01, gamma=0.9, epsilon=0.3, q_table=None, agent = True):

        if q_table is None:
            q_table = {}
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.q_table = q_table
        self.size = size**2
        self.agent = agent
        self.initial_qtable()

    def initial_qtable(self):
        x = self.size // 2
        first_state = '-' * self.size
        self.check_state_exist(first_state)
        self.q_table[first_state][x] = 20

    def get_action(self, state, value):
        ks = []
        for k,v in self.q_table[state].items():
            if v == value:
                ks.append(k)
        return rd.sample(ks, 1)[0]

    def choose_action(self, state):
        self.check_state_exist(state)
        # action selection
        if np.random.uniform() <= self.epsilon:
            # exploitation, choose best action
            value = max(self.q_table[state].values())
            action = self.get_action(state, value)

        else:
            # exploration, choose random action
            action = rd.sample(self.q_table[state].keys(), 1)[0]

        return action

    def learn(self, s, a, r, symbol, done = False):  # state, action, reward, next_state
        # update
        if not done:
            for action in self.q_table[s]:
                s_ = self.find_next_state(s, action, symbol)
                self.check_state_exist(s_)
                self.step_learn(s, action, r, s_)

        else:  # next state is terminal
            self.q_table[s][a] = self.gamma * r

    def step_learn(self, s, a, r, s_):
        q_predict = self.q_table[s][a]

        value_ = max(self.q_table[s_].values())
        action_ = self.get_action(s_, value_)
        q_target = r - self.gamma * self.q_table[s_][action_]

        self.q_table[s][a] += self.alpha * (q_target - q_predict)

    def find_next_state(self, s, a, symbol):
        next_state = s[:a] + symbol + s[a+1:]
        return next_state

    def find_pre_state(self, state, actions):
        pre_state = state[:actions[-2]] + '-' + state[actions[-2]+1:]
        return pre_state

    def updata_pre_terminal(self, state, actions, point):
        pre_state = self.find_pre_state(state, actions)
        self.q_table[pre_state][actions[-2]] = -point

    def check_state_exist(self, state):
        if state not in self.q_table:
            # append new state to q table
            self.q_table[state] = {}
            #print(state)
            for i in range(self.size):
                if state[i] == '-':
                    self.q_table[state][i] = 0

    def learn2(self, states, actions, reward):
        n = len(states)
        factor = 1
        for i in range(n-1,0,-1):
            s_ = states[i]
            s = states[i-1]
            a = actions[i-1]
            r = reward
            factor *= -1

            if i == n-1:
                self.q_table[s_][actions[-1]] = self.gamma * r
            else:
                q_predict = self.q_table[s][a]

                self.check_state_exist(s_)
                value_ = max(self.q_table[s_].values())
                action_ = self.get_action(s_, value_)
                q_target =  - self.gamma * self.q_table[s_][action_] * factor

                self.q_table[s][a] += self.alpha * (q_target - q_predict)
