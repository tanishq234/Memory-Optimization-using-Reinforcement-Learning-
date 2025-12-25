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


def evaluate_throughput(page_faults, total_accesses, MAT=100e-9, PFST=10e-3):
    p = page_faults / total_accesses
    
    EAT = (1 - p) * MAT + p * PFST

    throughput = 1 / EAT

    return p, EAT, throughput


if __name__ == "__main__":
    pages = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3]
    capacity = 3

    total_accesses = len(pages)

    fifo_faults = fifo(pages, capacity)
    lru_faults = lru(pages, capacity)
    optimal_faults = optimal(pages, capacity)

    fifo_results = evaluate_throughput(fifo_faults, total_accesses)
    lru_results = evaluate_throughput(lru_faults, total_accesses)
    optimal_results = evaluate_throughput(optimal_faults, total_accesses)

    print("=== Page Fault Counts ===")
    print("FIFO:", fifo_faults)
    print("LRU:", lru_faults)
    print("Optimal:", optimal_faults)

    print("\n=== Throughput Evaluation ===")
    print(f"FIFO Throughput:   {fifo_results[2]:.2e} accesses/sec")
    print(f"LRU Throughput:    {lru_results[2]:.2e} accesses/sec")
    print(f"Optimal Throughput:{optimal_results[2]:.2e} accesses/sec")
