import random
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

class DQN(nn.Module):
    def __init__(self, input_dim, output_dim):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, output_dim)
        )

    def forward(self, x):
        return self.net(x)


class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.model = DQN(state_size, action_size)
        self.target = DQN(state_size, action_size)
        self.optimizer = optim.Adam(self.model.parameters(), lr=0.001)

        self.memory = []
        self.gamma = 0.95
        self.epsilon = 1.0
        self.min_epsilon = 0.01
        self.decay = 0.995
        self.batch_size = 64

    def store(self, transition):
        self.memory.append(transition)
        if len(self.memory) > 20000:
            self.memory.pop(0)

    def act(self, state, greedy=False):
        if not greedy and random.random() < self.epsilon:
            return random.randint(0, self.action_size - 1)
        q_values = self.model(torch.FloatTensor(state))
        return torch.argmax(q_values).item()

    def train_step(self):
        if len(self.memory) < self.batch_size:
            return

        batch = random.sample(self.memory, self.batch_size)

        states, actions, rewards, next_states, dones = zip(*batch)

        states = torch.FloatTensor(np.array(states))
        next_states = torch.FloatTensor(np.array(next_states))
        actions = torch.LongTensor(actions)
        rewards = torch.FloatTensor(rewards)
        dones = torch.FloatTensor(dones)

        q_vals = self.model(states).gather(1, actions.unsqueeze(1)).squeeze()
        next_q_vals = self.target(next_states).max(1)[0]
        targets = rewards + (1 - dones) * self.gamma * next_q_vals

        loss = nn.MSELoss()(q_vals, targets)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        self.epsilon = max(self.min_epsilon, self.epsilon * self.decay)

    def update_target(self):
        self.target.load_state_dict(self.model.state_dict())

    def save(self, path):
        torch.save({
            'model_state_dict': self.model.state_dict(),
            'target_state_dict': self.target.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'epsilon': self.epsilon
        }, path)

    def load(self, path):
        checkpoint = torch.load(path)
        self.model.load_state_dict(checkpoint['model_state_dict'])
        self.target.load_state_dict(checkpoint['target_state_dict'])
        self.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        self.epsilon = checkpoint['epsilon']
