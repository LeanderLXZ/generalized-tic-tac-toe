from env import Board
from DQN import DeepQNetwork

def train(time):
    step= 0

    for episode in range(4000*time+1):
        # initial observation
        board.reset()
        state = board.get_state()

        while True:
            # RL choose action based on observation
            action = RL.choose_action(state)
            # RL take action and get next observation and reward
            reward, done = board.step(action, agent=False)
            state_ = board.get_state()
            RL.store_transition(state, action, reward, state_)
            if RL.memory_counter > MEMORY_CAPACITY:
                RL.learn()
            if done:
                break
            step += 1

            # observation
            state = state_
            # RL choose action based on observation
            action = RL.choose_action(state)
            # RL take action and get next observation and reward
            reward, done = board.step(action)
            state_ = board.get_state()
            RL.store_transition(state, action, reward, state_)
            # break while loop when end of this episode
            if RL.memory_counter > MEMORY_CAPACITY:
                RL.learn()
            if done:
                break

            step += 1

            state = state_


        print('episode is:',episode)

    # end of game
    print('training over')

    # end of game
    print('game over')


if __name__ == "__main__":
    size = 12
    m = 6
    MEMORY_CAPACITY = 4000
    board = Board(size,m)
    RL = DeepQNetwork(size**2,size**2)

    train(1)

    RL.save_net()
    print('Finish')
