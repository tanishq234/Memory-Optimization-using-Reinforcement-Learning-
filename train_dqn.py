import os
import sys
import json
import glob
from env.paging_env import PagingEnv
from rl_agent.dqn_agent import DQNAgent

EPISODES = 50
NUM_FRAMES = 8
UPDATE_TARGET_FREQ = 10

def train():
    print("=== Training DQN Paging Agent ===", flush=True)
    
    
    datasets = glob.glob("datasets/generated/*.json")
    if not datasets:
        print("Error: No datasets found. Run generate_datasets.py first!", flush=True)
        return
    
    all_pages = []
    for dataset_path in datasets:
        with open(dataset_path) as f:
            all_pages.extend(json.load(f))
    
    print(f"Loaded {len(all_pages)} page references from {len(datasets)} datasets", flush=True)
    
    
    env = PagingEnv(all_pages, frame_size=NUM_FRAMES)
    state_size = NUM_FRAMES + 1
    action_size = NUM_FRAMES
    
    agent = DQNAgent(state_size, action_size)

    best_faults = float('inf')
    
    print("Starting training...", flush=True)
    
    for episode in range(EPISODES):
        state = env.reset()
        total_reward = 0
        steps = 0
        
        while True:
            action = agent.act(state)
            next_state, reward, done = env.step(action)
            
            agent.store((state, action, reward, next_state, float(done)))
            agent.train_step()
            
            state = next_state
            total_reward += reward
            steps += 1
            
            if done:
                break
        
        
        if (episode + 1) % UPDATE_TARGET_FREQ == 0:
            agent.update_target()
        
        page_faults = env.page_faults
        
        if page_faults < best_faults:
            best_faults = page_faults
        
        
        print(f"[Episode {episode+1:3d}/{EPISODES}] "
              f"Reward: {total_reward:7.2f} | "
              f"Faults: {page_faults:4d} | "
              f"Steps: {steps:4d} | "
              f"ε: {agent.epsilon:.3f} | "
              f"Best: {best_faults:4d}", flush=True)
    
    
    os.makedirs("models", exist_ok=True)
    agent.save("models/dqn_agent.pth")
    print("\n✅ Training complete. Model saved to models/dqn_agent.pth\n", flush=True)

if __name__ == "__main__":
    
    sys.stdout.reconfigure(line_buffering=True)
    train()