# Memory-Optimization-using-Reinforcement-Learning-
“This project explores how reinforcement learning can improve memory management in operating systems. A DQN-based model learns smart page replacement decisions to reduce page faults. Its results are compared with FIFO, LRU, and Optimal methods, making the concept easy to understand and interesting to explore.”

Features

Simulation of memory page replacement behavior

Reinforcement learning–based decision making using DQN

Comparison with FIFO, LRU, and Optimal algorithms

Support for multiple memory reference datasets

Graphical visualization of performance results

Modular and easy-to-understand code structure

```
📂 memory-optimization-using-rl
│
├── 📂 algorithms
│ └── page_algorithms.py → FIFO, LRU, Optimal implementations
│
├── 📂 rl_agent
│ └── dqn_agent.py → Deep Q-Network agent logic
│
├── 📂 env
│ └── paging_env.py → Memory paging environment
│
├── 📂 datasets
│ └── 📂 generated → Page reference datasets (JSON)
│
├── 📂 models
│ └── dqn_agent.pth → Trained RL model
│
├── 📂 results
│ ├── evaluation_results.json → Stored evaluation metrics
│ └── page_faults_comparison.png → Graphical comparison output
│
├── 📜 train_dqn.py → Trains the RL agent
├── 📜 evaluate_and_compare.py → Evaluates RL vs FIFO/LRU/Optimal
├── 📜 graphical_comparision.py → Generates comparison graphs
└── 📜 README.md → Project documentation
```
