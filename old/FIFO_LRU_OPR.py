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


if __name__ == "__main__":
    pages = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3]
    capacity = 3

    print("Pages:", pages)
    print("Capacity:", capacity)
    print("FIFO Page Faults:", fifo(pages, capacity))
    print("LRU Page Faults:", lru(pages, capacity))
    print("Optimal Page Faults:", optimal(pages, capacity))
