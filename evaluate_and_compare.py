import json
import glob
import os
from algorithms.page_algorithms import fifo, lru, optimal
from rl_agent.dqn_agent import DQNAgent
from env.paging_env import PagingEnv

NUM_FRAMES = 8

def evaluate_rl_agent(agent, pages, frame_size):
    """Evaluate RL agent on a page sequence"""
    env = PagingEnv(pages, frame_size=frame_size)
    state = env.reset()
    
    while True:
        action = agent.act(state, greedy=True)  
        state, _, done = env.step(action)
        
        if done:
            break
    
    return env.page_faults

def evaluate():
    print("=== Evaluating RL vs FIFO/LRU/Optimal ===\n")

    datasets = sorted(glob.glob("datasets/generated/*.json"))
    
    if not datasets:
        print("Error: No datasets found!")
        return
    
    
    state_size = NUM_FRAMES + 1
    action_size = NUM_FRAMES
    agent = DQNAgent(state_size, action_size)
    
    try:
        agent.load("models/dqn_agent.pth")
        print("✅ Model loaded successfully\n")
    except FileNotFoundError:
        print("Error: Model not found. Run train_dqn.py first!")
        return

    results = {
        "fifo": [],
        "lru": [],
        "optimal": [],
        "dqn": [],
        "labels": []
    }

    for path in datasets:
        with open(path) as f:
            pages = json.load(f)

        fifo_faults = fifo(pages, NUM_FRAMES)
        lru_faults = lru(pages, NUM_FRAMES)
        opt_faults = optimal(pages, NUM_FRAMES)
        rl_faults = evaluate_rl_agent(agent, pages, NUM_FRAMES)

        dataset_name = path.split('/')[-1].replace('.json', '')
        results["labels"].append(dataset_name)
        results["fifo"].append(fifo_faults)
        results["lru"].append(lru_faults)
        results["optimal"].append(opt_faults)
        results["dqn"].append(rl_faults)

        print(f"Dataset: {dataset_name} ({len(pages)} refs)")
        print(f"  FIFO:    {fifo_faults} faults")
        print(f"  LRU:     {lru_faults} faults")
        print(f"  Optimal: {opt_faults} faults")
        print(f"  DQN RL:  {rl_faults} faults")
        print()

    
    os.makedirs("results", exist_ok=True)
    
    
    with open("results/evaluation_results.json", "w") as f:
        json.dump(results, f, indent=2)
    print("✅ Evaluation complete. Results saved to results/evaluation_results.json\n")
    
    
    print("Generating graph...")
    try:
        from graphical_comparision import plot_results
        plot_results(results)
    except ImportError as e:
        print(f"Warning: Could not import graphical_comparision module: {e}")
        print("Make sure graphical_comparision.py exists in the project directory")
    except Exception as e:
        print(f"Error generating graph: {e}")

if __name__ == "__main__":
    evaluate()
