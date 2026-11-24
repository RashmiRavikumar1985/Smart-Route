"""
Generate performance visualization charts for submission.
"""
import os
import csv
import sys

# Ensure matplotlib uses non-GUI backend
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

OUTPUT_DIR = "outputs/plots"
CSV_DIR = "outputs/csv"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def read_csv(filepath):
    with open(filepath, "r") as f:
        return list(csv.DictReader(f))


def plot_training_rewards():
    """Plot training reward curves for all algorithms."""
    fig, ax = plt.subplots(figsize=(12, 6))
    colors = {"PPO": "#2196F3", "DQN": "#FF5722", "A2C": "#4CAF50"}

    for algo in ["PPO", "DQN", "A2C"]:
        filepath = os.path.join(CSV_DIR, f"training_log_{algo.lower()}.csv")
        if not os.path.exists(filepath):
            continue
        data = read_csv(filepath)
        episodes = [int(d["episode"]) for d in data]
        rewards = [float(d["reward"]) for d in data]

        ax.plot(episodes, rewards, label=algo, color=colors[algo], alpha=0.4, linewidth=1)

        # Smoothed line (moving average)
        if len(rewards) >= 3:
            window = min(5, len(rewards))
            smoothed = np.convolve(rewards, np.ones(window)/window, mode='valid')
            ax.plot(range(window-1, len(rewards)), smoothed,
                    color=colors[algo], linewidth=2.5, label=f"{algo} (smoothed)")

    ax.set_xlabel("Episode", fontsize=13)
    ax.set_ylabel("Episode Reward", fontsize=13)
    ax.set_title("Training Reward Curves: PPO vs DQN vs A2C", fontsize=15, fontweight='bold')
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "training_reward_curves.png"), dpi=150)
    print("  Saved: training_reward_curves.png")
    plt.close()


def plot_evaluation_comparison():
    """Bar chart comparing average evaluation rewards."""
    filepath = os.path.join(CSV_DIR, "algorithm_comparison.csv")
    if not os.path.exists(filepath):
        return
    data = read_csv(filepath)

    algos = [d["algorithm"] for d in data]
    avg_rewards = [float(d["avg_eval_reward"]) for d in data]
    std_rewards = [float(d["std_eval_reward"]) for d in data]
    colors = ["#2196F3", "#FF5722", "#4CAF50"]

    fig, ax = plt.subplots(figsize=(8, 6))
    bars = ax.bar(algos, avg_rewards, yerr=std_rewards, capsize=8,
                  color=colors, edgecolor='black', linewidth=1.2, alpha=0.85)

    for bar, val in zip(bars, avg_rewards):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                f'{val:.2f}', ha='center', va='bottom', fontsize=12, fontweight='bold')

    ax.set_ylabel("Average Evaluation Reward", fontsize=13)
    ax.set_title("Algorithm Comparison: Evaluation Performance", fontsize=15, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "evaluation_comparison.png"), dpi=150)
    print("  Saved: evaluation_comparison.png")
    plt.close()


def plot_training_time():
    """Bar chart of training times."""
    filepath = os.path.join(CSV_DIR, "algorithm_comparison.csv")
    if not os.path.exists(filepath):
        return
    data = read_csv(filepath)

    algos = [d["algorithm"] for d in data]
    times = [float(d["training_time_sec"]) for d in data]
    colors = ["#2196F3", "#FF5722", "#4CAF50"]

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(algos, times, color=colors, edgecolor='black', linewidth=1.2, alpha=0.85)
    for bar, val in zip(bars, times):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                f'{val:.0f}s', ha='center', va='bottom', fontsize=12, fontweight='bold')
    ax.set_ylabel("Training Time (seconds)", fontsize=13)
    ax.set_title("Training Time Comparison", fontsize=15, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "training_time_comparison.png"), dpi=150)
    print("  Saved: training_time_comparison.png")
    plt.close()


def plot_evaluation_boxplot():
    """Boxplot of evaluation rewards per algorithm."""
    filepath = os.path.join(CSV_DIR, "evaluation_results.csv")
    if not os.path.exists(filepath):
        return
    data = read_csv(filepath)

    algo_rewards = {}
    for d in data:
        algo = d["algorithm"]
        if algo not in algo_rewards:
            algo_rewards[algo] = []
        algo_rewards[algo].append(float(d["total_reward"]))

    fig, ax = plt.subplots(figsize=(8, 6))
    labels = list(algo_rewards.keys())
    values = [algo_rewards[k] for k in labels]
    colors = ["#2196F3", "#FF5722", "#4CAF50"]

    bp = ax.boxplot(values, labels=labels, patch_artist=True, widths=0.5)
    for patch, color in zip(bp['boxes'], colors[:len(labels)]):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)

    ax.set_ylabel("Total Evaluation Reward", fontsize=13)
    ax.set_title("Evaluation Reward Distribution per Algorithm", fontsize=15, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "evaluation_boxplot.png"), dpi=150)
    print("  Saved: evaluation_boxplot.png")
    plt.close()


def plot_episode_length():
    """Plot episode lengths across training."""
    fig, ax = plt.subplots(figsize=(12, 5))
    colors = {"PPO": "#2196F3", "DQN": "#FF5722", "A2C": "#4CAF50"}

    for algo in ["PPO", "DQN", "A2C"]:
        filepath = os.path.join(CSV_DIR, f"training_log_{algo.lower()}.csv")
        if not os.path.exists(filepath):
            continue
        data = read_csv(filepath)
        episodes = [int(d["episode"]) for d in data]
        lengths = [int(d["length"]) for d in data]
        ax.plot(episodes, lengths, label=algo, color=colors[algo], linewidth=1.5, alpha=0.8)

    ax.set_xlabel("Episode", fontsize=13)
    ax.set_ylabel("Episode Length (steps)", fontsize=13)
    ax.set_title("Episode Length During Training", fontsize=15, fontweight='bold')
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "episode_lengths.png"), dpi=150)
    print("  Saved: episode_lengths.png")
    plt.close()


def plot_system_architecture():
    """Create a system architecture diagram."""
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8)
    ax.axis('off')

    # Title
    ax.text(7, 7.5, "Smart Route: System Architecture",
            ha='center', fontsize=16, fontweight='bold')

    # Perception Layer
    rect1 = plt.Rectangle((0.5, 5), 3.5, 1.8, fill=True, facecolor='#E3F2FD',
                           edgecolor='#1565C0', linewidth=2, zorder=2)
    ax.add_patch(rect1)
    ax.text(2.25, 6.3, "PERCEPTION LAYER", ha='center', fontsize=11, fontweight='bold', color='#1565C0')
    ax.text(2.25, 5.8, "YOLOv8 Vehicle Detection", ha='center', fontsize=9)
    ax.text(2.25, 5.4, "Traffic Density Estimation", ha='center', fontsize=9)

    # Decision Layer
    rect2 = plt.Rectangle((5.25, 5), 3.5, 1.8, fill=True, facecolor='#E8F5E9',
                           edgecolor='#2E7D32', linewidth=2, zorder=2)
    ax.add_patch(rect2)
    ax.text(7, 6.3, "DECISION LAYER", ha='center', fontsize=11, fontweight='bold', color='#2E7D32')
    ax.text(7, 5.8, "RL Agent (PPO/DQN/A2C)", ha='center', fontsize=9)
    ax.text(7, 5.4, "Policy: MlpPolicy", ha='center', fontsize=9)

    # Simulation Layer
    rect3 = plt.Rectangle((10, 5), 3.5, 1.8, fill=True, facecolor='#FFF3E0',
                           edgecolor='#E65100', linewidth=2, zorder=2)
    ax.add_patch(rect3)
    ax.text(11.75, 6.3, "SIMULATION LAYER", ha='center', fontsize=11, fontweight='bold', color='#E65100')
    ax.text(11.75, 5.8, "SUMO Simulator", ha='center', fontsize=9)
    ax.text(11.75, 5.4, "TraCI Interface", ha='center', fontsize=9)

    # Arrows
    ax.annotate('', xy=(5.15, 5.9), xytext=(4.1, 5.9),
                arrowprops=dict(arrowstyle='->', color='black', lw=2))
    ax.annotate('', xy=(9.9, 5.9), xytext=(8.85, 5.9),
                arrowprops=dict(arrowstyle='->', color='black', lw=2))

    # State/Action/Reward boxes
    rect_s = plt.Rectangle((3, 2.5), 2.5, 2, fill=True, facecolor='#F3E5F5',
                            edgecolor='#6A1B9A', linewidth=1.5, zorder=2)
    ax.add_patch(rect_s)
    ax.text(4.25, 4, "STATE", ha='center', fontsize=10, fontweight='bold', color='#6A1B9A')
    ax.text(4.25, 3.5, "• Queue length/lane", ha='center', fontsize=8)
    ax.text(4.25, 3.1, "• Waiting time", ha='center', fontsize=8)
    ax.text(4.25, 2.7, "• Signal phase", ha='center', fontsize=8)

    rect_a = plt.Rectangle((5.75, 2.5), 2.5, 2, fill=True, facecolor='#E0F7FA',
                            edgecolor='#00695C', linewidth=1.5, zorder=2)
    ax.add_patch(rect_a)
    ax.text(7, 4, "ACTION", ha='center', fontsize=10, fontweight='bold', color='#00695C')
    ax.text(7, 3.5, "Select traffic", ha='center', fontsize=8)
    ax.text(7, 3.1, "signal phase", ha='center', fontsize=8)
    ax.text(7, 2.7, "(N-S / E-W green)", ha='center', fontsize=8)

    rect_r = plt.Rectangle((8.5, 2.5), 2.5, 2, fill=True, facecolor='#FFEBEE',
                            edgecolor='#B71C1C', linewidth=1.5, zorder=2)
    ax.add_patch(rect_r)
    ax.text(9.75, 4, "REWARD", ha='center', fontsize=10, fontweight='bold', color='#B71C1C')
    ax.text(9.75, 3.5, "Minimize:", ha='center', fontsize=8)
    ax.text(9.75, 3.1, "• Waiting time", ha='center', fontsize=8)
    ax.text(9.75, 2.7, "• Queue length", ha='center', fontsize=8)

    # Feedback loop arrow
    ax.annotate('', xy=(4.25, 4.9), xytext=(4.25, 4.55),
                arrowprops=dict(arrowstyle='->', color='#6A1B9A', lw=1.5))
    ax.annotate('', xy=(7, 4.9), xytext=(7, 4.55),
                arrowprops=dict(arrowstyle='->', color='#00695C', lw=1.5))
    ax.annotate('', xy=(9.75, 4.9), xytext=(9.75, 4.55),
                arrowprops=dict(arrowstyle='->', color='#B71C1C', lw=1.5))

    # Tools row
    tools = [("Python 3.11", 1.5), ("Stable-Baselines3", 4), ("SUMO 1.28", 7),
             ("YOLOv8", 9.5), ("TensorBoard", 12)]
    for name, x in tools:
        rect = plt.Rectangle((x-0.8, 0.5), 1.6, 0.8, fill=True, facecolor='#ECEFF1',
                              edgecolor='#455A64', linewidth=1, zorder=2, linestyle='--')
        ax.add_patch(rect)
        ax.text(x, 0.9, name, ha='center', fontsize=8, fontweight='bold', color='#455A64')

    ax.text(7, 1.6, "Tools & Technologies", ha='center', fontsize=11,
            fontweight='bold', color='#455A64')

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "system_architecture.png"), dpi=150, bbox_inches='tight')
    print("  Saved: system_architecture.png")
    plt.close()


if __name__ == "__main__":
    print("\nGenerating Performance Charts...")
    print("-" * 40)
    plot_training_rewards()
    plot_evaluation_comparison()
    plot_training_time()
    plot_evaluation_boxplot()
    plot_episode_length()
    plot_system_architecture()
    print("\nAll charts saved to outputs/plots/")
