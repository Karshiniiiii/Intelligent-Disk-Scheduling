
import matplotlib.pyplot as plt

def plot_request_trace(requests, title="Disk Head Movement"):
    requests = list(requests)
    if not requests:
        print("No requests to display.")
        return

    plt.figure(figsize=(10, 5))
    positions = [50] + requests
    plt.plot(range(len(positions)), positions, marker="o")
    plt.title(title)
    plt.xlabel("Request sequence")
    plt.ylabel("Disk track")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_algorithm_comparison(results):
    names = list(results.keys())
    movements = [
        results[name]["head_movement"]
        for name in names
    ]

    plt.figure(figsize=(9, 5))
    plt.bar(names, movements)
    plt.title("Disk Scheduling Algorithm Comparison")
    plt.xlabel("Algorithm")
    plt.ylabel("Total Head Movement")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    sample = [98, 183, 37, 122, 14, 124, 65, 67]
    plot_request_trace(sample)
