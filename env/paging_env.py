import numpy as np

class PagingEnv:
    def __init__(self, pages, frame_size=4):
        self.pages = pages
        self.frame_size = frame_size
        self.reset()

    def reset(self):
        self.pointer = 0
        self.memory = [-1] * self.frame_size
        self.page_faults = 0
        return self._get_state()

    def _get_state(self):
        if self.pointer >= len(self.pages):
            return np.array(self.memory + [0], dtype=np.float32)
        next_page = self.pages[self.pointer]
        return np.array(self.memory + [next_page], dtype=np.float32)

    def step(self, action):
        if self.pointer >= len(self.pages):
            return self._get_state(), 0, True
            
        page = self.pages[self.pointer]

        if page in self.memory:
            reward = 0.2
        else:
            reward = -1
            self.page_faults += 1
            action = min(action, self.frame_size - 1)
            self.memory[action] = page

        self.pointer += 1
        done = self.pointer >= len(self.pages)

        if done:
            next_state = np.array(self.memory + [0], dtype=np.float32)
        else:
            next_state = self._get_state()
            
        return next_state, reward, done
