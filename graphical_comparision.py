
import matplotlib.pyplot as plt

def plot_results(data):
    labels = data["labels"]

    plt.figure(figsize=(12, 6))
    plt.plot(labels, data["fifo"], marker='o', label="FIFO")
    plt.plot(labels, data["lru"], marker='o', label="LRU")
    plt.plot(labels, data["optimal"], marker='o', label="Optimal")
    plt.plot(labels, data["dqn"], marker='o', label="DQN RL")

    plt.title("Page Faults Comparison of Page Replacement Algorithms")
    plt.xlabel("Dataset Reference Size")
    plt.ylabel("Page Faults (Lower is Better)")
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.savefig("results/page_faults_comparison.png")
    print("✅ Graph saved to results/page_faults_comparison.png")