import matplotlib.pyplot as plt



def fifo(pages, capacity):
    memory = []
    page_faults = 0

    for page in pages:
        if page not in memory:
            if len(memory) == capacity:
                memory.pop(0)
            memory.append(page)
            page_faults += 1
    return page_faults


def lru(pages, capacity):
    memory = []
    page_faults = 0

    for page in pages:
        if page not in memory:
            if len(memory) == capacity:
                memory.pop(0)
            memory.append(page)
            page_faults += 1
        else:
            memory.remove(page)
            memory.append(page)
    return page_faults


def optimal(pages, capacity):
    memory = []
    page_faults = 0

    for i in range(len(pages)):
        page = pages[i]
        if page not in memory:
            if len(memory) < capacity:
                memory.append(page)
            else:
                future_use = []
                for frame in memory:
                    if frame in pages[i+1:]:
                        future_use.append(pages[i+1:].index(frame))
                    else:
                        future_use.append(float('inf'))
                memory.pop(future_use.index(max(future_use)))
                memory.append(page)
            page_faults += 1
    return page_faults



def calculate_throughput(page_faults, total_references,
                         MAT=100, PFST=10_000_000):

    fault_rate = page_faults / total_references

    EAT = (1 - fault_rate) * MAT + fault_rate * PFST

    throughput = 1 / EAT

    return throughput


page_sets = [
    [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3],
    [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5],
    [0, 1, 2, 3, 4, 0, 1, 2, 0, 1, 3, 4],
]

frame_sizes = [2, 3, 4]



labels = []
fifo_tp = []
lru_tp = []
optimal_tp = []

for pages in page_sets:
    for frames in frame_sizes:

        total = len(pages)

        fifo_faults = fifo(pages, frames)
        lru_faults = lru(pages, frames)
        optimal_faults = optimal(pages, frames)

        fifo_tp.append(calculate_throughput(fifo_faults, total))
        lru_tp.append(calculate_throughput(lru_faults, total))
        optimal_tp.append(calculate_throughput(optimal_faults, total))

        labels.append(f"{total}p-{frames}f")


plt.figure(figsize=(12, 6))

plt.plot(labels, fifo_tp, marker='o', label="FIFO Throughput")
plt.plot(labels, lru_tp, marker='o', label="LRU Throughput")
plt.plot(labels, optimal_tp, marker='o', label="Optimal Throughput")

plt.title("Throughput Comparison of Page Replacement Algorithms")
plt.xlabel("Page Set and Frame Size")
plt.ylabel("Throughput (Higher is Better)")
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()
